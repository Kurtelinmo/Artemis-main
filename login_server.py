#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import os
import mimetypes

class LoginHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/imagen.png':
            # Servir la imagen
            import os
            image_path = os.path.join('extras', 'imagen (3).png')
            try:
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as f:
                        self.send_response(200)
                        self.send_header('Content-Type', 'image/png')
                        self.send_header('Cache-Control', 'no-cache')
                        self.end_headers()
                        self.wfile.write(f.read())
                else:
                    print(f'Imagen no encontrada en: {os.path.abspath(image_path)}')
                    self.send_error(404)
            except Exception as e:
                print(f'Error sirviendo imagen: {e}')
                self.send_error(500)
        elif self.path == '/debug':
            # Debug: mostrar archivos disponibles
            import os
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            files = []
            if os.path.exists('extras'):
                files = os.listdir('extras')
            debug_html = f'<h1>Debug</h1><p>Directorio actual: {os.getcwd()}</p><p>Archivos en extras/: {files}</p>'
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
        
        valid_users = {'admin': 'password123', 'user': 'artemis2024'}
        
        if username in valid_users and valid_users[username] == password:
            self.send_response(302)
            self.send_header('Location', 'http://200.229.229.27:5000')
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
    server = HTTPServer(('0.0.0.0', 8080), LoginHandler)
    print('Servidor de login iniciado en puerto 8080')
    print('URL: http://200.229.229.27:8080')
    server.serve_forever()