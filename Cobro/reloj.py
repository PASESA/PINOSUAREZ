import tkinter as tk
from math import radians, cos, sin

class BlinkingLabel:

    def __init__(self):
        self.label = None
        self._original_bg = None
        self._blink_id = None
        self.color_alert = "red"

    def toggle_color(self) -> None:
        """
        Alterna entre el color de fondo original y el color de alerta en el Label.

        Returns:
            None
        """
        if self.label.cget("bg") == self.color_alert:
            self.label.config(bg=self._original_bg)
        else:
            self.label.config(bg=self.color_alert)
        # Configura el siguiente parpadeo
        self._blink_id = self.label.after(self.blink_interval, self.toggle_color)

    def start_blinking(self, label: tk.Label, interval_ms: int):
        """
        Inicia el parpadeo del Label.
        Args:
            label (tk.Label): El widget Label al que se aplicará el parpadeo.
            interval_ms (int): El intervalo de tiempo en milisegundos para el parpadeo.
        """
        self.label = label

        self._original_bg = self.label.cget("bg")
        self._blink_id = None
        self.blink_interval = interval_ms

        self.toggle_color()

    def stop_blinking(self) -> None:
        """
        Detiene el parpadeo del Label y restaura el color de fondo original.

        Returns:
            None
        """
        self.label.config(bg=self._original_bg)
        if self._blink_id is not None:
            # Cancela el próximo parpadeo si está programado
            self.label.after_cancel(self._blink_id)
            self._original_bg = None
            self._blink_id = None
            print("se de tiene parpadeo")

