import sys


class SSD:
    def __init__(self):
        pass

    def read(self, addr):
        try:
            filename = './nand.txt'
            nand_file = open(filename, 'r')
            lines = nand_file.readlines()

            filename = './result.txt'
            result_file = open(filename, 'w')
            result_file.write(lines[addr].strip())
        except:
            pass

    def write(self, addr, value):
        pass

