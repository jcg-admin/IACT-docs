#!/bin/bash

echo "========================================="
echo "POSTGRESQL DATA DIRECTORY DIAGNOSTICO"
echo "========================================="
echo ""

echo "1. Estado del cluster:"
sudo pg_lsclusters
echo ""

echo "2. Contenido del data directory:"
sudo -u postgres ls -la /var/lib/postgresql/16/main/ | head -20
echo ""

echo "3. Permisos del data directory:"
stat /var/lib/postgresql/16/main/ | grep -E "Access:|Uid:"
echo ""

echo "4. Archivo PG_VERSION:"
if sudo -u postgres test -f /var/lib/postgresql/16/main/PG_VERSION; then
    echo "Existe: SI"
    sudo -u postgres cat /var/lib/postgresql/16/main/PG_VERSION
else
    echo "Existe: NO (PROBLEMA)"
fi
echo ""

echo "5. Configuracion listen_addresses:"
sudo grep "^listen_addresses" /etc/postgresql/16/main/postgresql.conf || echo "No configurado"
echo ""

echo "6. Log de PostgreSQL (ultimas 30 lineas):"
sudo tail -30 /var/log/postgresql/postgresql-16-main.log
echo ""

echo "7. Estado systemd:"
sudo systemctl status postgresql@16-main --no-pager
echo ""

echo "8. Intentar iniciar manualmente:"
sudo -u postgres /usr/lib/postgresql/16/bin/pg_ctl status -D /var/lib/postgresql/16/main
echo ""
