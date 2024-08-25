import logging
import os
import time
import re
import json

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains


load_dotenv(override=True)

logging.basicConfig(
    filename="scrapper.log",
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
)
logger = logging.getLogger()


def initate_driver(options):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def instagram_scrapper(driver, keyword):

    url = f"https://www.instagram.com/"
    driver.get(url)
    logger.info(f"Navigated to URL: {url}")

    # input Username
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.NAME, "username"))
    ).send_keys(os.environ.get("USERNAME"))
    # Input Password
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.NAME, "password"))
    ).send_keys(os.environ.get("PASSWORD"))
    # Logging in
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button._acan._acap._acas._aj1-._ap30")
        )
    ).click()
    logger.info("Logged in")
    time.sleep(10)

    # Going on hashtag page
    tag_url = url + "explore/tags/" + keyword
    driver.get(tag_url)
    logger.info(f"Navigated to URL: {tag_url}")
    time.sleep(2)
    result = []
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    posts = driver.find_elements(By.CLASS_NAME, "_aagu")
    logger.info(f"Found {len(posts)} posts, Scrapping started")
    for i in range(len(posts)):
        try:
            post = driver.find_elements(By.CLASS_NAME, "_aagu")[i]
            post.click()
            time.sleep(5)
            logger.info(f"Clicked on post")

            post_soup = BeautifulSoup(driver.page_source, "html.parser")

            caption = post_soup.find("h1").get_text()
            likes = (
                post_soup.find(
                    "span",
                    class_="x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs xt0psk2 x1i0vuye xvs91rp x1s688f x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj",
                )
                .get_text()
                .split(" ")[0]
                .replace(",", "")
            )
            # getting all img/videos
            try:
                next_button = driver.find_element(By.CLASS_NAME, "_9zm2")
            except:
                next_button = None
            if next_button:
                x = True
                while x == True:
                    try:
                        next_button = driver.find_element(By.CLASS_NAME, "_9zm2")
                        next_button.click()
                        time.sleep(1)
                    except NoSuchElementException:
                        x = False
                        current_url = driver.current_url
                post_url, index = current_url.split("img_index=")
                post_content = [
                    post_url + "img_index=" + str(i) for i in range(1, int(index) + 1)
                ]
            else:
                post_content = [driver.current_url]

            # Going to User's profile to get followers
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div._aaqt"))
            ).click()
            time.sleep(5)
            profile_soup = BeautifulSoup(driver.page_source, "html.parser")
            followers = (
                profile_soup.find(
                    "span", class_="x5n08af x1s688f", attrs={"title": True}
                )
                .get("title")
                .replace(",", "")
            )

            # getting email from bio
            bio = profile_soup.find(
                "span", class_="_ap3a _aaco _aacu _aacx _aad7 _aade"
            ).get_text()
            email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
            emails = re.findall(email_pattern, bio)
            result.append(
                {
                    "caption": caption,
                    "likes_count": likes if likes.isnumeric() else "1-99",
                    "followers_count": followers,
                    "email": emails[0] if emails else None,
                    "content": post_content,
                }
            )
            driver.execute_script("window.history.go(-2)")
            time.sleep(2)
        except Exception as e:
            logger.error(
                f"Skipping post {i}, URL: {driver.current_url}, Error occurred: {e}"
            )
            driver.get(tag_url)
            time.sleep(2)
            continue
    logger.info(f"Scrapped {len(result)} {keyword} posts")
    return result


if __name__ == "__main__":

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    driver = initate_driver(options)
    logger.info("Webdriver initiated")
    keywords = os.environ.get("KEYWORDS", "pets").split(",")
    for keyword in keywords:
        data = instagram_scrapper(driver, keyword=keyword)

        with open(f"{keyword}.json", "w") as file:
            json.dump(data, file, indent=4)
    driver.quit()
