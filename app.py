# luis GERARDO tucux RIVERA
import json
import os

os.environ["TK_SILENCE_DEPRECATION"] = "1"
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

CONFIG_FILE = "config.json"
TEMP_FILE = "config.tmp"
BACKUP_FILE = "config.bak"

DEFAULT_CONFIG = {
    "nombre_usuario": "José María",
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
    self.root.title("Gestión de Configuración")
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
        if not isinstance(data, dict):
          raise ValueError("Formato de diccionario inválido.")
        config = DEFAULT_CONFIG.copy()
        config.update(data)
        return config

    except (json.JSONDecodeError, ValueError):
      messagebox.showwarning(
          "Aviso",
          "El archivo de configuración presenta un formato inválido. Se"
          " cargarán los valores predeterminados.",
      )
      return DEFAULT_CONFIG.copy()

    except PermissionError:
      messagebox.showerror(
          "Error",
          "No se cuentan con los permisos necesarios para leer el archivo.",
      )
      return DEFAULT_CONFIG.copy()

    except Exception:
      return DEFAULT_CONFIG.copy()

  def guardar_configuracion(self):
    try:
      if os.path.exists(CONFIG_FILE):
        shutil.copy2(CONFIG_FILE, BACKUP_FILE)

      with open(TEMP_FILE, "w", encoding="utf-8") as f:
        json.dump(self.config_data, f, ensure_ascii=False, indent=4)

      os.replace(TEMP_FILE, CONFIG_FILE)
      messagebox.showinfo("Éxito", "Los cambios se guardaron correctamente.")

    except PermissionError:
      messagebox.showerror(
          "Error", "No hay permisos de escritura en el directorio."
      )
      if os.path.exists(TEMP_FILE):
        os.remove(TEMP_FILE)

    except Exception as e:
      messagebox.showerror("Error", f"Ocurrió un error al guardar: {e}")
      if os.path.exists(TEMP_FILE):
        os.remove(TEMP_FILE)


  def crear_menu(self):
    menubar = tk.Menu(self.root)

    # Menú Archivo
    archivo_menu = tk.Menu(menubar, tearoff=0)
    archivo_menu.add_command(label="Nuevo", state="disabled")
    archivo_menu.add_command(label="Abrir", state="disabled")
    menubar.add_cascade(label="Archivo", menu=archivo_menu)

    # Menú Edición
    edicion_menu = tk.Menu(menubar, tearoff=0)
    edicion_menu.add_command(label="Deshacer", state="disabled")
    menubar.add_cascade(label="Edición", menu=edicion_menu)

    # Menú Ver
    ver_menu = tk.Menu(menubar, tearoff=0)
    ver_menu.add_command(label="Zoom", state="disabled")
    menubar.add_cascade(label="Ver", menu=ver_menu)

    # Menú Configuración
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
        text="Panel Principal - Configuración Actual",
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

    ttk.Label(top, text="Nombre de usuario:").pack(anchor="w", padx=20, pady=5)
    ent_nombre = ttk.Entry(top)
    ent_nombre.insert(0, self.config_data.get("nombre_usuario"))
    ent_nombre.pack(fill=tk.X, padx=20)

    ttk.Label(top, text="Tema interfaz:").pack(anchor="w", padx=20, pady=5)
    cb_tema = ttk.Combobox(top, values=["Claro", "Oscuro"], state="readonly")
    cb_tema.set(self.config_data.get("tema"))
    cb_tema.pack(fill=tk.X, padx=20)

    ttk.Label(top, text="Idioma:").pack(anchor="w", padx=20, pady=5)
    cb_idioma = ttk.Combobox(top, values=["es-ES", "en-US"], state="readonly")
    cb_idioma.set(self.config_data.get("idioma"))
    cb_idioma.pack(fill=tk.X, padx=20)

    ttk.Label(top, text="Tamaño fuente:").pack(anchor="w", padx=20, pady=5)
    ent_fuente = ttk.Entry(top)
    ent_fuente.insert(0, str(self.config_data.get("tamanio_fuente")))
    ent_fuente.pack(fill=tk.X, padx=20)

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

    def guardar_cambios_ui():
      try:
        self.config_data["nombre_usuario"] = ent_nombre.get()
        self.config_data["tema"] = cb_tema.get()
        self.config_data["idioma"] = cb_idioma.get()
        self.config_data["tamanio_fuente"] = int(ent_fuente.get())

        foto_txt = lbl_ruta_val.cget("text")
        if foto_txt != "Sin selección":
          self.config_data["foto_perfil"] = foto_txt

        self.guardar_configuracion()
        self.lbl_info.config(text=self.obtener_texto_resumen())
        top.destroy()
      except ValueError:
        messagebox.showerror(
            "Error", "El tamaño de fuente debe ser un número entero."
        )

    btn_guardar = ttk.Button(
        top, text="Guardar Cambios", command=guardar_cambios_ui
    )
    btn_guardar.pack(pady=20)

if __name__ == "__main__":
  root = tk.Tk()
  app = ConfigApp(root)
  root.mainloop()