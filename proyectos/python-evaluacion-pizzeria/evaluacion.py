# evaluacion_gui.py
import tkinter as tk
from tkinter import ttk, messagebox

BONO_BASE = 2400.0

def nivel_y_valor(puntuacion: float):
    """Devuelve (nivel, es_valida). Válidos: 0.0, 0.4, >=0.6"""
    if puntuacion == 0.0:
        return "Inaceptable", True
    elif puntuacion == 0.4:
        return "Aceptable", True
    elif puntuacion >= 0.6:
        return "Meritorio", True
    else:
        return "No válido", False

def formato_eur(v: float) -> str:
    # Formato estilo EU: separador de miles '.' y decimal ','
    s = f"{v:,.2f}"
    s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"€{s}"

def calcular():
    raw = entrada_puntuacion.get().strip().replace(",", ".")
    try:
        p = float(raw)
    except ValueError:
        messagebox.showerror("Error", "Ingresa un número (0.0, 0.4 o 0.6 en adelante).")
        return

    nivel, ok = nivel_y_valor(p)
    if not ok:
        messagebox.showwarning("Puntuación inválida",
                               "Solo se aceptan 0.0, 0.4 o 0.6 en adelante.")
        lbl_resultado.config(text="—")
        return

    dinero = BONO_BASE * p
    lbl_resultado.config(text=f"Nivel: {nivel}\nDinero a recibir: {formato_eur(dinero)}")

# --- UI ---
root = tk.Tk()
root.title("Evaluación de empleados")
root.geometry("420x240")
root.resizable(False, False)

frm = ttk.Frame(root, padding=16)
frm.pack(fill="both", expand=True)

ttk.Label(frm, text="Puntuación (0.0, 0.4, 0.6+):").grid(row=0, column=0, sticky="w")
entrada_puntuacion = ttk.Entry(frm, width=20)
entrada_puntuacion.grid(row=0, column=1, sticky="w", padx=8)
entrada_puntuacion.insert(0, "0.0")

btn = ttk.Button(frm, text="Calcular", command=calcular)
btn.grid(row=0, column=2, padx=8)

ttk.Separator(frm, orient="horizontal").grid(row=1, column=0, columnspan=3, sticky="ew", pady=12)
lbl_resultado = ttk.Label(frm, text="—", font=("Segoe UI", 11, "bold"))
lbl_resultado.grid(row=2, column=0, columnspan=3, sticky="w")

# Centrar ventana
root.update_idletasks()
w = root.winfo_width(); h = root.winfo_height()
x = (root.winfo_screenwidth() - w) // 2
y = (root.winfo_screenheight() - h) // 2
root.geometry(f"{w}x{h}+{x}+{y}")

root.mainloop()
