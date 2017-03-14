import time
import os.path as path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from manga_crawler import Crawler


def print_formatted_urls(list_urls):
    index = 0
    print("\nChoose the manga you want to check: ")
    for url in list_urls:
        index = index + 1
        name = url.split('/')[4]
        print("\n %d.- %s" % (index, name))
    return index


def get_html_manga_souce(manga_name):
    driver = webdriver.Firefox()
    driver.set_page_load_timeout(3)
    driver.get("http://mangafox.me/directory/")
    elem = driver.find_element_by_id("searchform_name")
    elem.send_keys(manga_name)
    elem.send_keys(Keys.RETURN)
    time.sleep(6)
    driver.find_element_by_class_name("search_button").click()
    time.sleep(1)
    source = driver.page_source
    driver.close()
    return source


def get_list_of_mangas(manga_name):
    list_urls = []
    # testing purposes...
    if path.isfile("test.html"):
        fo = open("test.html", "r")
        soup = BeautifulSoup(fo.read(), 'html.parser')
        fo.close()
    else:
        source = get_html_manga_souce(manga_name)
        soup = BeautifulSoup(source, 'html.parser')
        # test
        fo = open("test.html", "w")
        fo.write(source)
        fo.close()

    div = soup.find(id="mangalist")
    mangalist = div.find("ul", "list")
    manga_anchors = mangalist.find_all("a")
    for anchor in manga_anchors:
        if anchor.get('href').count('/') == 5:
            list_urls.append(anchor.get('href'))
    list_urls = set(list_urls)
    return list_urls


def get_user_choice(list_urls):
    choice = None
    while 1:
        num_options = print_formatted_urls(list_urls)
        try:
            choice = input("\nOption:  ")
            choice = int(choice)
            if(choice in range(1, num_options + 1)):
                return list_urls[choice - 1]
            else:
                print("Choose a number in the range...")
        except NameError:
            print("Try again...")


def get_mangas_in_range(crawler, manga_chosen, chapters):
    range_mangas = map(int, chapters.split('-'))
    for mng in range_mangas:
        print(str(mng))


# manga_chosen: url to manga's main page.
def get_single_manga(crawler, manga_chosen, chapters):
    crawler.crawl_image_from_chapter(manga_chosen, chapters)


# chapters: String, volumen: String, manga_name: String
def main_choose_manga(manga_name, chapters=None, volumen=None):
    crawler = Crawler()
    list_urls = list(get_list_of_mangas(manga_name))
    manga_chosen = get_user_choice(list_urls)
    # print(manga_chosen)
    if volumen is not None:
        # DOWNLOAD VOLUMEN
        return -1
    if chapters is None:
        # DOWNLOAD EVERY CHAPTER AVAILABLE...
        return -1
    elif '-' in chapters:
        get_mangas_in_range(crawler, manga_chosen, chapters)
        return -1
    else:
        # DOWNLOAD A SINGLE CHAPTER.
        get_single_manga(crawler, manga_chosen, chapters)
        return -1


main_choose_manga('bleach', '1')
