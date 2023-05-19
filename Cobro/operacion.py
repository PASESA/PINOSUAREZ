import pymysql
import random
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


	def cifrar_folio(self, folio):
		"""
		Cifra un número de folio utilizando una tabla de sustitución numérica.

		Args:
			folio (int): Número de folio a cifrar.

		Returns:
			str: Número de folio cifrado.
		"""

		# Convierte el número de folio en una cadena de texto.
		folio = str(folio)

		# Genera un número aleatorio de 5 dígitos y lo convierte en una cadena de texto.
		num_random = random.randint(10000, 99999)
		numero_seguridad = str(num_random)

		# Concatena el número de seguridad al número de folio.
		folio = folio + numero_seguridad

		# Imprime el número de folio cifrado (sólo para propósitos de depuración).
		print(folio)

		# Tabla de sustitución numérica.
		tabla = {'0': '5', '1': '3', '2': '9', '3': '1', '4': '7', '5': '0', '6': '8', '7': '4', '8': '6', '9': '2'}

		# Convierte el número de folio cifrado a una lista de dígitos.
		digitos = list(folio)

		# Sustituye cada dígito por el número correspondiente en la tabla de sustitución.
		cifrado = [tabla[digito] for digito in digitos]

		# Convierte la lista cifrada de vuelta a una cadena de texto.
		cifrado = ''.join(cifrado)

		# Devuelve el número de folio cifrado.
		return cifrado


	def descifrar_folio(self, folio_cifrado):
		"""
		Descifra un número de folio cifrado utilizando una tabla de sustitución numérica.

		Args:
			folio_cifrado (str): Número de folio cifrado.

		Returns:
			str: Número de folio descifrado.
		"""
		try:
			# Verifica si el número de folio es válido.
			if len(folio_cifrado) <= 5:
				raise ValueError("El folio no es válido, escanee nuevamente, si el error persiste contacte con un administrador.")

			# Verifica si el número de folio tiene caracteres inválidos.
			caracteres_invalidos = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+', '{', '}', '[', ']', '|', '\\', ':', ';', '<', '>', ',', '.', '/', '?']
			if any(caracter in folio_cifrado for caracter in caracteres_invalidos):
				raise TypeError("El folio no tiene un formato válido")

			# Tabla de sustitución numérica.
			tabla = {'0': '5', '1': '3', '2': '9', '3': '1', '4': '7', '5': '0', '6': '8', '7': '4', '8': '6', '9': '2'}

			# Convierte el número de folio cifrado a una lista de dígitos.
			digitos_cifrados = list(folio_cifrado)

			# Crea una tabla de sustitución inversa invirtiendo la tabla original.
			tabla_inversa = {valor: clave for clave, valor in tabla.items()}

			# Sustituye cada dígito cifrado por el número correspondiente en la tabla de sustitución inversa.
			descifrado = [tabla_inversa[digito] for digito in digitos_cifrados]

			# Convierte la lista descifrada de vuelta a una cadena de texto.
			descifrado = ''.join(descifrado)

			# Elimina los últimos 4 dígitos, que corresponden al número aleatorio generado en la función cifrar_folio.
			descifrado = descifrado[:-5]

			# Retorna el folio descifrado.
			return descifrado

		# Maneja el error si el formato del número de folio es incorrecto.
		except TypeError as error:
			mb.showerror("Error", f"El folio tiene un formato incorrecto, si el error persiste contacte a un administrador y muestre el siguiente error:\n{error}")
			return None

		# Maneja cualquier otro error que pueda ocurrir al descifrar el número de folio.
		except Exception as error:
			mb.showerror("Error", f"Ha ocurrido un error al descifrar el folio, intente nuevamente, si el error persiste contacte a un administrador y muestre el siguiente error:\n{error}")
			return None


	def generar_QR(self, QR_info: str, path: str = "reducida.png") -> None:
		"""Genera un código QR a partir de la información dada y lo guarda en un archivo de imagen.

		Args:
			QR_info (str): La información para generar el código QR.
			path (str, optional): La ruta y el nombre del archivo de imagen donde se guardará el código QR, por defecto es "reducida.png".
		"""
		# Generar el código QR
		img = qrcode.make(QR_info)

		# Redimensionar el código QR a un tamaño específico
		img = img.get_image().resize((320, 320))

		# Guardar la imagen redimensionada en un archivo
		img.save(path)

