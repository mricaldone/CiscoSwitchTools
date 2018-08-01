import os

class ScreenWriter:
    
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def write(self, txt):
        print(txt)
        
    def input(self, msg):
        return input(msg)
    
    def wait(self):
        os.system('pause' if os.name == 'nt' else 'read -s -n 1 -p "Press any key to continue..."')