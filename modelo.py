import sqlite3
from passlib.hash import bcrypt

class Modelo:
    def __init__(self):
        self.conn = sqlite3.connect('greengrowth.db')
        self.crear_tablas()
    
    def crear_tablas(self):
        cursor = self.conn.cursor()
        
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            nombre_completo TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            rol TEXT NOT NULL DEFAULT 'usuario'
        )
        ''')
        
        # Tabla de invernaderos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS invernaderos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            superficie REAL NOT NULL,
            tipo_cultivo TEXT NOT NULL,
            fecha_creacion TEXT NOT NULL,
            responsable TEXT NOT NULL,
            capacidad_produccion TEXT NOT NULL,
            sistema_riego TEXT NOT NULL,
            temperatura REAL,
            humedad REAL,
            luminosidad REAL,
            ultimo_riego TEXT,
            usuario_id INTEGER,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
        ''')
        
        self.conn.commit()
    
    def registrar_usuario(self, username, password, nombre_completo, email):
        try:
            hashed = bcrypt.hash(password)
            cursor = self.conn.cursor()
            cursor.execute('''
            INSERT INTO usuarios (username, password, nombre_completo, email)
            VALUES (?, ?, ?, ?)
            ''', (username, hashed, nombre_completo, email))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def autenticar_usuario(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, password, nombre_completo, rol FROM usuarios WHERE username = ?', (username,))
        usuario = cursor.fetchone()
        
        if usuario and bcrypt.verify(password, usuario[1]):
            return {
                'id': usuario[0],
                'nombre_completo': usuario[2],
                'rol': usuario[3]
            }
        return None
    
    def obtener_datos_invernaderos(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT id, nombre, temperatura, humedad, luminosidad, ultimo_riego 
        FROM invernaderos LIMIT 5
        ''')
        return [{
            'id': row[0],
            'nombre': row[1],
            'temperatura': row[2],
            'humedad': row[3],
            'luminosidad': row[4],
            'ultimo_riego': row[5]
        } for row in cursor.fetchall()]
    
    def actualizar_datos(self, id_invernadero, temperatura, humedad, luminosidad):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
            UPDATE invernaderos 
            SET temperatura = ?, humedad = ?, luminosidad = ?, ultimo_riego = datetime('now')
            WHERE id = ?
            ''', (temperatura, humedad, luminosidad, id_invernadero))
            self.conn.commit()
            return cursor.rowcount > 0
        except:
            return False
    
    def obtener_invernaderos(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, nombre, tipo_cultivo, responsable FROM invernaderos')
        return [{
            'id': row[0],
            'nombre': row[1],
            'tipo_cultivo': row[2],
            'responsable': row[3]
        } for row in cursor.fetchall()]
    
    def obtener_invernadero(self, id_invernadero):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM invernaderos WHERE id = ?', (id_invernadero,))
        row = cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'nombre': row[1],
                'superficie': row[2],
                'tipo_cultivo': row[3],
                'fecha_creacion': row[4],
                'responsable': row[5],
                'capacidad_produccion': row[6],
                'sistema_riego': row[7],
                'temperatura': row[8],
                'humedad': row[9],
                'luminosidad': row[10],
                'ultimo_riego': row[11]
            }
        return None
    
    def registrar_invernadero(self, datos, usuario_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
            INSERT INTO invernaderos (
                nombre, superficie, tipo_cultivo, fecha_creacion, 
                responsable, capacidad_produccion, sistema_riego, usuario_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datos['nombre'], datos['superficie'], datos['tipo_cultivo'],
                datos['fecha_creacion'], datos['responsable'], 
                datos['capacidad_produccion'], datos['sistema_riego'], usuario_id
            ))
            self.conn.commit()
            return True
        except:
            return False
    
    def actualizar_invernadero(self, id_invernadero, datos):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
            UPDATE invernaderos 
            SET nombre = ?, superficie = ?, tipo_cultivo = ?, fecha_creacion = ?,
                responsable = ?, capacidad_produccion = ?, sistema_riego = ?
            WHERE id = ?
            ''', (
                datos['nombre'], datos['superficie'], datos['tipo_cultivo'],
                datos['fecha_creacion'], datos['responsable'], 
                datos['capacidad_produccion'], datos['sistema_riego'], id_invernadero
            ))
            self.conn.commit()
            return cursor.rowcount > 0
        except:
            return False
    
    def eliminar_invernadero(self, id_invernadero):
        try:
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM invernaderos WHERE id = ?', (id_invernadero,))
            self.conn.commit()
            return cursor.rowcount > 0
        except:
            return False