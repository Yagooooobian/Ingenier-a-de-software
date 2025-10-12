# evaluacion_gui.py — GUI con selector de moneda
import tkinter as tk
from tkinter import ttk, messagebox

BONO_BASE_EUR = 2550.0  # valor final tras resolver conflicto

# Tasas de ejemplo: 1 EUR -> X moneda
RATES = {
    "EUR": 1.0,
    "USD": 1.08,   # aprox
    "MXN": 19.50,  # aprox
}

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

# ---- Formateo de moneda ----
def formato_eur(v: float) -> str:
    s = f"{v:,.2f}"
    s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"€{s}"

def formato_usd(v: float) -> str:
    return f"${v:,.2f} USD"

def formato_mxn(v: float) -> str:
    return f"${v:,.2f} MXN"

def formatea(valor: float, moneda: str) -> str:
    if moneda == "EUR": return formato_eur(valor)
    if moneda == "USD": return formato_usd(valor)
    if moneda == "MXN": return formato_mxn(valor)
    return f"{valor:.2f} {moneda}"

def convertir_desde_eur(monto_eur: float, moneda_destino: str) -> float:
    return monto_eur * RATES.get(moneda_destino, 1.0)

def calcular():
    raw = entrada_puntuacion.get().strip().replace(",", ".")
    moneda = combo_moneda.get().strip().upper()
    anios_raw = entrada_anios.get().strip()

    if not raw:
        messagebox.showwarning("Falta dato", "Ingresa la puntuación.")
        return
    if moneda not in ("EUR", "USD", "MXN"):
        messagebox.showwarning("Moneda inválida", "Elige EUR, USD o MXN.")
        return
    try:
        p = float(raw)
    except ValueError:
        messagebox.showerror("Error", "La puntuación debe ser numérica (ej. 0.0, 0.4, 0.6).")
        return
    try:
        anios = int(anios_raw or "0")
        if anios < 0: raise ValueError()
    except ValueError:
        messagebox.showerror("Error", "Años de antigüedad debe ser un entero ≥ 0.")
        return

    nivel, ok = nivel_y_valor(p)
    if not ok:
        messagebox.showwarning("Puntuación no válida", "Solo se aceptan 0.0, 0.4 o ≥0.6.")
        lbl_resultado.config(text="—")
        return

    # Fórmula B (Luis): € por año (100€/año hasta 5; luego 50€/año)
    extra_eur = min(anios, 5) * 100.0 + max(anios - 5, 0) * 50.0
    dinero_eur = BONO_BASE_EUR * p + extra_eur

    dinero_out = convertir_desde_eur(dinero_eur, moneda)
    extra_out = convertir_desde_eur(extra_eur, moneda)
    lbl_resultado.config(
        text=(
            f"Nivel: {nivel}\n"
            f"Puntuación: {p}\n"
            f"Antigüedad: {anios} años (extra {formatea(extra_out, moneda)})\n"
            f"Dinero a recibir: {formatea(dinero_out, moneda)}"
        )
    )


# --- UI ---
root = tk.Tk()
root.title("Evaluación de empleados")
root.geometry("520x260")
root.resizable(False, False)

frm = ttk.Frame(root, padding=16)
frm.pack(fill="both", expand=True)

# Fila 0: Puntuación
ttk.Label(frm, text="Puntuación (0.0, 0.4, 0.6+):").grid(row=0, column=0, sticky="w")
entrada_puntuacion = ttk.Entry(frm, width=18)
entrada_puntuacion.grid(row=0, column=1, sticky="w", padx=8)
entrada_puntuacion.insert(0, "0.0")

# Fila 1: Moneda
ttk.Label(frm, text="Moneda:").grid(row=1, column=0, sticky="w", pady=(8,0))
combo_moneda = ttk.Combobox(frm, values=["EUR", "USD", "MXN"], width=15, state="readonly")
combo_moneda.grid(row=1, column=1, sticky="w", padx=8, pady=(8,0))
combo_moneda.set("EUR")

# Fila 2: Antigüedad
ttk.Label(frm, text="Años de antigüedad:").grid(row=2, column=0, sticky="w", pady=(8,0))
entrada_anios = ttk.Entry(frm, width=10)
entrada_anios.grid(row=2, column=1, sticky="w", padx=8, pady=(8,0))
entrada_anios.insert(0, "0")
entrada_anios.bind("<Return>", lambda *_: calcular())


# Botón Calcular
btn = ttk.Button(frm, text="Calcular", command=calcular)
btn.grid(row=0, column=2, rowspan=2, padx=12)

ttk.Separator(frm, orient="horizontal").grid(row=3, column=0, columnspan=3, sticky="ew", pady=12)
# Resultado
lbl_resultado = ttk.Label(frm, text="—", font=("Segoe UI", 11, "bold"))
lbl_resultado.grid(row=4, column=0, columnspan=3, sticky="w")

# Accesos rápidos
entrada_puntuacion.bind("<Return>", lambda *_: calcular())
combo_moneda.bind("<Return>", lambda *_: calcular())

# Centrar ventana
root.update_idletasks()
w = root.winfo_width(); h = root.winfo_height()
x = (root.winfo_screenwidth() - w) // 2
y = (root.winfo_screenheight() - h) // 2
root.geometry(f"{w}x{h}+{x}+{y}")

root.mainloop()
