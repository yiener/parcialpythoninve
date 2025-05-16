import tkinter as tk
from tkinter import messagebox
from modelo import Modelo
from vista import VistaInicial, VistaLogin, VistaRegistro, VistaPrincipal
from vista_invernaderos import VistaInvernaderos

class Controlador:
    def __init__(self, root):
        self.root = root
        self.modelo = Modelo()
        self.usuario_actual = None
        self.mostrar_bienvenida()
    
    def mostrar_bienvenida(self):
        self.vista_actual = VistaInicial(self.root, self)
    
    def mostrar_login(self):
        self.vista_actual = VistaLogin(self.root, self)
    
    def mostrar_registro(self):
        self.vista_actual = VistaRegistro(self.root, self)
    
    def registrar_usuario(self, nombre_completo, email, username, password, confirm_password):
        if not all([nombre_completo, email, username, password, confirm_password]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "La contraseña debe tener al menos 6 caracteres")
            return
        
        if self.modelo.registrar_usuario(username, password, nombre_completo, email):
            messagebox.showinfo("Éxito", "Registro exitoso. Por favor inicie sesión")
            self.mostrar_login()
        else:
            messagebox.showerror("Error", "No se pudo completar el registro. El usuario o email ya existen")
    
    def autenticar_usuario(self, username, password):
        usuario = self.modelo.autenticar_usuario(username, password)
        if usuario:
            self.usuario_actual = usuario
            self.vista_actual.limpiar_pantalla()
            self.vista_principal = VistaPrincipal(self.root, self, self.usuario_actual)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
    
    def mostrar_gestion_invernaderos(self):
        self.vista_principal.limpiar_pantalla()
        self.vista_invernaderos = VistaInvernaderos(self.root, self, self.usuario_actual)
    
    def volver_a_principal(self):
        if hasattr(self, 'vista_invernaderos'):
            self.vista_invernaderos.limpiar_pantalla()
        self.vista_principal = VistaPrincipal(self.root, self, self.usuario_actual)
    
    def cerrar_sesion(self):
        self.usuario_actual = None
        if hasattr(self, 'vista_principal'):
            self.vista_principal.limpiar_pantalla()
        self.mostrar_bienvenida()
    
    def obtener_invernaderos(self):
        return self.modelo.obtener_invernaderos()
    
    def obtener_invernadero(self, id_invernadero):
        return self.modelo.obtener_invernadero(id_invernadero)
    
    def registrar_invernadero(self, datos, usuario_id):
        return self.modelo.registrar_invernadero(datos, usuario_id)
    
    def actualizar_invernadero(self, id_invernadero, datos):
        return self.modelo.actualizar_invernadero(id_invernadero, datos)
    
    def eliminar_invernadero(self, id_invernadero):
        return self.modelo.eliminar_invernadero(id_invernadero)