class FileIO:
    def __init__(self, name, mode):
        if mode is 'r':
            self.contents = open(name + ".in", 'r').read().split("\n")
            self.out_file = None
            self.mode = 0
        elif mode is 'w':
            self.out_file = open(name + ".out", 'w')
            self.contents = None
            self.mode = 1
        elif mode is 'rw' or 'wr':
            self.contents = open(name + ".in", 'r').read().split("\n")
            self.out_file = open(name + ".out", 'w')
            self.mode = 2

    def readList(self, line_index):
        if self.mode is 0 or self.mode is 2:
            return list(map(int, self.contents[line_index].split(" ")))
        else:
            raise ValueError("hashcode/FileIO: Function reserved for READ and READ/WRITE modes only.")

    def readInt(self, line_index):
        if self.mode is 0 or self.mode is 2:
            return int(self.contents[line_index])
        else:
            raise ValueError("hashcode/FileIO: Function reserved for READ and READ/WRITE modes only.")


    def readGroup(self, line_index, length_pattern):
        if self.mode is 0 or self.mode is 2:
            return_list = []

            for i in range(length_pattern):
                return_list.append(self.readList(line_index + i))

            return return_list
        else:
            raise ValueError("hashcode/FileIO: Function reserved for READ and READ/WRITE modes only.")

    def readRepeatingGroup(self, line_index, length_pattern, iterations):
        if self.mode is 0 or self.mode is 2:
            return_list = []

            for i in range(iterations):
                self.readGroup(line_index + length_pattern * i, length_pattern)

            return return_list
        else:
            raise ValueError("hashcode/FileIO: Function reserved for READ and READ/WRITE modes only.")

    def writeLine(self, line):
        if self.mode is 1 or self.mode is 2:
            return self.out_file.write(line)
        else:
            raise ValueError("hashcode/FileIO: Function reserved for WRITE and READ/WRITE modes only.")

    def writeList(self, list):
        if self.mode is 1 or self.mode is 2:
            line = " ".join(map(str, list))
            return self.out_file.write(line + "\n")
        else:
            raise ValueError("hashcode/FileIO: Function reserved for WRITE and READ/WRITE modes only.")


    def writeClose(self):
        if self.mode is 1 or self.mode is 2:
            self.out_file.close()
        else:
            raise ValueError("hashcode/FileIO: Function reserved for WRITE and READ/WRITE modes only.")

class Logger:
    def __init__(self):
        pass

    def printParameters(self, param_dict):
        print("Simulation Parameters")
        print("-------------------------------")
        for key, value in param_dict.items():
            print("{}: {}".format(key, value))
        print("-------------------------------")
        print()


    def printList(self, name, list):
        print(name)
        print("-------------------------------")
        for item in list:
            print(item)
        print("-------------------------------")
        print()