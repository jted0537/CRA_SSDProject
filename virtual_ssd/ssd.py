import sys


class SSD:
    def __init__(self):
        pass

    def read(self, addr):
        return 1

    def write(self, addr, value):
        pass


def main(argv):
    if argv[1] != 'ssd':
        return "INVALID COMMAND"

if __name__ == "__main__":
    main(sys.argv)


