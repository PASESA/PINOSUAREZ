from datetime import datetime, date, time, timedelta
formato = "%H:%M:%S"
from escpos.printer import *
import qrcode
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import scrolledtext as st
from tkinter import font
import pymysql
import re
import operacion
import time
import serial
import RPi.GPIO as io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
data = [("NOMBRE", "NOTA 1", "NOTA 2", "NOTA 3", "PROM.", "ESTADO")]

###
import itertools
from random import randint
from statistics import mean
from reportlab.lib.pagesizes import A4
#from reportlab.lib.pagesizes import A4
#from reportlab.pdfgen import canvas
out1 = 17
io.setmode(io.BCM)              # modo in/out pin del micro
io.setwarnings(False)           # no señala advertencias de pin ya usados
io.setup(out1,io.OUT)           # configura en el micro las salidas
class FormularioOperacion:
    def __init__(self):
        #creamos un objeto que esta en el archivo operacion dentro la clase Operacion
        self.operacion1=operacion.Operacion()
        self.ventana1=tk.Tk()
        self.ventana1.title(" CONSULTA")
        self.cuaderno1 = ttk.Notebook(self.ventana1)
        self.cuaderno1.config(cursor="")         # Tipo de cursor
        self.ExpedirRfid()
        self.consulta_por_folio()
        #self.calcular_cambio()
        self.listado_completo()
        self.cuaderno1.grid(column=0, row=0, padx=5, pady=5)
        self.ventana1.mainloop()
