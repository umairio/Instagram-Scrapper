# Instagram Scraper

## Overview
The **Instagram Hashtag Scraper** is a Python tool designed to automate the process of scraping Instagram posts and associated metadata based on specific hashtags. It uses Selenium to interact with Instagram's web interface, allowing users to gather data such as post captions, likes, comments, and media links (images and videos).

## Installation

1. **Clone the Repository**
   ```bash
   git clone git@github.com:umairio/Instagram-Scrapper.git
   cd instagram-hashtag-scraper
   ```

2. **Create a Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` File**

    In your project directory, create a `.env` file (make sure the file is named exactly `.env`).
    Add your Instagram credentials to the `.env` file:

   ```
   USERNAME=your_instagram_username
   PASSWORD=your_instagram_password
   KEYWORDS=your_hashtags
   ```

## Example
```bash
python3 scraper.py 
```

## Output
The output will be a JSON file containing an array of post objects with the following structure:
```json
{
    "caption": "\ud83d\udcfd from @\u5e03\u5076\u5c0f\u4e03 | DY#catloversclub",
    "likes_count": "28012",
    "followers_count": "8132646",
    "email": "PetsLoversClub@gmail.com",
    "content": [
        "https://www.instagram.com/p/C_FYnl4y9zY/?img_index=1",
        "https://www.instagram.com/p/C_FYnl4y9zY/?img_index=2"
    ]
}
```
