from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as BS
import time
import csv
import asyncio

def get_html(url):
    print("[INFO] Getting html!")
    
    chrome_options = Options()
    
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(chrome_options = chrome_options)
    driver.get(url)
    element = driver.find_element_by_tag_name("body")
    
    html = driver.page_source
    
    soup = BS(html, "html.parser")
    count = int(soup.find_all("span", class_ = "style-scope yt-formatted-string")[0].text[0]) + 1
        
    for i in range(0, count):
        print(f"[INFO] Loading page: {i + 1}/{count}!")
        
        element.send_keys(Keys.END)
        time.sleep(1)
    
    html = driver.page_source
    
    return html

def download_html(html):
    print(html)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

def write_video_names(video_names):
    for video_name in video_names:
        with open("Video_names.txt", "a", encoding="utf-8") as f:
            f.write(video_name + "\n")

def get_video_name_from_playlist(html):
    print("[INFO] Parsing Youtube playlist!")
    
    soup = BS(html, "html.parser")
    titles = soup.find_all("a", class_ = "yt-simple-endpoint style-scope ytd-playlist-video-renderer")
    autors = soup.find_all("a", class_ = "yt-simple-endpoint style-scope yt-formatted-string", spellcheck = "false")
    autors.remove(autors[0])
    autors.remove(autors[1])
    
    video_names = []
    
    print("[INFO] Filtering song names!")
    for i in range(0, len(titles)):
        title = titles[i].text[11:-9]
        autor = autors[i].text
        
        recicle_bin = [
            "(Official", "[Official",
            "(Oficial", "[Oficial",
            "(Lyric", "[Lyric",
            "(Music",
            "(Changes",
            "(Fan", "[Fan",
            "(From", "[From",
            "(Feat", "[Feat", "(Ft", "[Ft",
            "(Audio", "[Audio",
            "| Video Oficial", "| Video Official",
            "| Official Video",
            "Official Audio",
            "(Animated", "[Animated",
            "(With", "[With",
            "(Music", "[Music",
            "(Vertical", "[Vertical",
            "(By", "[By",
            "(The", "[The",
            "(Performance", "[Performance",
            "(Premium", "[Premium",
            "(Fifty",
            "(Live", "[Live",
            "- Topic",
            "Feat", "Ft",
            ","
        ]
        
        for bins in recicle_bin[0:-3]:
            for i in range(0, len(title)):
                    if bins.lower() in title[i:i + len(bins)]:
                        title = title[0:i]
                        if " " in title[-1:]:
                            title = title[0:-1]
                    elif bins in title[i:i + len(bins)]:
                        title = title[0:i]
                        if " " in title[-1:]:
                            title = title[0:-1]
                    elif bins.upper() in title[i:i + len(bins)]:
                        title = title[0:i]
                        if " " in title[-1:]:
                            title = title[0:-1]
        
        connectors = ["-", "–", "||", "|", "//", "/", ":"]
        
        for connector in connectors:
            if connector in title:
                title = title.replace(connector, "-")
        
        if "-" not in title:
            if "|" not in title:
                title = f"{autor} - {title}"
        
        full_song_name = []
        
        for connector in connectors:
            if connector in title:                
                full_song_name = title.split(connector)
        
        autor = ""
        song = ""
        
        if len(full_song_name) > 2:
            for i in range(0, len(full_song_name) - 1):
                autor += full_song_name[i]
                
                if i < len(full_song_name) - 2:
                    autor += "-"
            
            song = full_song_name[len(full_song_name) - 1]
        else:
            autor = full_song_name[0]
            song = full_song_name[1]
                
        song_list = [autor, song]
        
        forbidden_symbols = ["\."[:-1], "/", ":", "*", "?", '"', "<", ">", "|", "+", ".", "%", "!", "@", "“", "”", "'"]
        
        for forbidden_symbol in forbidden_symbols:
            for i in range(0, 2):
                song_list[i] = song_list[i].replace(forbidden_symbol, "")
        
        for bins in recicle_bin:
            for i in range(0, 2):
                for j in range(0, len(song_list[i])):
                    if bins.lower() in song_list[i][j:j + len(bins)]:
                        song_list[i] = song_list[i][0:j]
                        if " " in song_list[i][-1:]:
                            song_list[i] = song_list[i][0:-1]
                    elif bins in song_list[i][j:j + len(bins)]:
                        song_list[i] = song_list[i][0:j]
                        if " " in song_list[i][-1:]:
                            song_list[i] = song_list[i][0:-1]
                    elif bins.upper() in song_list[i][j:j + len(bins)]:
                        song_list[i] = song_list[i][0:j]
                        if " " in song_list[i][-1:]:
                            song_list[i] = song_list[i][0:-1]
                    elif " " in song_list[i][-1:]:
                        song_list[i] = song_list[i][0:-1]
                    elif " " in song_list[i][0:1]:
                        song_list[i] = song_list[i][1:len(song_list[i])]
        
        title = f"{song_list[0]} - {song_list[1]}"
            
        video_names.append(title)
    
    return video_names

API_KEY = "AIzaSyAHCGm5gPtR1UnoyKHldnMWrDp8RDo8byw"
HOST = "https://www.youtube.com"
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
}