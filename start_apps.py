import subprocess
import sys
import time

def start_login_app():
    """Inicia la aplicación de login en puerto 8080"""
    return subprocess.Popen([sys.executable, "login_app.py"])

def start_main_app():
    """Inicia la aplicación principal en puerto 5000"""
    return subprocess.Popen(["./scripts/start_dev"], shell=True)

if __name__ == "__main__":
    print("Iniciando aplicación de login en puerto 8080...")
    login_process = start_login_app()
    
    time.sleep(2)  # Esperar un poco antes de iniciar la app principal
    
    print("Iniciando aplicación principal Artemis en puerto 5000...")
    main_process = start_main_app()
    
    print("\nAplicaciones iniciadas:")
    print("- Login: http://200.229.229.27:8080")
    print("- Artemis: http://200.229.229.27:5000")
    print("\nCredenciales de prueba:")
    print("- admin / password123")
    print("- user / artemis2024")
    print("\nPresiona Ctrl+C para detener ambas aplicaciones")
    
    try:
        # Esperar a que terminen los procesos
        login_process.wait()
        main_process.wait()
    except KeyboardInterrupt:
        print("\nDeteniendo aplicaciones...")
        login_process.terminate()
        main_process.terminate()
        login_process.wait()
        main_process.wait()
        print("Aplicaciones detenidas.")