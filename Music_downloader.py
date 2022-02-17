from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup as BS
import requests
import db as mdb
import time
import os

def get_searched_html(url, video_name):
    if sites_elements.get(url).get("auto_search"):
        html = requests.get(f"{url}search?q={video_name}", headers = HEADERS).text
        download_html(html)
    else:
        print(f"[INFO] Finding song: {video_name}!")

        chrome_options = Options()
        chrome_options.add_experimental_option("prefs", {"download.default_directory": "J:\Projects\Python\Dmitros_music_downloader_bot\Downloads\Musics",
                                                        "safebrowsing.enabled": "false"})

        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.add_argument("--disable-notifications")

        driver = webdriver.Chrome(executable_path = "J:/Projects/Python/Dmitros_music_downloader_bot/chromedriver.exe", chrome_options=chrome_options)
        driver.get(url)
        
        try:
            search = WebDriverWait(driver, 20
                                    ).until(expected_conditions.element_to_be_clickable((By.ID,
                                                                                        sites_elements.get(url).get("search"))))
        except StaleElementReferenceException:
            search = WebDriverWait(driver, 10
                                    ).until(expected_conditions.element_to_be_clickable((By.ID,
                                                                                        sites_elements.get(url).get("search"))))
        
        enter_button = driver.find_element(By.TAG_NAME, "button")

        find = True

        """try:"""
        search.send_keys(video_name)
        enter_button.click()
        time.sleep(2)
        
        find = True

        """try:"""
        search.send_keys(video_name)
        enter_button.click()
            
        html = driver.page_source
        """except WebDriverException:
            if i < len(sites) - 1:
                print(f"[INFO] Song: \"{video_name}\" not found from site: {sites[i]}!")
            else:
                print(f"[INFO] Song: \"{video_name}\" not found!")
            
            find = False
            
            driver.close()"""
        
    return html

def download_html(html):
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

def get_music_links(video_name, song_links, url, html):
    soup = BS(html, "html.parser")
    
    if sites_elements.get(url).get("song_link") != "":
        full_song_names = soup.find_all(sites_elements.get(url).get("song_element"), class_ = sites_elements.get(url).get("full_song_name"))
    else:
        full_song_names = soup.find_all("a", class_ = sites_elements.get(url).get("full_song_name"))
    
    song_link = ""
    
    song_index = -1
    
    for full_song_name in full_song_names:        
        autor = video_name.split(" - ")[0]
        song_name = video_name.split(" - ")[1]
        
        song_index += 1
        
        if sites_elements.get(url).get("autor") != "":
            if autor.lower() in full_song_name.text.lower():
                if song_name.lower() in full_song_name.text.lower():
                    if sites_elements.get(url).get("song_link") != "":
                        song_link = soup.find_all("a", class_ = sites_elements.get(url).get("song_link"))[song_index].get("href")
                    else:
                        song_link = full_song_name.get("href")
                    
                    break
        else:
            new_full_song_name = f"{sites_elements.get(url).get('autor')} - {full_song_name.text}"
            
            if autor.lower() in new_full_song_name.lower():
                if song_name.lower() in new_full_song_name.lower():
                    if sites_elements.get(url).get("song_link") != "":
                        song_link = soup.find_all("a", class_ = sites_elements.get(url).get("song_link"))[song_index].get("href")
                    else:
                        song_link = full_song_name.get("href")
                    
                    break
    
    if song_link != "":
        if str(url) not in str(song_link):
            song_link = f"{url[:-1]}{song_link}"
        
        song_links.append(song_link)
    else:
        print(f"[INFO] Song: \"{video_name}\" not found!")

def download(video_name, url, song_link):
    needed_song_info = []
    needed_quality = "320"
    
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {"download.default_directory": "J:\Projects\Python\Dmitros_music_downloader_bot\Downloads\Musics",
                                                    "safebrowsing.enabled": "false"})

    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(song_link)
    
    info_wrapper = driver.find_element(By.CLASS_NAME, sites_elements.get(url).get("info_wrapper"))
    
    needed_song_info = info_wrapper.text.split("\n")
                    
    if needed_quality in needed_song_info[sites_elements.get(url).get("needed_quality")]:
        try:
            try:
                try:
                    download_button = WebDriverWait(driver, 10
                                                    ).until(expected_conditions.presence_of_all_elements_located((By.CLASS_NAME,
                                                                                                        sites_elements.get(url).get("download_button"))))
                    download_button[sites_elements.get(url).get("button_index")].click()
                except NoSuchElementException:
                    print(f"[ERROR] Cant download song: \"{video_name}\"!")
                    
                    driver.close()
                    
            except ElementClickInterceptedException:
                print(f"[ERROR] Cant download song: \"{video_name}\"!")
                
                driver.close()
        except TimeoutException:
            print(f"[ERROR] Cant download song: \"{video_name}\"!")            
            
            driver.close()
        
        seconds = 0
        download_wait = True
        path = "app\Downloads\Musics"
        
        rename_song = ""
        
        print(f"[INFO] Downloading song: {video_name}!")
        
        while download_wait:
            time.sleep(1)
            download_wait = False
            
            for file_name in os.listdir(path):
                if file_name.endswith(".crdownload"):
                    download_wait = True
                    
                    rename_song = file_name[0:-11]
            seconds += 1
        
        for file_name in os.listdir(path):
            if rename_song == file_name:
                os.rename(f"{path}/{rename_song}", f"{path}/{video_name}.mp3")
        
        print(f"[INFO] Song: \"{video_name}\" downloaded successfully in {seconds} seconds!")
    else:
        print(f"[INFO] Cant find high quality for song: \"{video_name}\"!")
    
        driver.close()

def download_song(song_name):
    for site in sites:
        print(site)
        
        downloaded = False
        path = "app\Downloads\Musics"
        
        for file_name in os.listdir(path):
            if song_name.lower() in file_name.lower():
                downloaded = True
                
                break
        
        if downloaded == False:
            html_file = get_searched_html(site, song_name)

            download_html(html_file)

            song_links = []

            get_music_links(song_name, song_links, site, html_file)

            print(song_links)
            
            if song_links != []:
                download(song_name, site, song_links[0])
            else:
                print(f"[INFO] Song: \"{song_name}\" not found!")
        
        else:
            print("Downloaded!")
            
            break
    
    return True

def download_songs(song_list):
    time.sleep(2)
    
    for song_name in song_list:
        download_song(song_name)

HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
}

needed_song_info = []

sites = [
    "https://mp3party.net/",
    "https://su.muzmo.cc/",
    "https://new.zmus.org/"
]

sites_elements = {
    "https://mp3party.net/": {
        "auto_search": True,
        "search": "",
        "enter_button": "",
        "song_link": "",
        "song_element": "",
        "autor": "",
        "full_song_name": "track__title",
        "info_wrapper": "track__infoWrapper",
        "needed_quality": 1,
        "download_button": "c-button_download",
        "button_index": 0
        },
    "https://su.muzmo.cc/": {
        "auto_search": True,
        "search": "",
        "enter_button": "",
        "song_link": "",
        "song_element": "",
        "autor": "",
        "full_song_name": "block",
        "info_wrapper": "text",
        "needed_quality": 0,
        "download_button": "block",
        "button_index": 1
        },
    "https://new.zmus.org/": {
        "auto_search": True,
        "search": "",
        "enter_button": "",
        "song_link": "",
        "song_element": "",
        "autor": "playlist-item-subtitle",
        "full_song_name": "playlist-item-title",
        "info_wrapper": "song-tags-list",
        "needed_quality": 1,
        "download_button": "song-download-btn",
        "button_index": 1
        }
}