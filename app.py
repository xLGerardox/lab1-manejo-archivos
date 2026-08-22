import tkinter as tk
from tkinter import messagebox, ttk


class ConfigApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Gestión de Configuración - Lab 1")
    self.root.geometry("400x300")

    self.crear_menu()
    self.crear_interfaz_principal()

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

    # Menú Settings (Pendiente de implementar funcionalidad completa)
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
        frame, text="Bienvenido a la App", font=("Arial", 14, "bold")
    ).pack(pady=20)


if __name__ == "__main__":
  root = tk.Tk()
  app = ConfigApp(root)
  root.mainloop()