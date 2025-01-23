# app/main.py
from flask import Blueprint, render_template
import os
from flask import Flask
from app.models import Post, Vote
from flask import render_template
import logging

# Definir blueprint para la página principal
main_bp = Blueprint('main', __name__)

# Configuración básica de logging
logger = logging.getLogger("app_logger")

@main_bp.route('/')
def welcome():
    try:
        logger.info("Accediendo a la página principal (bienvenida).")
        return render_template('bienvenida.html')
    except Exception as e:
        logger.error(f"Error al cargar la página de bienvenida: {e}")
        flash('Hubo un error al cargar la página principal, por favor inténtalo de nuevo.', 'danger')
        return render_template('error.html')  # Podrías tener una página de error personalizada