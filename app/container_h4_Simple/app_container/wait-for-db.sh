#!/bin/sh

# Espera a que PostgreSQL esté listo para aceptar conexiones
#until PGPASSWORD=$POSTGRES_PASSWORD psql -h db_service -U $POSTGRES_USER -d $POSTGRES_DB -c '\q'; do
# Extraer los valores de la variable DATABASE_URL
#!/bin/sh

# Extraer los valores de la variable DATABASE_URL
export PGPASSWORD=$POSTGRES_PASSWORD  # Se usa para la conexión de psql

# Obtener la URL de la base de datos de la variable de entorno
DB_URL=$DATABASE_URL

# Extraer las partes de la URL
DB_HOST=$(echo $DB_URL | sed -e 's|^postgresql://\([^:]*\):.*|\1|')  # Extrae el host
DB_PORT=$(echo $DB_URL | sed -e 's|^postgresql://.*:\([0-9]*\)/.*|\1|')  # Extrae el puerto
DB_USER=$(echo $DB_URL | sed -e 's|^postgresql://\([^:]*\):.*|\1|')  # Extrae el usuario
DB_NAME=$(echo $DB_URL | sed -e 's|^postgresql://.*@.*\/\(.*\)$|\1|')  # Extrae el nombre de la base de datos

# Espera a que PostgreSQL esté listo para aceptar conexiones
until psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -p "$DB_PORT" -c '\q'; do
  echo "Esperando a que la base de datos esté lista..."
  sleep 2
done

echo "Base de datos lista, iniciando la aplicación..."
