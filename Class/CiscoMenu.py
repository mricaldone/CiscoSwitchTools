from .ScreenWriter import ScreenWriter
from .SwitchCisco import SwitchCisco
from .Exceptions.WrongPasswordError import WrongPasswordError

class CiscoMenu:

	def __init__(self):
		self.scrw = ScreenWriter()

	def mostrar_menu_listar_vlans(self):
		self.scrw.clear()
		self.sw.listar_vlans()
		self.scrw.wait()

	def mostrar_menu_cambiar_vlan_de_una_interfase(self):
		self.scrw.clear()
		n_interfase = self.scrw.input("Ingrese el numero de interfase: ")
		n_vlan = self.scrw.input("Ingrese el numero de VLAN: ")
		self.sw.cambiar_interface_de_vlan(n_interfase, n_vlan)
		self.scrw.wait()

	def mostrar_menu_reiniciar_interfase(self):
		self.scrw.clear()
		n_interfase = self.scrw.input("Ingrese el numero de interfase: ")
		self.sw.reiniciar_interface(n_interfase)
		self.scrw.wait()
		
	def mostrar_menu_buscar_mac(self):
		self.scrw.clear()
		mac_address = self.scrw.input("Ingrese la direccion mac (Formato 0000.0000.0000): ")
		self.sw.buscar_mac(mac_address)
		self.scrw.wait()

	def mostrar_menu_grabar_cambios(self):
		self.scrw.clear()
		self.sw.grabar_cambios()
		self.scrw.wait()
		
	def mostrar_menu_exportar_configuracion(self):
		self.scrw.clear()
		nombre_archivo = self.sw.obtener_nombre() + ".txt"
		self.scrw.write("Archivo " + nombre_archivo + "generado.")
		self.sw.exportar_configuracion()
		self.scrw.wait()

	def mostrar_menu_principal(self):
		sw_nombre = self.sw.obtener_nombre()
		sw_ip = self.sw.obtener_ip()
		sw_mac = self.sw.obtener_mac_address()
		opcion = -1
		while opcion != 0:
			opcion = -1
			while opcion < 0 or opcion > 6:
				self.scrw.clear()
				self.scrw.write("Cisco Switch Tools                           ")
				self.scrw.write("Conectado a " + sw_ip + " (" + sw_nombre + ")")
				self.scrw.write("MAC Address: " + sw_mac + "                  ")
				self.scrw.write("─────────────────────────────────────────────")
				self.scrw.write("1 - Listar VLANs                             ")
				self.scrw.write("2 - Cambiar la VLAN de una interfase         ")
				self.scrw.write("3 - Reiniciar una interfase                  ")
				self.scrw.write("4 - Buscar una direccion MAC                 ")
				self.scrw.write("5 - Grabar cambios                           ")
				self.scrw.write("6 - Exportar archivo de configuración        ")
				self.scrw.write("─────────────────────────────────────────────")
				self.scrw.write("0 - Salir")
				self.scrw.write("")
				opcion = int(self.scrw.input("Ingrese opcion: "))
			if opcion == 1:
				self.mostrar_menu_listar_vlans()
			if opcion == 2:
				self.mostrar_menu_cambiar_vlan_de_una_interfase()
			if opcion == 3:
				self.mostrar_menu_reiniciar_interfase()
			if opcion == 4:
				self.mostrar_menu_buscar_mac()
			if opcion == 5:
				self.mostrar_menu_grabar_cambios()
			if opcion == 6:
				self.mostrar_menu_exportar_configuracion()
		self.scrw.clear()

	def mostrar_portada(self):
		self.scrw.clear()
		self.scrw.write("   _______________ __________     __________  ____  __   _____")
		self.scrw.write("  / ____/  _/ ___// ____/ __ \   /_  __/ __ \/ __ \/ /  / ___/")
		self.scrw.write(" / /    / / \__ \/ /   / / / /    / / / / / / / / / /   \__ \ ")
		self.scrw.write("/ /____/ / ___/ / /___/ /_/ /    / / / /_/ / /_/ / /______/ / ")
		self.scrw.write("\____/___//____/\____/\____/    /_/  \____/\____/_____/____/  ")
		self.scrw.write("                                                              ")
		self.scrw.write("                     Matias Ricaldone 2018                    ")                             
		self.scrw.write("                                                              ")
		self.scrw.wait()

	def mostrar_formulario_de_conexion(self):
		self.scrw.clear()
		ip = self.scrw.input("IP del switch: ")
		psw = self.scrw.input_password()
		try:
			self.sw = SwitchCisco(ip, psw)
		except TimeoutError as e:
			self.scrw.write("Error de conexión.")
			exit()
		except WrongPasswordError as e:
			self.scrw.write("Error de contraseña.")
			exit()

	def run(self):
		self.mostrar_portada()
		self.mostrar_formulario_de_conexion()
		self.mostrar_menu_principal()
