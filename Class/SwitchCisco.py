import sys
import telnetlib
from .Exceptions.WrongPasswordError import WrongPasswordError

LOOP_LIMIT = 1000

class SwitchCisco:

	def __init__(self, ip, psw):
		self.ip = ip
		self.psw = psw
		self.name = self.generar_nombre()

	def generar_nombre(self):
		self.loguearse()
		self.enviar_comando("")
		self.leer_linea()
		nombre = self.leer_linea().replace('\n','').replace('\r','').replace('>','')
		if "Password" in nombre:
			raise WrongPasswordError
		self.desloguearse()
		return nombre
	
	def obtener_nombre(self):
		return self.name
	
	def obtener_ip(self):
		return self.ip

	def enviar_comando(self, cmd):
		cmd = cmd + "\n"
		self.tn.write(cmd.encode("ascii"))
	
	def leer_linea(self):
		return self.tn.read_until("\n".encode("ascii")).decode("ascii")
	
	def leer_lineas(self):
		return self.tn.read_all().decode("ascii")

	def desloguearse(self):
		self.enviar_comando("exit")

	def loguearse(self):
		self.tn = telnetlib.Telnet(self.ip)
		self.tn.read_until("Password: ".encode("ascii"))
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
		print(self.leer_lineas())

	def encender_interface(self, interface):
		self.loguearse_su()
		self.enviar_comando("configure terminal")
		self.enviar_comando("interface fastethernet 0/" + interface)
		self.enviar_comando("no shutdown")
		self.enviar_comando("end")
		self.desloguearse()
		print(self.leer_lineas())

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
		print(self.leer_lineas())

	def cambiar_interface_de_vlan(self, interface, vlan):
		self.loguearse_su()
		self.enviar_comando("configure terminal")
		self.enviar_comando("interface fastethernet 0/" + interface)
		self.enviar_comando("switchport access vlan " + vlan)
		self.enviar_comando("end")
		self.desloguearse()
		print(self.leer_lineas())

	def buscar_mac(self, mac_address):
		self.loguearse()
		self.enviar_comando("show mac address-table address " + mac_address)
		self.desloguearse()
		print(self.leer_lineas())
		
	def listar_vlans(self):
		self.loguearse()
		self.enviar_comando("show vlan")
		print(self.leer_linea())
		print(self.leer_linea())
		for i in range(LOOP_LIMIT):
			line = self.leer_linea()
			print(line.replace('\n',''))
			if line.startswith(self.name):
				break
			self.enviar_comando("\r")
		self.desloguearse()
		print(self.leer_lineas())

	def exportar_configuracion(self):
		self.loguearse_su()
		self.enviar_comando("show run")
		print(self.leer_linea())
		print(self.leer_linea())
		print(self.leer_linea())
		print(self.leer_linea())
		f = open(self.name + ".txt","w+")
		for i in range(LOOP_LIMIT):
			line = self.leer_linea()
			f.write(line.replace(" --More--         ",""))
			if line.startswith(self.name):
				break
			self.enviar_comando("\r")
		f.close()
		self.desloguearse()
		print(self.leer_lineas())
		
	def grabar_cambios(self):
		self.loguearse_su()
		self.enviar_comando("write")
		self.desloguearse()
		print(self.leer_lineas())
