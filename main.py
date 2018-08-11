import sys

from Class.CiscoMenu import CiscoMenu

def main():
	ip = None
	if len(sys.argv) > 1:
		ip = sys.argv[1]
	menu = CiscoMenu(ip)
	menu.run()
	
main()