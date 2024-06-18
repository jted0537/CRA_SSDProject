import os
import pickle


class SSD:
    DATA_LOC = "../nand.txt"
    DATA_READ = "../result.txt"
    INIT_DATA = "0x00000000"
    MAX_ADDR = 100
    WRITE_SUCCESS = "SUCCESS"

    def __init__(self):
        if not os.path.exists(SSD.DATA_LOC):
            self.init_nand()

    def init_nand(self):
        initial_data = {}
        for i in range(SSD.MAX_ADDR):
            initial_data[i] = SSD.INIT_DATA

        with open(SSD.DATA_LOC, "wb") as handle:
            pickle.dump(initial_data, handle)

    def read(self, addr):
        try:
            with open(SSD.DATA_LOC, "rb") as handle:
                read_data = pickle.load(handle)

            with open(SSD.DATA_READ, 'w') as read_file:
                read_file.write(read_data[addr])
                read_file.close()
        except:
            pass

    def write(self, addr, value):
        pass

