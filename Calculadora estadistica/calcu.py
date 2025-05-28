import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, binom
from datetime import datetime
import os

# Ruta para guardar las gráficas
RUTA_SALIDA = "graficas"
os.makedirs(RUTA_SALIDA, exist_ok=True)

def guardar_grafica(nombre):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{nombre}_{timestamp}.png"
    filepath = os.path.join(RUTA_SALIDA, filename)
    plt.savefig(filepath)
    return filepath

# ------------------ DISTRIBUCIÓN NORMAL ------------------
def calcular_normal():
    try:
        mu = float(entry_mu.get())
        sigma = float(entry_sigma.get())
        a = float(entry_a.get())
        b = float(entry_b.get())

        if sigma <= 0:
            raise ValueError("La desviación estándar debe ser mayor que cero.")
        if a > b:
            raise ValueError("El límite inferior 'a' debe ser menor que el límite superior 'b'.")

        probabilidad = norm.cdf(b, mu, sigma) - norm.cdf(a, mu, sigma)

        x = np.linspace(mu - 4*sigma, mu + 4*sigma, 1000)
        y = norm.pdf(x, mu, sigma)

        x_fill = np.linspace(a, b, 1000)
        y_fill = norm.pdf(x_fill, mu, sigma)

        plt.figure(figsize=(8, 5))
        plt.plot(x, y, label='Distribución Normal', color='blue')
        plt.fill_between(x_fill, y_fill, color='skyblue', alpha=0.5,
                         label=f'Área P({a} ≤ X ≤ {b}) = {probabilidad:.4f}')
        plt.title('Distribución Normal y Área entre a y b')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.legend()
        plt.grid(True)
        ruta = guardar_grafica("normal")
        plt.show()
        plt.close()

        messagebox.showinfo("Resultado", f"P({a} ≤ X ≤ {b}) = {probabilidad:.4f}\nImagen guardada en: {ruta}")
    except ValueError as e:
        messagebox.showerror("Error de entrada", str(e))

# ------------------ DISTRIBUCIÓN BINOMIAL ------------------
def calcular_binomial():
    try:
        n = int(entry_n.get())
        p = float(entry_p.get())
        x = int(entry_x.get())

        if not (0 <= p <= 1):
            raise ValueError("La probabilidad p debe estar entre 0 y 1.")
        if not (0 <= x <= n):
            raise ValueError("El valor x debe estar entre 0 y n.")

        probabilidad = binom.pmf(x, n, p)

        valores_x = np.arange(0, n+1)
        valores_y = binom.pmf(valores_x, n, p)

        plt.figure(figsize=(8, 5))
        plt.bar(valores_x, valores_y, color='lightgreen', label='Distribución Binomial')
        plt.bar(x, binom.pmf(x, n, p), color='green', label=f'P(X = {x}) = {probabilidad:.4f}')
        plt.title(f'Distribución Binomial (n={n}, p={p})')
        plt.xlabel('x')
        plt.ylabel('P(X = x)')
        plt.legend()
        plt.grid(True)
        ruta = guardar_grafica("binomial")
        plt.show()
        plt.close()

        messagebox.showinfo("Resultado", f"P(X = {x}) = {probabilidad:.4f}\nImagen guardada en: {ruta}")
    except ValueError as e:
        messagebox.showerror("Error de entrada", str(e))

# ------------------ INTERFAZ ------------------
root = tk.Tk()
root.title("Calculadora de Distribuciones")
root.geometry("450x350")

notebook = ttk.Notebook(root)

# --- Pestaña Normal ---
frame_normal = ttk.Frame(notebook)
notebook.add(frame_normal, text="Distribución Normal")

labels_normal = ["Media (μ):", "Desviación estándar (σ):", "Límite inferior (a):", "Límite superior (b):"]
entries_normal = []

for i, texto in enumerate(labels_normal):
    tk.Label(frame_normal, text=texto).grid(row=i, column=0, padx=10, pady=5, sticky="e")
    entry = tk.Entry(frame_normal)
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries_normal.append(entry)

entry_mu, entry_sigma, entry_a, entry_b = entries_normal

btn_normal = tk.Button(frame_normal, text="Calcular", command=calcular_normal)
btn_normal.grid(row=4, column=0, columnspan=2, pady=10)

# --- Pestaña Binomial ---
frame_binomial = ttk.Frame(notebook)
notebook.add(frame_binomial, text="Distribución Binomial")

labels_binomial = ["Número de ensayos (n):", "Probabilidad de éxito (p):", "Valor de x:"]
entries_binomial = []

for i, texto in enumerate(labels_binomial):
    tk.Label(frame_binomial, text=texto).grid(row=i, column=0, padx=10, pady=5, sticky="e")
    entry = tk.Entry(frame_binomial)
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries_binomial.append(entry)

entry_n, entry_p, entry_x = entries_binomial

btn_binomial = tk.Button(frame_binomial, text="Calcular", command=calcular_binomial)
btn_binomial.grid(row=3, column=0, columnspan=2, pady=10)

notebook.pack(expand=1, fill="both")
root.mainloop()