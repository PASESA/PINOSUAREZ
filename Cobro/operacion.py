import pymysql
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
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
        Cifra el texto plano utilizando el algoritmo AES en modo CBC.

        Args:
            texto_plano (str): Texto plano a cifrar.
            clave (str): Clave secreta para cifrar el texto. Por defecto es "PASE".

        Returns:
            tuple: Una tupla con dos elementos:
                texto_cifrado (str): Texto cifrado en Base64.
                iv (bytes): Vector de inicialización utilizado en el cifrado.
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

            # Retornar el texto cifrado y el vector de inicialización
            return texto_cifrado, cipher.iv

        except AttributeError: mb.showerror("Error", "La información a codificar debe ser un string")
        except Exception as e:
            print(e)
            mb.showerror("Error", f"Error al encriptar, intente nuevamente, si el error persiste contacte a un adminsitrador y muestre el siguiente mensaje de error:\n{e}.")


    def descifrar_AES(self, texto_cifrado: str, iv: bytes, clave: str = "PASE") -> str:
        """
        Descifra el texto cifrado utilizando el algoritmo AES en modo CBC.

        Args:
            texto_cifrado (str): Texto cifrado en Base64 a descifrar.
            iv (bytes): Vector de inicialización utilizado en el cifrado.
            clave (str): Clave secreta utilizada en el cifrado. Por defecto es "PASE".

        Returns:
            texto_descifrado (str): Texto descifrado.
        """
        try:
            # Convertir la clave en una clave de 32 caracteres
            clave_hash = hashlib.sha256(clave.encode()).digest()

            # Decodificar el texto cifrado de Base64
            texto_cifrado_bytes = base64.b64decode(texto_cifrado)

            # Convertir el vector de inicialización a una cadena de texto en formato hexadecimal
            iv_hex = iv.hex()

            # Convertir la cadena de texto hexadecimal en bytes
            iv_bytes = bytes.fromhex(iv_hex)

            # Crear un objeto de descifrado AES
            cipher = AES.new(clave_hash, AES.MODE_CBC, iv_bytes)

            # Descifrar el texto cifrado y eliminar el relleno
            texto_descifrado_bytes = cipher.decrypt(texto_cifrado_bytes)
            texto_descifrado = unpad(texto_descifrado_bytes, AES.block_size).decode()

            # Retornar el texto descifrado
            return texto_descifrado

        except Exception as e:
            print(e)
            mb.showerror("Error", f"Error al desencriptar, intente nuevamente, si el error persiste contacte a un adminsitrador y muestre el siguiente mensaje de error:\n{e}.")
            return None


