"""
FastAPI Backend para AWS SES v2
Maneja automáticamente la firma de AWS y envío de emails
"""

from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AWS SES v2 API",
    description="API para envío de emails usando AWS SES v2 con firma automática",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class AWSCredentials(BaseModel):
    access_key: str
    secret_key: str
    region: str = "us-east-1"

class EmailDestination(BaseModel):
    to_addresses: List[EmailStr]
    cc_addresses: Optional[List[EmailStr]] = None
    bcc_addresses: Optional[List[EmailStr]] = None

class EmailContent(BaseModel):
    subject: str
    text_body: Optional[str] = None
    html_body: Optional[str] = None
    charset: str = "UTF-8"

class SendEmailRequest(BaseModel):
    credentials: AWSCredentials
    from_email: EmailStr
    destination: EmailDestination
    content: EmailContent
    configuration_set: Optional[str] = None
    tags: Optional[Dict[str, str]] = None

class SendEmailResponse(BaseModel):
    success: bool
    message_id: Optional[str] = None
    error: Optional[str] = None
    timestamp: datetime

@app.get("/")
async def root():
    """Endpoint de salud básico"""
    return {
        "message": "AWS SES v2 API está funcionando",
        "version": "1.0.0",
        "timestamp": datetime.now()
    }

@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud"""
    return {
        "status": "healthy",
        "service": "aws-ses-api",
        "timestamp": datetime.now()
    }

@app.post("/send-email", response_model=SendEmailResponse)
async def send_email(request: SendEmailRequest):
    """
    Envía un email usando AWS SES v2
    
    - **credentials**: Credenciales AWS (access_key, secret_key, region)
    - **from_email**: Dirección de email del remitente
    - **destination**: Destinatarios (to, cc, bcc)
    - **content**: Contenido del email (subject, text_body, html_body)
    - **configuration_set**: (Opcional) Set de configuración de SES
    - **tags**: (Opcional) Tags para el email
    """
    try:
        # Crear cliente SES v2 con las credenciales proporcionadas
        ses_client = boto3.client(
            'sesv2',
            aws_access_key_id=request.credentials.access_key,
            aws_secret_access_key=request.credentials.secret_key,
            region_name=request.credentials.region
        )
        
        # Preparar el contenido del email
        email_content = {}
        
        if request.content.text_body and request.content.html_body:
            # Ambos formatos
            email_content = {
                "Simple": {
                    "Subject": {
                        "Data": request.content.subject,
                        "Charset": request.content.charset
                    },
                    "Body": {
                        "Text": {
                            "Data": request.content.text_body,
                            "Charset": request.content.charset
                        },
                        "Html": {
                            "Data": request.content.html_body,
                            "Charset": request.content.charset
                        }
                    }
                }
            }
        elif request.content.html_body:
            # Solo HTML
            email_content = {
                "Simple": {
                    "Subject": {
                        "Data": request.content.subject,
                        "Charset": request.content.charset
                    },
                    "Body": {
                        "Html": {
                            "Data": request.content.html_body,
                            "Charset": request.content.charset
                        }
                    }
                }
            }
        else:
            # Solo texto o texto por defecto
            text_content = request.content.text_body or "Email enviado desde AWS SES API"
            email_content = {
                "Simple": {
                    "Subject": {
                        "Data": request.content.subject,
                        "Charset": request.content.charset
                    },
                    "Body": {
                        "Text": {
                            "Data": text_content,
                            "Charset": request.content.charset
                        }
                    }
                }
            }
        
        # Preparar destinatarios
        destination = {
            "ToAddresses": request.destination.to_addresses
        }
        
        if request.destination.cc_addresses:
            destination["CcAddresses"] = request.destination.cc_addresses
            
        if request.destination.bcc_addresses:
            destination["BccAddresses"] = request.destination.bcc_addresses
        
        # Preparar parámetros del email
        email_params = {
            "FromEmailAddress": request.from_email,
            "Destination": destination,
            "Content": email_content
        }
        
        # Agregar configuración opcional
        if request.configuration_set:
            email_params["ConfigurationSetName"] = request.configuration_set
            
        if request.tags:
            email_params["EmailTags"] = [
                {"Name": key, "Value": value} 
                for key, value in request.tags.items()
            ]
        
        # Enviar el email
        logger.info(f"Enviando email desde {request.from_email} a {request.destination.to_addresses}")
        
        response = ses_client.send_email(**email_params)
        
        logger.info(f"Email enviado exitosamente. MessageId: {response['MessageId']}")
        
        return SendEmailResponse(
            success=True,
            message_id=response['MessageId'],
            timestamp=datetime.now()
        )
        
    except NoCredentialsError:
        logger.error("Credenciales AWS inválidas")
        raise HTTPException(
            status_code=401,
            detail="Credenciales AWS inválidas"
        )
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        
        logger.error(f"Error de AWS SES: {error_code} - {error_message}")
        
        # Manejar errores específicos de SES
        if error_code == 'MessageRejected':
            raise HTTPException(
                status_code=400,
                detail=f"Mensaje rechazado por SES: {error_message}"
            )
        elif error_code == 'MailFromDomainNotVerified':
            raise HTTPException(
                status_code=400,
                detail="El dominio del remitente no está verificado en SES"
            )
        elif error_code == 'ConfigurationSetDoesNotExist':
            raise HTTPException(
                status_code=400,
                detail="El conjunto de configuración especificado no existe"
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Error de AWS SES: {error_message}"
            )
            
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )

@app.post("/send-simple-email")
async def send_simple_email(
    access_key: str = Form(...),
    secret_key: str = Form(...),
    region: str = Form(...),
    from_email: str = Form(...),
    to_email: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...),
    html_message: Optional[str] = Form(None)
):
    """
    Endpoint simplificado para envío rápido de emails
    """
    try:
        # Log de entrada para debugging
        logger.info(f"Recibida solicitud simple: from={from_email}, to={to_email}, region={region}")
        
        # Validar emails básico
        if "@" not in from_email or "@" not in to_email:
            raise HTTPException(
                status_code=400,
                detail="Los emails deben tener formato válido"
            )
        
        # Crear la solicitud usando el modelo completo
        simple_request = SendEmailRequest(
            credentials=AWSCredentials(
                access_key=access_key,
                secret_key=secret_key,
                region=region
            ),
            from_email=from_email,
            destination=EmailDestination(
                to_addresses=[to_email]
            ),
            content=EmailContent(
                subject=subject,
                text_body=message,
                html_body=html_message
            )
        )
        
        # Usar el endpoint principal
        return await send_email(simple_request)
        
    except HTTPException:
        # Re-raise HTTPExceptions as-is
        raise
    except Exception as e:
        error_msg = str(e) if str(e) else "Error desconocido"
        logger.error(f"Error en send_simple_email: {error_msg}")
        logger.error(f"Tipo de error: {type(e).__name__}")
        raise HTTPException(
            status_code=500,
            detail=f"Error enviando email: {error_msg}"
        )

@app.get("/docs")
async def custom_docs():
    """Redirige a la documentación automática de FastAPI"""
    return {"message": "Documentación disponible en /docs"}

@app.post("/test-endpoint")
async def test_endpoint(
    access_key: str = Form(...),
    secret_key: str = Form(...),
    region: str = Form(...),
    from_email: str = Form(...),
    to_email: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...)
):
    """
    Endpoint de prueba que valida parámetros sin enviar email real
    """
    return {
        "status": "success",
        "message": "Parámetros recibidos correctamente",
        "data": {
            "region": region,
            "from_email": from_email,
            "to_email": to_email,
            "subject": subject,
            "message_length": len(message),
            "access_key_prefix": access_key[:4] + "..." if len(access_key) > 4 else "short"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)