import tkinter as tk
import math

class RelojAnalogico:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Reloj Analógico")
        self.interface()
    
    def interface(self):
        # Frame contenedor principal
        self.frame_contenedor = tk.LabelFrame(self.root, padx=5, pady=5)
        self.frame_contenedor.grid(row=0, column=0)


        # Frame para los colores y rango
        self.frame_colores = tk.LabelFrame(self.frame_contenedor, text="Colores y Rangos", padx=5, pady=5)
        self.frame_colores.grid(row=0, column=0, padx=5, pady=5)

        # Etiqueta informativa para el color verde
        label_hora_inicial = tk.Label(self.frame_colores, text="Primera hora", font=("Arial", 15))
        label_hora_inicial.grid(row=0, column=0, columnspan=2, pady=5)

        # Color verde para cuando el tiempo sea menor o igual a una hora
        color_green_dark = "#006400"
        color_box = tk.Label(self.frame_colores, bg=color_green_dark, width=12, height=2)
        color_box.grid(row=1, column=1, sticky="w")

        range_label = tk.Label(self.frame_colores, text="0 - 60  Minutos", font=("Arial", 15), padx=5)
        range_label.grid(row=1, column=0, sticky="w")

        # Etiqueta informativa para el color verde
        label_hora_despues = tk.Label(self.frame_colores, text="Despues de la primera hora", font=("Arial", 15))
        label_hora_despues.grid(row=2, column=0, columnspan=2, pady=5)
        # Colores para cada cuarto de hora
        colors = ["#FFD700", "#FFA500", "#FF4500", "#FF0000"]

        # Etiquetas informativas y recuadros de colores
        for i in range(4):
            range_label = tk.Label(self.frame_colores, text=f"{(i * 15) + 1} - {(i + 1) * 15}  Minutos", font=("Arial", 15), padx=5)
            range_label.grid(row=i+3, column=0, sticky="w")

            color_box = tk.Label(self.frame_colores, bg=colors[i], width=12, height=2)
            color_box.grid(row=i+3, column=1, sticky="w")


        # Frame para el reloj
        self.frame_total_reloj = tk.LabelFrame(self.frame_contenedor, text="Reloj", padx=5, pady=5)
        self.frame_total_reloj.grid(row=0, column=1, sticky=tk.NW)

        self.frame_horas = tk.Frame(self.frame_total_reloj, padx=5, pady=5)
        self.frame_horas.grid(row=0, column=0)

        self.label_horas = tk.Label(self.frame_horas, text="0 Hrs", font=("Arial", 20))
        self.label_horas.grid(row=0, column=0)

        self.frame_reloj = tk.Frame(self.frame_total_reloj, padx=5, pady=5)
        self.frame_reloj.grid(row=1, column=0)

        self.canvas_background = tk.Canvas(self.frame_reloj, width=300, height=300, bg="white")
        self.canvas_background.pack()

        # Dibujar el círculo del reloj en el canvas de fondo
        self.canvas_background.create_oval(45, 45, 255, 255, width=10)

        # Dibujar las divisiones de los minutos en el canvas de fondo
        for i in range(60):
            angle = math.radians(90 - i * 6)  # Corrección para el 0 en la parte superior
            x1 = 150 + 100 * math.cos(angle)
            y1 = 150 - 100 * math.sin(angle)
            x2 = 150 + 120 * math.cos(angle)
            y2 = 150 - 120 * math.sin(angle)

            # Dibujar las líneas de división
            self.canvas_background.create_line(x1, y1, x2, y2, width=2)

            # Dibujar los números de los minutos en las líneas de división
            if i % 5 == 0:
                number = i // 5 * 5
                x_text = 150 + 130 * math.cos(angle)  # Ajustar la posición de los números
                y_text = 150 - 130 * math.sin(angle)  # Ajustar la posición de los números
                self.canvas_background.create_text(x_text, y_text, text=str(number), font=("Arial", 13))

        # Dibujar las divisiones en 4 partes iguales en el canvas de fondo
        for i in range(4):
            angle_division = math.radians(i * 90)  # Ángulo para cada división (0, 90, 180, 270 grados)
            x1_division = 150 + 100 * math.cos(angle_division)
            y1_division = 150 - 100 * math.sin(angle_division)
            x2_division = 150 + 120 * math.cos(angle_division)  # Ajustar la longitud de las divisiones
            y2_division = 150 - 120 * math.sin(angle_division)  # Ajustar la longitud de las divisiones
            self.canvas_background.create_line(x1_division, y1_division, x2_division, y2_division, width=5, fill="gray")

        self.x_minute = 150
        self.y_minute = 150
        self.minute_hand = self.canvas_background.create_line(150, 150, self.x_minute, self.y_minute, width=5, fill="black", tags="minute")

        # Frame para los datos
        self.frame_datos = tk.LabelFrame(self.frame_contenedor, text="Datos", padx=5, pady=5)
        self.frame_datos.grid(row=0, column=2, padx=5, pady=5)


        # Etiqueta para el tiempo total
        self.label_tiempo_entrada = tk.Label(self.frame_datos, text="Entrada: 00:00 Hrs", font=("Arial", 15))
        self.label_tiempo_entrada.grid(row=0, column=0, padx=5, pady=5)

        # Etiqueta para el importe total
        self.label_tiempo_salida = tk.Label(self.frame_datos, text="Salida: 00:00 Hrs", font=("Arial", 15))
        self.label_tiempo_salida.grid(row=1, column=0, padx=5, pady=5)



        # Etiqueta para el tiempo total
        self.label_tiempo = tk.Label(self.frame_datos, text="Tiempo Total", font=("Arial", 15))
        self.label_tiempo.grid(row=2, column=0, padx=5, pady=5)

        # Etiqueta para el tiempo total
        self.label_tiempo_total = tk.Label(self.frame_datos, text="00:00", font=("Arial", 25))
        self.label_tiempo_total.grid(row=3, column=0, padx=5, pady=5)

        # Etiqueta para el tiempo total
        self.label_tarifa = tk.Label(self.frame_datos, text="Tarifa: Normal", font=("Arial", 15))
        self.label_tarifa.grid(row=4, column=0, padx=5, pady=5)


        # Etiqueta para el importe total
        self.label_importe = tk.Label(self.frame_datos, text="Importe Total", font=("Arial", 15))
        self.label_importe.grid(row=5, column=0, padx=5, pady=5)

        # Etiqueta para el importe total
        self.label_importe_total = tk.Label(self.frame_datos, text="$0.00", font=("Arial", 25))
        self.label_importe_total.grid(row=6, column=0, padx=5, pady=5)

    def update_background(self, minutes):
        # Colores para cada cuarto de hora
        colors = ["#FFD700", "#FFA500", "#FF4500", "#FF0000"]

        # Dibujar el área anterior a la manecilla de minutos con el color correspondiente
        self.canvas_background.delete("previous_area")
        start_angle = 90 - minutes * 6
        extent = minutes * 6
        color_green_dark = "#006400"
        color = color_green_dark

        if minutes <= 60:color = color_green_dark
        else:
            _, minutes = divmod(minutes, 60)
            if minutes < 16 and minutes >= 1: color = colors[0]
            elif minutes < 31 and minutes >= 16: color = colors[1]
            elif minutes < 46 and minutes >= 31: color = colors[2]
            elif minutes <= 59 and minutes >= 46: color = colors[3]

        self.canvas_background.create_arc(50, 50, 250, 250, start=start_angle, extent=extent, fill=color, outline=color, tags="previous_area")
        self.update_clock(minutes)

    def update_clock(self, minutes):
        # Calcular el ángulo de la manecilla de minutos en grados
        angle_minute = 90 - minutes * 6

        # Si la cantidad de horas es mayor o igual a 1, limitar el ángulo a 0 grados
        if minutes // 60 >= 1:
            angle_minute = 90

        # Calcular la posición de la manecilla en coordenadas polares
        x = 150 + 100 * math.cos(math.radians(angle_minute))
        y = 150 - 100 * math.sin(math.radians(angle_minute))

        # Dibujar la manecilla de minutos en el canvas_background
        self.canvas_background.coords(self.minute_hand, 150, 150, x, y)

    def set_time(self, entrada = "00:00", salida = "00:00", hour=0, minute=0, importe=0):
        self.update_background(0)

        self.hour = hour

        if hour >= 1: hour = 1

        total_minutes = hour * 60 + minute
        current_minutes = 0
        if hour == 0 and minute <= 59: total_minutes = 59

        time_per_frame = 0.9 / (total_minutes)

        while current_minutes <= total_minutes:
            self.update_background(current_minutes)
            self.root.update()  # Actualizar la ventana
            current_minutes += 1
            self.root.after(int(time_per_frame * 1000))  # Convertir a milisegundos

            if current_minutes % 60 == 0:
                self.label_horas.config(text = f"{hora} Hrs", font=("Arial", 20))

        # Actualizar el Label de tiempo con el tiempo final
        time_str = "{:02d} Hrs {:02d} Min".format(self.hour, minute)

        self.label_tiempo_entrada.config(text = f"Entrada: {entrada[:-3]} Hrs")
        self.label_tiempo_salida.config(text = f"Salida: {salida[:-3]} Hrs")

        self.label_tiempo_total.config(text = f"{time_str}")
        self.label_importe_total.config(text = f"${importe}.00")

    def update_data(self, tarifa, importe):
        self.label_importe_total.config(text = f"${importe}")
        self.label_tarifa.config(text = f"Tarifa: {tarifa}.00")
    
    def clear_data(self):
        self.label_tiempo_entrada.config(text = f"Entrada: 00:00 Hrs")
        self.label_tiempo_salida.config(text = f"Salida: 00:00 Hrs")

        self.label_tiempo_total.config(text = f"00 Hrs 00 Min")
        self.label_importe_total.config(text = f"$0.00")


    def open_window(self):
        self.root.mainloop()

# Ejemplo de uso:
reloj = RelojAnalogico()
entrada = "01:00:00"
salida = "02:30:00"
importe = 100
hora = 2
minuto = 1


reloj.set_time(entrada=entrada, salida=salida, hour= hora,minute= minuto, importe=importe)
reloj.open_window()

# reloj.update_data("Otra xd", "500")
# reloj.clear_data()

