#!/bin/bash

echo "Instalando servicio TCL Login..."

# Copiar archivo de servicio
sudo cp tcl-login.service /etc/systemd/system/

# Recargar systemd
sudo systemctl daemon-reload

# Habilitar el servicio para que inicie con el sistema
sudo systemctl enable tcl-login.service

# Iniciar el servicio
sudo systemctl start tcl-login.service

# Verificar estado
sudo systemctl status tcl-login.service

echo ""
echo "Servicio instalado. Comandos útiles:"
echo "- Ver estado: sudo systemctl status tcl-login"
echo "- Iniciar: sudo systemctl start tcl-login"
echo "- Detener: sudo systemctl stop tcl-login"
echo "- Reiniciar: sudo systemctl restart tcl-login"
echo "- Ver logs: sudo journalctl -u tcl-login -f"