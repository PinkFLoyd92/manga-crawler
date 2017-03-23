import argparse

DESCRIPTION = "Easy way to download all your mangas from mangafox."


class ArgParser:
    def __init__(self, description=None):
        "docstring"
        if description is not None:
            self.parser = argparse.ArgumentParser(description=description)
        else:
            self.parser = argparse.ArgumentParser(description=DESCRIPTION)
        pass

    def add_arg(self):
        self.parser.add_argument("-m",
                                 "--manga",
                                 type=str,
                                 help="Choose Manga to look-up for...")
        self.parser.add_argument("-vl",
                                 "--volume",
                                 type=int,
                                 help="Choose volume...")
        self.parser.add_argument("-c",
                                 "--chapter",
                                 type=str,
                                 help="Choose chapter...")

        self.parser.add_argument("-a",
                                 "--all",
                                 help="download every chapter available...",
                                 action="store_true")

        self.parser.add_argument("--config",
                                 help="Custom config file.")
