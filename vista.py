import tkinter as tk
from tkinter import ttk, messagebox

class VistaInicial:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.configurar_interfaz()
    
    def configurar_interfaz(self):
        self.limpiar_pantalla()
        
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(self.main_frame, text="Bienvenido a GreenGrowth", 
                 font=("Helvetica", 16, "bold")).pack(pady=20)
        
        ttk.Button(self.main_frame, text="Iniciar Sesión", 
                  command=self.controlador.mostrar_login).pack(pady=10, fill=tk.X)
        
        ttk.Button(self.main_frame, text="Registrarse", 
                  command=self.controlador.mostrar_registro).pack(pady=10, fill=tk.X)
    
    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()

class VistaLogin:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.configurar_interfaz()
    
    def configurar_interfaz(self):
        self.limpiar_pantalla()
        
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(self.main_frame, text="Inicio de Sesión", 
                 font=("Helvetica", 14, "bold")).pack(pady=10)
        
        
        form_frame = ttk.Frame(self.main_frame)
        form_frame.pack(pady=10)
        
        ttk.Label(form_frame, text="Usuario:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.username_entry = ttk.Entry(form_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Contraseña:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.password_entry = ttk.Entry(form_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Iniciar Sesión", 
                  command=self.intentar_login).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Volver", 
                  command=self.controlador.mostrar_bienvenida).pack(side=tk.LEFT, padx=5)
    
    def intentar_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.controlador.autenticar_usuario(username, password)
    
    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()

class VistaRegistro:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.configurar_interfaz()
    
    def configurar_interfaz(self):
        self.limpiar_pantalla()
        
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(self.main_frame, text="Registro de Usuario", 
                 font=("Helvetica", 14, "bold")).pack(pady=10)
        
        
        form_frame = ttk.Frame(self.main_frame)
        form_frame.pack(pady=10)
        
        campos = [
            ("Nombre Completo", "nombre_completo"),
            ("Email", "email"),
            ("Usuario", "username"),
            ("Contraseña", "password"),
            ("Confirmar Contraseña", "confirm_password")
        ]
        
        self.entries = {}
        for i, (label, key) in enumerate(campos):
            ttk.Label(form_frame, text=label+":").grid(row=i, column=0, padx=5, pady=5, sticky="e")
            entry = ttk.Entry(form_frame, show="*" if "password" in key else "")
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[key] = entry
        
    
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Registrarse", 
                  command=self.registrar_usuario).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Volver", 
                  command=self.controlador.mostrar_bienvenida).pack(side=tk.LEFT, padx=5)
    
    def registrar_usuario(self):
        datos = {k: v.get() for k, v in self.entries.items()}
        self.controlador.registrar_usuario(
            datos['nombre_completo'],
            datos['email'],
            datos['username'],
            datos['password'],
            datos['confirm_password']
        )
    
    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()

class VistaPrincipal:
    def __init__(self, root, controlador, usuario):
        self.root = root
        self.controlador = controlador
        self.usuario = usuario
        self.configurar_interfaz()
    
    def configurar_interfaz(self):
        self.limpiar_pantalla()
        
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        
        status_frame = ttk.Frame(self.main_frame)
        status_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(status_frame, text=f"Usuario: {self.usuario['nombre_completo']}").pack(side=tk.LEFT)
        ttk.Label(status_frame, text=f"Rol: {self.usuario['rol'].capitalize()}").pack(side=tk.RIGHT)
        
        
        ttk.Label(self.main_frame, text="Panel Principal", 
                 font=("Helvetica", 16, "bold")).pack(pady=10)
        
        
        content_frame = ttk.Frame(self.main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        
        
        ttk.Button(content_frame, text="Gestionar Invernaderos", 
                      command=self.controlador.mostrar_gestion_invernaderos).pack(pady=10, fill=tk.X)
        
        ttk.Button(content_frame, text="Cerrar Sesión", 
                  command=self.controlador.cerrar_sesion).pack(pady=10, fill=tk.X)
    
    def mostrar_datos(self, datos):
        
        pass
    
    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()