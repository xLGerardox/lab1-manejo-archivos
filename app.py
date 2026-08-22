import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

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
    self.root.title("LAB1 - GESTION DE CONFIG")
    self.root.geometry("450x500")

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

    # Menú Archivo (Simulado)
    archivo_menu = tk.Menu(menubar, tearoff=0)
    archivo_menu.add_command(label="Nuevo", state="disabled")
    archivo_menu.add_command(label="Abrir", state="disabled")
    menubar.add_cascade(label="Archivo", menu=archivo_menu)

    # Menú Edición (Simulado)
    edicion_menu = tk.Menu(menubar, tearoff=0)
    edicion_menu.add_command(label="Deshacer", state="disabled")
    menubar.add_cascade(label="Edición", menu=edicion_menu)

    # Menú Ver (Simulado)
    ver_menu = tk.Menu(menubar, tearoff=0)
    ver_menu.add_command(label="Zoom", state="disabled")
    menubar.add_cascade(label="Ver", menu=ver_menu)

    # Menú Settings (Funcional)
    settings_menu = tk.Menu(menubar, tearoff=0)
    settings_menu.add_command(
        label="Abrir Configuración", command=self.abrir_ventana_settings
    )
    menubar.add_cascade(label="Settings", menu=settings_menu)

    self.root.config(menu=menubar)

  def crear_interfaz_principal(self):
    self.frame = ttk.Frame(self.root, padding="20")
    self.frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(
        self.frame,
        text="panel principal- configuración actual",
        font=("Arial", 12, "bold"),
    ).pack(pady=10)

    self.lbl_info = ttk.Label(
        self.frame, text=self.obtener_texto_resumen(), justify=tk.LEFT
    )
    self.lbl_info.pack(pady=10)

    btn_settings = ttk.Button(
        self.frame,
        text="Modificar Settings",
        command=self.abrir_ventana_settings,
    )
    btn_settings.pack(pady=20)

  def obtener_texto_resumen(self):
    return (
        f"Nombre de usuario: {self.config_data.get('nombre_usuario')}\n"
        f"Tema: {self.config_data.get('tema')}\n"
        f"Idioma: {self.config_data.get('idioma')}\n"
        f"Tamaño Fuente: {self.config_data.get('tamanio_fuente')}\n"
        f"Foto de Perfil: {self.config_data.get('foto_perfil') or 'Ninguna'}"
    )

  def abrir_ventana_settings(self):
    top = tk.Toplevel(self.root)
    top.title("Configuración de Usuario")
    top.geometry("350x450")

    # Nombre usuario
    ttk.Label(top, text="Nombre de usuario:").pack(anchor="w", padx=20, pady=5)
    ent_nombre = ttk.Entry(top)
    ent_nombre.insert(0, self.config_data.get("nombre_usuario"))
    ent_nombre.pack(fill=tk.X, padx=20)

    # Tema
    ttk.Label(top, text="Tema interfaz:").pack(anchor="w", padx=20, pady=5)
    cb_tema = ttk.Combobox(top, values=["Claro", "Oscuro"], state="readonly")
    cb_tema.set(self.config_data.get("tema"))
    cb_tema.pack(fill=tk.X, padx=20)

    # Idioma
    ttk.Label(top, text="Idioma:").pack(anchor="w", padx=20, pady=5)
    cb_idioma = ttk.Combobox(top, values=["es-ES", "en-US"], state="readonly")
    cb_idioma.set(self.config_data.get("idioma"))
    cb_idioma.pack(fill=tk.X, padx=20)

    # Tamaño fuente
    ttk.Label(top, text="Tamaño fuente:").pack(anchor="w", padx=20, pady=5)
    ent_fuente = ttk.Entry(top)
    ent_fuente.insert(0, str(self.config_data.get("tamanio_fuente")))
    ent_fuente.pack(fill=tk.X, padx=20)

    # Foto de perfil selector
    def seleccionar_foto():
      ruta = filedialog.askopenfilename(
          title="Seleccionar foto de perfil",
          filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")],
      )
      if ruta:
        lbl_ruta_val.config(text=ruta)

    btn_foto = ttk.Button(
        top, text="Seleccionar Foto de Perfil", command=seleccionar_foto
    )
    btn_foto.pack(pady=10, padx=20, anchor="w")

    lbl_ruta_val = ttk.Label(
        top,
        text=self.config_data.get("foto_perfil") or "Sin selección",
        wraplength=300,
    )
    lbl_ruta_val.pack(padx=20, anchor="w")

    def guardar_temporal_ui():
      try:
        self.config_data["nombre_usuario"] = ent_nombre.get()
        self.config_data["tema"] = cb_tema.get()
        self.config_data["idioma"] = cb_idioma.get()
        self.config_data["tamanio_fuente"] = int(ent_fuente.get())

        foto_txt = lbl_ruta_val.cget("text")
        if foto_txt != "Sin selección":
          self.config_data["foto_perfil"] = foto_txt

        self.lbl_info.config(text=self.obtener_texto_resumen())
        messagebox.showinfo(
            "Info",
            "Cambios aplicados en memoria",
        )
        top.destroy()
      except ValueError:
        messagebox.showerror(
            "Errorrrr, solo nums enteros"
        )

    btn_guardar = ttk.Button(
        top, text="SE APLICARAN CAMBIOS", command=guardar_temporal_ui
    )
    btn_guardar.pack(pady=20)


if __name__ == "__main__":
  root = tk.Tk()
  app = ConfigApp(root)
  root.mainloop()