from posts_service import create_app
import os

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5004)  # Cambié el puerto a 5002 para este servicio
