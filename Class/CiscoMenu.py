from ScreenWriter.py import ScreenWriter

class CiscoMenu:
    
    def __init__(self):
        self.sw = ScreenWriter()
    
    def mostrar_menu_listar_vlans(self):
        self.sw.clear()
        self.sw.print("Listado de vlans...")
        
    def mostrar_menu_cambiar_vlan_de_una_interfase(self):
        self.sw.clear()
        n_interfase = self.sw.input("Ingrese el numero de interfase")
        n_vlan = self.sw.input("Ingrese el numero de VLAN")
        self.sw.print("<RESPUESTA>")
        self.sw.wait()
        
    def mostrar_menu_reiniciar_interfase(self):
        self.sw.clear()
        n_interfase = self.sw.input("Ingrese el numero de interfase")
        self.sw.print("<RESPUESTA>")
        self.sw.wait()
    
    def run(self):
        opcion = -1
        while(opcion != 0):
            opcion = -1
            while(opcion < 0 or opcion > 3):
                self.sw.clear()
                self.sw.print("Cisco Switch Tools")
                self.sw.print("-------------------------------------------")
                self.sw.print("1 - Listar VLANs")
                self.sw.print("2 - Cambiar la VLAN de una interfase")
                self.sw.print("3 - Reiniciar una interfase")
                self.sw.print("-------------------------------------------")
                self.sw.print("0 - Salir")
                opcion = int(self.sw.input("Ingrese opcion: "))
            if(opcion == 1) self.mostrar_menu_listar_vlans()
            if(opcion == 2) self.mostrar_menu_cambiar_vlan_de_una_interfase()
            if(opcion == 3) self.mostrar_menu_reiniciar_interfase()
        
        