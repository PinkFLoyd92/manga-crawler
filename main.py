import manga_chooser
# import sys
from argparser import ArgParser
from config_parser import read_file

# MANGA_CHAPTER = sys.argv[2]
# MANGA_NAME = sys.argv[1]
DEFAULT_PATH = "Projects/mangafox/config/default.cfg"  # test...


def main():
    # test... Currently downloading just one chapter
    # manga_chooser.main_choose_manga(MANGA_NAME, MANGA_CHAPTER)
    arg_manager = ArgParser()
    arg_manager.add_arg()
    args = arg_manager.parser.parse_args()
    if args.config:
        manga_chooser.main_choose_manga(args.manga,
                                        args.chapter,
                                        read_file(args.config))
    # --manga/-m bleach --chapter/-c 1
    manga_chooser.main_choose_manga(manga_name=args.manga,
                                    chapters=args.chapter,
                                    path=read_file(DEFAULT_PATH),
                                    volumen=None)


if __name__ == '__main__':
    main()
