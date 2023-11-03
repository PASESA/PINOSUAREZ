from datetime import datetime, date, timedelta
from escpos.printer import Usb, USBNotFoundError
import tkinter as tk
from tkinter import ttk
from tkinter import *
from operacion import Operacion
import traceback

###--###
data_rinter = (0x04b8, 0x0202, 0)

logo_1 = "LOGO1.jpg"
AutoA = "AutoA.png"

qr_imagen = "reducida.png"

nombre_estacionamiento = 'Pino Suarez 27'

font_promo = ('Arial', 9, "bold")
estilo = ('Arial', 12)
font_entrada = ('Arial', 20)
font_entrada_negritas = ('Arial', 20, 'bold')
font_mensaje = ('Arial', 40)
font_reloj = ('Arial', 65)
font_cancel = ('Arial', 15)

button_color = "#062546"#"#39acec""#6264d4"
button_letters_color = "white"

class FormularioOperacion:
    def __init__(self):
        self.folio_auxiliar = None

        self.DB=Operacion()
        self.root=tk.Tk()
        self.root.title(f"{nombre_estacionamiento} Entrada")

        # Obtener el ancho y alto de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Configura la ventana para que ocupe toda la pantalla
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")

        # Colocar el LabelFrame en las coordenadas calculadas
        self.principal = tk.LabelFrame(self.root)
        self.principal.pack(expand=True, padx=5, pady=5, anchor='n')

        self.ExpedirRfid()
        self.check_inputs()

        self.root.mainloop()
        ###########################Inicia Pagina1##########################

    def ExpedirRfid(self):
        seccion_entrada = tk.Frame(self.principal)
        seccion_entrada.grid(column=0, row=0, padx=2, pady=2, sticky=tk.NSEW)

        frame_bienvenida = tk.Frame(seccion_entrada)
        frame_bienvenida.grid(column=0, row=0, padx=2, pady=2)

        frame_mensaje_bienvenida = tk.Frame(frame_bienvenida)
        frame_mensaje_bienvenida.grid(column=0, row=0, padx=2, pady=2)

        # Asegura que la fila y la columna del frame se expandan con el contenedor
        frame_mensaje_bienvenida.grid_rowconfigure(0, weight=1)
        frame_mensaje_bienvenida.grid_columnconfigure(0, weight=1)

        label_entrada = tk.Label(frame_mensaje_bienvenida, text=f"Bienvenido(a) al estacionamiento {nombre_estacionamiento}", font=('Arial', 25), justify='center')
        label_entrada.grid(row=0, column=0)



        frame_datos_entrada = tk.Frame(seccion_entrada)
        frame_datos_entrada.grid(column=0, row=1, padx=2, pady=2)

        frame_info_cliente=tk.Frame(frame_datos_entrada)
        frame_info_cliente.grid(column=0, row=0, padx=2, pady=2)

        frame_info_placa=tk.Frame(frame_info_cliente)
        frame_info_placa.grid(column=0, row=0, padx=2, pady=2)

        label_placa=tk.Label(frame_info_placa, text="Ingrese Placa o lea Tarjetón", font=('Arial', 25))
        label_placa.grid(column=0, row=0, padx=2, pady=2)

        self.Placa=tk.StringVar()
        self.entry_placa=tk.Entry(frame_info_placa, width=20, textvariable=self.Placa, font=('Arial', 35, 'bold'), justify='center')
        self.entry_placa.bind('<Return>', self.Pensionados)
        self.entry_placa.grid(column=0, row=1, padx=2, pady=2)



        frame_boton=tk.Frame(frame_datos_entrada)
        frame_boton.grid(column=2, row=0, padx=2, pady=2)

        frame_folio = tk.Frame(frame_boton)
        frame_folio.grid(column=0, row=0, padx=2, pady=2)

        label_folio=tk.Label(frame_folio, text="Folio:", font=font_entrada)
        label_folio.grid(column=0, row=0, padx=2, pady=2, sticky="nsew")
        self.MaxId=tk.StringVar()
        entryMaxId=ttk.Entry(frame_folio, width=12, textvariable=self.MaxId, state="readonly", font=font_entrada)
        entryMaxId.grid(column=1, row=0, padx=2, pady=2, sticky=tk.NW)

        boton_entrada=tk.Button(frame_boton, text="Generar Entrada", width=15, height=3, anchor="center", background=button_color, fg=button_letters_color, font=font_entrada_negritas, command=self.agregarRegistroRFID)
        boton_entrada.grid(column=0, row=1, padx=2, pady=2)
        

        frame_info = tk.LabelFrame(seccion_entrada)#, background = '#CCC')
        frame_info.grid(column=0, row=2, padx=2, pady=2)

        self.label_informacion = tk.Label(frame_info, text="... ", width=25, font=font_mensaje, justify='center')
        self.label_informacion.grid(column=0, row=0, padx=2, pady=2)



        frame_reloj = tk.Frame(seccion_entrada)
        frame_reloj.grid(column=0, row=3, padx=2, pady=2)

        self.Reloj = tk.Label(frame_reloj, text="Reloj", background="white", font=font_reloj, justify='center')
        self.Reloj.grid(column=0, row=0, padx=2, pady=2)
        self.entry_placa.focus()


    def check_inputs(self):
        fecha_hora =datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        self.Reloj.config(text=fecha_hora)            
        self.root.after(60, self.check_inputs)


    def agregarRegistroRFID(self):
        placa=self.Placa.get()
        if not placa:
            self.label_informacion.config(text=f"Error: Ingrese una placa")
            return

        MaxFolio=self.DB.MaxfolioEntrada()
        MaxFolio = MaxFolio[0][0]
        folio_boleto = MaxFolio + 1
        self.MaxId.set(folio_boleto)

        folio_cifrado = self.DB.cifrar_folio(folio = folio_boleto)
        # print(f"QR entrada: {folio_cifrado}")

        #Generar QR
        self.DB.generar_QR(folio_cifrado)

        fechaEntro = datetime.today()

        horaentrada = str(fechaEntro)
        horaentrada=horaentrada[:19]
        # self.labelhr.configure(text=(horaentrada[:-3], "Entro"))
        corteNum = 0
        datos=(fechaEntro, corteNum, placa)

        printer = Usb(0x04b8, 0x0202, 0)
        printer.set("center")
        printer.text("BOLETO DE ENTRADA\n")

        printer.set(height=2, align='center')
        printer.text(f'FOLIO 000{folio_boleto}\n')
        printer.set("center")        
        printer.text('Entro: '+horaentrada[:-3]+'\n')
        printer.text('Placas '+placa+'\n')
        printer.set(align="left")
        printer.image(logo_1)
        printer.image(qr_imagen)
        printer.image(AutoA)
        printer.text("--------------------------------------\n")
        printer.cut()
        
        printer.set("center")
        printer.text("BOLETO PARABRISAS\n")
        printer.text(f'FOLIO 000{folio_boleto}\n')
        printer.text('Entro: '+horaentrada[:-3]+'\n')
        printer.set("left")
        printer.text('Placas: '+placa+'\n')
        printer.text('Color:_____________________ \n')
        printer.text('Marca:_____________________ \n')
        printer.set(align="left")
        printer.cut()

        printer.set("center")
        printer.text("BOLETO LOCALIZACION\n")
        printer.set(height=2, align='right')
        printer.text(f'FOLIO 000{folio_boleto}\n')
        printer.set("center")
        printer.text('Entro: '+horaentrada[:-3]+'\n')
        printer.set(height=2, align='left')       
        printer.text('Placas:'+placa+'\n')
        printer.set("left")
        printer.text('Color:_____________________ \n')
        printer.text('Marca:_____________________ \n')        
        printer.text("Lugar:______________________ \n")
        printer.text("--------------------------------------\n")
        printer.cut()

        printer.close()

        self.DB.altaRegistroRFID(datos)
        self.Placa.set('')
        self.label_informacion.config(text="Se genera boleto")

    def Pensionados(self, event):
        try:
            position_id = len(f"Pension-{nombre_estacionamiento}-")
            numtarjeta = self.Placa.get()
            ID_pen = int(numtarjeta[position_id:])

            print(ID_pen)
            Existe = self.DB.ValidarPen(ID_pen)

            if len(Existe) == 0:
                self.label_informacion.config(text="No existe Pensionado")
                self.Placa.set("")
                self.entry_placa.focus()
                return

            respuesta = self.DB.ConsultaPensionado_entrar(Existe)

            for fila in respuesta:
                VigAct = fila[0]
                Estatus = fila[1]
                Tolerancia = int(fila[3])
                Placas = fila[4]
                Nom_cliente = fila[5]
                Apell1_cliente = fila[6]
                Apell2_cliente = fila[7]

            if VigAct is None:
                self.label_informacion.config(text="Tarjeton desactivado")
                self.Placa.set("")
                self.entry_placa.focus()
                return

            elif Estatus == 'Adentro':
                self.label_informacion.config(text="El Pensionado ya está dentro")
                self.Placa.set("")
                self.entry_placa.focus()
                return

            # Obtener la fecha y hora actual en formato deseado
            VigAct = VigAct.strftime("%Y-%m-%d %H:%M:%S")
            # Convertir la cadena de caracteres en un objeto datetime
            VigAct = datetime.strptime(VigAct, "%Y-%m-%d %H:%M:%S")

            # Obtener la fecha y hora actual en formato deseado
            hoy = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            # Convertir la cadena de caracteres en un objeto datetime
            hoy = datetime.strptime(hoy, "%Y-%m-%d %H:%M:%S")

            limite = self.get_date_limit(VigAct, Tolerancia)
            print(limite)

            if hoy >= limite:
                self.label_informacion.config(text="Vigencia Vencida")
                self.Placa.set("")
                self.entry_placa.focus()
                return

            Entrada = datetime.today()
            datos = (Existe, ID_pen, Entrada, 'Adentro', 0)
            datos1 = ('Adentro', Existe)
            self.DB.MovsPensionado(datos)
            self.DB.UpdPensionado(datos1)

            self.Placa.set("")
            self.entry_placa.focus()
            self.label_informacion.config(text=f"Entro pensionado ID-{ID_pen}")

            #Generar QR
            QR_pension = numtarjeta
            self.DB.generar_QR(QR_pension)
            print(f"QR pension: {QR_pension}")

            printer = Usb(0x04b8, 0x0202, 0)
            printer.set(align="center")

            printer.image(logo_1)
            printer.text("BOLETO DE ENTRADA\nPENSION\n")
            printer.set(align = "left")

            printer.text(f'ID: {numtarjeta}\n')
            printer.text(f'Nombre: {Nom_cliente} {Apell1_cliente} {Apell2_cliente}\n')
            printer.text(f'Hora de entrada: {hoy}\n')
            printer.text(f'Placas: {Placas}\n')
            printer.text(f'Vigencia: {VigAct}\n\n')

            printer.set(align = "center")
            printer.image(qr_imagen)

            printer.cut()
            printer.close()


        except ValueError as e:
            print(e)
            traceback.print_exc()
            self.label_informacion.config(text="No se puede leer QR")
            self.Placa.set("")
            self.entry_placa.focus()
            return

        except Exception as e:
            print(e)
            traceback.print_exc()
            self.label_informacion.config(text="Ha ocurrido un error")
            self.Placa.set("")
            self.entry_placa.focus()
            return




    def get_date_limit(self, date_start:datetime, Tolerance:int) -> datetime:
        """
        Calcula la fecha límite a partir de una fecha de inicio y una cantidad de días de Tolerancia.

        :param date_start (datetime): Fecha de inicio.
        :param Tolerance (int): Cantidad de días laborables a agregar.
        :return (datetime): Fecha límite después de agregar la cantidad de días laborables.
        """
        date_limit = date_start

        while Tolerance > 0:
            date_limit  += timedelta(days=1)
            # Verifica si el día no es fin de semana (lunes a viernes)
            if date_limit.weekday() < 5:
                Tolerance -= 1
        
        return date_limit



aplicacion1=FormularioOperacion()

