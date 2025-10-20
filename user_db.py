#!/usr/bin/env python3
import sqlite3
import hashlib
import os

class UserDB:
    def __init__(self, db_path='users.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Inicializa la base de datos y crea las tablas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                can_read BOOLEAN DEFAULT 1,
                can_write BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Crear usuarios por defecto si no existen
        self.create_default_users()
    
    def hash_password(self, password):
        """Hash de la contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username, password, can_read=True, can_write=False):
        """Crear nuevo usuario"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (username, password_hash, can_read, can_write)
                VALUES (?, ?, ?, ?)
            ''', (username, self.hash_password(password), can_read, can_write))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def authenticate(self, username, password):
        """Autenticar usuario y devolver permisos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT can_read, can_write FROM users 
            WHERE username = ? AND password_hash = ?
        ''', (username, self.hash_password(password)))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {'can_read': bool(result[0]), 'can_write': bool(result[1])}
        return None
    
    def update_permissions(self, username, can_read=None, can_write=None):
        """Actualizar permisos de usuario"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if can_read is not None:
            updates.append('can_read = ?')
            params.append(can_read)
        
        if can_write is not None:
            updates.append('can_write = ?')
            params.append(can_write)
        
        if updates:
            params.append(username)
            cursor.execute(f'''
                UPDATE users SET {', '.join(updates)}
                WHERE username = ?
            ''', params)
            conn.commit()
        
        conn.close()
    
    def list_users(self):
        """Listar todos los usuarios"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT username, can_read, can_write, created_at FROM users')
        users = cursor.fetchall()
        conn.close()
        
        return [{'username': u[0], 'can_read': bool(u[1]), 'can_write': bool(u[2]), 'created_at': u[3]} for u in users]
    
    def create_default_users(self):
        """Crear usuarios por defecto"""
        self.create_user('admin', 'password123', can_read=True, can_write=True)
        self.create_user('user', 'artemis2024', can_read=True, can_write=False)
        self.create_user('readonly', 'read123', can_read=True, can_write=False)

if __name__ == '__main__':
    # Ejemplo de uso
    db = UserDB()
    
    print("Usuarios en la base de datos:")
    for user in db.list_users():
        print(f"- {user['username']}: Lectura={user['can_read']}, Escritura={user['can_write']}")
    
    # Probar autenticación
    print("\nPruebas de autenticación:")
    test_users = [('admin', 'password123'), ('user', 'artemis2024'), ('invalid', 'wrong')]
    
    for username, password in test_users:
        perms = db.authenticate(username, password)
        if perms:
            print(f"✓ {username}: Lectura={perms['can_read']}, Escritura={perms['can_write']}")
        else:
            print(f"✗ {username}: Credenciales inválidas")