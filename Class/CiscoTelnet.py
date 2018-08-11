import telnetlib

READ_TIMEOUT = 5000
LOOP_LIMIT = 1000

class CiscoTelnet:
	
	def __init__(self, ip):
		self.tn = telnetlib.Telnet(ip)
	
	def enviar_comando(self, cmd):
		cmd = cmd + "\n"
		self._write(cmd)
	
	def leer_linea(self):
		return self._read_until("\n")
	
	def leer_todo(self):
		return self._read_all()
	'''
	def enviar_comando_y_leer(self, cmd):
		txt = ""
		cmd = cmd + "\n"
		self.tn.write(cmd.encode("ascii"))
		txt = txt + self.tn.read_until("\n".encode("ascii")).decode("ascii") + "\n"
		txt = txt + self.tn.read_until("\n".encode("ascii")).decode("ascii") + "\n"
		for i in range(LOOP_LIMIT):
			data = self.tn.expect([" --More-- ".encode("ascii"), (self.name + ">").encode("ascii"), (self.name + "#").encode("ascii")], READ_TIMEOUT)
			line = data[2].decode("ascii").replace("--More--","").replace("\x08","").strip()
			txt = txt + line + "\n"
			if data[0] == 0:
				self.tn.write("\r\n".encode("ascii"))
			if data[0] == -1 or data[0] == 1 or data[0] == 2:
				break
		return txt
	'''
	
	def _write(self, texto):
		return self.tn.write(texto.encode("ascii"))
	
	def _expect(self, lista):
		for i in range(len(lista)):
			lista[i] = lista[i].encode("ascii")
		index, match, text = self.tn.expect(lista, READ_TIMEOUT)
		return text.decode("ascii")
	
	def _read_until(self, texto):
		return self.tn.read_until(texto.encode("ascii"), READ_TIMEOUT).decode("ascii")
	
	def _read_all(self):
		return self.tn.read_all().decode("ascii")
	
	def enviar_comando_y_leer(self, cmd):
		self.enviar_comando(cmd)
		stop_line = " --More-- "
		texto = self._expect([stop_line])
		if texto.endswith(stop_line):
			texto = texto[:-len(stop_line)]
			#return self.enviar_comando_y_leer(" ")
		return texto
	
	def esperar_contrasenya(self):
		self._read_until("Password: ")
		
	def desconectarse(self):
		self.tn.close()