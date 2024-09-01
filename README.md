# Hinatazaka46 Oshi-images OneDrive Widget for MacOS
## Overview
- Shoma's Spring Project
- An application that scrapes official blogs and outputs random images from onedrive widget

## Hinatazaka46 Official Blog
[![Image from Gyazo](https://i.gyazo.com/27a4bdad6c8b3c6d666c0af257cb1fbe.jpg)](https://gyazo.com/27a4bdad6c8b3c6d666c0af257cb1fbe)

## Architecture
![アーキテクチャ（Hinatazaka）](https://github.com/user-attachments/assets/db26d6ae-e6ff-4e02-b1b9-310c2981214c)


## Quick Start
1. clone this repo to your local one
```
git clone https://github.com/MasamichiKanakubo/spr-hinata-scraping.git
```

2. build and activate the virtual environment
```
python3 -m venv venv
source venv/bin/activate
```

3. install the package
```
pip install -r requirements.txt
```

4. build docker compose
```docker
docker compose build
```

5. run docker compose
```
docker compose up
```

After stop the application, shut down docker compose
```
docker compose down
```
