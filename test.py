import telnetlib

tn = telnetlib.Telnet("172.20.201.11")
tn.read_until(b"Password: ")
tn.write(b"hendrix\n")

### OBTIENE LA LINEA VACIA ###
tn.write(b"\n")
tn.read_until(b"\n")
empty_line = tn.read_until(b"\n")
print("Linea vacia >> ", empty_line)
##############################

tn.write(b"show vlan\n")

while True:
	line = tn.read_until(b"\n")
	print(line)
	if empty_line in line:
		break
	tn.write(b"\r\n")
tn.write(b"\n")	
'''
for i in range(100):
	string = tn.read_eager()
	print(i, string)
	tn.write(b"\r\n")
tn.write(b"\n")
print(tn.read_eager().decode("ascii"))
'''
'''
tn.write(b"\r")
print(tn.read_eager().decode("ascii"))
tn.write(b"\r")
print(tn.read_eager().decode("ascii"))
tn.write(b"\n")
print(tn.read_eager().decode("ascii"))
tn.write(b"exit\n")
'''
tn.write(b"exit\n")
sess_op = tn.read_all().decode("ascii")
#print(sess_op)
