#stores the instruction fetched from mem
class MBR:
    def __init__(self,word):
        self.word = None
    
    def set_word(self,word):
        self.word = word
    
    def get_word(self,word):
        return self.word