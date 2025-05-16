import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class VistaInvernaderos:
    def __init__(self, root, controlador, usuario=None):
        self.root = root
        self.controlador = controlador
        self.usuario = usuario
        self.configurar_interfaz()
    
    def configurar_interfaz(self):
        self.limpiar_pantalla()
        
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        
        toolbar = ttk.Frame(self.main_frame)
        toolbar.pack(fill=tk.X, pady=5)
        
        ttk.Button(toolbar, text="Nuevo Invernadero", 
                  command=self.mostrar_formulario_registro).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Actualizar Lista", 
                  command=self.actualizar_lista).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Volver", 
                  command=self.controlador.volver_a_principal).pack(side=tk.RIGHT)
        
        
        self.tree = ttk.Treeview(self.main_frame, columns=('nombre', 'tipo_cultivo', 'responsable'), selectmode='browse')
        self.tree.heading('#0', text='ID')
        self.tree.column('#0', width=50)
        self.tree.heading('nombre', text='Nombre')
        self.tree.heading('tipo_cultivo', text='Tipo de Cultivo')
        self.tree.heading('responsable', text='Responsable')
        self.tree.pack(fill=tk.BOTH, expand=True)
        
    
        action_frame = ttk.Frame(self.main_frame)
        action_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(action_frame, text="Ver Detalles", 
                  command=self.ver_detalles).pack(side=tk.LEFT, padx=2)
        ttk.Button(action_frame, text="Editar", 
                  command=self.editar_invernadero).pack(side=tk.LEFT, padx=2)
        ttk.Button(action_frame, text="Eliminar", 
                  command=self.eliminar_invernadero).pack(side=tk.LEFT, padx=2)
        
        self.actualizar_lista()
    
    def actualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        invernaderos = self.controlador.obtener_invernaderos()
        for inv in invernaderos:
            self.tree.insert('', 'end', iid=inv['id'], text=inv['id'],
                            values=(inv['nombre'], inv['tipo_cultivo'], inv['responsable']))
    
    def mostrar_formulario_registro(self, invernadero=None):
        self.top = tk.Toplevel(self.root)
        self.top.title("Registrar Invernadero" if not invernadero else "Editar Invernadero")
        
        frame = ttk.Frame(self.top, padding="20")
        frame.pack()
        
        campos = [
            ("Nombre del invernadero", "nombre"),
            ("Superficie (m²)", "superficie"),
            ("Tipo de cultivo", "tipo_cultivo"),
            ("Fecha de creación (YYYY-MM-DD)", "fecha_creacion"),
            ("Responsable", "responsable"),
            ("Capacidad de producción", "capacidad_produccion")
        ]
        
        self.entries = {}
        for i, (label, key) in enumerate(campos):
            ttk.Label(frame, text=label+":").grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entry = ttk.Entry(frame)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[key] = entry
            
            if invernadero and key in invernadero:
                entry.insert(0, str(invernadero[key]))
        
        
        ttk.Label(frame, text="Sistema de riego:").grid(row=len(campos), column=0, sticky="e", padx=5, pady=5)
        self.sistema_riego = tk.StringVar()
        self.sistema_riego.set(invernadero['sistema_riego'] if invernadero else 'Automatizado')
        
        sistemas = ['Manual', 'Automatizado', 'Por goteo']
        for i, sistema in enumerate(sistemas):
            rb = ttk.Radiobutton(frame, text=sistema, value=sistema, variable=self.sistema_riego)
            rb.grid(row=len(campos)+1+i, column=1, sticky="w", padx=5, pady=2)
        

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=len(campos)+4, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Guardar", 
                  command=lambda: self.guardar_invernadero(invernadero['id'] if invernadero else None)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", 
                  command=self.top.destroy).pack(side=tk.LEFT, padx=5)
    
    def guardar_invernadero(self, id_invernadero=None):
        datos = {k: v.get() for k, v in self.entries.items()}
        datos['sistema_riego'] = self.sistema_riego.get()
        
        
        if not datos['nombre'] or not datos['responsable']:
            messagebox.showerror("Error", "Nombre y responsable son campos obligatorios")
            return
        
        try:
            datos['superficie'] = float(datos['superficie'])
            datetime.strptime(datos['fecha_creacion'], '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Superficie debe ser numérico y fecha en formato YYYY-MM-DD")
            return
        
        if id_invernadero:
            if self.controlador.actualizar_invernadero(id_invernadero, datos):
                messagebox.showinfo("Éxito", "Invernadero actualizado correctamente")
                self.top.destroy()
                self.actualizar_lista()
        else:
            if self.controlador.registrar_invernadero(datos, self.usuario['id']):
                messagebox.showinfo("Éxito", "Invernadero registrado correctamente")
                self.top.destroy()
                self.actualizar_lista()
    
    def ver_detalles(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un invernadero")
            return
        
        invernadero = self.controlador.obtener_invernadero(seleccionado[0])
        if invernadero:
            top = tk.Toplevel(self.root)
            top.title(f"Detalles - {invernadero['nombre']}")
            
            frame = ttk.Frame(top, padding="20")
            frame.pack()
            
            detalles = [
                ("Nombre del invernadero", invernadero['nombre']),
                ("Superficie (m²)", invernadero['superficie']),
                ("Tipo de cultivo", invernadero['tipo_cultivo']),
                ("Fecha de creación", invernadero['fecha_creacion']),
                ("Responsable", invernadero['responsable']),
                ("Capacidad de producción", invernadero['capacidad_produccion']),
                ("Sistema de riego", invernadero['sistema_riego'])
            ]
            
            for i, (label, valor) in enumerate(detalles):
                ttk.Label(frame, text=label+":", font=('Helvetica', 10, 'bold')).grid(row=i, column=0, sticky="e", padx=5, pady=2)
                ttk.Label(frame, text=valor).grid(row=i, column=1, sticky="w", padx=5, pady=2)
            
            ttk.Button(frame, text="Cerrar", command=top.destroy).grid(row=len(detalles), column=0, columnspan=2, pady=10)
    
    def editar_invernadero(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un invernadero")
            return
        
        invernadero = self.controlador.obtener_invernadero(seleccionado[0])
        if invernadero:
            self.mostrar_formulario_registro(invernadero)
    
    def eliminar_invernadero(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un invernadero")
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este invernadero?"):
            if self.controlador.eliminar_invernadero(seleccionado[0]):
                messagebox.showinfo("Éxito", "Invernadero eliminado correctamente")
                self.actualizar_lista()
    
    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()