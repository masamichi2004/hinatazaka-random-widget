import pickle
from pathlib import Path

import requests
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import requests

# 各URLやスコープ
API_SERVICE_NAME = "photoslibrary"
API_VERSION = "v1"
# SCOPES = ["https://www.googleapis.com/auth/photoslibrary.appendonly"]
SCOPES = ["https://www.googleapis.com/auth/photoslibrary"]
OFFICIAL_BLOG_URL = "https://www.hinatazaka46.com/s/official/diary/member?ima=0000"
TARGET_MEMBER_NAME = "山口 陽世"



class GooglePhotoFacade:
    # ログインしてセッションオブジェクトを返す
    def __init__(
        self,
        credential_path: str,
        token_path: str = "",
    ):
        with build(
            API_SERVICE_NAME,
            API_VERSION,
            credentials=self._login(credential_path, token_path),
            static_discovery=False,
        ) as service:
            self.service = service
            print("Google OAuth is Complete.")

        self.credential_path = credential_path
        self.token_path = token_path

    def _login(self, credential_path: str, token_path: str) -> any:
        """Googleの認証を行う

        Args:
            credential_path (str): GCPから取得したclient_secret.jsonのパス
            token_path (str): Oauth2認証によって得られたトークンを保存するパス。

        Returns:
            googleapiclient.discovery.Resource: _description_
        """

        if Path(token_path).exists():
            # TOKENファイルを読み込み
            with open(token_path, "rb") as token:
                credential = pickle.load(token)
            if credential.valid:
                print("トークンが有効です.")
                return credential
            if credential and credential.expired and credential.refresh_token:
                print("トークンの期限切れのため、リフレッシュします.")
                # TOKENをリフレッシュ
                credential.refresh(Request())
        else:
            print("トークンが存在しないため、作成します.")
            credential = InstalledAppFlow.from_client_secrets_file(
                credential_path, SCOPES
            ).run_local_server()

        # CredentialをTOKENファイルとして保存
        with open(token_path, "wb") as token:
            pickle.dump(credential, token)

        return credential

    def upload(
        self, local_file_path: str, album_id:str
    ):

        self._login(self.credential_path, self.token_path)  # トークンの期限を確認
        
        save_file_name:str = Path(local_file_path).name
        with open(str(local_file_path), "rb") as image_data:
            url = "https://photoslibrary.googleapis.com/v1/uploads"
            headers = {
                "Authorization": "Bearer " + self.service._http.credentials.token,
                "Content-Type": "application/octet-stream",
                "X-Goog-Upload-File-Name": save_file_name.encode(),
                "X-Goog-Upload-Protocol": "raw",
            }
            
            response = requests.post(url, data=image_data.raw, headers=headers)

        upload_token = response.content.decode("utf-8")
        print("Google Photoへのアップロードが完了しました。")
        body = {
            "newMediaItems": 
                [
                    {
                    "simpleMediaItem": {"uploadToken": upload_token}
                    }
                ],
                "albumId": album_id
            }

        upload_response = self.service.mediaItems().batchCreate(body=body).execute()
        print("Google Photoへのアップロードした動画の登録に成功しました。")

        # uploadしたURLを返す
        return upload_response["newMediaItemResults"][0]["mediaItem"]
    

    # def delete_album(self, album_id: str):
    #     # アルバム内の全アイテムを取得して削除する
    #     response = self.service.mediaItems().search(body={"albumId": album_id}).execute()
    #     print("response: ",response)
    #     media_items = response.get('mediaItems', [])
        
    #     if not media_items:
    #         print(f"アルバム {album_id} にはアイテムがありません。")
    #     else:
    #         media_item_ids = [item['id'] for item in media_items]
    #         delete_body = {
    #             "mediaItemIds": media_item_ids
    #         }
    #         self.service.mediaItems().batchRemoveMediaItems(body=delete_body).execute()
    #         print(f"アルバム {album_id} 内のアイテムが削除されました。")

    #     # アルバム自体を削除する（実際にはアルバム内の全アイテムを削除することで代替）
    #     url = f"https://photoslibrary.googleapis.com/v1/albums/{album_id}"
    #     headers = {
    #         "Authorization": f"Bearer {self.service._http.credentials.token}"
    #     }
    #     response = requests.delete(url, headers=headers)
    #     if response.status_code == 200:
    #         print(f"アルバム {album_id} が削除されました。")
    #     else:
    #         print(f"アルバム {album_id} の削除に失敗しました: {response.content}")
            
    def create_album(self, album_title: str):
        body = {
            "album": {"title": album_title}
        }
        response = self.service.albums().create(body=body).execute()
        print(f"新しく作成されたアルバムID: {response['id']}")
        return response["id"]