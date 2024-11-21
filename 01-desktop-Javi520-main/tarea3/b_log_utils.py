import os

class BLog:
    total_num_tests: int
    passed_tests: int

    def __init__(self, fileName: str, path: str = ""):
        try:
            self.file_stream = open(file= './' + fileName, mode= 'w')
            self.total_num_tests = 0
            self.passed_tests = 0
        except OSError:
            print("Error while creating the log file, log system will not work")
    

    def log_(self, info: str = ""):
        #logging
        self.file_stream.write(info)
    
    def logn_(self, info: str = ""):
        #logging
        self.log_(info)
        self.file_stream.write("\n")

    def log(self, info: str = "", positivity: bool = True):
        #statistics
        if(positivity):
            self.passed_tests += 1
        self.total_num_tests += 1

        #logging
        self.file_stream.write(info)
    
    def logn(self, info: str = "", positivity: bool = True):
        self.log(info, positivity)
        self.file_stream.write("\n")
    
    def bake(self):
        try:
            self.file_stream.write("\n" +
                int.__str__(self.passed_tests) +
                " tests were success of " +
                int.__str__(self.total_num_tests) +
                "\n")
            self.file_stream.flush()
            self.file_stream.close()
        except OSError:
            print("Error IO")
        except Exception as err:
            print("Unkown error: ", err)