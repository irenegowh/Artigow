#!/bin/sh

# Espera a que PostgreSQL esté listo para aceptar conexiones
#until PGPASSWORD=$POSTGRES_PASSWORD psql -h db_service -U $POSTGRES_USER -d $POSTGRES_DB -c '\q'; do
# Extraer los valores de la variable DATABASE_URL
export PGPASSWORD=$POSTGRES_PASSWORD

# Si tienes la URL de la base de datos en la variable DATABASE_URL
DB_URL=$DATABASE_URL

# Extraer partes de la URL
DB_HOST=$(echo $DB_URL | sed -e 's/.*\/\/\(.*\):.*/\1/')
DB_PORT=$(echo $DB_URL | sed -e 's/.*:\([0-9]*\)\/.*/\1/')
DB_USER=$(echo $DB_URL | sed -e 's/.*\/\/\(.*\):.*/\1/' | sed -e 's/:.*//')
DB_NAME=$(echo $DB_URL | sed -e 's/.*\/\(.*\)/\1/')

# Espera a que PostgreSQL esté listo para aceptar conexiones
until psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -p "$DB_PORT" -c '\q'; do
  echo "Esperando a que la base de datos esté lista..."
  sleep 2
done

echo "Base de datos lista, iniciando la aplicación..."