###########################Inicia Pagina1##########################
    def ExpedirRfid(self):
        self.pagina1 = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina1, text="MODULO PARA CONSULTA")
        #enmarca los controles LabelFrame
        self.labelframe1=ttk.LabelFrame(self.pagina1, text="Dar Entrada")
        self.labelframe1.grid(column=1, row=0, padx=0, pady=0)

                
        self.Adentroframe=ttk.LabelFrame(self.pagina1, text="Consulta")
        self.Adentroframe.grid(column=2, row=0, padx=0, pady=0)
        self.Autdentro=tk.Button(self.Adentroframe, text="Boletos sin Cobro", command=self.Autdentro, width=15, height=1, anchor="center")
        self.Autdentro.grid(column=2, row=0, padx=4, pady=4)        
        self.scrolledtext=st.ScrolledText(self.Adentroframe, width=20, height=3)
        self.scrolledtext.grid(column=1,row=0, padx=4, pady=4)
        self.FeshaIni=tk.StringVar()
        self.entryFeshaIni=tk.Entry(self.Adentroframe, width=10, textvariable=self.FeshaIni)
        self.entryFeshaIni.grid(column=1, row=1, padx=4, pady=4)
        self.lblPlaca=ttk.Label(self.Adentroframe, text="Fecha Inicial")
        self.lblPlaca.grid(column=2, row=1, padx=0, pady=0)
        
        self.ConsPeriodo=tk.Button(self.Adentroframe, text="Consulta Periodo", command=self.Intervalo, width=15, height=1, anchor="center")
        self.ConsPeriodo.grid(column=2, row=3, padx=4, pady=4)        
        self.scrolledFeshaFin=st.ScrolledText(self.Adentroframe, width=20, height=3)
        self.scrolledFeshaFin.grid(column=1,row=3, padx=4, pady=4)
        self.FeshaFin=tk.StringVar()
        self.entryFeshaFin=tk.Entry(self.Adentroframe, width=10, textvariable=self.FeshaFin)
        self.entryFeshaFin.grid(column=1, row=2, padx=4, pady=4)
        self.lblFeshaFin=ttk.Label(self.Adentroframe, text="Fecha Final")
        self.lblFeshaFin.grid(column=2, row=2, padx=0, pady=0)
        self.ConsPeriodo=tk.Button(self.Adentroframe, text="IMPRIMIR PDF", command=self.Autdentro, width=15, height=1, anchor="center")
        self.ConsPeriodo.grid(column=2, row=4, padx=4, pady=4)
        self.ConsPeriodo=tk.Button(self.Adentroframe, text="IMPRIMIR MS EXCEL", command=self.Autdentro, width=15, height=1, anchor="center")
        self.ConsPeriodo.grid(column=1, row=4, padx=4, pady=4) 
                    
      
       
        self.MaxId=tk.StringVar()
        self.entryMaxId=ttk.Entry(self.labelframe1, width=10, textvariable=self.MaxId, state="readonly")
        self.entryMaxId.grid(column=1, row=0, padx=4, pady=4)
        self.lbltitulo=ttk.Label(self.labelframe1, text="FOLIO")
        self.lbltitulo.grid(column=0, row=0, padx=0, pady=0)
        #####tomar placas del auto
        self.Placa=tk.StringVar()
        self.entryPlaca=tk.Entry(self.labelframe1, width=10, textvariable=self.Placa)
        self.entryPlaca.grid(column=1, row=1, padx=4, pady=4)
        self.lblPlaca=ttk.Label(self.labelframe1, text="COLOCAR PLACAS")
        self.lblPlaca.grid(column=0, row=1, padx=0, pady=0)

        self.labelhr=ttk.Label(self.labelframe1
        , text="HORA ENTRADA")
        self.labelhr.grid(column=0, row=2, padx=0, pady=0)
        self.boton1=tk.Button(self.labelframe1, text="Generar Entrada", command=self.agregarRegistroRFID, width=13, height=3, anchor="center", background="Cadetblue")
        self.boton1.grid(column=1, row=4, padx=4, pady=4)

        self.boton2=tk.Button(self.pagina1, text="Salir del programa", command=quit, width=15, height=1, anchor="center", background="red")
        self.boton2.grid(column=0, row=0, padx=4, pady=4)
        #llamar a operacion y meter en Entrada la hora en el momento actual y un numero de corte 0
    def Intervalo(self):
        
        Intervalo=self.operacion1.Intervalo()
        print('cuantos registros son:',len(Intervalo))
        self.scrolledFeshaFin.delete("1.0", tk.END)
        for fila in Intervalo:
            self.scrolledFeshaFin.insert(tk.END, "Folio num: "+str(fila[0])+"\nEntro: "+str(fila[1])+"\nSalio: "+str(fila[2])+"\n\n")
        #self.hacerelpdf()
        for (id, Entrada, Salida, TiempoTotal,Importe, CorteInc, vobo, Placas, TarifaPreferente, TipoPromocion) in Intervalo:
                print("{}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(id, Entrada, Salida, TiempoTotal, Importe, CorteInc, vobo, Placas, TarifaPreferente, TipoPromocion ))  
        #for fila in Intervalo:
        for r in range(len(Intervalo)):
            #for r in range(len(Intervalo)):
            for fila in Intervalo:
            #for c in range(0, 5):
                print(10, '{}, {}'.format(r, fila))
                
        
        #self.hacerelpdf()
        
               
    def hacerelpdf(self):
        Intervalo=self.operacion1.Intervalo()# aqui hace la consulta a la base de datos
        
        print('cuantos registros son:',len(Intervalo))
        for x in range(len(Intervalo)):          
        #for fila in Intervalo:
            page_width = 612
            page_height = 792
            self.canvas = canvas.Canvas("Reporte.pdf", pagesize=(page_width, page_height)) 
            self.canvas.setLineWidth(.3)
            self.canvas.setFont('Helvetica', 10)
            valoini=(Intervalo)
            #print('ver que onda',valoini[0][0])
            valoini=str(Intervalo[0])
            buscar= ' datetime.datetime'
            reemplazar_por=''
            valoini= valoini.replace(buscar, reemplazar_por) 
            buscar1= '('
            cambiarpor=''
            valoini= valoini.replace(buscar1, cambiarpor) 
                     
            l4c0=(Intervalo[4][0])
            l4c1=(Intervalo[4][1])
            l4c1= l4c1.strftime("%d/%m/%y %H:%M:%S")
            l4c2=(Intervalo[4][2])
            l4c2= l4c2.strftime("%d/%m/%y %H:%M:%S")
            l4c3=(Intervalo[4][3])
            l4c4=(Intervalo[4][4])
            l4c5=(Intervalo[4][5])
            l4c6=(Intervalo[4][6]) 
            l4c7=(Intervalo[4][7])
            l4c8=(Intervalo[4][8])
            l4c9=(Intervalo[4][9])     
            
            l5c0=(Intervalo[5][0])
            l5c1=(Intervalo[5][1])
            l5c1= l5c1.strftime("%d/%m/%y %H:%M:%S")
            l5c2=(Intervalo[5][2])
            l5c2= l5c2.strftime("%d/%m/%y %H:%M:%S")
            l5c3=(Intervalo[5][3])
            l5c4=(Intervalo[5][4])
            l5c5=(Intervalo[5][5])
            l5c6=(Intervalo[5][6]) 
            l5c7=(Intervalo[5][7])
            l5c8=(Intervalo[5][8])
            l5c9=(Intervalo[5][9])
                                            
            l6c0=(Intervalo[6][0])
            l6c1=(Intervalo[6][1])
            l6c1= l6c1.strftime("%d/%m/%y %H:%M:%S")
            l6c2=(Intervalo[6][2])
            l6c2= l6c2.strftime("%d/%m/%y %H:%M:%S")
            l6c3=(Intervalo[6][3])
            l6c4=(Intervalo[6][4])
            l6c5=(Intervalo[6][5])
            l6c6=(Intervalo[6][6]) 
            l6c7=(Intervalo[6][7])
            l6c8=(Intervalo[6][8])
            l6c9=(Intervalo[6][9])

            valodos=str(Intervalo[0])
            buscar= ' datetime.datetime'
            reemplazar_por=''
            valodos= valodos.replace(buscar, reemplazar_por)             
            
            valotres=str(Intervalo[2])
            buscar= ' datetime.datetime'
            reemplazar_por=''
            valotres= valotres.replace(buscar, reemplazar_por) 

            self.canvas.drawImage('LOGO.jpg', 15, 715, 70, 70)
            self.canvas.line(15,712,580,712)             
            self.canvas.drawString(15,703,'l   id    l   Entrada   l   Salida   l  TiempoTotal  l  Importe  l CorteInc l vobo    l Placas l TarifaPreferente l TipoPromocionl ')
            self.canvas.line(15,702,580,702)              
            self.canvas.drawString(15,685,valoini)               
            self.canvas.drawString(15,675,valodos)               
            self.canvas.drawString(15,665,valotres) 
            self.canvas.drawString (15,655, str(l4c0))           
            self.canvas.drawString (50,655, l4c1) 
            self.canvas.drawString (145,655, l4c2) 
            self.canvas.drawString (235,655, l4c3) 
            self.canvas.drawString (280,655, str(l4c4)) 
            self.canvas.drawString (320,655, str(l4c5))
            self.canvas.drawString (350,655, str(l4c6))
            self.canvas.drawString (380,655, str(l4c7))
            self.canvas.drawString (445,655, str(l4c8))
            self.canvas.drawString (500,655, str(l4c9))    

            self.canvas.drawString (15,645, str(l5c0))           
            self.canvas.drawString (50,645, l5c1) 
            self.canvas.drawString (145,645, l5c2) 
            self.canvas.drawString (235,645, l5c3) 
            self.canvas.drawString (280,645, str(l5c4)) 
            self.canvas.drawString (320,645, str(l5c5))
            self.canvas.drawString (350,645, str(l5c6))
            self.canvas.drawString (380,645, str(l5c7))
            self.canvas.drawString (445,645, str(l5c8))
            self.canvas.drawString (500,645, str(l5c9))    

            self.canvas.drawString (15,635, str(l6c0))           
            self.canvas.drawString (50,635, l6c1) 
            self.canvas.drawString (145,635, l6c2) 
            self.canvas.drawString (235,635, l6c3) 
            self.canvas.drawString (280,635, str(l6c4)) 
            self.canvas.drawString (320,635, str(l6c5))
            self.canvas.drawString (350,635, str(l6c6))
            self.canvas.drawString (380,635, str(l6c7))
            self.canvas.drawString (445,635, str(l6c8))
            self.canvas.drawString (500,635, str(l6c9))    
            
            self.canvas.drawString (15,625, str(Intervalo[7][0]))           
            self.canvas.drawString (50,625, Intervalo[7][1].strftime("%d/%m/%y %H:%M:%S"))
            #self.canvas.drawString (145,625, str(Intervalo[7][2])#.strftime("%d/%m/%y %H:%M:%S")) 
            #self.canvas.drawString (235,625, str(Intervalo[7][3])) 
            #self.canvas.drawString (280,625, Intervalo[7][0]) 
            #self.canvas.drawString (320,625, Intervalo[7][0])
            #self.canvas.drawString (350,625, Intervalo[7][0])
            #self.canvas.drawString (380,625, Intervalo[7][0])
            #self.canvas.drawString (445,625, Intervalo[7][0])
            #self.canvas.drawString (500,625, Intervalo[7][0])                

            self.canvas.drawString(80,148,"CDMX 55-25-01-08")
            self.canvas.drawString(80,140,"Suc Tenayuca M laurent 961")
            self.canvas.drawString(80,132,'Col Sta Cruz Atoyac 03310')
            self.canvas.drawString(80,124,'Delegacion Benito Juarez ')
            self.canvas.setFont('Helvetica', 12)
            self.canvas.drawString(30,25,"Entro:")
            self.canvas.setFont('Helvetica', 8)
            self.canvas.drawString(30,15,"Folio:")
            self.canvas.drawString(30,5,'Placas:')
            self.canvas.line(30,3,200,3)
            self.canvas.save() 
            #print ("\ncelda1=%s, \ncelda2=%s, \ncelda3=%s" % (celda1, fila[1], fila[2]))  

    def Autdentro(self):
        respuesta=self.operacion1.Autos_dentro()
        self.scrolledtext.delete("1.0", tk.END)
        for fila in respuesta:
            self.scrolledtext.insert(tk.END, "Entrada num: "+str(fila[0])+"\nEntro: "+str(fila[1])+"\n\n")
    def agregarRegistroRFID(self):
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$impresion    $$$$$$$$$$$$$$$$$$$
        MaxFolio=str(self.operacion1.MaxfolioEntrada())
        MaxFolio = MaxFolio.strip("[(,)]")
        n1 = MaxFolio
        n2 = "1"
        masuno = int(n1)+int(n2)
        masuno = str(masuno)
        self.MaxId.set(masuno)
        fechaEntro = datetime.today()
        horaentrada = str(fechaEntro)
        horaentrada=horaentrada[:18]
        self.labelhr.configure(text=(horaentrada, "Entró"))
        corteNum = 0
        placa=str(self.Placa.get(), )
        datos=(fechaEntro, corteNum, placa)
        # hacer la foto de codigo qr
        #img = qrcode.make("2 de septiembre")
        fSTR=str(fechaEntro)
        imgqr=(fSTR + masuno)
        #img = qrcode.make(fechaEntro)
        img = qrcode.make(imgqr)
        # Obtener imagen con el tamaño indicado
        reducida = img.resize((100, 75))
        # Mostrar imagen reducida.show()
        # Guardar imagen obtenida con el formato JPEG
        reducida.save("reducida.png")
        f = open("reducida.png", "wb")
        img.save(f)
        f.close()
        #aqui lo imprimimos
        #p = Usb(0x04b8, 0x0202, 0)
        p = Usb(0x04b8, 0x0202, 0)#esta es la impresora con sus valores que se obtienen con lsusb
        p.set("center")
        p.text("BOLETO DE ENTRADA\n")
        folioZZ=('FOLIO 000' + masuno)
        p.text(folioZZ+'\n')
        p.text('Entro: '+horaentrada+'\n')
        p.text('Placas '+placa+'\n')
        p.set(align="left")
        p.image("LOGO1.jpg")
        p.cut()
        p.image("LOGO1.jpg")
        p.text("--------------------------------------\n")
        p.set(align="center")
        p.text("BOLETO DE ENTRADA\n")
        folioZZ=('FOLIO 000' + masuno)
        p.text('Entro: '+horaentrada+'\n')
        p.text('Placas '+placa+'\n')
        p.text(folioZZ+'\n')
        p.image("AutoA.png")
        p.set(align = "center")
        p.image("reducida.png")
        p.image("LOGO8.jpg")
        p.text("            Le Atiende:               \n")
        p.text("--------------------------------------\n")
        p.cut()
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$impresion fin$$$$$$$$$$$$$$$$
        self.operacion1.altaRegistroRFID(datos)
        self.Placa.set('')
#########################fin de pagina1 inicio pagina2#########################
    def consulta_por_folio(self):
        self.pagina2 = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina2, text=" Módulo de Cobro")
        #en el frame
        self.labelframe2=ttk.LabelFrame(self.pagina2, text="Autos")
        self.labelframe2.grid(column=0, row=0, padx=5, pady=10)
        self.label1=ttk.Label(self.labelframe2, text="Lector QR")
        self.label1.grid(column=0, row=0, padx=4, pady=4)
        self.label3=ttk.Label(self.labelframe2, text="Entro:")
        self.label3.grid(column=0, row=1, padx=4, pady=4)
        self.label4=ttk.Label(self.labelframe2, text="Salio:")
        self.label4.grid(column=0, row=2, padx=4, pady=4)
        #en otro frame
        self.labelframe3=ttk.LabelFrame(self.pagina2, text="Datos del COBRO")
        self.labelframe3.grid(column=1, row=0, padx=5, pady=10)
        self.lbl1=ttk.Label(self.labelframe3, text="Hr Salida")
        self.lbl1.grid(column=0, row=1, padx=4, pady=4)
        self.lbl2=ttk.Label(self.labelframe3, text="TiempoTotal")
        self.lbl2.grid(column=0, row=2, padx=4, pady=4)
        self.lbl3=ttk.Label(self.labelframe3, text="Importe")
        self.lbl3.grid(column=0, row=3, padx=4, pady=4)

        self.labelPerdido=ttk.LabelFrame(self.pagina2, text="Perdido")
        self.labelPerdido.grid(column=2,row=1,padx=5, pady=10)
        self.lblFOLIO=ttk.Label(self.labelPerdido, text=" FOLIO PERDIDO")
        self.lblFOLIO.grid(column=0, row=1, padx=4, pady=4)
        self.PonerFOLIO=tk.StringVar()
        self.entryPonerFOLIO=tk.Entry(self.labelPerdido, width=15, textvariable=self.PonerFOLIO)
        self.entryPonerFOLIO.grid(column=1, row=1)
        self.boton2=tk.Button(self.labelPerdido, text="B./SIN cobro", command=self.BoletoDentro, width=10, height=2, anchor="center")
        self.boton2.grid(column=0, row=0)
        self.boton3=tk.Button(self.labelPerdido, text="Boleto Perdido", command=self.BoletoPerdido, width=10, height=2, anchor="center")
        self.boton3.grid(column=0, row=2)
        self.scrolledtxt=st.ScrolledText(self.labelPerdido, width=28, height=7)
        self.scrolledtxt.grid(column=1,row=0, padx=10, pady=10)
        self.labelpromo=ttk.LabelFrame(self.pagina2, text="Promociones")
        self.labelpromo.grid(column=2, row=0, padx=5, pady=10)
        self.promolbl=ttk.Label(self.labelpromo, text="Leer el  QR de Promocion")
        self.promolbl.grid(column=0, row=0, padx=4, pady=4)
        self.promolbl1=ttk.Label(self.labelpromo, text="Codigo QR")
        self.promolbl1.grid(column=0, row=1, padx=4, pady=4)
        self.promolbl2=ttk.Label(self.labelpromo, text="Tipo Prom")
        self.promolbl2.grid(column=0, row=2, padx=4, pady=4)
        self.labelcuantopagas=ttk.LabelFrame(self.pagina2, text='cual es el pago')
        self.labelcuantopagas.grid(column=0,row=1, padx=5, pady=10)
        self.cuantopagas=ttk.Label(self.labelcuantopagas, text="la cantidad entregada")
        self.cuantopagas.grid(column=0, row=0, padx=4, pady=4)
        self.importees=ttk.Label(self.labelcuantopagas, text="el importe es")
        self.importees.grid(column=0, row=1, padx=4, pady=4)
        self.cambio=ttk.Label(self.labelcuantopagas, text="el cambio es")
        self.cambio.grid(column=0, row=2, padx=4, pady=4)
        self.cuantopagasen=tk.StringVar()
        self.entrycuantopagasen=tk.Entry(self.labelcuantopagas, width=15, textvariable=self.cuantopagasen)
        #self.entrycuantopagasen.bind('<Return>',self.calcular_cambio)
        self.entrycuantopagasen.grid(column=1, row=0)
        self.elimportees=tk.StringVar()
        self.entryelimportees=tk.Entry(self.labelcuantopagas, width=15, textvariable=self.elimportees, state="readonly")
        self.entryelimportees.grid(column=1, row=1)
        self.elcambioes=tk.StringVar()
        self.entryelcambioes=tk.Entry(self.labelcuantopagas, width=15, textvariable=self.elcambioes, state="readonly")
        self.entryelcambioes.grid(column=1, row=2)
        self.label11=ttk.Label(self.labelframe3, text="DIAS")
        self.label11.grid(column=1, row=4, padx=1, pady=1)
        self.label12=ttk.Label(self.labelframe3, text="HORAS")
        self.label12.grid(column=1, row=5, padx=1, pady=1)
        self.label7=ttk.Label(self.labelframe3, text="MINUTOS")
        self.label7.grid(column=1, row=6, padx=1, pady=1)
        self.label8=ttk.Label(self.labelframe3, text="SEGUNDOS")
        self.label8.grid(column=1, row=7, padx=1, pady=1)
        self.label9=ttk.Label(self.labelframe3, text="TOTAL COBRO")
        self.label9.grid(column=1, row=8, padx=1, pady=1)
        self.label15=ttk.Label(self.pagina2, text="Viabilidad de COBRO")
        self.label15.grid(column=1, row=2, padx=0, pady=0)
        #se crea objeto para ver pedir el folio la etiqueta con texto
        self.folio=tk.StringVar()
        self.entryfolio=tk.Entry(self.labelframe2, textvariable=self.folio)
        self.entryfolio.bind('<Return>',self.consultar)#con esto se lee automatico y se va a consultar
        self.entryfolio.grid(column=1, row=0, padx=4, pady=4)
        #se crea objeto para mostrar el dato de la  Entrada solo lectura
        self.descripcion=tk.StringVar()
        self.entrydescripcion=ttk.Entry(self.labelframe2, textvariable=self.descripcion, state="readonly")
        self.entrydescripcion.grid(column=1, row=1, padx=4, pady=4)
        #se crea objeto para mostrar el dato la Salida solo lectura
        self.precio=tk.StringVar()
        self.entryprecio=ttk.Entry(self.labelframe2, textvariable=self.precio, state="readonly")
        self.entryprecio.grid(column=1, row=2, padx=4, pady=4)
        #se crea objeto para MOSTRAR LA HORA DEL CALCULO
        self.copia=tk.StringVar()
        self.entrycopia=tk.Entry(self.labelframe3, width=20, textvariable=self.copia, state = "readonly")
        self.entrycopia.grid(column=1, row=1)
        #SE CREA UN OBJETO caja de texto IGUAL A LOS DEMAS Y MUESTRA EL TOTAL DEL TIEMPO
        self.ffeecha=tk.StringVar()
        self.entryffeecha=tk.Entry(self.labelframe3, width=20, textvariable=self.ffeecha, state= "readonly")
        self.entryffeecha.grid(column=1, row=2)
        #SE CREA UN OBJETO caja de texto IGUAL A LOS DEMAS para mostrar el importe y llevarlo a guardar en BD
        self.importe=tk.StringVar()
        self.entryimporte=tk.Entry(self.labelframe3, width=20, textvariable=self.importe, state= "readonly")
        self.entryimporte.grid(column=1, row=3)
        #creamos un objeto para obtener la lectura de la PROMOCION
        self.promo=tk.StringVar()
        self.entrypromo=tk.Entry(self.labelpromo, width=20, textvariable=self.promo)
        self.entrypromo.grid(column=1, row=1)
        #este es donde pongo el tipo de PROMOCION
        self.PrTi=tk.StringVar()
        self.entryPrTi=tk.Entry(self.labelpromo, width=20, textvariable=self.PrTi, state= "readonly")
        self.entryPrTi.grid(column=1, row=2)
        #botones
        #self.boton1=tk.Button(self.labelframe2, text="Consultar", command=self.consultar, width=20, height=5, anchor="center")
        #self.boton1.grid(column=1, row=4)
        self.boton2=tk.Button(self.labelpromo, text="PROMOCION", command=self.CalculaPromocion, width=20, height=5, anchor="center")
        self.boton2.grid(column=1, row=4)
        #self.boton3=tk.Button(self.pagina2, text="COBRAR ", command=self.GuardarCobro, width=20, height=5, anchor="center", background="Cadetblue")
        #self.boton3.grid(column=1, row=1)
        #self.boton4=tk.Button(self.labelframe3, text="IMPRIMIR", command=self.Comprobante, width=10, height=2, anchor="center", background="Cadetblue")
        #self.boton4.grid(column=0, row=4)
        self.bcambio=tk.Button(self.labelcuantopagas, text="cambio", command=self.calcular_cambio, width=10, height=2, anchor="center", background="Cadetblue")
        self.bcambio.grid(column=0, row=4)
    def BoletoDentro(self):
        respuesta=self.operacion1.Autos_dentro()
        self.scrolledtxt.delete("1.0", tk.END)
        for fila in respuesta:
            self.scrolledtxt.insert(tk.END, "Folio num: "+str(fila[0])+"\nEntro: "+str(fila[1])+"\nPlacas: "+str(fila[2])+"\n\n")
    def BoletoPerdido(self):
       datos=str(self.PonerFOLIO.get(), )
       datos=int(datos)
       datos=str(datos)
       self.folio.set(datos)
       datos=(self.folio.get(), )
       respuesta=self.operacion1.consulta(datos)
       if len(respuesta)>0:
           self.descripcion.set(respuesta[0][0])
           self.precio.set(respuesta[0][1])
           self.CalculaPermanencia()#nos vamos a la funcion de calcular permanencia
           fecha = datetime.today()
           fecha1= fecha.strftime("%Y-%m-%d %H:%M:%S")
           fechaActual= datetime.strptime(fecha1, '%Y-%m-%d %H:%M:%S')
           date_time_str=str(self.descripcion.get())
           date_time_obj= datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
           date_time_mod = datetime.strftime(date_time_obj, '%Y/%m/%d/%H/%M/%S')
           date_time_mod2 = datetime.strptime(date_time_mod, '%Y/%m/%d/%H/%M/%S')
           ffeecha = fechaActual - date_time_mod2
            #self.label11.configure(text=(ffeecha.days, "dias"))
           segundos_vividos = ffeecha.seconds
           horas_dentro, segundos_vividos = divmod(segundos_vividos, 3600)
        #    self.label12.configure(text=(horas_dentro, "horas"))
           minutos_dentro, segundos_vividos = divmod(segundos_vividos, 60)
           if horas_dentro <= 24:
                importe = 200
           if horas_dentro > 24 or ffeecha.days >= 1:
                importe = 200+((ffeecha.days)*720 + (horas_dentro * 30))
           self.importe.set(importe)
           self.label9.configure(text =(importe, "cobro"))
           self.PrTi.set("Per")
           self.Comprobante()
           #p = Usb(0x04b8, 0x0202, 0)
           p = Usb(0x04b8, 0x0202, 0)#esta es la impresora con sus valores que se obtienen con lsusb
           p.text('Boleto Perdido\n')
           FoliodelPerdido = str(self.PonerFOLIO.get(),)
           p.text('Folio boleto cancelado: '+FoliodelPerdido+'\n')
           fecha = datetime.today()
           fechaNota = datetime.today()
           fechaNota= fechaNota.strftime("%b-%d-%A-%Y %H:%M:%S")
           horaNota = str(fechaNota)
           p.set(align="left")
           p.set('Big line\n', font='b')
           p.text('Fecha: '+horaNota+'\n')
           EntradaCompro = str(self.descripcion.get(),)
           p.text('El auto entro: '+EntradaCompro+'\n')
           SalioCompro = str(self.copia.get(),)
           p.text('El auto salio: '+SalioCompro+'\n')
           self.GuardarCobro()
           self.PonerFOLIO.set("")
           p.cut()
           self.promo.set("")
           self.PonerFOLIO.set("")

       else:
           self.descripcion.set('')
           self.precio.set('')
           mb.showinfo("Información", "No existe un auto con dicho código")
    def consultar(self,event):
        datos=str(self.folio.get(), )
        if len(datos) > 20:#con esto revisamos si lee el folio o la promocion
            datos=datos[26:]
            datos=int(datos)
            datos=str(datos)
            self.folio.set(datos)
            datos=(self.folio.get(), )
            respuesta=self.operacion1.consulta(datos)
            if len(respuesta)>0:
                self.descripcion.set(respuesta[0][0])
                self.precio.set(respuesta[0][1])
                self.CalculaPermanencia()#nos vamos a la funcion de calcular permanencia
            else:
                self.descripcion.set('')
                self.precio.set('')
                mb.showinfo("Información", "No existe un auto con dicho código")
        else:
            mb.showinfo("Promocion", "leer primero el folio")
            self.folio.set("")
            self.entryfolio.focus()
    def CalculaPermanencia(self):# funcion que  CALCULA LA PERMANENCIA DEL FOLIO SELECCIONADO
        salida = str(self.precio.get(), )#deveria ser salida en lugar de precio pero asi estaba el base

        if len(salida)>5:#None tiene 4 letras si es mayor a 5 es que tiene ya la fecha
            self.label15.configure(text=("Este Boleto ya Tiene cobro"))
            self.elcambioes.set("")
            self.elimportees.set("")
            self.cuantopagasen.set("")
            self.descripcion.set('')
            self.precio.set('')
            self.copia.set("")
            self.importe.set("")
            self.ffeecha.set("")
            self.folio.set("")
            self.label7.configure(text=(""))
            self.label8.configure(text =(""))
            self.label9.configure(text =(""))
