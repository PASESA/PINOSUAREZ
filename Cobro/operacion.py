import pymysql
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import qrcode
from tkinter import messagebox as mb

class Operacion:

	def abrir(self):
		conexion=pymysql.connect(host="localhost",
								 user="Aurelio",
								 passwd="RG980320",
								 database="Parqueadero1")

		return conexion


	def altaRegistroRFID(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="insert into Entradas(Entrada, CorteInc, Placas) values (%s,%s,%s)"
		cursor.execute(sql, datos)
		cone.commit()
		cone.close()

	def guardacobro(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql = "update Entradas set vobo = %s, Importe = %s, TiempoTotal = %s, Entrada = %s, Salida = %s,TarifaPreferente = %s where id = %s;"
		cursor.execute(sql, datos)
		cone.commit()
		cone.close()

	def consulta(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select Entrada, Salida from Entradas where id=%s"
	   #sql="select descripcion, precio from articulos where codigo=%s"
		cursor.execute(sql, datos)
		cone.close()
		return cursor.fetchall()

	def recuperar_todos(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select id, Entrada, Salida from Entradas"
		cursor.execute(sql)
		cone.close()
		return cursor.fetchall()

	def recuperar_sincobro(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select id, Entrada, Salida, Importe from Entradas where CorteInc = 0 and Importe is not null "
		cursor.execute(sql)
		cone.close()
		return cursor.fetchall()
	def desglose_cobrados(self,Numcorte):
		cone=self.abrir()
		cursor=cone.cursor()
		#sql="SELECT TarifaPreferente,Importe, Count(*) as cuantos FROM Entradas where CorteInc = 6 "
		#sql="SELECT TarifaPreferente,Importe, Count(*) as cuantos FROM Entradas where CorteInc = %s GROUP BY TarifaPreferente,Importe;"
		sql="SELECT Count(*),TarifaPreferente,Importe, Count(*)*Importe  as cuantos FROM Entradas where CorteInc = %s GROUP BY TarifaPreferente,Importe;"
		#sql="select id, Entrada, Salida, Importe from Entradas where CorteInc = 0 and Importe is not null "
		cursor.execute(sql,Numcorte)
		cone.close()
		return cursor.fetchall()
	def Autos_dentro(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select id, Entrada, Placas from Entradas where CorteInc = 0 and Importe is null and Salida is null "
		cursor.execute(sql)
		cone.close()
		return cursor.fetchall()

	def CuantosAutosdentro(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select count(*) from Entradas where CorteInc = 0 and Importe is null and Salida is null "
		cursor.execute(sql)
		cone.close()
		return cursor.fetchall()
	def Quedados_Sensor(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select Quedados from Cortes where Folio=%s"
	   #sql="select descripcion, precio from articulos where codigo=%s"
		cursor.execute(sql, datos)
		cone.close()
		return cursor.fetchall()

	def NumBolQued(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select NumBolQued from Cortes where Folio=%s"
	   #sql="select descripcion, precio from articulos where codigo=%s"
		cursor.execute(sql, datos)
		cone.close()
		return cursor.fetchall()
	def EntradasSensor(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select EntSens from AccesosSens where Folio=1"
	   #sql="select descripcion, precio from articulos where codigo=%s"
		cursor.execute(sql)
		cone.close()
		return cursor.fetchall()
	def SalidasSensor(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select SalSens from AccesosSens where Folio=1"
	   #sql="select descripcion, precio from articulos where codigo=%s"
		cursor.execute(sql)
		cone.close()
		return cursor.fetchall()

	def CuantosBoletosCobro(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select count(*) from Entradas where CorteInc = 0 and Importe is not null and Salida is not null "
		cursor.execute(sql)
		cone.close()
		return cursor.fetchall()
	def BEDCorte(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select count(*) from Entradas where ((vobo is null and TarifaPreferente is null) or (vobo = 'lmf' and TarifaPreferente = ''))"
		cursor.execute(sql)
		cone.close()
		return cursor.fetchall()

	def BAnteriores(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select count(*) from Entradas where vobo = 'ant' "
		cursor.execute(sql)
		cone.close()
		return cursor.fetchall()

	def corte(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select sum(importe) from Entradas where CorteInc = 0"
		cursor.execute(sql)
		cone.close()
		return cursor.fetchall()
	def MaxfolioEntrada(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select max(id) from Entradas;"
		cursor.execute(sql)
		cone.close()
		return cursor.fetchall()

	def Maxfolio_Cortes(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select max(Folio) from Cortes;"
		cursor.execute(sql)
		cone.close()
		return cursor.fetchall()

	def ActualizarEntradasConcorte(self, maxnum):
		cone=self.abrir()
		cursor=cone.cursor()
		sql = "update Entradas set CorteInc = %s, vobo = %s where TiempoTotal is not null and CorteInc=0;"
		#sql = "update Entradas set CorteInc=%s where TiempoTotal is not null and CorteInc=0;"
		cursor.execute(sql,maxnum)
		cone.commit()
		cone.close()

	def NocobradosAnt(self, vobo):
		cone=self.abrir()
		cursor=cone.cursor()
		sql = "update Entradas set vobo = %s where Importe is null and CorteInc=0;"
		cursor.execute(sql,vobo)
		cone.commit()
		cone.close()

	def obtenerNumCorte(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select max(Folio) from Cortes"
		#sql = "update Entradas set CorteInc = 1 WHERE Importe > 0"
		cursor.execute(sql)
		#cone.commit()
		cone.close()
		return cursor.fetchall()
	def MaxnumId(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select max(idInicial) from Cortes"
		#sql = "update Entradas set CorteInc = 1 WHERE Importe > 0"
		cursor.execute(sql)
		#cone.commit()
		cone.close()
		return cursor.fetchall()

	def GuarCorte(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="insert into Cortes(Importe, FechaIni, FechaFin,Quedados,idInicial,NumBolQued) values (%s,%s,%s,%s,%s,%s)"
		#sql = "update Entradas set CorteInc = 1 WHERE Importe > 0"
		cursor.execute(sql,datos)
		cone.commit()
		cone.close()
	def UltimoCorte(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="select max(FechaFin) from Cortes;"
		#sql="select max(FechaFin) from Cortes;"
		cursor.execute(sql)
		cone.close()
		return cursor.fetchall()
		
	def Cortes_MaxMin(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="SELECT max(FechaFin), min(FechaFin) FROM Cortes where MONTH(FechaFin)=%s AND YEAR(FechaFin)=%s " 
		cursor.execute(sql,datos)
		cone.close()
		return cursor.fetchall()
	def Cortes_Folio(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="SELECT Folio FROM Cortes where FechaFin=%s" 
		cursor.execute(sql,datos)
		cone.close()
		return cursor.fetchall()
	def Registros_corte(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="SELECT id, Entrada, Salida, TiempoTotal, Importe, CorteInc, Placas, TarifaPreferente FROM Entradas where CorteInc > (%s-1) AND CorteInc < (%s+1)"  #CorteInc > (%s-1) AND CorteInc < (%s+1)
		cursor.execute(sql,datos)
		cone.close()
		return cursor.fetchall()
	def Totales_corte(self, datos1):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="SELECT sum(Importe), max(CorteInc), min(CorteInc) FROM Entradas where CorteInc > (%s-1) AND CorteInc < (%s+1)" #Entrada > %s AND Entrada < %s
		cursor.execute(sql,datos1)
		cone.close()
		return cursor.fetchall()

 #####USUARIOS###

	def ConsultaUsuario(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="SELECT Id_usuario, Contrasena, Nom_usuario FROM Usuarios WHERE Usuario = %s"
		cursor.execute(sql,datos)
		cone.close()
		return cursor.fetchall() 
	def CajeroenTurno(self):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="SELECT min(id_movs), nombre, inicio, turno, Idusuario FROM MovsUsuarios where CierreCorte is null"
		cursor.execute(sql)
		cone.close()
		return cursor.fetchall()   
	def IniciosdeTurno(self, dato):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="SELECT inicio, usuario FROM MovsUsuarios where inicio > %s" #and CierreCorte = 'No aplica'  Idusuario = %s and 
		cursor.execute(sql, dato)
		cone.close()
		return cursor.fetchall()                 
	def ActuaizaUsuario(self, actual):
		cone=self.abrir()
		cursor=cone.cursor()
		sql="INSERT INTO MovsUsuarios(Idusuario, usuario, inicio, nombre, turno) values (%s,%s,%s,%s,%s)"
		#sql="INSERT INTO PagosPens(idcliente, num_tarjeta, Fecha_pago, Fecha_vigencia, Mensualidad, Monto) values (%s,%s,%s,%s,%s,%s)"
		cursor.execute(sql,actual)
		cone.commit()
		cone.close()
	def Cierreusuario(self, datos):
		cone=self.abrir()
		cursor=cone.cursor()
		sql = "update MovsUsuarios set CierreCorte = %s where  id_movs = %s;"
		cursor.execute(sql,datos)
		cone.commit()
		cone.close()
	def NoAplicausuario(self, dato):
		cone=self.abrir()
		cursor=cone.cursor()
		sql = "update MovsUsuarios set CierreCorte = 'No aplica' where  id_movs > %s;"
		cursor.execute(sql,dato)        
		cone.commit()
		cone.close()


	def cifrar_AES(self, texto_plano: str, clave: str = "PASE") -> tuple:
		"""
		Cifra un mensaje en texto plano utilizando el algoritmo de cifrado AES con una clave proporcionada.

		Args:
			texto_plano (str): El mensaje que se desea cifrar en texto plano.
			clave (str, opcional): La clave que se utilizará para cifrar el mensaje. Debe ser una cadena de caracteres ASCII.
				Por defecto es "PASE".

		Returns:
			tuple: Una tupla que contiene el texto cifrado y el vector de inicialización utilizado para cifrar el mensaje.
				El texto cifrado es una cadena de caracteres ASCII codificada en Base64, y el vector de inicialización es una cadena
				de bytes de 16 caracteres.

		Raises:
			TypeError: Si el argumento texto_plano no es una cadena de caracteres.
			TypeError: Si el argumento clave no es una cadena de caracteres.
			ValueError: Si la longitud de la clave proporcionada es mayor que 32 caracteres.

		"""
		try:
			# Convertir la clave en una clave de 32 caracteres
			clave_hash = hashlib.sha256(clave.encode()).digest()

			# Crear un objeto de cifrado AES
			cipher = AES.new(clave_hash, AES.MODE_CBC)

			# Cifrar el texto plano y convertirlo en una cadena de bytes
			texto_cifrado_bytes = cipher.encrypt(pad(texto_plano.encode(), AES.block_size))

			# Codificar la cadena de bytes en Base64
			texto_cifrado = base64.b64encode(texto_cifrado_bytes).decode()

			# Guardar el vector de inicialización
			iv = cipher.iv

			# Retornar el texto cifrado y el vector de inicialización
			return texto_cifrado, iv

		except TypeError as error:
			mb.showwarning("Error", f"El texto a decifrar no es una cadena de caracteres, intente nuevamente.\nSi el error continua muestre el siguiente mensaje a un administrador: {error}")

		except ValueError as error:
			mb.showwarning("Error", f"la longitud de la clave proporcionada es mayor que 32 caracteres, intente nuevamente.\nSi el error continua muestre el siguiente mensaje a un administrador: {error}")

		except Exception as e:
			mb.showwarning("Error", f"Ha ocurrido un error inesperado al codificar, intente nuevamente.\nSi el error continua muestre el siguiente mensaje a un administrador: {e}")

	def descifrar_AES(self, texto_cifrado: str, iv: bytes, clave: str = "PASE") -> str:
		"""
		Descifra un mensaje cifrado en texto plano utilizando el algoritmo de cifrado AES con una clave y un vector de inicialización proporcionados.

		Args:
			texto_cifrado (str): El mensaje cifrado que se desea descifrar. Debe ser una cadena de caracteres ASCII codificada en Base64.
			iv (bytes): El vector de inicialización utilizado para cifrar el mensaje. Debe ser una cadena de bytes de 16 caracteres.
			clave (str, opcional): La clave que se utilizará para cifrar el mensaje. Debe ser una cadena de caracteres ASCII.
				Por defecto es "PASE".

		Returns:
			texto_descifrado (str): El texto descifrado en formato de cadena de caracteres ASCII.

		Raises:
			TypeError: Si el argumento texto_cifrado no es una cadena de caracteres.
			TypeError: Si el argumento iv no es una cadena de bytes.
			TypeError: Si el argumento clave no es una cadena de caracteres.
			ValueError: Si la longitud de la clave proporcionada es mayor que 32 caracteres.
			ValueError: Si la longitud del vector de inicialización proporcionado es diferente de 16 caracteres.
			ValueError: Si el mensaje cifrado no tiene una longitud válida.

		"""

		try:
			# Convertir la clave en una clave de 32 caracteres
			clave_hash = hashlib.sha256(clave.encode()).digest()

			# Decodificar el texto cifrado de Base64
			texto_cifrado_bytes = base64.b64decode(texto_cifrado)

			# Verificar la longitud del vector de inicialización
			if len(iv) != 16:
				raise ValueError("El vector de inicialización debe ser una cadena de bytes de 16 caracteres.")

			# Crear un objeto de descifrado AES
			cipher = AES.new(clave_hash, AES.MODE_CBC, iv)

			# Descifrar el texto cifrado y eliminar el relleno
			texto_descifrado_bytes = cipher.decrypt(texto_cifrado_bytes)
			texto_descifrado = unpad(texto_descifrado_bytes, AES.block_size).decode()

			# Retornar el texto descifrado
			return texto_descifrado

		except TypeError as error:
			mb.showwarning("Error", f"El texto a desifrar no es una cadena de caracteres, intente nuevamente.\nSi el error continua muestre el siguiente mensaje a un administrador: {error}")

		except ValueError as error:
			mb.showwarning("Error", f"Ha ocurrido un error de valor, intente nuevamente.\nSi el error continua muestre el siguiente mensaje a un administrador: {error}")

		except Exception as e:
			mb.showwarning("Error", f"Ha ocurrido un error inesperado al decodificar, intente nuevamente.\nSi el error continua muestre el siguiente mensaje a un administrador: {e}")

	def generar_QR(self, QR_info: str, path: str = "reducida.png") -> None:
		"""Genera un código QR a partir de la información dada y lo guarda en un archivo de imagen.

		Args:
			QR_info (str): La información para generar el código QR.
			path (str, optional): La ruta y el nombre del archivo de imagen donde se guardará el código QR. 
								Por defecto es "reducida.png".
		"""
		# Generar el código QR
		img = qrcode.make(QR_info)

		# Redimensionar el código QR a un tamaño específico
		img = img.get_image().resize((350, 350))

		# Guardar la imagen redimensionada en un archivo
		img.save(path)


