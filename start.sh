#!/bin/bash

# Script de inicio para desarrollo local

echo "🚀 Iniciando AWS SES API..."

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements.txt

# Verificar si existe .env
if [ ! -f ".env" ]; then
    echo "⚙️ Creando archivo .env desde .env.example..."
    cp .env.example .env
    echo "🔔 Recuerda configurar tus variables en .env"
fi

# Ejecutar la aplicación
echo "🌟 Iniciando FastAPI..."
python main.py