#            self.label10.configure(text=(""))
            self.label11.configure(text=(""))
            self.label12.configure(text=(""))
           # self.elimportees.configure(text=(""))
            self.entryfolio.focus()
        else:
            self.PrTi.set("Normal")    
            self.label15.configure(text="Lo puedes COBRAR")
            fecha = datetime.today()
            fecha1= fecha.strftime("%Y-%m-%d %H:%M:%S")
            fechaActual= datetime.strptime(fecha1, '%Y-%m-%d %H:%M:%S')
            self.copia.set(fechaActual)
            date_time_str=str(self.descripcion.get())
            date_time_obj= datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            date_time_mod = datetime.strftime(date_time_obj, '%Y/%m/%d/%H/%M/%S')
            date_time_mod2 = datetime.strptime(date_time_mod, '%Y/%m/%d/%H/%M/%S')
            ffeecha = fechaActual - date_time_mod2
            self.label11.configure(text=(ffeecha.days, "dias"))
            segundos_vividos = ffeecha.seconds
            horas_dentro, segundos_vividos = divmod(segundos_vividos, 3600)
            self.label12.configure(text=(horas_dentro, "horas"))
            minutos_dentro, segundos_vividos = divmod(segundos_vividos, 60)
            self.label7.configure(text=(minutos_dentro, "minutos"))
            #calcular la diferencia de segundos
            seg1 = ffeecha.seconds
            #print ("dif = seg1 = ", seg1)
            seg2 = ffeecha.seconds/60
            #print ("dif/60 = seg2 = ", seg2)
            seg3 = int(seg2)
            #print ("entero y redondear seg3 = ", seg3)
            seg4 = seg2-seg3
            #print ("seg2 - seg 3 = seg4 = ", seg4)
            seg5 = seg4*60
            #print ("seg5 =", seg5)
            seg6 = round(seg5)
            #print  ("segundos dentro ===> ", seg6)
            self.label8.configure(text =(seg6, "segundos"))
            #self.label9.configure(text =(ffeecha, "tiempo dentro"))
            self.ffeecha.set(ffeecha)
            if minutos_dentro < 15 and minutos_dentro  >= 0:
                minutos = 1
            if minutos_dentro < 30 and minutos_dentro  >= 15:
                minutos = 2
            if minutos_dentro < 45 and minutos_dentro  >= 30:
                minutos = 3
            if minutos_dentro <= 59 and minutos_dentro  >= 45:
                minutos = 4
            if ffeecha.days == 0 and horas_dentro == 0:
               importe = 30
               self.importe.set(importe)
               #self.elimportees.set(importe)
               self.label9.configure(text =(importe, "cobro"))
               self.entrypromo.focus()
            else:
                importe = ((ffeecha.days)*720 + (horas_dentro * 30)+(minutos)*7.5)
                self.importe.set(importe)
                self.label9.configure(text =(importe, "Cobrar"))
                #self.calcular_cambio()
                self.entrypromo.focus()
    def calcular_cambio(self):
        elimporte=str(self.importe.get(), )
        self.elimportees.set(elimporte)
        valorescrito=str(self.cuantopagasen.get(),)
        elimporte=float(elimporte)
        valorescrito=int(valorescrito)
        cambio=valorescrito-elimporte
        cambio=str(cambio)
        self.elcambioes.set(cambio)
        self.Comprobante()#manda a llamar el comprobante y lo imprime
        self.GuardarCobro()#manda a llamar guardar cobro para cobrarlo y guardar registro        
        io.output(out1,0)
        time.sleep(1)
        io.output(out1,1)

    def Comprobante(self):
        #p = Usb(0x04b8, 0x0202, 0)
        p = Usb(0x04b8, 0x0202, 0)#esta es la impresora con sus valores que se obtienen con lsusb
        p.text("Comprobante de pago\n")
        p.image("LOGO1.jpg")
        #Compro de comprobante
        ImporteCompro=str(self.importe.get(),)
        #mb.showinfo("ImporteCompro",ImporteCompro)
        p.text("El importe es $"+ImporteCompro+"\n")
        EntradaCompro = str(self.descripcion.get(),)
        p.text('El auto entro: '+EntradaCompro+'\n')
        SalioCompro = str(self.copia.get(),)
        p.text('El auto salio: '+SalioCompro+'\n')
        TiempoCompro = str(self.ffeecha.get(),)
        p.text('El auto permanecio: '+TiempoCompro+'\n')
        folioactual=str(self.folio.get(), )
        p.text('El folio del boleto es: '+folioactual+'\n')
        p.text('Le atendio: ')
        p.cut()
    def GuardarCobro(self):
        salida = str(self.precio.get(), )#deveria ser salida en lugar de precio pero asi estaba el base

        if len(salida)>5:
            self.label15.configure(text=("con salida, INMODIFICABLE"))
            mb.showinfo("Información", "Ya Tiene Salida")
            self.descripcion.set('')
            self.precio.set('')
            self.copia.set("")
            self.importe.set("")
            self.ffeecha.set("")
            self.folio.set("")
            self.label7.configure(text=(""))
            self.label8.configure(text =(""))
            self.label9.configure(text =(""))
            self.label11.configure(text=(""))
            self.label12.configure(text=(""))
            self.label15.configure(text=(""))
            self.entryfolio.focus()
        else:
            #self.Comprobante()
            self.label15.configure(text=(salida, "SI se debe modificar"))
            importe1 =str(self.importe.get(),)
            folio1= str(self.folio.get(),)
            valorhoy = str(self.copia.get(),)
            fechaActual1 = datetime.strptime(valorhoy, '%Y-%m-%d %H:%M:%S' )
            fechaActual= datetime.strftime(fechaActual1,'%Y-%m-%d %H:%M:%S' )
            ffeecha1= str(self.ffeecha.get(),)
            valor=str(self.descripcion.get(),)
            fechaOrigen = datetime.strptime(valor, '%Y-%m-%d %H:%M:%S')
            promoTipo = str(self.PrTi.get(),)
            vobo = "lmf"#este
            datos=(vobo, importe1, ffeecha1, fechaOrigen, fechaActual, promoTipo, folio1)
            self.operacion1.guardacobro(datos)
            self.descripcion.set('')
            self.precio.set('')
            self.copia.set("")
            self.label7.configure(text=(""))
            self.label8.configure(text =(""))
            self.label9.configure(text =(""))
            self.label11.configure(text=(""))
            self.label12.configure(text=(""))
            self.label15.configure(text=(""))
            self.importe.set("")
            self.ffeecha.set("")
            self.folio.set("")
            self.PrTi.set("")
            #self.elcambioes.set("")
            #self.elimportees.set("")
            #self.cuantopagasen.set("")
            self.entryfolio.focus()#se posiciona en leer qr
    def CalculaPromocion(self):
        TipoPromocion = str(self.promo.get(), )#se recibe el codigo
        TipoProIni=TipoPromocion[:8]
        if TipoProIni==("AM ADMIN"):
           NumP=TipoPromocion[10:]
           self.importe.set(0)
           self.label9.configure(text =(0, "cobro"))
           self.PrTi.set("ADMIN")
