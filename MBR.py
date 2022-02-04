#stores the instruction fetched from mem
class MBR:
    def __init__(self,val=None):
        self.val = val
    
    def set_val(self,val):
        self.val = val
    
    def get_val(self):
        return self.val