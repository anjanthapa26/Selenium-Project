import os


def create_demo_file():
    if not os.path.exists('./demofile.txt'):
        with open('./demofile.txt') as d_file:
            d_file.write()


def setup():
    create_demo_file()


if __name__ == '__main__':
    setup()