#           mb.showinfo("ADMIN",NumP)
           self.promo.set("")
###########starbucks
        if TipoProIni==("ST STARB"):
           NumP=TipoPromocion[12:]
           fecha = datetime.today()
           fecha1= fecha.strftime("%Y-%m-%d %H:%M:%S")
           fechaActual= datetime.strptime(fecha1, '%Y-%m-%d %H:%M:%S')
           date_time_str=str(self.descripcion.get())
           date_time_obj= datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
           date_time_mod = datetime.strftime(date_time_obj, '%Y/%m/%d/%H/%M/%S')
           date_time_mod2 = datetime.strptime(date_time_mod, '%Y/%m/%d/%H/%M/%S')
           ffeecha = fechaActual - date_time_mod2            #self.label11.configure(text=(ffeecha.days, "dias"))
           segundos_vividos = ffeecha.seconds
           horas_dentro, segundos_vividos = divmod(segundos_vividos, 3600)
           minutos_dentro, segundos_vividos = divmod(segundos_vividos, 60)
           if minutos_dentro >=0 and minutos_dentro<=15:
                importe = 0
           if minutos_dentro >15 and minutos_dentro < 60:
                importe = 20
           if horas_dentro == 1 and minutos_dentro <=30:
                importe = 20
           if horas_dentro == 1 and minutos_dentro <= 45 and minutos_dentro > 30:
                importe = 27.5
           if horas_dentro == 1 and minutos_dentro < 60 and minutos_dentro > 45:
                importe = 35
           if horas_dentro == 2 and minutos_dentro <=15:
                importe = 42.5
           if horas_dentro == 2 and minutos_dentro >15 and minutos_dentro <= 30:
                importe = 50
           if horas_dentro == 2 and minutos_dentro >30 and minutos_dentro <= 45:
                importe = 57.5
           if horas_dentro == 2 and minutos_dentro >45 and minutos_dentro < 60:
                importe = 65
           if horas_dentro == 3 and minutos_dentro <=15:
                importe = 72.5
           if horas_dentro == 3 and minutos_dentro >15 and minutos_dentro <= 30:
                importe = 80
           if horas_dentro == 3 and minutos_dentro >30 and minutos_dentro <= 45:
                importe = 87.5
           if horas_dentro == 3 and minutos_dentro >45 and minutos_dentro < 60:
                importe = 95
           if horas_dentro >= 4:
                importe = ((ffeecha.days)*720 + (horas_dentro * 30)+(minutos)*1)
           self.importe.set(importe)
           self.label9.configure(text =(importe, "cobro"))
           self.PrTi.set("StB")
           #mb.showinfo("STARBUCKS",NumP)
           self.promo.set("")
