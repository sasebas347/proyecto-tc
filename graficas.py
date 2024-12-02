import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Datos ficticios
estados = ["Pago", "No Pago", "Vencido", "Cortado"]
cantidad_referencias = [15, 25, 10, 5]
montos_por_estado = [5000, 10000, 4000, 2000]

# Función para crear la gráfica de pastel
def crear_grafica_pastel():
    fig, ax = plt.subplots()
    ax.pie(
        cantidad_referencias, 
        labels=estados, 
        autopct='%1.1f%%', 
        colors=['#4CAF50', '#FFC107', '#FF5722', '#F44336']
    )
    ax.set_title("Distribución de Estados")
    return fig

# Función para crear la gráfica de barras
def crear_grafica_barras():
    fig, ax = plt.subplots()
    ax.bar(estados, montos_por_estado, color=['#4CAF50', '#FFC107', '#FF5722', '#F44336'])
    ax.set_title("Monto Total por Estado")
    ax.set_ylabel("Monto ($)")
    ax.set_xlabel("Estados")
    return fig

# Crear ventana principal
root = tk.Tk()
root.title("Control de Cuentas por Cobrar")

# Título
titulo = tk.Label(root, text="Control de Cuentas por Cobrar", font=("Arial", 20))
titulo.pack(pady=10)

# Frame para la gráfica de pastel
frame_pastel = ttk.LabelFrame(root, text="Gráfica de Pastel")
frame_pastel.pack(padx=10, pady=10, fill="both", expand=True)

fig_pastel = crear_grafica_pastel()
canvas_pastel = FigureCanvasTkAgg(fig_pastel, master=frame_pastel)
canvas_pastel.draw()
canvas_pastel.get_tk_widget().pack()

# Frame para la gráfica de barras
frame_barras = ttk.LabelFrame(root, text="Gráfica de Barras")
frame_barras.pack(padx=10, pady=10, fill="both", expand=True)

fig_barras = crear_grafica_barras()
canvas_barras = FigureCanvasTkAgg(fig_barras, master=frame_barras)
canvas_barras.draw()
canvas_barras.get_tk_widget().pack()

# Ejecutar aplicación
root.mainloop()