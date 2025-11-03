#!/bin/bash

# Script para crear el repositorio en GitHub usando GitHub CLI
# Asegúrate de tener gh CLI instalado y autenticado

echo "🚀 Creando repositorio AWS SES API en GitHub..."

# Verificar si gh está instalado
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) no está instalado."
    echo "📦 Instalar con: sudo apt install gh"
    echo "🔑 Autenticar con: gh auth login"
    exit 1
fi

# Verificar si está autenticado
if ! gh auth status &> /dev/null; then
    echo "🔑 No estás autenticado. Ejecuta: gh auth login"
    exit 1
fi

# Crear el repositorio en GitHub
echo "📚 Creando repositorio..."
gh repo create aws-ses-api \
    --description "FastAPI backend para AWS SES v2 con firma automática - Listo para Coolify" \
    --public \
    --clone=false

# Agregar el remote
echo "🔗 Agregando remote origin..."
git remote add origin https://github.com/iaisep/aws-ses-api.git

# Push del código
echo "📤 Subiendo código..."
git push -u origin main

echo "✅ Repositorio creado exitosamente!"
echo "🌐 URL: https://github.com/iaisep/aws-ses-api"
echo ""
echo "🚀 Próximos pasos para Coolify:"
echo "1. Ve a tu panel de Coolify"
echo "2. Crear nuevo servicio > Git Repository"
echo "3. Conectar: https://github.com/iaisep/aws-ses-api"
echo "4. Configurar como 'Docker Application'"
echo "5. Puerto: 8000"
echo "6. Deploy!"