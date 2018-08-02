import sys
import telnetlib

LOOP_LIMIT = 1000

class SwitchCisco:

	def __init__(self, ip, psw):
		self.ip = ip
		self.psw = psw
		self.name = self.generar_nombre()

	def generar_nombre(self):
		self.loguearse()
		self.tn.write(b"\n")
		self.tn.read_until(b"\n")
		nombre = self.tn.read_until(b"\n").decode("ascii").replace('\n','').replace('\r','').replace('>','')
		self.desloguearse()
		return nombre
	
	def obtener_nombre(self):
		return self.name
	
	def obtener_ip(self):
		return self.ip

	def enviar_comando(self, cmd):
		self.tn.write(cmd.encode('ascii') + b"\n")

	def desloguearse(self):
		self.enviar_comando("exit")

	def loguearse(self):
		self.tn = telnetlib.Telnet(self.ip)
		self.tn.read_until(b"Password: ")
		self.enviar_comando(self.psw)

	def loguearse_su(self):
		self.loguearse()
		self.enviar_comando("enable")
		self.enviar_comando(self.psw)

	def apagar_interface(self, interface):
		self.loguearse_su()
		self.enviar_comando("configure terminal")
		self.enviar_comando("interface fastethernet 0/" + interface)
		self.enviar_comando("shutdown")
		self.enviar_comando("end")
		self.desloguearse()
		print(self.tn.read_all().decode('ascii'))

	def encender_interface(self, interface):
		self.loguearse_su()
		self.enviar_comando("configure terminal")
		self.enviar_comando("interface fastethernet 0/" + interface)
		self.enviar_comando("no shutdown")
		self.enviar_comando("end")
		self.desloguearse()
		print(self.tn.read_all().decode('ascii'))

	def reiniciar_interface(self, interface):
		self.loguearse_su()
		self.enviar_comando("configure terminal")
		self.enviar_comando("interface fastethernet 0/" + interface)
		self.enviar_comando("shutdown")
		self.enviar_comando("end")
		self.enviar_comando("configure terminal")
		self.enviar_comando("interface fastethernet 0/" + interface)
		self.enviar_comando("no shutdown")
		self.enviar_comando("end")
		self.desloguearse()
		print(self.tn.read_all().decode('ascii'))

	def cambiar_interface_de_vlan(self, interface, vlan):
		self.loguearse_su()
		self.enviar_comando("configure terminal")
		self.enviar_comando("interface fastethernet 0/" + interface)
		self.enviar_comando("switchport access vlan " + vlan)
		self.enviar_comando("end")
		self.desloguearse()
		print(self.tn.read_all().decode('ascii'))

	def buscar_mac(self, mac_address):
		self.loguearse()
		self.enviar_comando("show mac address-table address " + mac_address)
		self.desloguearse()
		print(self.tn.read_all().decode('ascii'))
		
	def listar_vlans(self):
		self.loguearse()
		self.tn.write(b"show vlan\n")
		print(self.tn.read_until(b"\n").decode("ascii"))
		print(self.tn.read_until(b"\n").decode("ascii"))
		for i in range(LOOP_LIMIT):
			line = self.tn.read_until(b"\n").decode("ascii")
			print(line.replace('\n',''))
			if self.name in line:
				break
			self.tn.write(b"\r\n")
		self.desloguearse()
		print(self.tn.read_all().decode('ascii'))

	def grabar_cambios(self):
		self.loguearse_su()
		self.enviar_comando("write")
		self.desloguearse()
		print(self.tn.read_all().decode('ascii'))
