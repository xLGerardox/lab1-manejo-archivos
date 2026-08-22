import json
import os
import tkinter as tk
from tkinter import messagebox, ttk

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "nombre_usuario": "Usuario",
    "tema": "Claro",
    "idioma": "es-ES",
    "tamanio_fuente": 12,
    "color_menu": "#f0f0f0",
    "color_letra": "#000000",
    "foto_perfil": "",
}


class ConfigApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Gestión de Configuración - Lab 1")
    self.root.geometry("450x400")

    self.config_data = self.cargar_configuracion()

    self.crear_menu()
    self.crear_interfaz_principal()

  def cargar_configuracion(self):
    if not os.path.exists(CONFIG_FILE):
      return DEFAULT_CONFIG.copy()
    try:
      with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        config = DEFAULT_CONFIG.copy()
        config.update(data)
        return config
    except Exception:
      return DEFAULT_CONFIG.copy()

  def crear_menu(self):
    menubar = tk.Menu(self.root)
    archivo_menu = tk.Menu(menubar, tearoff=0)
    archivo_menu.add_command(label="Nuevo", state="disabled")
    menubar.add_cascade(label="Archivo", menu=archivo_menu)

    settings_menu = tk.Menu(menubar, tearoff=0)
    settings_menu.add_command(
        label="Abrir Configuración",
        command=lambda: messagebox.showinfo(
            "Info", "Ventana de settings en desarrollo"
        ),
    )
    menubar.add_cascade(label="Settings", menu=settings_menu)
    self.root.config(menu=menubar)

  def crear_interfaz_principal(self):
    frame = ttk.Frame(self.root, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(
        frame, text="Configuración Actual leída", font=("Arial", 12, "bold")
    ).pack(pady=10)

    texto_resumen = (
        f"Usuario: {self.config_data.get('nombre_usuario')}\n"
        f"Tema: {self.config_data.get('tema')}\n"
        f"Idioma: {self.config_data.get('idioma')}\n"
        f"Fuente: {self.config_data.get('tamanio_fuente')}"
    )
    ttk.Label(frame, text=texto_resumen, justify=tk.LEFT).pack(pady=10)


if __name__ == "__main__":
  root = tk.Tk()
  app = ConfigApp(root)
  root.mainloop()