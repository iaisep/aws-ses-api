# 🚀 Configuración en Coolify - AWS SES API

## ⚡ Resumen Rápido
Esta API maneja **automáticamente la firma AWS** - tú solo envías las credenciales desde n8n y la API se encarga del resto.

## 📋 Pasos para Deploy en Coolify

### 1. Crear Nuevo Servicio
1. En Coolify: **"Create New Resource"** → **"Git Repository"**
2. **Repository URL**: `https://github.com/iaisep/aws-ses-api`
3. **Branch**: `main`
4. **Build Pack**: `Docker`

### 2. Configuración del Servicio
- **Name**: `aws-ses-api`
- **Type**: `Docker Application`
- **Port**: `8000`
- **Domain**: `ses-api.tudominio.com`

### 3. Deploy
1. Click **"Deploy"**
2. Espera el build
3. ¡Listo!

## 🔗 Uso desde n8n

### HTTP Request Node Configuración:
```javascript
// Método: POST
// URL: https://ses-api.tudominio.com/send-simple-email
// Content-Type: application/x-www-form-urlencoded

// Body (Form Data):
{
  "access_key": "TUS_CREDENCIALES_AWS_ACCESS_KEY",
  "secret_key": "TUS_CREDENCIALES_AWS_SECRET_KEY", 
  "region": "us-east-1",
  "from_email": "noreply@tudominio.com",
  "to_email": "{{ $json.email }}",
  "subject": "{{ $json.subject }}",
  "message": "{{ $json.content }}",
  "html_message": "{{ $json.htmlContent }}"
}
```

## 🧪 Prueba rápida
```bash
curl -X POST "https://ses-api.tudominio.com/send-simple-email" \
  -d "access_key=TU_ACCESS_KEY" \
  -d "secret_key=TU_SECRET_KEY" \
  -d "region=us-east-1" \
  -d "from_email=test@tudominio.com" \
  -d "to_email=destino@ejemplo.com" \
  -d "subject=Test API" \
  -d "message=¡API funcionando!"
```

## 🔐 Seguridad
- ✅ **NO** hay credenciales hardcodeadas
- ✅ Las credenciales se pasan dinámicamente desde n8n
- ✅ La API solo maneja la firma AWS automáticamente
- ✅ No se almacenan credenciales (solo en memoria durante la request)

## 📊 Endpoints Disponibles
- `GET /health` - Health check
- `POST /send-email` - Envío completo (JSON)
- `POST /send-simple-email` - Envío simple (Form data)
- `GET /docs` - Documentación Swagger

## 🎯 Beneficios vs n8n directo
- ❌ **Sin error 414** (no más URLs largas)
- ❌ **Sin problemas de firma** (automática)
- ❌ **Sin límites de contenido** (POST body)
- ✅ **Fácil de usar** (solo pasar credenciales)

## 🔧 Variables de Entorno (Opcionales)
```env
LOG_LEVEL=INFO
PORT=8000
ALLOWED_ORIGINS=https://workflow.tudominio.com
```

¡Tu API está lista para resolver el problema 414 de AWS SES desde n8n! 🚀