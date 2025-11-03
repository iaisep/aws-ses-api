# AWS SES v2 API

FastAPI backend para envío de emails usando AWS SES v2 con firma automática.

## 🚀 Características

- ✅ **Firma automática de AWS**: Maneja toda la complejidad de la autenticación AWS
- ✅ **API REST simple**: Endpoints fáciles de usar
- ✅ **Soporte completo de SES v2**: Todas las funciones de AWS SES v2
- ✅ **Validación robusta**: Validación de emails y datos usando Pydantic
- ✅ **Manejo de errores**: Respuestas claras y detalladas de errores
- ✅ **Documentación automática**: Swagger UI en `/docs`
- ✅ **Docker Ready**: Containerizado y listo para producción
- ✅ **CORS configurado**: Listo para uso desde frontend

## 📋 Requisitos

- Python 3.11+
- Docker (opcional)
- Credenciales AWS con permisos de SES

## 🛠️ Instalación Local

### Opción 1: Con Docker (Recomendado)

```bash
# Clonar el repositorio
git clone <repository-url>
cd aws-ses-api

# Construir la imagen
docker build -t aws-ses-api .

# Ejecutar el contenedor
docker run -p 3000:3000 aws-ses-api
```

### Opción 2: Python Virtual Environment

```bash
# Crear ambiente virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python main.py
```

## 🔗 Endpoints

### `GET /`
Endpoint de salud básico

### `GET /health`
Verificación de salud del servicio

### `POST /send-email`
Envío completo de email con todas las opciones

**Ejemplo de request:**
```json
{
  "credentials": {
    "access_key": "AKIA...",
    "secret_key": "...",
    "region": "us-east-1"
  },
  "from_email": "sender@example.com",
  "destination": {
    "to_addresses": ["recipient@example.com"],
    "cc_addresses": ["cc@example.com"],
    "bcc_addresses": ["bcc@example.com"]
  },
  "content": {
    "subject": "Test Subject",
    "text_body": "Plain text content",
    "html_body": "<h1>HTML content</h1>",
    "charset": "UTF-8"
  },
  "configuration_set": "my-config-set",
  "tags": {
    "Environment": "Production",
    "Campaign": "Newsletter"
  }
}
```

### `POST /send-simple-email`
Envío simplificado para casos básicos

**Parámetros:**
- `access_key`: AWS Access Key
- `secret_key`: AWS Secret Key
- `region`: AWS Region
- `from_email`: Email del remitente
- `to_email`: Email del destinatario
- `subject`: Asunto del email
- `message`: Contenido en texto plano
- `html_message`: (Opcional) Contenido en HTML

## 📚 Documentación API

Una vez ejecutando la aplicación, visita:
- **Swagger UI**: `http://localhost:3000/docs`
- **ReDoc**: `http://localhost:3000/redoc`

## 🔐 Configuración AWS

### Permisos requeridos en IAM:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ses:SendEmail",
                "ses:SendRawEmail",
                "ses:GetSendQuota",
                "ses:GetSendStatistics"
            ],
            "Resource": "*"
        }
    ]
}
```

### Dominios verificados:
Asegúrate de que tu dominio esté verificado en AWS SES.

## 🚀 Deployment en Coolify

1. **Crear nuevo proyecto en Coolify**
2. **Conectar repositorio de GitHub**
3. **Configurar como Docker Application**
4. **Configurar variables de entorno** (si usas `.env`)
5. **Deploy automático**

### Variables de entorno para Coolify:

```env
PORT=3000
HOST=0.0.0.0
LOG_LEVEL=INFO
```

## 🧪 Testing

### Prueba rápida con curl:

```bash
curl -X POST "http://localhost:3000/send-simple-email" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "access_key=YOUR_ACCESS_KEY" \
  -d "secret_key=YOUR_SECRET_KEY" \
  -d "region=us-east-1" \
  -d "from_email=sender@example.com" \
  -d "to_email=recipient@example.com" \
  -d "subject=Test Email" \
  -d "message=Hello from AWS SES API!"
```

### Prueba con n8n:

```javascript
// En un nodo HTTP Request de n8n
{
  "method": "POST",
  "url": "http://your-api-domain.com/send-simple-email",
  "headers": {
    "Content-Type": "application/x-www-form-urlencoded"
  },
  "body": {
    "access_key": "{{ $credentials.aws.accessKeyId }}",
    "secret_key": "{{ $credentials.aws.secretAccessKey }}",
    "region": "us-east-1",
    "from_email": "noreply@universidadisep.com",
    "to_email": "{{ $json.email }}",
    "subject": "{{ $json.subject }}",
    "message": "{{ $json.content }}",
    "html_message": "{{ $json.htmlContent }}"
  }
}
```

## 🔧 Configuración Avanzada

### Limits y timeouts:
```python
# En main.py puedes configurar:
MAX_EMAIL_SIZE = 10 * 1024 * 1024  # 10MB
MAX_RECIPIENTS = 50
REQUEST_TIMEOUT = 30  # segundos
```

### CORS personalizado:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://workflow.universidadisep.com"],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
```

## 📊 Monitoring

La aplicación incluye logs estructurados que puedes monitorear:

```bash
# Ver logs en tiempo real
docker logs -f container-name

# Buscar errores
docker logs container-name | grep ERROR
```

## 🛡️ Seguridad

- ✅ Usuario no-root en Docker
- ✅ Validación de entrada con Pydantic
- ✅ Manejo seguro de credenciales (no se almacenan)
- ✅ Logs que no exponen credenciales
- ✅ CORS configurado apropiadamente

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

MIT License

## 🆘 Soporte

Para problemas o preguntas:
- Crea un issue en GitHub
- Revisa los logs de la aplicación
- Verifica la configuración de AWS SES