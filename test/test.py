
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import qrcode



def cifrar_AES(texto_plano, clave):
    # Convertir la clave en una clave de 32 caracteres
    clave_hash = hashlib.sha256(clave.encode()).digest()

    # Crear un objeto de cifrado AES
    cipher = AES.new(clave_hash, AES.MODE_CBC)

    # Cifrar el texto plano y convertirlo en una cadena de texto hexadecimal
    texto_cifrado_hex = cipher.encrypt(pad(texto_plano.encode(), AES.block_size)).hex()

    # Codificar la cadena hexadecimal en Base64
    texto_cifrado = base64.b64encode(bytes.fromhex(texto_cifrado_hex)).decode()

    # Retornar el texto cifrado y el vector de inicialización
    return texto_cifrado, cipher.iv

def descifrar_AES(texto_cifrado, clave, iv):
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
    texto_descifrado = texto_descifrado_bytes.decode().rstrip('\0')

    # Retornar el texto descifrado
    return texto_descifrado


179163


FOLIO = "123456789"

print(f"Folio a cifrar: {FOLIO}")


clave = "PASE"

texto_cifrado, iv = cifrar_AES(FOLIO, clave)

# Imprimir el texto cifrado y el vector de inicialización
print(f"Folio cifrado: {texto_cifrado}")
print(f"Tamaño: {len(texto_cifrado)}")

# Descifrar el texto cifrado
texto_descifrado = descifrar_AES(texto_cifrado, clave, iv)
# Imprimir el texto descifrado
print(f"Folio descifrado: {texto_descifrado}")



imgqr=(texto_cifrado) 

img = qrcode.make(imgqr)
# Obtener imagen con el tamaño indicado
#reducida = img.resize((100, 75))
# Mostrar imagen reducida.show()
# Guardar imagen obtenida con el formato JPEG
img.save("test/reducida.png")