class RelojAnalogico:
    def __init__(self):
        """Inicializa la interfaz del reloj analógico."""
        self.root = tk.Toplevel()
        self.root.title("Reloj Analógico")
        # Colores para cada cuarto de hora
        self.colors = ["#b9d8f9", "#5ba3f1", "#1270d3", "#062546"]
        self.color_first_hour = "#062445"
        self.blink_interval = 500

        self.blinking_label = BlinkingLabel()

        self.interface()
    
    def interface(self) -> None:
        """Configura la interfaz gráfica del reloj analógico."""
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
        range_label = tk.Label(self.frame_colores, text="0 - 60  Minutos", font=("Arial", 15), padx=5)
        range_label.grid(row=1, column=0, sticky="w")

        self.color_box_0 = tk.Label(self.frame_colores, bg=self.color_first_hour, width=12, height=2)
        self.color_box_0.grid(row=1, column=1, sticky="w")

        # Etiqueta informativa para el color verde
        label_hora_despues = tk.Label(self.frame_colores, text="Despues de la primera hora", font=("Arial", 15))
        label_hora_despues.grid(row=2, column=0, columnspan=2, pady=5)

        # Etiquetas informativas y recuadros de colores
        range_label_1 = tk.Label(self.frame_colores, text=f"01 - 15  Minutos", font=("Arial", 15), padx=5)
        range_label_1.grid(row=3, column=0, sticky="w")

        self.color_box_1 = tk.Label(self.frame_colores, bg=self.colors[0], width=12, height=2)
        self.color_box_1.grid(row=3, column=1, sticky="w")

        range_label_2 = tk.Label(self.frame_colores, text=f"16 - 30  Minutos", font=("Arial", 15), padx=5)
        range_label_2.grid(row=4, column=0, sticky="w")

        self.color_box_2 = tk.Label(self.frame_colores, bg=self.colors[1], width=12, height=2)
        self.color_box_2.grid(row=4, column=1, sticky="w")

        range_label_3 = tk.Label(self.frame_colores, text=f"31 - 45  Minutos", font=("Arial", 15), padx=5)
        range_label_3.grid(row=5, column=0, sticky="w")

        self.color_box_3 = tk.Label(self.frame_colores, bg=self.colors[2], width=12, height=2)
        self.color_box_3.grid(row=5, column=1, sticky="w")

        range_label_4 = tk.Label(self.frame_colores, text=f"46 - 60  Minutos", font=("Arial", 15), padx=5)
        range_label_4.grid(row=6, column=0, sticky="w")

        self.color_box_4 = tk.Label(self.frame_colores, bg=self.colors[3], width=12, height=2)
        self.color_box_4.grid(row=6, column=1, sticky="w")


        # Frame para el reloj
        frame_total_reloj = tk.LabelFrame(self.frame_contenedor, text="Reloj", padx=5, pady=5)
        frame_total_reloj.grid(row=0, column=1, sticky=tk.NW)

        frame_horas = tk.Frame(frame_total_reloj, padx=5, pady=5)
        frame_horas.grid(row=0, column=0)

        self.label_horas = tk.Label(frame_horas, text="0 Hrs", font=("Arial", 20))
        self.label_horas.grid(row=0, column=0)

        frame_reloj = tk.Frame(frame_total_reloj, padx=5, pady=5)
        frame_reloj.grid(row=1, column=0)

        self.canvas_background = tk.Canvas(frame_reloj, width=300, height=300, bg="white")
        self.canvas_background.pack()

        # Dibujar el círculo del reloj en el canvas de fondo
        self.canvas_background.create_oval(45, 45, 255, 255, width=10)

        # Dibujar las divisiones de los minutos en el canvas de fondo
        for i in range(60):
            angle = radians(90 - i * 6)  # Corrección para el 0 en la parte superior
            x1 = 150 + 100 * cos(angle)
            y1 = 150 - 100 * sin(angle)
            x2 = 150 + 120 * cos(angle)
            y2 = 150 - 120 * sin(angle)

            # Dibujar las líneas de división
            self.canvas_background.create_line(x1, y1, x2, y2, width=2)

            # Dibujar los números de los minutos en las líneas de división
            if i % 5 == 0:
                number = i // 5 * 5
                x_text = 150 + 130 * cos(angle)  # Ajustar la posición de los números
                y_text = 150 - 130 * sin(angle)  # Ajustar la posición de los números
                self.canvas_background.create_text(x_text, y_text, text=str(number), font=("Arial", 13))

        # Dibujar las divisiones en 4 partes iguales en el canvas de fondo
        for i in range(4):
            angle_division = radians(i * 90)  # Ángulo para cada división (0, 90, 180, 270 grados)
            x1_division = 150 + 100 * cos(angle_division)
            y1_division = 150 - 100 * sin(angle_division)
            x2_division = 150 + 120 * cos(angle_division)  # Ajustar la longitud de las divisiones
            y2_division = 150 - 120 * sin(angle_division)  # Ajustar la longitud de las divisiones
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

        self.update_background(0)

    def update_background(self, minutes: int) -> None:
        """Actualiza el fondo del reloj con el color correspondiente según los minutos transcurridos.

        Args:
            minutes (int): Minutos transcurridos.

        Returns:
            None
        """
        # Dibujar el área anterior a la manecilla de minutos con el color correspondiente
        self.canvas_background.delete("previous_area")
        start_angle = 90 - minutes * 6
        extent = minutes * 6
        color = self.color_first_hour

        if minutes <= 60:
            color = self.color_first_hour
            label_select = self.color_box_0
        else:
            _, minutes = divmod(minutes, 60)
            if minutes < 16 and minutes >= 1:
                color = self.colors[0]
                label_select = self.color_box_1
            elif minutes < 31 and minutes >= 16:
                color = self.colors[1]
                label_select = self.color_box_2
            elif minutes < 46 and minutes >= 31:
                color = self.colors[2]
                label_select = self.color_box_3
            elif minutes <= 59 and minutes >= 46:
                color = self.colors[3]
                label_select = self.color_box_4

        self.canvas_background.create_arc(50, 50, 250, 250, start=start_angle, extent=extent, fill=color, outline=color, tags="previous_area")
        self.update_clock(minutes)

        return label_select

    def update_clock(self, minutes: int) -> None:
        """Actualiza la posición de la manecilla de minutos en el reloj.

        Args:
            minutes (int): Minutos transcurridos.

        Returns:
            None
        """
        # Calcular el ángulo de la manecilla de minutos en grados
        angle_minute = 90 - minutes * 6

        # Si la cantidad de horas es mayor o igual a 1, limitar el ángulo a 0 grados
        if minutes // 60 >= 1:
            angle_minute = 90

        # Calcular la posición de la manecilla en coordenadas polares
        x = 150 + 100 * cos(radians(angle_minute))
        y = 150 - 100 * sin(radians(angle_minute))

        # Dibujar la manecilla de minutos en el canvas_background
        self.canvas_background.coords(self.minute_hand, 150, 150, x, y)

    def set_time(self, entrada: str = "00:00", salida: str = "00:00", hour: int = 0, minute: int = 0, importe: float = 0) -> None:
        """Simula el paso del tiempo y actualiza la interfaz del reloj.

        Args:
            entrada (str): Hora de entrada.
            salida (str): Hora de salida.
            hour (int): Horas transcurridas.
            minute (int): Minutos transcurridos.
            importe (float): Importe total.

        Returns:
            None
        """
        label_select = None
        self.update_background(0)

        self.hour = hour

        if hour >= 1: hour = 1

        total_minutes = hour * 60 + minute
        current_minutes = 0
        if hour == 0 and minute <= 59: total_minutes = 59

        time_per_frame = 0.5 / (total_minutes)

        while current_minutes <= total_minutes:
            label_select = self.update_background(current_minutes)
            self.root.update()  # Actualizar la ventana
            current_minutes += 1
            self.root.after(int(time_per_frame * 1000))  # Convertir a milisegundos

            if current_minutes % 60 == 0:
                self.label_horas.config(text = f"{self.hour} Hrs", font=("Arial", 20))


        self.blinking_label.start_blinking(label_select, self.blink_interval)

        # Actualizar el Label de tiempo con el tiempo final
        time_str = "{:02d} Hrs {:02d} Min".format(self.hour, minute)

        self.label_tiempo_entrada.config(text = f"Entrada: {entrada[:-3]} Hrs")
        self.label_tiempo_salida.config(text = f"Salida: {salida[:-3]} Hrs")

        self.label_tiempo_total.config(text = f"{time_str}")
        self.label_importe_total.config(text = f"${importe}.00")


    def update_data(self, tarifa: str, importe: float) -> None:
        """Actualiza la información de la tarifa y el importe en la interfaz.

        Args:
            tarifa (str): Tarifa actual.
            importe (float): Importe total.

        Returns:
            None
        """
        self.label_importe_total.config(text = f"${importe}")
        self.label_tarifa.config(text = f"Tarifa: {tarifa}")
    
    def clear_data(self) -> None:
        """Limpia los datos en la interfaz.

        Returns:
            None
        """
        self.blinking_label.stop_blinking()
        self.canvas_background.delete("previous_area")
        self.label_tiempo_entrada.config(text = f"Entrada: 00:00 Hrs")
        self.label_tiempo_salida.config(text = f"Salida: 00:00 Hrs")

        self.label_tiempo_total.config(text = f"00 Hrs 00 Min")
        self.label_importe_total.config(text = f"$0.00")
        self.label_tarifa.config(text = f"Tarifa: Normal")
        self.label_horas.config(text = "0 Hrs")
        self.update_background(0)

    def open_window(self):
        self.root.mainloop()



# Ejemplo de uso:
# reloj = RelojAnalogico()

# entrada = "01:00:00"
# salida = "02:30:00"
# importe = "100"
# hora = 1
# minuto = 46

# reloj.set_time(entrada=entrada, salida=salida, hour= hora,minute= minuto, importe=importe)



