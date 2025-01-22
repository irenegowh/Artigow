#!/bin/sh

# Espera a que PostgreSQL esté listo para aceptar conexiones
#until PGPASSWORD=$POSTGRES_PASSWORD psql -h db_service -U $POSTGRES_USER -d $POSTGRES_DB -c '\q'; do
# Extraer los valores de la variable DATABASE_URL

# Extraer los valores de las variables de entorno
echo "DB_HOST: $DB_HOST"
echo "DB_USER: $DB_USER"
echo "DB_PASSWORD: $DB_PASSWORD"
echo "DB_NAME: $DB_NAME"
echo "DB_PORT: $DB_PORT"

export PGPASSWORD=$DB_PASSWORD  # Se usa para la conexión de psql

# Espera a que PostgreSQL esté listo para aceptar conexiones
until psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -p "$DB_PORT" -c '\q'; do
  echo "Esperando a que la base de datos esté lista..."
  sleep 2
done

echo "Base de datos lista, iniciando la aplicación..."
