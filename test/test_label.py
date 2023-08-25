import tkinter as tk

class BlinkingLabel:
    def __init__(self, label, interval_ms):
        self.label = label
        self.label.config(width=20, height=2)
        self.label.pack(pady=50)

        self._original_bg = self.label.cget("bg")
        self._blink_id = None
        self.blink_interval = interval_ms

    def toggle_color(self):
        if self.label.cget("bg") == "white":
            self.label.config(bg=self._original_bg)
        else:
            self.label.config(bg="white")
        self._blink_id = self.label.after(self.blink_interval, self.toggle_color)

    def start_blinking(self):
        self.toggle_color()

    def stop_blinking(self):
        self.label.config(bg=self._original_bg)
        if self._blink_id is not None:
            self.label.after_cancel(self._blink_id)

root = tk.Tk()
root.geometry("300x200")

blink_interval = 500

label_to_blink = tk.Label(root, text="Parpadeando", bg="green")
blinking_label = BlinkingLabel(label_to_blink, blink_interval)
blinking_label.start_blinking()

# Detener el parpadeo después de 5 segundos
root.after(5000, blinking_label.stop_blinking)

root.mainloop()
