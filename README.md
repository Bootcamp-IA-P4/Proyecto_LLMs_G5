# AI Social Content Generator

Plataforma web para la generación automática de contenido para redes sociales y divulgación científica utilizando modelos de lenguaje grande (LLMs) y técnicas de Retrieval-Augmented Generation (RAG).

## 🚀 Características principales

### Generación de contenido para redes sociales

- **Plataformas soportadas**: LinkedIn, Twitter, Instagram, Blog
- **Personalización avanzada**: Audiencias (juvenil, general, técnica) e idiomas (español, inglés, francés)
- **Modelos LLM**: Integración con Groq (llama3-8b-8192, gemma2-9b-it)
- **Generación de imágenes**: Integración con Stability AI para contenido visual

### Sistema de divulgación científica con RAG

- **Fuentes académicas**: Búsqueda automática en ArXiv
- **Procesamiento inteligente**: Embeddings con HuggingFace y búsqueda semántica con FAISS
- **Contenido riguroso**: Generación basada en documentos científicos reales
- **Metadatos detallados**: Información completa de fuentes y relevancia

### Backend robusto

- **Autenticación segura**: JWT con bcrypt para hashing de contraseñas
- **API RESTful**: Endpoints organizados y documentados
- **Base de datos**: Supabase con esquemas optimizados
- **Almacenamiento**: Cloudinary para gestión de imágenes
- **Monitoreo**: Integración con LangSmith para logs y trazabilidad

## 🛠️ Tecnologías utilizadas

### Backend

- **FastAPI**: Framework web moderno y rápido
- **LangChain**: Orquestación de LLMs y RAG
- **Groq**: Inferencia de modelos de lenguaje
- **Supabase**: Base de datos PostgreSQL como servicio
- **Cloudinary**: Almacenamiento y optimización de imágenes
- **FAISS**: Vector database para búsqueda semántica
- **HuggingFace**: Modelos de embeddings

### Frontend

- **HTML5/CSS3/JavaScript**: Interfaz web responsiva
- **Jinja2**: Motor de plantillas
- **FastAPI StaticFiles**: Servido de archivos estáticos

### Integraciones

- **ArXiv API**: Acceso a documentos científicos
- **Stability AI**: Generación de imágenes
- **LangSmith**: Monitoreo y logging

## 📁 Estructura del proyecto

```
PROYECTO_LLMS_05/
├── client/                      # Frontend (HTML, CSS, JS)
│   ├── static/
│   │   ├── css/
│   │   ├── img/                 # Logos y recursos gráficos
│   │   └── js/
│   └── templates/               # Plantillas HTML
│
├── server/                      # Backend
│   ├── config/settings.py       # Configuración
│   ├── generators/              # Generadores de contenido
│   │   ├── image.py
│   │   └── text.py
│   ├── models/                  # Modelos Pydantic
│   ├── prompts/                 # Plantillas de prompts
│   ├── routes/                  # Endpoints API
│   ├── services/                # Lógica de negocio
│   ├── utils/                   # Utilidades
│   └── main.py                  # Punto de entrada
│
├── .env.example
├── requirements.txt
└── README.md
```

## 🔧 Instalación y configuración

### Prerrequisitos

- Python 3.8+
- pip
- Cuentas en Supabase, Groq, Stability AI y Cloudinary

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd PROYECTO_LLMS_05
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Copiar `.env.example` a `.env` y completar:

```env
# Base de datos
SUPABASE_URL=tu_url_de_supabase
SUPABASE_KEY=tu_key_de_supabase

# Modelos LLM
GROQ_API_KEY=tu_api_key_de_groq

# Generación de imágenes
STABILITY_API_KEY=tu_api_key_de_stability

# Almacenamiento
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret

# Autenticación JWT
SECRET_KEY=tu_secret_key_jwt
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Monitoreo (opcional)
LANGSMITH_API_KEY=tu_api_key_langsmith
```

### 4. Configurar base de datos en Supabase

Crear las siguientes tablas:

```sql
-- Tabla de usuarios
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR UNIQUE NOT NULL,
    password_hash VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabla de posts de redes sociales
CREATE TABLE posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    platform VARCHAR NOT NULL,
    audience VARCHAR NOT NULL,
    language VARCHAR NOT NULL,
    model VARCHAR NOT NULL,
    text_content TEXT NOT NULL,
    image_url VARCHAR,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabla de posts científicos
CREATE TABLE science_posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    topic VARCHAR NOT NULL,
    audience VARCHAR NOT NULL,
    language VARCHAR NOT NULL,
    model VARCHAR NOT NULL,
    max_docs INTEGER NOT NULL,
    text_content TEXT NOT NULL,
    sources JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 5. Ejecutar la aplicación

```bash
uvicorn server.main:app --reload
```

La aplicación estará disponible en `http://localhost:8000`

## 📖 Uso de la API

### Autenticación

```bash
# Registro
POST /api/auth/register
{
    "email": "usuario@email.com",
    "password": "contraseña"
}

# Login
POST /api/auth/login
{
    "email": "usuario@email.com",
    "password": "contraseña"
}
```

### Generación de contenido

```bash
# Contenido para redes sociales
POST /api/content/generate
Authorization: Bearer <token>
{
    "platform": "linkedin",
    "topic": "inteligencia artificial",
    "audience": "técnica",
    "language": "es",
    "model": "llama3-8b-8192",
    "include_image": true,
    "image_prompt": "AI technology concept"
}

# Contenido científico
POST /api/science/generate
Authorization: Bearer <token>
{
    "topic": "machine learning",
    "audience": "general",
    "language": "es",
    "model": "llama3-8b-8192",
    "max_docs": 5
}
```

## 👥 Colaboradores

- **Orlando Alcalá**
- **Andrea Alonso**
- **Nhoeli Salazar**
- **Juan Domingo**

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abrir un Pull Request
