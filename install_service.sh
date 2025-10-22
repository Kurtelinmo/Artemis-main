#!/bin/bash

# Script para instalar login_server_db.py como servicio systemd

# Obtener la ruta absoluta del directorio actual
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Crear archivo de servicio con rutas correctas
sudo tee /etc/systemd/system/login-server-db.service > /dev/null <<EOF
[Unit]
Description=Login Server DB Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$SCRIPT_DIR
ExecStart=/usr/bin/python3 $SCRIPT_DIR/login_server_db.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Recargar systemd y habilitar el servicio
sudo systemctl daemon-reload
sudo systemctl enable login-server-db.service
sudo systemctl start login-server-db.service

echo "Servicio instalado y iniciado correctamente"
echo "Para verificar el estado: sudo systemctl status login-server-db.service"
echo "Para ver logs: sudo journalctl -u login-server-db.service -f"