
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import qrcode
from tkinter import messagebox as mb


def cifrar_AES(texto_plano: str, clave: str = "PASE") -> tuple:
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
    except Exception as e:print(e)


def descifrar_AES(texto_cifrado: str, iv: bytes, clave: str = "PASE") -> str:
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
        mb.showerror("Error", "La información a decifrar es incorrecta.")
        return None


folio = "9999999999"
#folio = "0123456789"

texto_cifrado, iv = cifrar_AES(texto_plano = folio)

print(f"Folio a cifrar: {folio}\n")
print(f"Vector: {iv}\n")

imgqr = tuple((texto_cifrado, iv))
print(f"QR info: {imgqr}\n")

img = qrcode.make(imgqr)
# Obtener imagen con el tamaño indicado
####reducida = img.resize((100, 75))
# Mostrar imagen reducida.show()
# Guardar imagen obtenida con el formato PNG
img.save("reducida.png")


folio_cifrado = imgqr[0]
vector = imgqr[1]

print(f"Folio cifrado: {folio_cifrado}")
print(f"Vector: {vector}")


texto_descifrado = descifrar_AES(texto_cifrado = folio_cifrado, iv = vector)

print(f"Folio desifrado: {texto_descifrado}")

if folio == texto_descifrado: print("DESIFRADO CORRECTO")

