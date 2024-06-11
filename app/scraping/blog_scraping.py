import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import os #OS関連の機能へのアクセスやファイルパスの操作など、さまざまなOS関連の機能を提供

OFFISIAL_BLOG_URL = 'https://www.hinatazaka46.com/s/official/diary/member'


class HinatazakaBlogScraper:
    def __init__(self, url: str):
        response = requests.get(url)
        web_content = response.text
        self.soup = BeautifulSoup(web_content, 'html.parser')
        
    def fetch_latest_author_dict(self) -> Dict[str, str]:
        # `p-blog-top__item`クラスの要素をすべて取得
        blog_items = self.soup.find_all(class_='p-blog-top__item')

        # 名前とリンクを辞書にしてリストに格納
        blogger_dict: dict = {}
        for item in blog_items:
            name_tag = item.find(class_='c-blog-top__name')
            link_tag = item.find('a', href=True)
            if name_tag and link_tag:
                name = name_tag.get_text(strip=True)
                href = link_tag['href']
                blogger_dict[name] = href
        return blogger_dict
    
    def get_image_from_method(self, target_url: str):
        response2 = requests.get(target_url)
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
        return image_count