from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

VALID_CREDENTIALS = {
    "admin": "password123",
    "user": "artemis2024"
}

LOGIN_HTML = '''
<!DOCTYPE html>
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
                        {% if error %}
                        <div class="alert alert-danger">{{ error }}</div>
                        {% endif %}
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
</html>
'''

@app.route('/')
def login_form():
    return render_template_string(LOGIN_HTML)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username in VALID_CREDENTIALS and VALID_CREDENTIALS[username] == password:
        return redirect('http://200.229.229.27:5000')
    else:
        return render_template_string(LOGIN_HTML, error='Credenciales inválidas')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)