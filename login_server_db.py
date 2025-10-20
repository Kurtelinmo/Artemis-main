#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import json
from user_db import UserDB

class LoginHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.db = UserDB()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        if self.path == '/debug':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            
            users = self.db.list_users()
            debug_html = '<h1>Usuarios en BD</h1><ul>'
            for user in users:
                debug_html += f"<li>{user['username']}: R={user['can_read']}, W={user['can_write']}</li>"
            debug_html += '</ul>'
            self.wfile.write(debug_html.encode('utf-8'))
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html = """<!DOCTYPE html>
<html>
<head>
    <title>TCL Web Scanner Login</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial; background: #f0f0f0; margin: 0; padding: 50px; }
        .login-box { max-width: 400px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        .image-bottom { text-align: center; margin-top: 20px; }
        .image-bottom img { max-width: 200px; height: auto; }
        h2 { text-align: center; color: #333; margin-bottom: 30px; font-size: 32px; font-weight: bold; }
        input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background: #dc3545; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #c82333; }
        .error { color: red; text-align: center; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>TCL Web Scanner</h2>
        <form method="post" action="/">
            <input type="text" name="username" placeholder="Usuario" required>
            <input type="password" name="password" placeholder="Contraseña" required>
            <button type="submit">Iniciar Sesión</button>
        </form>
        <div class="image-bottom">
            <img src="https://logos-world.net/wp-content/uploads/2020/04/Toyota-Logo.png" alt="Toyota">
        </div>
    </div>
</body>
</html>"""
            self.wfile.write(html.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = urllib.parse.parse_qs(post_data)
        
        username = params.get('username', [''])[0]
        password = params.get('password', [''])[0]
        
        # Autenticar con base de datos
        permissions = self.db.authenticate(username, password)
        
        if permissions:
            # Crear URL con permisos como parámetros
            perms_param = f"read={permissions['can_read']}&write={permissions['can_write']}&user={username}"
            redirect_url = f"http://200.229.229.27:5000?{perms_param}"
            
            self.send_response(302)
            self.send_header('Location', redirect_url)
            self.end_headers()
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html = """<!DOCTYPE html>
<html>
<head>
    <title>TCL Web Scanner Login</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial; background: #f0f0f0; margin: 0; padding: 50px; }
        .login-box { max-width: 400px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        .image-bottom { text-align: center; margin-top: 20px; }
        .image-bottom img { max-width: 200px; height: auto; }
        h2 { text-align: center; color: #333; margin-bottom: 30px; font-size: 32px; font-weight: bold; }
        input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background: #dc3545; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #c82333; }
        .error { color: red; text-align: center; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>TCL Web Scanner</h2>
        <div class="error">Credenciales incorrectas</div>
        <form method="post" action="/">
            <input type="text" name="username" placeholder="Usuario" required>
            <input type="password" name="password" placeholder="Contraseña" required>
            <button type="submit">Iniciar Sesión</button>
        </form>
        <div class="image-bottom">
            <img src="https://logos-world.net/wp-content/uploads/2020/04/Toyota-Logo.png" alt="Toyota">
        </div>
    </div>
</body>
</html>"""
            self.wfile.write(html.encode('utf-8'))

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8090), LoginHandler)
    print('Servidor de login con BD iniciado en puerto 8090')
    print('URL: http://200.229.229.27:8090')
    print('Debug: http://200.229.229.27:8090/debug')
    server.serve_forever()