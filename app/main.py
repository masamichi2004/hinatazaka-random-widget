import pickle
from pathlib import Path

import requests
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import requests
from bs4 import BeautifulSoup
import os #OS関連の機能へのアクセスやファイルパスの操作など、さまざまなOS関連の機能を提供

import shutil

# 各URLやスコープ
API_SERVICE_NAME = "photoslibrary"
API_VERSION = "v1"
# SCOPES = ["https://www.googleapis.com/auth/photoslibrary.appendonly"]
SCOPES = ["https://www.googleapis.com/auth/photoslibrary"]



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

def check_url(blog_name):
    if blog_name != "富田 鈴花":
        return
    print("山口陽世のブログが更新されました．保存を開始します．")
    blog_url = soup.find('a', class_ = "p-blog-main__image")
    href = blog_url.get("href")
    return  "https://www.hinatazaka46.com" + href


if __name__ == "__main__":
    g = GooglePhotoFacade(
        credential_path="credentials.json", token_path="token.pkl"
    )
    
    # g.delete_album("AGpp2nau1aZmLOV-xAxso1vA-YEt45Km8eOpame1gaFzHn2x3vjuCd_mKn542Xvs8UN4mm9rRVGqs")
    
    # album_id = g.create_album("山口陽世")
    # print("albumIDは ", album_id)
    
    url = 'https://www.hinatazaka46.com/s/official/diary/member?ima=0000r'
    response = requests.get(url)
    web_content = response.text

    soup = BeautifulSoup(web_content, 'html.parser')

    blog_name_div = soup.find('div', class_ = 'c-blog-main__name')
    blog_name = blog_name_div.get_text(strip=True) if blog_name_div else None

    new_url = check_url(blog_name)
    
    # album_id = g.create_album("blog_picture")
    # print(album_id)
    
    if new_url:
        response2 = requests.get(new_url)
        web_content2 = response2.text
        soup2 = BeautifulSoup(web_content2, 'html.parser')

        image_elements = soup2.find_all('img') #このリストの中には'img'の要素が入っており，.jpg以外の拡張子の画像も含まれる
        directory_name = 'haruyo_yamaguchi'# ディレクトリの名前を決める
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)

        image_count = 1
        # すべての画像要素を処理して保存
        for img in image_elements: #リスト内の画像要素でループ
            image_url = img['src']  # 'src'属性から画像のURLを取得
            if image_url.endswith('.jpg'):
                image_response = requests.get(image_url)# 画像をダウンロード
                
                filename = f'{directory_name}/haruyo_yamaguchi{image_count}.jpg' # ファイル名を決定
                # ローカルに保存
                with open(filename, 'wb') as f: #バイナリーモード
                                                #'rd'はバイナリーモードで読み込み
                    f.write(image_response.content)
                    print(f"{filename}を保存しました") #保存したことを表示
                # イメージカウンターを増やす
                image_count += 1

        for i in range(1,image_count - 1):
            g.upload(
                local_file_path=f"haruyo_yamaguchi/haruyo_yamaguchi{i}.jpg", # ここに保存する画像を指定する。
                album_id="AGpp2nYJaO5iOon6PNbFy1VIkM9BFmflNtIGlt-Lujn5mD2oTolE7PaARc0kpq0WMh5RUAUL0I6N"
            )
        
    shutil.rmtree("haruyo_yamaguchi")