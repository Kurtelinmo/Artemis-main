#!/usr/bin/env python3
import http.server
import socketserver
import urllib.parse
from urllib.parse import parse_qs

VALID_CREDENTIALS = {
    "admin": "password123",
    "user": "artemis2024"
}

LOGIN_HTML = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Artemis - Login</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .login-container { min-height: 100vh; }
        .card { border: none; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
        .btn-primary { background: linear-gradient(45deg, #667eea, #764ba2); border: none; }
    </style>
</head>
<body>
    <div class="container-fluid login-container d-flex align-items-center justify-content-center">
        <div class="row w-100">
            <div class="col-md-4 mx-auto">
                <div class="card">
                    <div class="card-body p-5">
                        <div class="text-center mb-4">
                            <h2 class="fw-bold text-primary">Artemis Scanner</h2>
                            <p class="text-muted">Ingresa tus credenciales</p>
                        </div>
                        {error}
                        <form method="post" action="/login">
                            <div class="mb-3">
                                <label for="username" class="form-label">Usuario</label>
                                <input type="text" class="form-control" id="username" name="username" required>
                            </div>
                            <div class="mb-3">
                                <label for="password" class="form-label">Contraseña</label>
                                <input type="password" class="form-control" id="password" name="password" required>
                            </div>
                            <button type="submit" class="btn btn-primary w-100 py-2">Iniciar Sesión</button>
                        </form>
                        <div class="mt-3 text-center">
                            <small class="text-muted">
                                Usuarios de prueba: admin/password123 o user/artemis2024
                            </small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>'''

class LoginHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(LOGIN_HTML.format(error='').encode())
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(post_data)
            
            username = form_data.get('username', [''])[0]
            password = form_data.get('password', [''])[0]
            
            if username in VALID_CREDENTIALS and VALID_CREDENTIALS[username] == password:
                self.send_response(302)
                self.send_header('Location', 'http://200.229.229.27:5000')
                self.end_headers()
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                error_msg = '<div class="alert alert-danger">Credenciales inválidas</div>'
                self.wfile.write(LOGIN_HTML.format(error=error_msg).encode())
        else:
            self.send_error(404)

if __name__ == "__main__":
    PORT = 8080
    with socketserver.TCPServer(("", PORT), LoginHandler) as httpd:
        print(f"Servidor de login iniciado en puerto {PORT}")
        print(f"Accede a: http://200.229.229.27:{PORT}")
        print("Credenciales: admin/password123 o user/artemis2024")
        httpd.serve_forever()