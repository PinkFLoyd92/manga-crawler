import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from manga_crawler import Crawler
from config_parser import change_to_main_manga_dir
from config_parser import change_to_manga_dir
import urllib.request
import requests


def print_formatted_urls(list_urls):
    index = 0
    print("\nChoose the manga you want to check: ")
    for url in list_urls:
        index = index + 1
        name = url.split('/')[4]
        print("\n %d.- %s" % (index, name))
    return index


# this is one method, using selenium (not used...)
def get_html_manga_souce_selenium(manga_name):
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


def get_html_manga_source(manga_name):
    link = "http://mangafox.me/search.php?name_method=cw&name= " + manga_name  + "&type=&author_method=cw&author=&artist_method=cw&artist=&genres[Action]=0&genres[Adult]=0&genres[Adventure]=0&genres[Comedy]=0&genres[Doujinshi]=0&genres[Drama]=0&genres[Ecchi]=0&genres[Fantasy]=0&genres[Gender+Bender]=0&genres[Harem]=0&genres[Historical]=0&genres[Horror]=0&genres[Josei]=0&genres[Martial+Arts]=0&genres[Mature]=0&genres[Mecha]=0&genres[Mystery]=0&genres[One+Shot]=0&genres[Psychological]=0&genres[Romance]=0&genres[School+Life]=0&genres[Sci-fi]=0&genres[Seinen]=0&genres[Shoujo]=0&genres[Shoujo+Ai]=0&genres[Shounen]=0&genres[Shounen+Ai]=0&genres[Slice+of+Life]=0&genres[Smut]=0&genres[Sports]=0&genres[Supernatural]=0&genres[Tragedy]=0&genres[Webtoons]=0&genres[Yaoi]=0&genres[Yuri]=0&released_method=eq&released=&rating_method=eq&rating=&is_completed=&advopts=1"
    file = urllib.request.urlopen(link)
    return file.read().decode(file.headers.get_content_charset())


def get_list_of_mangas(manga_name):
    list_urls = []
    # testing purposes...
    # if path.isfile("test2.html"):
    #     fo = open("test.html", "r")
    #     soup = BeautifulSoup(fo.read(), 'html.parser')
    #     fo.close()
    # else:
    #     source = get_html_manga_source(manga_name)
    #     soup = BeautifulSoup(source, 'html.parser')
    #     # test
    #     fo = open("test.html", "w")
    #     fo.write(source)
    #     fo.close()

    source = get_html_manga_source(manga_name)
    soup = BeautifulSoup(source, 'html.parser')

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


def get_mangas_in_range(crawler, manga_chosen, chapters, path=None):
    range_mangas = map(int, chapters.split('-'))
    range_mangas = list(range_mangas)
    crawler.crawl_image_from_chapters(manga_chosen, range_mangas, path=path)


def get_number_of_chapters(manga_chosen):
    chapters = []
    main_manga_doc = requests.get(manga_chosen)
    soup = BeautifulSoup(main_manga_doc.content, 'html.parser')
    anchors = soup.find_all('a')
    for a in anchors:
        try:
            if('tips' in a['class']):
                chapters.append(a['href'].split('/')[5][1::])
        except KeyError:
            pass
    return chapters


def get_all_mangas(crawler, manga_chosen, path=None):
    range_chapters = get_number_of_chapters(manga_chosen)
    crawler.crawl_image_from_chapters(manga_chosen,
                                      range_chapters,
                                      path=path)


# manga_chosen: url to manga's main page.
def get_single_manga(crawler, manga_chosen, chapters):
    crawler.crawl_image_from_chapter(manga_chosen, chapters)


# chapters: String, volumen: String, manga_name: String
def main_choose_manga(manga_name,
                      chapters=None,
                      volumen=None,
                      path=None,
                      all_manga=False):
    root_dir = change_to_main_manga_dir(path)  # root manga directory..
    crawler = Crawler()
    list_urls = list(get_list_of_mangas(manga_name))
    manga_chosen = get_user_choice(list_urls)
    # print(manga_chosen)
    if volumen is not None:
        # DOWNLOAD VOLUMEN
        return -1
    if chapters is None and all_manga is True:
        # DOWNLOAD EVERY CHAPTER AVAILABLE...
        get_all_mangas(crawler, manga_chosen, path=root_dir)
        return -1
    elif '-' in chapters:
        get_mangas_in_range(crawler, manga_chosen, chapters, path=root_dir)
        return -1
    else:
        # DOWNLOAD A SINGLE CHAPTER.
        name = manga_chosen.split('/')[4]
        change_to_manga_dir(path, name, chapters)
        get_single_manga(crawler, manga_chosen, chapters)
        return -1