########## Promocion Sonora
        if TipoProIni==("SG SONOR"):
           NumP=TipoPromocion[15:]
           fecha = datetime.today()
           fecha1= fecha.strftime("%Y-%m-%d %H:%M:%S")
           fechaActual= datetime.strptime(fecha1, '%Y-%m-%d %H:%M:%S')
           date_time_str=str(self.descripcion.get())
           date_time_obj= datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
           date_time_mod = datetime.strftime(date_time_obj, '%Y/%m/%d/%H/%M/%S')
           date_time_mod2 = datetime.strptime(date_time_mod, '%Y/%m/%d/%H/%M/%S')
           ffeecha = fechaActual - date_time_mod2
           segundos_vividos = ffeecha.seconds
           horas_dentro, segundos_vividos = divmod(segundos_vividos, 3600)
           minutos_dentro, segundos_vividos = divmod(segundos_vividos, 60)
           if minutos_dentro < 60:
               importe = 50
           if horas_dentro >= 1 and horas_dentro <= 3 :
                importe = 50
           if horas_dentro == 3 and minutos_dentro < 1:
                importe = 50
           if horas_dentro == 3 and minutos_dentro >= 1:
                importe = 70
           if horas_dentro >= 4 and horas_dentro < 8:
                importe = 70
           if horas_dentro == 8 and minutos_dentro <=15:
                importe = 77
           if horas_dentro == 8 and minutos_dentro >=16:
                importe = 85
           if horas_dentro == 9 and minutos_dentro <=15:
                importe = 100
           if horas_dentro == 9 and minutos_dentro >=16:
                importe = 115              
           if horas_dentro >= 10:
                importe = ((ffeecha.days)*720 + (horas_dentro * 30)+(minutos_dentro)*1)
           self.importe.set(importe)
           self.label9.configure(text =(importe, "cobro"))
           self.PrTi.set("SNR")
          # mb.showinfo("SONORA",NumP)
           self.promo.set("")
#############promocion at pote
        if TipoProIni==("AT APOTE"):
           NumP=TipoPromocion[10:]
           self.importe.set(70)
           self.label9.configure(text =(70, "cobro"))
           self.PrTi.set("APOTEK")
#           mb.showinfo("ADMIN",NumP)
           self.promo.set("")
############ promocion crepas and wafles
        if TipoProIni==("PR PROVE"):
           NumP=TipoPromocion[18:]
           fecha = datetime.today()
           fecha1= fecha.strftime("%Y-%m-%d %H:%M:%S")
           fechaActual= datetime.strptime(fecha1, '%Y-%m-%d %H:%M:%S')
           date_time_str=str(self.descripcion.get())
           date_time_obj= datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
           date_time_mod = datetime.strftime(date_time_obj, '%Y/%m/%d/%H/%M/%S')
           date_time_mod2 = datetime.strptime(date_time_mod, '%Y/%m/%d/%H/%M/%S')
           ffeecha = fechaActual - date_time_mod2
           segundos_vividos = ffeecha.seconds
           horas_dentro, segundos_vividos = divmod(segundos_vividos, 3600)
           minutos_dentro, segundos_vividos = divmod(segundos_vividos, 60)
           if minutos_dentro >=0 and minutos_dentro<15:
                importe = 0
                minutos = 0
           if minutos_dentro >=16 and minutos_dentro<30:
                importe = 7.5
                minutos = 7.5
           if minutos_dentro >=31 and minutos_dentro<45:
                importe = 15
                minutos = 15
           if minutos_dentro >=46 and minutos_dentro<59:
                importe = 22.5
                minutos = 22.5                            
           if horas_dentro >= 1:
                importe = ((ffeecha.days)*720 + (horas_dentro * 30)+(minutos)*1)
           self.importe.set(importe)
           self.label9.configure(text =(importe, "cobro"))
           self.PrTi.set("PRV")
          # mb.showinfo("CREPES&WAFLES",NumP)
           self.promo.set("")
