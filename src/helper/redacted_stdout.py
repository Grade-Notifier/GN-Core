import sys

class STDOutOptions:
    ERROR = 0
    STDOUT = 1

class RedactedPrint:

    def __init__(self, option, redacted_list):
        self.func = None
        self.origOut = None
        self.option = option
        self.redacted_list = redacted_list

    def enable(self, func=None):

            if self.option == STDOutOptions.STDOUT:
                sys.stdout = self
            else:
                sys.stderr = self

            ## Monkey Patch
            self.origOut = sys.__stdout__ \
                if self.option == STDOutOptions.STDOUT \
                else sys.__stderr__

    def disable(self):
        self.origOut.flush()
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def write(self, text):
        if text.split() == []:
            self.origOut.write(text)
        for word in self.redacted_list:
            text = text.replace(word, "REDACTED")
        self.origOut.write(text)
             
    #pass all other methods to __stdout__ so that we don't have to override them
    def __getattr__(self, name):
        return self.origOut.__getattr__(name)
    