#!/bin/sh

# Espera a que PostgreSQL esté listo para aceptar conexiones
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$DB_HOST" -U $POSTGRES_USER -d $POSTGRES_DB -c '\q'; do
  echo "Esperando a que la base de datos esté lista..."
  sleep 2
done

echo "Base de datos lista, iniciando la aplicación..."
