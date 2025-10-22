#!/bin/bash

# Script para desinstalar el servicio login-server-db

sudo systemctl stop login-server-db.service
sudo systemctl disable login-server-db.service
sudo rm /etc/systemd/system/login-server-db.service
sudo systemctl daemon-reload

echo "Servicio desinstalado correctamente"