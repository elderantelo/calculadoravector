
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculadora de Vectores (2D/3D) con Interfaz Gráfica y Gráficas + Ángulo
"""

import math
import tkinter as tk
from tkinter import ttk, messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D

def parse_vector(text, expected_dim=None):
    text = text.strip()
    if not text:
        raise ValueError("El vector no puede estar vacío.")
    sep = ',' if ',' in text else (';' if ';' in text else ' ')
    parts = [p for p in text.replace(';', sep).split(sep) if p.strip() != '']
    try:
        vec = [float(p) for p in parts]
    except Exception:
        raise ValueError("Usa solo números (ej.: 1 2 3).")
    if expected_dim is not None and len(vec) != expected_dim:
        raise ValueError(f"Se esperaban {expected_dim} componentes, recibidas {len(vec)}.")
    return vec

def magnitude(v):
    return math.sqrt(sum(x*x for x in v))

def dot(a, b):
    if len(a) != len(b):
        raise ValueError("Dimensiones distintas para producto punto.")
    return sum(x*y for x, y in zip(a, b))

def cross2d(a, b):
    if len(a) != 2 or len(b) != 2:
        raise ValueError("Producto cruz 2D requiere vectores 2D.")
    return a[0]*b[1] - a[1]*b[0]

def cross3d(a, b):
    if len(a) != 3 or len(b) != 3:
        raise ValueError("Producto cruz 3D requiere vectores 3D.")
    x1, y1, z1 = a
    x2, y2, z2 = b
    return [y1*z2 - z1*y2, z1*x2 - x1*z2, x1*y2 - y1*x2]

def angle_between(a, b):
    mag_a = magnitude(a)
    mag_b = magnitude(b)
    if mag_a == 0 or mag_b == 0:
        raise ValueError("Uno de los vectores tiene módulo cero.")
    cos_theta = dot(a, b) / (mag_a * mag_b)
    cos_theta = max(min(cos_theta, 1), -1)
    angle_rad = math.acos(cos_theta)
    return math.degrees(angle_rad)

class VectorCalcApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora de Vectores 2D/3D con Gráficas y Ángulo")
        self.geometry("1000x600")

        self.operations = [
            "Suma 2D", "Suma 3D",
            "Módulo 2D", "Módulo 3D",
            "Producto Punto 2D", "Producto Punto 3D",
            "Producto Cruz 2D", "Producto Cruz 3D",
            "Ángulo entre vectores 2D", "Ángulo entre vectores 3D"
        ]

        self.create_widgets()
        self.update_inputs()

    def create_widgets(self):
        top = ttk.Frame(self)
        top.pack(padx=10, pady=10, fill="x")

        ttk.Label(top, text="Operación:").pack(side="left")
        self.op_var = tk.StringVar(value=self.operations[0])
        self.op_menu = ttk.Combobox(top, textvariable=self.op_var, values=self.operations, state="readonly", width=30)
        self.op_menu.pack(side="left", padx=5)
        self.op_menu.bind("<<ComboboxSelected>>", lambda e: self.update_inputs())

        ttk.Button(top, text="Calcular", command=self.calculate).pack(side="right")
        ttk.Button(top, text="Limpiar", command=self.clear_all).pack(side="right", padx=5)

        input_frame = ttk.LabelFrame(self, text="Vectores")
        input_frame.pack(padx=10, pady=5, fill="x")

        self.entry_a = ttk.Entry(input_frame, width=40)
        self.entry_b = ttk.Entry(input_frame, width=40)
        ttk.Label(input_frame, text="Vector A:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_a.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(input_frame, text="Vector B:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_b.grid(row=1, column=1, padx=5, pady=5)

        output_frame = ttk.LabelFrame(self, text="Resultado")
        output_frame.pack(padx=10, pady=5, fill="both", expand=True)

        self.output = tk.Text(output_frame, height=6)
        self.output.pack(fill="both", expand=True, padx=5, pady=5)

        graph_frame = ttk.LabelFrame(self, text="Gráfica")
        graph_frame.pack(padx=10, pady=5, fill="both", expand=True)

        self.figure = Figure(figsize=(6, 4))
        self.ax2d = self.figure.add_subplot(121)
        self.ax3d = self.figure.add_subplot(122, projection='3d')

        self.canvas = FigureCanvasTkAgg(self.figure, master=graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def clear_all(self):
        self.entry_a.delete(0, "end")
        self.entry_b.delete(0, "end")
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.configure(state="disabled")
        self.ax2d.clear()
        self.ax3d.clear()
        self.canvas.draw()

    def update_inputs(self):
        op = self.op_var.get()
        self.entry_b.configure(state="normal")
        if "Módulo" in op:
            self.entry_b.configure(state="disabled")

    def plot_vectors(self, a, b=None, result=None):
        dim = len(a)
        self.ax2d.clear()
        self.ax3d.clear()

        if dim == 2:
            def draw(v, color, label):
                self.ax2d.quiver(0, 0, v[0], v[1], angles='xy', scale_units='xy', scale=1, color=color, label=label, linewidth=2)
                self.ax2d.text(v[0], v[1], f"{label}: ({v[0]}, {v[1]})", fontsize=9, color=color)

            self.ax2d.set_title("Plano XY")
            self.ax2d.set_xlim(-10, 10)
            self.ax2d.set_ylim(-10, 10)
            self.ax2d.grid(True)
            draw(a, 'blue', 'A')
            if b: draw(b, 'green', 'B')
            if result: draw(result, 'red', 'Resultado')
            self.ax2d.legend()
        else:
            def draw3d(v, color, label):
                self.ax3d.quiver(0, 0, 0, v[0], v[1], v[2], color=color, linewidth=2)
                self.ax3d.text(v[0], v[1], v[2], f"{label}: ({v[0]}, {v[1]}, {v[2]})", fontsize=9, color=color)

            self.ax3d.set_title("Espacio XYZ")
            self.ax3d.set_xlim([-10, 10])
            self.ax3d.set_ylim([-10, 10])
            self.ax3d.set_zlim([-10, 10])
            draw3d(a, 'blue', 'A')
            if b: draw3d(b, 'green', 'B')
            if result: draw3d(result, 'red', 'Resultado')
            self.ax3d.legend()

        self.canvas.draw()

    def calculate(self):
        op = self.op_var.get()
        try:
            dim = 2 if "2D" in op else 3
            a = parse_vector(self.entry_a.get(), dim)
            b = None
            if "Módulo" not in op:
                b = parse_vector(self.entry_b.get(), dim)
            result = None

            if "Suma" in op:
                result = [a[i] + b[i] for i in range(len(a))]
                self.display_result(f"A + B = {[int(x) if x.is_integer() else round(x,4) for x in result]}")
            elif "Módulo" in op:
                result = magnitude(a)
                self.display_result(f"|A| = {int(result) if result.is_integer() else round(result,4)}")
            elif "Producto Punto" in op:
                result = dot(a, b)
                self.display_result(f"A · B = {int(result) if result.is_integer() else round(result,4)}")
            elif "Producto Cruz 2D" in op:
                result = cross2d(a, b)
                self.display_result(f"A × B (escalar) = {int(result) if result.is_integer() else round(result,4)}")
            elif "Producto Cruz 3D" in op:
                result = cross3d(a, b)
                self.display_result(f"A × B = {[int(x) if x.is_integer() else round(x,4) for x in result]}")
            elif "Ángulo entre vectores" in op:
                result = angle_between(a, b)
                self.display_result(f"θ = {round(result, 2)}°")

            self.plot_vectors(a, b, result if isinstance(result, list) else None)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_result(self, text):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("end", text)
        self.output.configure(state="disabled")

if __name__ == "__main__":
    app = VectorCalcApp()
    app.mainloop()
