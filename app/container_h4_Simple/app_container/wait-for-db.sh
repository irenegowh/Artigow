#!/bin/sh

# Espera a que PostgreSQL esté listo para aceptar conexiones
#until PGPASSWORD=$POSTGRES_PASSWORD psql -h db_service -U $POSTGRES_USER -d $POSTGRES_DB -c '\q'; do
# Extraer los valores de la variable DATABASE_URL
#!/bin/sh

# Extraer los valores de la variable DATABASE_URL
export PGPASSWORD=$DB_PASSWORD  # Se usa para la conexión de psql

# Espera a que PostgreSQL esté listo para aceptar conexiones
until psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -p "$DB_PORT" -c '\q'; do
  echo "Esperando a que la base de datos esté lista..."
  sleep 2
done

echo "Base de datos lista, iniciando la aplicación..."
