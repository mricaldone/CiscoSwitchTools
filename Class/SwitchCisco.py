import sys
import telnetlib

class SwitchCisco:

	def __init__(self, ip, psw):
		self.ip = ip
		self.psw = psw

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

	def listar_vlans(self):
		self.loguearse()
		self.enviar_comando("show vlan")
		self.tn.write(b"\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r\r")
		self.enviar_comando("")
		self.desloguearse()
		print(self.tn.read_all().decode('ascii'))

