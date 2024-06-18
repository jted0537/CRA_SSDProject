class Shell:
    def __init__(self):
        self._lbas = [0] * 100

    def write(self, addr, val):
        pass

    def read(self, addr):
        pass

    def exit(self):
        pass

    def help(self):
        pass

    def full_write(self):
        pass

    def full_read(self):
        for addr in range(100):
            self.read(addr)
