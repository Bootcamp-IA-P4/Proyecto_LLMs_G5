# ContentGenius AI

Plataforma web para la generación automática de contenido para redes sociales y divulgación científica utilizando modelos de lenguaje grande (LLMs) y técnicas de Retrieval-Augmented Generation (RAG).

## 🚀 Características principales

### Generación de contenido para redes sociales

- **Plataformas soportadas**: LinkedIn, Twitter, Instagram, Blog
- **Personalización avanzada**: Audiencias (juvenil, general, técnica) e idiomas (español, inglés, francés)
- **Modelos LLM**: Integración con Groq (llama3-8b-8192, gemma2-9b-it)
- **Generación de imágenes**: Integración con Stability AI para contenido visual
- **RAG para redes sociales**: Contenido enriquecido con fuentes científicas para mayor precisión

### Sistema de divulgación científica con RAG

- **Fuentes académicas**: Búsqueda automática en ArXiv
- **Procesamiento inteligente**: Embeddings con HuggingFace y búsqueda semántica con ChromaDB Cloud
- **Doble flujo RAG**: Sistema científico tradicional y RAG social para contenido adaptado a redes
- **Contenido riguroso**: Generación basada en documentos científicos reales
- **Metadatos detallados**: Información completa de fuentes y relevancia
- **Almacenamiento persistente**: ChromaDB Cloud para gestión escalable de vectores

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
- **ChromaDB Cloud**: Vector database persistente para búsqueda semántica
- **HuggingFace**: Modelos de embeddings
- **Docker**: Containerización para despliegue simplificado

### Frontend

- **HTML5/CSS3/JavaScript**: Interfaz web responsiva
- **Jinja2**: Motor de plantillas
- **FastAPI StaticFiles**: Servido de archivos estáticos

### Integraciones

- **ArXiv API**: Acceso a documentos científicos
- **Stability AI**: Generación de imágenes
- **ChromaDB Cloud**: Almacenamiento persistente de vectores
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
│   ├── chroma_db/               # Configuración de conexión a bbdd vectorial
│   ├── config/settings.py       # Configuración
│   ├── generators/              # Generadores de contenido
│   │   ├── image.py
│   │   └── text.py
│   ├── models/                  # Modelos Pydantic
│   ├── prompts/                 # Plantillas de prompts
│   ├── RAG/                     # Lógica de RAG para redes sociales
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

- Docker y Docker Compose (recomendado) o Python 3.8+
- Cuentas en Supabase, Groq, Stability AI, Cloudinary y ChromaDB Cloud

### Opción 1: Despliegue con Docker (Recomendado)

#### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd PROYECTO_LLMS_05
```

#### 2. Configurar variables de entorno

Copiar `.env.example` a `.env` y completar:

```env
# Supabase Configuration
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_anon_key_here

# JWT Configuration
SECRET_KEY=your_super_secret_jwt_key_change_this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Groq API
GROQ_API_KEY=your_groq_api_key_here

#LANGSMITH
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT="your_langsmith_project_name_here"

#Image
STABILITY_API_KEY=your_stability_api_key_here

# Coudinary
CLOUDINARY_CLOUD_NAME=your_cloudinary_cloud_name_here
CLOUDINARY_API_KEY=your_cloudinary_api_key_here
CLOUDINARY_API_SECRET=your_cloudinary_api_secret_here

# Chroma
CHROMA_API_KEY='your_chroma_api_key_here'
CHROMA_TENANT='your_chroma_tenant_here'
CHROMA_DATABASE='your_chroma_database_here'
```

#### 3. Construir y ejecutar

```bash
docker-compose up --build
```

La aplicación estará disponible en `http://localhost:8000`

### Opción 2: Instalación tradicional

#### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd PROYECTO_LLMS_05
```

#### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

#### 3. Configurar variables de entorno

(Usar la misma configuración que en la Opción 1)

#### 4. Ejecutar la aplicación

```bash
uvicorn server.main:app --reload
```

### Configurar base de datos en Supabase

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

# Explicaciones científicas para RRSS
POST /api/explain
Authorization: Bearer <token>
{
    "topic": "quantum computing",
    "platform": "linkedin",
    "audience": "técnica",
    "language": "es"
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
