# pizzeria_gui.py
import tkinter as tk
from tkinter import ttk, messagebox

BASE = ["Mozzarella", "Tomate"]
VEG = ["Pimiento", "Tofu"]
NO_VEG = ["Peperoni", "Jamón", "Salmón"]

def actualizar_menu(*_):
    opciones = VEG if es_veg.get() else NO_VEG
    menu = opt_ingrediente["menu"]
    menu.delete(0, "end")
    # set default
    ingrediente_var.set(opciones[0])
    for op in opciones:
        menu.add_command(label=op, command=tk._setit(ingrediente_var, op))

def resumen():
    adicionales = ingrediente_var.get()
    if not adicionales:
        messagebox.showwarning("Falta elegir", "Selecciona un ingrediente adicional.")
        return
    ingredientes = BASE + [adicionales]
    tipo = "Vegetariana" if es_veg.get() else "No vegetariana"

    msg = f"Tipo: {tipo}\nIngredientes: {', '.join(ingredientes)}"
    lbl_resumen.config(text=msg)
    messagebox.showinfo("Resumen del pedido", msg)

# --- UI ---
root = tk.Tk()
root.title("Pizzería Bella Napoli")
root.geometry("460x300")
root.resizable(False, False)

frm = ttk.Frame(root, padding=16)
frm.pack(fill="both", expand=True)

# Radio vegetariana
ttk.Label(frm, text="¿Pizza vegetariana?").grid(row=0, column=0, sticky="w")
es_veg = tk.BooleanVar(value=True)
ttk.Radiobutton(frm, text="Sí", variable=es_veg, value=True, command=actualizar_menu).grid(row=0, column=1, sticky="w")
ttk.Radiobutton(frm, text="No", variable=es_veg, value=False, command=actualizar_menu).grid(row=0, column=2, sticky="w")

# Menú ingrediente adicional
ttk.Label(frm, text="Ingrediente adicional (solo uno):").grid(row=1, column=0, columnspan=3, sticky="w", pady=(12, 0))
ingrediente_var = tk.StringVar()
opt_ingrediente = ttk.OptionMenu(frm, ingrediente_var, None)
opt_ingrediente.grid(row=2, column=0, columnspan=3, sticky="w")

# Botón y resumen
ttk.Button(frm, text="Hacer pedido", command=resumen).grid(row=3, column=0, pady=16, sticky="w")
lbl_resumen = ttk.Label(frm, text="—", font=("Segoe UI", 11, "bold"))
lbl_resumen.grid(row=4, column=0, columnspan=3, sticky="w")

# Iniciar opciones
actualizar_menu()

# Centrar ventana
root.update_idletasks()
w = root.winfo_width(); h = root.winfo_height()
x = (root.winfo_screenwidth() - w) // 2
y = (root.winfo_screenheight() - h) // 2
root.geometry(f"{w}x{h}+{x}+{y}")

root.mainloop()