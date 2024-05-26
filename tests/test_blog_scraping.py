import requests
from bs4 import BeautifulSoup
import os #OS関連の機能へのアクセスやファイルパスの操作など、さまざまなOS関連の機能を提供

url = 'https://www.hinatazaka46.com/s/official/diary/member?ima=0000r'
response = requests.get(url)
web_content = response.text
print(web_content)

soup = BeautifulSoup(web_content, 'html.parser')

blog_name_div = soup.find('div', class_ = 'c-blog-main__name')
blog_name = blog_name_div.get_text(strip=True) if blog_name_div else None
def check(blog_name):
    if blog_name != "富田 鈴花":
        print(blog_name)
        blog_url = soup.find('a', class_ = "p-blog-main__image")
        href = blog_url.get("href")
        new_url = "https://www.hinatazaka46.com" + href
        print(new_url)
        return
    print("山口陽世")
    blog_url = soup.find('a', class_ = "p-blog-main__image")
    href = blog_url.get("href")
    new_url = "https://www.hinatazaka46.com" + href
  
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

check(blog_name)


# image_elements = soup.find_all('img') #このリストの中には'img'の要素が入っており，.jpg以外の拡張子の画像も含まれる
# directory_name = 'haruyo_yamaguchi'# ディレクトリの名前を決める
# if not os.path.exists(directory_name):
#     os.makedirs(directory_name)

# image_count = 1
# # すべての画像要素を処理して保存
# for img in image_elements: #リスト内の画像要素でループ
#     image_url = img['src']  # 'src'属性から画像のURLを取得
#     if image_url.endswith('.jpg'):
#         image_response = requests.get(image_url)# 画像をダウンロード
        
#         filename = f'{directory_name}/haruyo_yamaguchi{image_count}.jpg' # ファイル名を決定
#         # ローカルに保存
#         with open(filename, 'wb') as f: #バイナリーモード
#                                         #'rd'はバイナリーモードで読み込み
#             f.write(image_response.content)
#             print(f"{filename}を保存しました") #保存したことを表示
#         # イメージカウンターを増やす
#         image_count += 1