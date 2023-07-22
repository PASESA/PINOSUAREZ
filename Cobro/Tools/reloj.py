import tkinter as tk
import math

class RelojAnalogico:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Reloj Analógico")
        self.root.geometry("600x500")

        # LabelFrame para los colores y rango
        self.frame_colores = tk.LabelFrame(self.root, text="Colores y Rangos", padx=10, pady=10)
        self.frame_colores.grid(row=0, column=0, rowspan=2, padx=10)

        # Colores para cada cuarto de hora
        colors = ["#FFD700", "#FFA500", "#FF4500", "#FF0000"]

        # Etiquetas informativas y recuadros de colores
        self.color_boxes = []
        self.range_labels = []
        for i in range(4):
            color_box = tk.Label(self.frame_colores, bg=colors[i], width=10, height=1)
            color_box.grid(row=i, column=1, sticky="w")
            self.color_boxes.append(color_box)

            range_label = tk.Label(self.frame_colores, text="{} - {}".format((i * 15) + 1, (i + 1) * 15), font=("Arial", 12), padx=10)
            range_label.grid(row=i, column=2, sticky="w")
            self.range_labels.append(range_label)

        self.frame_reloj = tk.LabelFrame(self.root, text="Reloj", padx=10, pady=10)
        self.frame_reloj.grid(row=0, column=1)

        self.canvas_background = tk.Canvas(self.frame_reloj, width=300, height=300, bg="white")
        self.canvas_background.pack()

        # Dibujar el círculo del reloj en el canvas de fondo
        self.canvas_background.create_oval(45, 45, 255, 255, width=8)

        # Dibujar las divisiones de los minutos en el canvas de fondo
        for i in range(60):
            angle = math.radians(90 - i * 6)  # Corrección para el 0 en la parte superior
            x1 = 150 + 100 * math.cos(angle)
            y1 = 150 - 100 * math.sin(angle)
            x2 = 150 + 120 * math.cos(angle)
            y2 = 150 - 120 * math.sin(angle)

            # Dibujar las líneas de división
            self.canvas_background.create_line(x1, y1, x2, y2)

            # Dibujar los números de los minutos en las líneas de división
            if i % 5 == 0:
                number = i // 5 * 5
                x_text = 150 + 130 * math.cos(angle)  # Ajustar la posición de los números
                y_text = 150 - 130 * math.sin(angle)  # Ajustar la posición de los números
                self.canvas_background.create_text(x_text, y_text, text=str(number), font=("Arial", 12))

        self.x_minute = 150
        self.y_minute = 150
        self.minute_hand = self.canvas_background.create_line(150, 150, self.x_minute, self.y_minute, width=6, fill="black", tags="minute")

        self.frame_tiempo = tk.LabelFrame(self.root, text="Tiempo", padx=10, pady=10)
        self.frame_tiempo.grid(row=1, column=1)

        self.label_tiempo = tk.Label(self.frame_tiempo, text="00:00", font=("Arial", 20))
        self.label_tiempo.pack()

        self.triangles = []  # Lista para mantener los triángulos creados y sus colores

    def create_triangle(self, minutes, color):
        # Calcular el ángulo del triángulo
        angle = math.radians(90 - minutes * 6)

        # Coordenadas de los vértices del triángulo
        x1 = 150
        y1 = 150
        x2 = 150 + 119 * math.cos(angle)  # Disminuir el tamaño del radio en 1 unidad
        y2 = 150 - 119 * math.sin(angle)  # Disminuir el tamaño del radio en 1 unidad
        x3 = 150 + 119 * math.cos(angle - math.radians(6))  # Disminuir el tamaño del radio en 1 unidad
        y3 = 150 - 119 * math.sin(angle - math.radians(6))  # Disminuir el tamaño del radio en 1 unidad

        # Dibujar el triángulo
        triangle = self.canvas_background.create_polygon(x1, y1, x2, y2, x3, y3, fill=color, outline=color, tags="triangles")
        self.triangles.append(triangle)

    def update_background(self, minutes):
        # Obtener el índice del color según el rango de minutos
        quarter = (minutes // 15) % 4
        quarter = int(quarter)

        # Colores para cada cuarto de hora
        colors = ["#FFD700", "#FFA500", "#FF4500", "#FF0000"]

        # Dibujar el área anterior a la manecilla de minutos con el color correspondiente
        self.canvas_background.delete("previous_area")
        start_angle = 90 - minutes * 6
        extent = minutes * 6

        if minutes <= 61:
            color_green_dark = "#006400"  # Color verde oscuro para los primeros 61 minutos
            self.canvas_background.create_arc(50, 50, 250, 250, start=start_angle, extent=extent, fill=color_green_dark, outline=color_green_dark, tags="previous_area")
        else:
            self.canvas_background.create_arc(50, 50, 250, 250, start=start_angle, extent=extent, fill=colors[quarter], outline=colors[quarter], tags="previous_area")

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

    def update_time(self, hour=0, minute=0):
        self.update_background(0)
        self.update_clock(0)

        total_minutes = hour * 60 + minute
        current_minutes = 0

        total_triangles = total_minutes + 1
        time_per_triangle = 3 / total_triangles  # Tiempo total de animación: 3 segundos

        while current_minutes <= total_minutes:
            self.update_background(current_minutes)
            self.update_clock(current_minutes)
            self.root.update()  # Actualizar la ventana
            current_minutes += 1
            self.root.after(int(time_per_triangle * 1000))  # Convertir a milisegundos

        # Actualizar el Label de tiempo con el tiempo final
        time_str = "{:02d}:{:02d}".format(hour, minute)
        self.label_tiempo.config(text=time_str)

    def open_window(self):
        self.root.mainloop()

# Ejemplo de uso:
reloj = RelojAnalogico()
reloj.update_time(20, 31)  # Actualizar el tiempo en el reloj a 06:31:00
reloj.open_window()