###################### Fin de Pagina2 Inicio Pagina3 ###############################
    def listado_completo(self):
        self.pagina3 = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina3, text="Módulo de Corte")
        self.labelframe1=ttk.LabelFrame(self.pagina3, text="Autos")
        self.labelframe1.grid(column=0, row=0, padx=1, pady=1)
        self.labelframe2=ttk.LabelFrame(self.pagina3, text="Generar Corte")
        self.labelframe2.grid(column=1, row=0, padx=0, pady=0)
        self.labelframe3=ttk.LabelFrame(self.pagina3, text="Consulta Cortes Anteriores")
        self.labelframe3.grid(column=0, row=1, padx=0, pady=0)

        self.labelframe4=ttk.LabelFrame(self.pagina3, text="Cuadro Comparativo")
        self.labelframe4.grid(column=1, row=1, padx=0, pady=0)
        self.lblSal=ttk.Label(self.labelframe4, text="Salida de Autos")
        self.lblSal.grid(column=3, row=1, padx=1, pady=1)
        self.lblS=ttk.Label(self.labelframe4, text="Entrada de Autos")
        self.lblS.grid(column=3, row=2, padx=1, pady=1)
        self.lblAnterior=ttk.Label(self.labelframe4, text="Autos del Turno anterior")
        self.lblAnterior.grid(column=3, row=3, padx=1, pady=1)
        self.lblEnEstac=ttk.Label(self.labelframe4, text="Autos en Estacionamiento")
        self.lblEnEstac.grid(column=3, row=4, padx=1, pady=1)
        self.lblC=ttk.Label(self.labelframe4, text="Boletos Cobrados:")
        self.lblC.grid(column=0, row=1, padx=1, pady=1)
        self.lblE=ttk.Label(self.labelframe4, text="Boletos Expedidos:")
        self.lblE.grid(column=0, row=2, padx=1, pady=1)
        self.lblA=ttk.Label(self.labelframe4, text="Boletos Turno Anterior:")
        self.lblA.grid(column=0, row=3, padx=1, pady=1)
        self.lblT=ttk.Label(self.labelframe4, text="Boletos Por Cobrar:")
        self.lblT.grid(column=0, row=4, padx=1, pady=1)
        self.BoletosCobrados=tk.StringVar()
        self.entryBoletosCobrados=tk.Entry(self.labelframe4, width=5, textvariable=self.BoletosCobrados, state= "readonly")
        self.entryBoletosCobrados.grid(column=1, row=1)
        self.BEDespuesCorte=tk.StringVar()
        self.entryBEDespuesCorte=tk.Entry(self.labelframe4, width=5, textvariable=self.BEDespuesCorte, state= "readonly")
        self.entryBEDespuesCorte.grid(column=1, row=2)
        self.BAnteriores=tk.StringVar()
        self.entryBAnteriores=tk.Entry(self.labelframe4, width=5, textvariable=self.BAnteriores, state= "readonly")
        self.entryBAnteriores.grid(column=1, row=3)
        self.BDentro=tk.StringVar()
        self.entryBDentro=tk.Entry(self.labelframe4, width=5, textvariable=self.BDentro, state= "readonly")
        self.entryBDentro.grid(column=1, row=4)
        self.SalidaAutos=tk.StringVar()
        self.entrySalidaAutos=tk.Entry(self.labelframe4, width=5, textvariable=self.SalidaAutos, state= "readonly")
        self.entrySalidaAutos.grid(column=2, row=1)
        self.SensorEntrada=tk.StringVar()
        self.entrySensorEntrada=tk.Entry(self.labelframe4, width=5, textvariable=self.SensorEntrada, state= "readonly", borderwidth=5)
        self.entrySensorEntrada.grid(column=2, row=2)
        self.Autos_Anteriores=tk.StringVar()
        self.entryAutos_Anteriores=tk.Entry(self.labelframe4, width=5, textvariable=self.Autos_Anteriores, state= "readonly")
        self.entryAutos_Anteriores.grid(column=2, row=3)
        self.AutosEnEstacionamiento=tk.StringVar()
        self.entryAutosEnEstacionamiento=tk.Entry(self.labelframe4, width=5, textvariable=self.AutosEnEstacionamiento, state= "readonly", borderwidth=5)
        self.entryAutosEnEstacionamiento.grid(column=2, row=4)
        self.boton6=tk.Button(self.labelframe4, text="Consulta Bol-Sensor", command=self.Puertoycontar, width=15, height=3, anchor="center")
        self.boton6.grid(column=1, row=0, padx=1, pady=1)

        self.FrmCancelado=ttk.LabelFrame(self.pagina3, text="Boleto Cancelado")
        self.FrmCancelado.grid(column=0, row=2, padx=0, pady=0)
        self.labelCorte=ttk.Label(self.labelframe2, text="Total del CORTE:")
        self.labelCorte.grid(column=0, row=1, padx=0, pady=0)
        self.label2=ttk.Label(self.labelframe2, text="Fecha Cort Actu:")
        self.label2.grid(column=0, row=2, padx=1, pady=1)
       
        self.label5=ttk.Label(self.labelframe3, text="CORTE a Consultar :")
        self.label5.grid(column=0, row=0, padx=1, pady=1)
        self.label6=ttk.Label(self.labelframe3, text="Fecha y hora del CORTE")
        self.label6.grid(column=0, row=2, padx=1, pady=1)
        self.CortesAnteri=tk.StringVar()
        self.entryCortesAnteri=tk.Entry(self.labelframe3, width=20, textvariable=self.CortesAnteri)
        self.entryCortesAnteri.grid(column=1, row=0)
        self.boton5=tk.Button(self.labelframe3, text="Imprimir salidas  Corte", command=self.desglose_cobrados, width=15, height=3, anchor="center")
        self.boton5.grid(column=1, row=1, padx=4, pady=4)
               
        self.label3=ttk.Label(self.labelframe2, text="Fecha Corte Ante:")
        self.label3.grid(column=0, row=3, padx=1, pady=1)
        self.label4=ttk.Label(self.labelframe2, text="El Numero de CORTE es:")
        self.label4.grid(column=0, row=4, padx=1, pady=1)
        self.lblCancelado=ttk.Label(self.FrmCancelado, text="COLOCAR FOLIO")
        self.lblCancelado.grid(column=0, row=1, padx=4, pady=4)
        self.FolioCancelado=tk.StringVar()
        self.entryFOLIOCancelado=tk.Entry(self.FrmCancelado, width=15, textvariable=self.FolioCancelado)
        self.entryFOLIOCancelado.grid(column=1, row=1)
        self.boton7=tk.Button(self.FrmCancelado, text="B./SIN cobro", command=self.BoletoDentro2, width=15, height=3, anchor="center")
        self.boton7.grid(column=0, row=0, padx=1, pady=1)
        #self.boton8=tk.Button(self.FrmCancelado, text="desglose", command=self.desglose_cobrados, width=15, height=3, anchor="center")
        #self.boton8.grid(column=1, row=3, padx=1, pady=1)

        self.btnCancelado=tk.Button(self.FrmCancelado, text="Cancelar Boleto ", command=self.BoletoCancelado, width=10, height=2, anchor="center")
        self.btnCancelado.grid(column=0, row=2)
        self.scrolledtxt2=st.ScrolledText(self.FrmCancelado, width=28, height=7)
        self.scrolledtxt2.grid(column=1,row=0, padx=1, pady=1)
        self.ImporteCorte=tk.StringVar()
        self.entryImporteCorte=tk.Entry(self.labelframe2, width=20, textvariable=self.ImporteCorte, state= "readonly", borderwidth=5)
        self.entryImporteCorte.grid(column=1, row=1)
        self.FechaCorte=tk.StringVar()
        self.entryFechaCorte=tk.Entry(self.labelframe2, width=20, textvariable=self.FechaCorte, state= "readonly")
        self.entryFechaCorte.grid(column=1, row=2)
        self.FechUCORTE=tk.StringVar()
        self.entryFechUCORTE=tk.Entry(self.labelframe2, width=20, textvariable=self.FechUCORTE, state= "readonly")
        self.entryFechUCORTE.grid(column=1, row=3)
        self.boton1=ttk.Button(self.labelframe1, text="Todas las Entradas", command=self.listar)
        self.boton1.grid(column=0, row=0, padx=4, pady=4)
        self.boton2=ttk.Button(self.labelframe1, text="Entradas sin corte", command=self.listar1)
        self.boton2.grid(column=0, row=2, padx=4, pady=4)
        self.boton3=tk.Button(self.labelframe2, text="Calcular Corte", command=self.Calcular_Corte, width=15, height=1)
        self.boton3.grid(column=2, row=0, padx=4, pady=4)
        self.boton4=tk.Button(self.labelframe2, text="Guardar Corte", command=self.Guardar_Corte, width=15, height=1, anchor="center", background="green")
        self.boton4.grid(column=2, row=4, padx=4, pady=4)
        self.scrolledtext1=st.ScrolledText(self.labelframe1, width=30, height=4)
        self.scrolledtext1.grid(column=0,row=1, padx=1, pady=1)
    def BoletoDentro2(self):
        respuesta=self.operacion1.Autos_dentro()
        self.scrolledtxt2.delete("1.0", tk.END)
        for fila in respuesta:
            self.scrolledtxt2.insert(tk.END, "Folio num: "+str(fila[0])+"\nEntro: "+str(fila[1])+"\nPlacas: "+str(fila[2])+"\n\n")
    def desglose_cobrados(self):    
        Numcorte=str(self.CortesAnteri.get(), )
        Numcorte=int(Numcorte)
        Numcorte=str(Numcorte)
        #mb.showinfo("Numcorte", Numcorte)
        io.output(out1,0)
        time.sleep(1)
        io.output(out1,1)
        respuesta=self.operacion1.desglose_cobrados(Numcorte)
