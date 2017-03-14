import manga_chooser
import sys

MANGA_CHAPTER = sys.argv[2]
MANGA_NAME = sys.argv[1]


def main():
    manga_chooser.main_choose_manga(MANGA_NAME, MANGA_CHAPTER)


if __name__ == '__main__':
    main()
