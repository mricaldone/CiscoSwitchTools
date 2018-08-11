import sys
import telnetlib
from .Exceptions.WrongPasswordError import WrongPasswordError
from .CiscoTelnet import CiscoTelnet

LOOP_LIMIT = 1000

class SwitchCisco:

	def __init__(self, ip, psw):
		self.ip = ip
		self.psw = psw
		self.telnet = CiscoTelnet(ip)
		#self.name = self.generar_nombre()
		#self.mac = self.generar_mac_address()	
		self.name = ""
		self.mac = ""

	def generar_nombre(self):
		self.loguearse()
		self.telnet.enviar_comando("")
		self.telnet.leer_linea()
		nombre = self.telnet.leer_linea().replace('\n','').replace('\r','').replace('>','')
		if "Password" in nombre:
			raise WrongPasswordError
		self.desloguearse()
		return nombre
	
	def generar_mac_address(self):
		mac_address = ""
		self.loguearse()
		lines = self.telnet.enviar_comando_y_leer("show version").split("\n")
		for line in lines:
			if line.startswith("Base ethernet MAC Address"):
				mac_address = ":".join(line.split(":")[1:])
				break
		#self.enviar_comando("show version")
		#self.leer_linea()
		#self.leer_linea()
		#for i in range(LOOP_LIMIT):
		#	line = self.leer_linea().replace("--More--","").replace("\x08","").strip()
		#	if line.startswith("Base ethernet"):
		#		mac_address = ":".join(line.split(":")[1:])
		#		break
		#	if line.startswith(self.name + ">"):
		#		break
		#	self.enviar_comando("\r")
		self.desloguearse()
		return mac_address
	
	def obtener_nombre(self):
		return self.name
	
	def obtener_ip(self):
		return self.ip
	
	def obtener_mac_address(self):
		return self.mac

	def desloguearse(self):
		self.telnet.enviar_comando("exit")
		self.telnet.desconectarse()

	def loguearse(self):
		self.telnet = CiscoTelnet(self.ip)
		self.telnet.esperar_contrasenya()
		self.telnet.enviar_comando(self.psw)

	def loguearse_su(self):
		self.loguearse()
		self.telnet.enviar_comando("enable")
		self.telnet.enviar_comando(self.psw)

	def apagar_interface(self, interface):
		self.loguearse_su()
		self.telnet.enviar_comando("configure terminal")
		self.telnet.enviar_comando("interface fastethernet 0/" + interface)
		self.telnet.enviar_comando("shutdown")
		self.telnet.enviar_comando("end")
		self.desloguearse()
		print(self.telnet.leer_todo())

	def encender_interface(self, interface):
		self.loguearse_su()
		self.enviar_comando("configure terminal")
		self.enviar_comando("interface fastethernet 0/" + interface)
		self.enviar_comando("no shutdown")
		self.enviar_comando("end")
		self.desloguearse()
		print(self.telnet.leer_todo())

	def reiniciar_interface(self, interface):
		self.loguearse_su()
		self.telnet.enviar_comando("configure terminal")
		self.telnet.enviar_comando("interface fastethernet 0/" + interface)
		self.telnet.enviar_comando("shutdown")
		self.telnet.enviar_comando("end")
		self.telnet.enviar_comando("configure terminal")
		self.telnet.enviar_comando("interface fastethernet 0/" + interface)
		self.telnet.enviar_comando("no shutdown")
		self.telnet.enviar_comando("end")
		self.desloguearse()
		print(self.telnet.leer_todo())

	def cambiar_interface_de_vlan(self, interface, vlan):
		self.loguearse_su()
		self.telnet.enviar_comando("configure terminal")
		self.telnet.enviar_comando("interface fastethernet 0/" + interface)
		self.telnet.enviar_comando("switchport access vlan " + vlan)
		self.telnet.enviar_comando("end")
		self.desloguearse()
		print(self.telnet.leer_todo())

	def buscar_mac(self, mac_address):
		self.loguearse()
		self.telnet.enviar_comando("show mac address-table address " + mac_address)
		self.desloguearse()
		print(self.telnet.leer_todo())
		
	def listar_vlans(self):
		self.loguearse()
		lines = self.telnet.enviar_comando_y_leer("show vlan brief").split("\n")
		for line in lines:
			print(line)
		#self.enviar_comando("show vlan")
		#print(self.leer_linea())
		#print(self.leer_linea())
		#for i in range(LOOP_LIMIT):
		#	line = self.leer_linea()
		#	print(line.replace('\n',''))
		#	if line.startswith(self.name):
		#		break
		#	self.enviar_comando("\r")
		self.desloguearse()

	def exportar_configuracion(self):
		self.loguearse_su()
		lines = self.telnet.enviar_comando_y_leer("show run").split("\n")
		for line in lines:
			print(line)
		#self.enviar_comando("show run")
		#print(self.leer_linea())
		#print(self.leer_linea())
		#print(self.leer_linea())
		#print(self.leer_linea())
		#f = open(self.name + ".txt","w+")
		#for i in range(LOOP_LIMIT):
		#	line = self.leer_linea().replace("--More--","").replace("\x08","").strip()
		#	print(line)
		#	if not line.startswith("Building") and not line.startswith("!") and not line.startswith("Current") and not line.startswith(self.name):
		#		f.write(line + "\n")
		#	if line.startswith(self.name):
		#		break
		#	self.enviar_comando("\r")
		#f.close()
		self.desloguearse()
		
	def grabar_cambios(self):
		self.loguearse_su()
		self.telnet.enviar_comando("write")
		self.desloguearse()
		print(self.telnet.leer_todo())
