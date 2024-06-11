import shutil

from app.google_photo.google_photo import GooglePhotoFacade
from app.scraping.blog_scraping import HinatazakaBlogScraper

OFFISIAL_BLOG_URL = 'https://www.hinatazaka46.com/s/official/diary/member'
HOME_URL = "https://www.hinatazaka46.com"
TARGET_MEMBER_NAME = "山口 陽世"

if __name__ == "__main__":
    google_photo = GooglePhotoFacade(
        credential_path="credentials.json", token_path="token.pkl"
    )
    
    scraper = HinatazakaBlogScraper(OFFISIAL_BLOG_URL)
    
    name_blog_dict = scraper.fetch_latest_author_dict()
    
    if TARGET_MEMBER_NAME not in name_blog_dict:
        print("更新情報はありません")
        
    url = HOME_URL + name_blog_dict[TARGET_MEMBER_NAME]
    print(url)
    src_count = scraper.get_image_from_method(url)

    for i in range(1,src_count - 1):
        google_photo.upload(
            local_file_path=f"haruyo_yamaguchi/haruyo_yamaguchi{i}.jpg", # ここに保存する画像を指定する。
            album_id="AGpp2nYJaO5iOon6PNbFy1VIkM9BFmflNtIGlt-Lujn5mD2oTolE7PaARc0kpq0WMh5RUAUL0I6N"
        )
        
    shutil.rmtree("haruyo_yamaguchi")