#        respuesta=self.operacion1.desglose_cobrados()
        self.scrolledtxt2.delete("1.0", tk.END)
        #mb.showinfo("respuesta", respuesta)
        #p = Usb(0x04b8, 0x0202, 0)
 
        print(respuesta)
        #separador=")"
        #resp=str(respuesta)
        #resp= resp.split(separador)
        resp=str(respuesta)
        resp1= resp[3:16]
        resp2 =resp[19:32] 
        print(resp1)
        print(resp2)
        print(resp)
        print('bajo esta linea')
        print (resp.count("Normal"))
        print (resp.find("Normal"))
        dato2 = resp.replace("), ", "\n")
        print('vemos que poner auqie',dato2)
        p = Usb(0x04b8, 0x0202, 0)#esta es la impresora con sus valores que se obtienen con lsusb
        p.text("El Numero de corte es "+Numcorte+'\n')
        print("El Numero de corte es "+Numcorte+'\n')
        for fila in respuesta:
            self.scrolledtxt2.insert(tk.END, " de: "+str(fila[0])+" de a:$"+str(fila[1])+"\nHay "+str(fila[2])+"\n")            
            celda1 = str(fila[0]) 
            celda2 = str(fila[1]) 
            celda3 = str(fila[2]) 
            p.text( " de: "+str(fila[0])+" de a:$"+str(fila[1])+"Hay "+str(fila[2])+"\n")
            page_width = 500
            page_height = 600
            self.canvas = canvas.Canvas("2.pdf", pagesize=(page_width, page_height)) 
            self.canvas.setLineWidth(.3)
            self.canvas.setFont('Helvetica', 10)
            self.canvas.drawString(80,400,"El Numero de corte es "+Numcorte+'\n')            
            
            self.canvas.setFont('Helvetica', 8)
            self.canvas.drawString (30,285,"\ncelda1=%s, celda2=%s, \ncelda3=%s " % (fila[0], fila[1], fila[2],)+"\n")
            self.canvas.drawString(30,250," vemos que pone enel pdf auquie "+dato2+'\n')              
            self.canvas.drawString (20,200," vemos que pone aqui celda1=%s, celda2=%s, \ncelda3=%s " % (celda1, celda2, celda3,)+"\n")            
            self.canvas.drawString(80,164," celda 2  "+celda2+'\n')
            self.canvas.drawString(80,156," celda 3  "+celda3+'\n')
            respuesta = str(respuesta)
            #separador = ","
            #respuesta =respuesta.split(separador)
            #self.canvas.drawString(30,350," respuesta sin ese split "+respuesta+'\n')
            self.canvas.drawString(30,325," respuesta  "+resp+'\n')
            self.canvas.drawString(30,315," corte lacadena [3:16] "+resp1+'\n')            
            self.canvas.drawString(30,305," corte la cadena [19:32] "+resp2+'\n')            
            self.canvas.drawString(80,148,"CDMX 55-25-01-08")
            self.canvas.drawString(80,140,"Suc Tenayuca M laurent 961")
            self.canvas.drawString(80,132,'Col Sta Cruz Atoyac 03310')
            self.canvas.drawString(80,124,'Delegacion Benito Juarez ')
            self.canvas.setFont('Helvetica', 12)
            self.canvas.drawString(30,25,"Entro:")
            self.canvas.setFont('Helvetica', 8)
            self.canvas.drawString(30,15,"Folio:")
            self.canvas.drawString(30,5,'Placas:')
            self.canvas.line(30,3,200,3)
            print ("\ncelda1=%s, \ncelda2=%s, \ncelda3=%s" % (celda1, fila[1], fila[2]))
 

 
        else:
            self.canvas.save()    
            p.cut()
    def BoletoCancelado(self):
       datos=str(self.FolioCancelado.get(), )
       datos=int(datos)
       datos=str(datos)
       self.folio.set(datos)
       datos=(self.folio.get(), )
       respuesta=self.operacion1.consulta(datos)
       if len(respuesta)>0:
           self.descripcion.set(respuesta[0][0])
           self.precio.set(respuesta[0][1])
           self.CalculaPermanencia()#nos vamos a la funcion de calcular permanencia
           fecha = datetime.today()
           fecha1= fecha.strftime("%Y-%m-%d %H:%M:%S")
           fechaActual= datetime.strptime(fecha1, '%Y-%m-%d %H:%M:%S')
           date_time_str=str(self.descripcion.get())
           date_time_obj= datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
           date_time_mod = datetime.strftime(date_time_obj, '%Y/%m/%d/%H/%M/%S')
           date_time_mod2 = datetime.strptime(date_time_mod, '%Y/%m/%d/%H/%M/%S')
           ffeecha = fechaActual - date_time_mod2
            #self.label11.configure(text=(ffeecha.days, "dias"))
           segundos_vividos = ffeecha.seconds
           horas_dentro, segundos_vividos = divmod(segundos_vividos, 3600)
        #    self.label12.configure(text=(horas_dentro, "horas"))
           minutos_dentro, segundos_vividos = divmod(segundos_vividos, 60)
           if horas_dentro <= 24:
                importe = 0
           if horas_dentro > 24 or ffeecha.days >= 1:
                importe =0
           self.importe.set(importe)
           self.label9.configure(text =(importe, "cobro"))
           self.PrTi.set("CDO")
           self.promo.set("")
           #p = Usb(0x04b8, 0x0202, 0)
           p = Usb(0x04b8, 0x0202, 0)#esta es la impresora con sus valores que se obtienen con lsusb
           p.text('Boleto Cancelado\n')
           FoliodelCancelado = str(self.FolioCancelado.get(),)
           p.text('Folio boleto cancelado: '+FoliodelCancelado+'\n')
           fecha = datetime.today()
           fechaNota = datetime.today()
           fechaNota= fechaNota.strftime("%b-%d-%A-%Y %H:%M:%S")
           horaNota = str(fechaNota)
           p.set(align="left")
           p.set('Big line\n', font='b')
           p.text('Fecha: '+horaNota+'\n')
           EntradaCompro = str(self.descripcion.get(),)
           p.text('El auto entro: '+EntradaCompro+'\n')
           SalioCompro = str(self.copia.get(),)
           p.text('El auto salio: '+SalioCompro+'\n')
           self.GuardarCobro()
           self.FolioCancelado.set("")
           p.cut()

       else:
           self.descripcion.set('')
           self.precio.set('')
           mb.showinfo("Información", "No existe un auto con dicho código")
    def listar(self):
        respuesta=self.operacion1.recuperar_todos()
        self.scrolledtext1.delete("1.0", tk.END)
        for fila in respuesta:
            self.scrolledtext1.insert(tk.END, "Entrada num: "+str(fila[0])+"\nEntro: "+str(fila[1])+"\nSalio: "+str(fila[2])+"\n\n")
    def listar1(self):
        respuesta=self.operacion1.recuperar_sincobro()
        self.scrolledtext1.delete("1.0", tk.END)
        #respuesta=str(respuesta)
        for fila in respuesta:
            self.scrolledtext1.insert(tk.END, "Entrada num: "+str(fila[0])+"\nEntro: "+str(fila[1])+"\nSalio: "+str(fila[2])+"\nImporte: "+str(fila[3])+"\n\n")
            #p = Usb(0x04b8, 0x0202, 0)
            p = Usb(0x04b8, 0x0202, 0)#esta es la impresora con sus valores que se obtienen con lsusb
            p.text('Entrada Num :')
            p.text(str(fila[0]))
            p.text('\n')
            p.text('Entro :')
            p.text(str(fila[1]))
            p.text('\n')
            p.text('Salio :')
            p.text(str(fila[2]))
            p.text('\n')
            p.text('importe :')
            p.text(str(fila[3]))
            p.text('\n')
        else:
            p.cut()
    def Calcular_Corte(self):
        respuesta=self.operacion1.corte()
        self.ImporteCorte.set(respuesta)
        ##obtengamo la fechaFin del ultimo corte
        ultiCort1=str(self.operacion1.UltimoCorte())
        #mb.showinfo("msj uno",ultiCort1)
        startLoc = 20
        endLoc = 43
        ultiCort1=(ultiCort1)[startLoc: endLoc]
        ultiCort1 = ultiCort1.strip('),')
        if len(ultiCort1) <= 17:
                            # mb.showinfo("msj dos",ultiCort1)
                             ultiCort1= datetime.strptime(ultiCort1, '%Y, %m, %d, %H, %M')
        else:
            ultiCort1= datetime.strptime(ultiCort1, '%Y, %m, %d, %H, %M, %S')        
            #mb.showinfo("msj tres",ultiCort1)
        ultiCort1 = datetime.strftime(ultiCort1, '%Y/%m/%d/%H/%M/%S')
        ultiCort1 = datetime.strptime(ultiCort1, '%Y/%m/%d/%H/%M/%S')
        self.FechUCORTE.set(ultiCort1)# donde el label no esta bloqueada
        ###ahora obtenemos la fecha del corte ha realizar
        fecha = datetime.today()
        fecha1= fecha.strftime("%Y-%m-%d %H:%M:%S")
        fechaActual= datetime.strptime(fecha1, '%Y-%m-%d %H:%M:%S')
        self.FechaCorte.set(fechaActual)#donde el label esta bloqueado
    def Guardar_Corte(self):
        self.Puertoycontar()
        ##la fecha final de este corte que es la actual
        fechaDECorte = str(self.FechaCorte.get(),)
        fechaDECorte = datetime.strptime(fechaDECorte, '%Y-%m-%d %H:%M:%S' )
        ######la fecha del inicial obtiene de labase de datos
        fechaInicio1 = str(self.FechUCORTE.get(),)
        fechaInicio2 = datetime.strptime(fechaInicio1, '%Y-%m-%d %H:%M:%S')
        fechaInicio = fechaInicio2
        ######el importe se obtiene de la suma
        ImpCorte2 =str(self.ImporteCorte.get(),)
        Im38=ImpCorte2.strip('(,)')
        AEE = 0#str(self.AutosEnEstacionamiento.get(),)
        maxnumid=str(self.operacion1.MaxfolioEntrada())
        maxnumid = "".join([x for x in maxnumid if x.isdigit()])#con esto solo obtenemos los numeros
        maxnumid=int(maxnumid)
        maxnumid=str(maxnumid)
        pasa = str(self.BDentro.get(),)
        NumBolQued = pasa.strip('(),')
        datos=(Im38, fechaInicio, fechaDECorte,AEE,maxnumid,NumBolQued)
        self.operacion1.GuarCorte(datos)
        maxnum1=str(self.operacion1.Maxfolio_Cortes())
        maxnum = "".join([x for x in maxnum1 if x.isdigit()])#con esto solo obtenemos los numeros
        maxnum=int(maxnum)
        maxnum=str(maxnum)
        vobo = "cor"#este es para que la instruccion no marque error
        ActEntradas = (maxnum, vobo )
        self.label4.configure(text=("Numero de corte",maxnum))
        #p = Usb(0x04b8, 0x0202, 0)
        p = Usb(0x04b8, 0x0202, 0)#esta es la impresora con sus valores que se obtienen con lsusb
        p.text("CORTE Num "+maxnum+"\n")
        p.text('IMPORTE: $ '+Im38+'\n')
        #p.text('IMPORTE: $ '+ImpCorte2+'\n')
        ultiCort1=str(self.FechUCORTE.get(),)
        ultiCort4= datetime.strptime(ultiCort1, '%Y-%m-%d %H:%M:%S')
        ultiCort5 = datetime.strftime(ultiCort4, '%A %d %m %Y a las %H:%M:%S')
        p.text('Inicio:')
        p.text(ultiCort5)
        p.text('\n')
        valorFEsteCorte = str(self.FechaCorte.get(),)
        fechaDECorte = datetime.strptime(valorFEsteCorte, '%Y-%m-%d %H:%M:%S' )
        fechaDECorte = datetime.strftime(fechaDECorte, '%A %d %m %Y a las %H:%M:%S' )
        p.text('Final :')
        p.text(str(fechaDECorte))
        p.text('\n')
        MaxFolio=str(self.operacion1.MaxfolioEntrada())
        MaxFolio = MaxFolio.strip("[(,)]")
        BEDespuesCorteImpre = str(self.BEDespuesCorte.get(),)
        BEDespuesCorteImpre = BEDespuesCorteImpre.strip("[(,)]")
        IniFolio =int(MaxFolio)-int(BEDespuesCorteImpre)
        IniFolio = str(IniFolio)
        p.text("Folio "+IniFolio+" al inicio del turno\n")
        p.text("Folio "+MaxFolio+" al final del turno\n")                        
        BolCobrImpresion=str(self.BoletosCobrados.get(),)
        p.text("Boletos Cobrados: "+BolCobrImpresion+"\n")
        #SalidasSen =  int(self.SalidaAutos.get(),)
        #SalidasSen =  str(SalidasSen)
        #p.text("Salidas Sensor: "+SalidasSen+"\n")

        p.text('Boletos Expedidos: '+BEDespuesCorteImpre+'\n')
        #EntradasSen = int(self.SensorEntrada.get(),)
        #EntradasSen =  str(EntradasSen)
        #p.text('Entradas Sensor: '+EntradasSen+'\n')
        BAnterioresImpr=str(self.BAnteriores.get(),)#######
        p.text("Boletos Turno Anterior: "+BAnterioresImpr+"\n")
        #AutosAnteriores = int(self.Autos_Anteriores.get(),)
        #AutosAnteriores = str(AutosAnteriores)
        #p.text('Sensor Turno Anterior: '+AutosAnteriores+'\n')
        BDentroImp = str(self.BDentro.get(),)
        p.text('Boletos por Cobrar: '+BDentroImp+'\n')
        AutosEnEstacImpre = str(self.AutosEnEstacionamiento.get(),)
        #p.text('Autos en estacionamiento por sensor: '+AutosEnEstacImpre+'\n')
        p.text('------------------------------')
        p.text('\n')
        #Bandera = o
        self.ImporteCorte.set("")
        #p.cut()
        self.operacion1.ActualizarEntradasConcorte(ActEntradas)
        vobo='ant'
        self.operacion1.NocobradosAnt(vobo)
        ponercorte =int(maxnum)
        #mb.showinfo("primero",ponercorte)
        self.CortesAnteri.set(ponercorte)
        #self.desglose_cobrados()
        Numcorte=str(self.CortesAnteri.get(), )
        Numcorte=int(Numcorte)
        Numcorte=str(Numcorte)
        #mb.showinfo("segundo", Numcorte)
        io.output(out1,0)
        time.sleep(1)
        io.output(out1,1)
        respuesta=self.operacion1.desglose_cobrados(Numcorte)
        self.scrolledtxt2.delete("1.0", tk.END)
        #mb.showinfo("respuesta", respuesta)
        #p = Usb(0x04b8, 0x0202, 0)
        p = Usb(0x04b8, 0x0202, 0)#esta es la impresora con sus valores que se obtienen con lsusb
        p.text("Cantidad e Importes "+'\n')
        p.text("Cantidad - Tarifa - valor C/U - Total "+'\n')
        for fila in respuesta:
            self.scrolledtxt2.insert(tk.END, str(fila[0])+" Boletos con tarifa "+str(fila[1])+"\n"+"valor c/u $"+str(fila[2])+" Total $"+str(fila[3])+"\n\n")
            p.text('   ')
            p.text(str(fila[0]))
            p.text('   -  ')
            p.text(str(fila[1]))
            p.text(' -  $')
            #p.text('valor c/u $')
            p.text(str(fila[2]))
            p.text('  -  $')
            p.text(str(fila[3]))
            p.text('\n')
        else:
            p.text(BolCobrImpresion+' Boletos           Suma total $'+Im38+'\n')    
            p.cut()
        #ser = serial.Serial('/dev/ttyAMA0', 9600)
        #Enviamos el caracter por serial, codificado en Unicode
        #entrada='c'
        #ser.write(str(entrada).encode())
    def Puertoycontar(self):
        #ser = serial.Serial('/dev/ttyAMA0', 9600)
        #Enviamos el caracter por serial, codificado en Unicode
        #entrada='e'
        #ser.write(str(entrada).encode())
        #Leemos lo que hay en el puerto y quitamos lo que no queremos
        #sArduino = str(ser.readline())
        #sArduino = "" .join([x for x in sArduino if x.isdigit()])#esto es para solo poner numeros
        #CuantosEntradas=str(self.operacion1.EntradasSensor())
        #sArduino = 1
        #CuantosEntradas = CuantosEntradas.strip('(),')
        #self.SensorEntrada.set(CuantosEntradas)
        #entrada='a'
        #ser.write(str(entrada).encode())
        #Leemos lo que hay en el puerto y quitamos lo que no queremos
        #sArduino = str(ser.readline())
        #sArduino = "" .join([x for x in sArduino if x.isdigit()])#esto es para solo poner num
        #CuantosSalidas=str(self.operacion1.SalidasSensor())
        #sArduino =1
        #CuantosSalidas = CuantosSalidas.strip('(),')
        #self.SalidaAutos.set(CuantosSalidas)
        #EntradasSen = int(self.SensorEntrada.get(),)
        #SalidasSen =  int(self.SalidaAutos.get(),)
        CuantosBoletosCobro=str(self.operacion1.CuantosBoletosCobro())
        CuantosBoletosCobro = CuantosBoletosCobro.strip('(),')
        self.BoletosCobrados.set(CuantosBoletosCobro)
        #BEDCorte=str(self.operacion1.BEDCorte())
        #BEDCorte = BEDCorte.strip('(),')
        #self.BEDespuesCorte.set(BEDCorte)
        #BAnteriores=str(self.operacion1.BAnteriores())
        #BAnteriores = BAnteriores.strip('(),')
        #self.BAnteriores.set(BAnteriores)
        MaxFolioCorte=str(self.operacion1.Maxfolio_Cortes())
        MaxFolioCorte=MaxFolioCorte.strip('(),')
        QuedadosBol=str(self.operacion1.Quedados_Sensor(MaxFolioCorte))
        QuedadosBol=QuedadosBol.strip('(),')
        self.BAnteriores.set(QuedadosBol)
        maxNumidIni=str(self.operacion1.MaxnumId())
        maxNumidIni = "".join([x for x in maxNumidIni if x.isdigit()])#con esto solo obtenemos los numeros
        maxNumidIni=int(maxNumidIni)
        maxFolioEntradas= str(self.operacion1.MaxfolioEntrada())
        maxFolioEntradas = "".join([x for x in maxFolioEntradas if x.isdigit()])#con esto solo obtenemos los numero
        maxFolioEntradas=int(maxFolioEntradas)
        BEDCorte=maxFolioEntradas-maxNumidIni
        BEDCorte=str(BEDCorte)
        self.BEDespuesCorte.set(BEDCorte)
        CuantosAutosdentro=str(self.operacion1.CuantosAutosdentro())
        MaxFolioCorte=str(self.operacion1.Maxfolio_Cortes())
        MaxFolioCorte=MaxFolioCorte.strip('(),')
        dentroCorte=str(self.operacion1.Quedados_Sensor(MaxFolioCorte))
        CuantosAutosdentro = CuantosAutosdentro.strip('(),')
        dentroCorte = dentroCorte.strip('(),')
        self.BDentro.set(CuantosAutosdentro)
        self.Autos_Anteriores.set(dentroCorte)
        #AutosAnteriores = int(self.Autos_Anteriores.get(),)
        #Cuantos_hay_dentro = ((AutosAnteriores + EntradasSen) - SalidasSen)
        #self.AutosEnEstacionamiento.set(Cuantos_hay_entro)

aplicacion1=FormularioOperacion()
