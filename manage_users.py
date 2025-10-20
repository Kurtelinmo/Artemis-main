#!/usr/bin/env python3
import sys
from user_db import UserDB

def show_help():
    print("""
Administrador de Usuarios TCL Web Scanner

Comandos:
  list                          - Listar todos los usuarios
  add <user> <pass> [r] [w]    - Crear usuario (r=lectura, w=escritura)
  perms <user> [r] [w]         - Cambiar permisos (r=lectura, w=escritura)
  test <user> <pass>           - Probar autenticación

Ejemplos:
  python3 manage_users.py add juan pass123 1 0    # Usuario solo lectura
  python3 manage_users.py add admin admin123 1 1  # Usuario admin completo
  python3 manage_users.py perms juan 1 1          # Dar permisos de escritura
  python3 manage_users.py test juan pass123       # Probar login
""")

def main():
    if len(sys.argv) < 2:
        show_help()
        return
    
    db = UserDB()
    command = sys.argv[1]
    
    if command == 'list':
        users = db.list_users()
        print(f"{'Usuario':<15} {'Lectura':<8} {'Escritura':<10} {'Creado'}")
        print("-" * 50)
        for user in users:
            print(f"{user['username']:<15} {'Sí' if user['can_read'] else 'No':<8} {'Sí' if user['can_write'] else 'No':<10} {user['created_at']}")
    
    elif command == 'add':
        if len(sys.argv) < 4:
            print("Error: Faltan parámetros. Uso: add <usuario> <contraseña> [lectura] [escritura]")
            return
        
        username = sys.argv[2]
        password = sys.argv[3]
        can_read = bool(int(sys.argv[4])) if len(sys.argv) > 4 else True
        can_write = bool(int(sys.argv[5])) if len(sys.argv) > 5 else False
        
        if db.create_user(username, password, can_read, can_write):
            print(f"✓ Usuario '{username}' creado exitosamente")
            print(f"  Lectura: {'Sí' if can_read else 'No'}")
            print(f"  Escritura: {'Sí' if can_write else 'No'}")
        else:
            print(f"✗ Error: El usuario '{username}' ya existe")
    
    elif command == 'perms':
        if len(sys.argv) < 4:
            print("Error: Faltan parámetros. Uso: perms <usuario> <lectura> <escritura>")
            return
        
        username = sys.argv[2]
        can_read = bool(int(sys.argv[3])) if len(sys.argv) > 3 else None
        can_write = bool(int(sys.argv[4])) if len(sys.argv) > 4 else None
        
        db.update_permissions(username, can_read, can_write)
        print(f"✓ Permisos actualizados para '{username}'")
    
    elif command == 'test':
        if len(sys.argv) < 4:
            print("Error: Faltan parámetros. Uso: test <usuario> <contraseña>")
            return
        
        username = sys.argv[2]
        password = sys.argv[3]
        
        perms = db.authenticate(username, password)
        if perms:
            print(f"✓ Autenticación exitosa para '{username}'")
            print(f"  Lectura: {'Sí' if perms['can_read'] else 'No'}")
            print(f"  Escritura: {'Sí' if perms['can_write'] else 'No'}")
        else:
            print(f"✗ Credenciales inválidas para '{username}'")
    
    else:
        print(f"Comando desconocido: {command}")
        show_help()

if __name__ == '__main__':
    main()