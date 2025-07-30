# ContentGenius AI 🧠

Plataforma web para la generación automática de contenido para redes sociales y divulgación científica utilizando **modelos de lenguaje grande (LLMs)** y técnicas de **Retrieval-Augmented Generation (RAG)**.

---

## Características principales ✨

### Generación de contenido para redes sociales 📱

* **Plataformas soportadas**: LinkedIn 👔, Twitter 🐦, Instagram 📸, Blog 📝
* **Personalización avanzada**: Audiencias (juvenil 🧑‍🎓, general 👥, técnica 🧑‍💻) e idiomas (español 🇪🇸, inglés 🇬🇧, francés 🇫🇷)
* **Modelos LLM**: Integración con Groq (llama3-8b-8192, gemma2-9b-it) 🚀
* **Generación de imágenes**: Integración con la Inference API de Hugging Face 🖼️, utilizando el modelo de alta calidad `black-forest-labs/FLUX.1-dev` para la creación de contenido visual.
* **RAG para redes sociales**: Contenido enriquecido con fuentes científicas para mayor precisión 🔬

### Sistema de divulgación científica con RAG 📚

* **Fuentes académicas**: Búsqueda automática en ArXiv 📖
* **Procesamiento inteligente**: Embeddings con HuggingFace y búsqueda semántica con ChromaDB Cloud 🧠
* **Doble flujo RAG**: Sistema científico tradicional y RAG social para contenido adaptado a redes 🔄
* **Contenido riguroso**: Generación basada en documentos científicos reales ✅
* **Metadatos detallados**: Información completa de fuentes y relevancia 📑
* **Almacenamiento persistente**: ChromaDB Cloud para gestión escalable de vectores ☁️

### Postprocesado de Imágenes para Web 🌐

* **Redimensionamiento Automático**: Tras la generación, las imágenes son procesadas automáticamente para optimizar su visualización en la web. 📏
* **Persistencia Dual**: Se guardan dos versiones de cada imagen:
    * La original (`_orig.png`) para preservar la máxima calidad. ✨
    * Una versión redimensionada a 768px de ancho (`_w768.png`), que ofrece un equilibrio perfecto entre nitidez y velocidad de carga. ⚡
* **Visualización Responsive**: Gracias al CSS, la imagen redimensionada se adapta fluidamente al 100% del ancho del contenedor de texto, garantizando una experiencia de usuario consistente en cualquier dispositivo (móvil o escritorio). 📱💻

### Backend robusto 💪

* **Autenticación segura**: JWT con bcrypt para hashing de contraseñas 🔐
* **API RESTful**: Endpoints organizados y documentados 🔗
* **Base de datos**: Supabase con esquemas optimizados 🗄️
* **Almacenamiento**: Cloudinary para gestión de imágenes 🏞️
* **Monitoreo**: Integración con LangSmith para logs y trazabilidad 📈

---

## ️ Tecnologías utilizadas 🛠️

### Backend 🖥️

* **FastAPI**: Framework web moderno y rápido ⚡
* **LangChain**: Orquestación de LLMs y RAG 🦜
* **Groq**: Inferencia de modelos de lenguaje 🚀
* **Supabase**: Base de datos PostgreSQL como servicio 🟩
* **Cloudinary**: Almacenamiento y optimización de imágenes ☁️
* **ChromaDB Cloud**: Vector database persistente para búsqueda semántica 🌈
* **HuggingFace**: Modelos de embeddings 🤗
* **Pillow (PIL)**: Librería para el procesamiento y manipulación de imágenes. 🖼️
* **Docker**: Containerización para despliegue simplificado 🐳

### Frontend 🌐

* **HTML5/CSS3/JavaScript**: Interfaz web responsiva 🎨
* **Jinja2**: Motor de plantillas 📝
* **FastAPI StaticFiles**: Servido de archivos estáticos 📁

### Integraciones 🤝

* **ArXiv API**: Acceso a documentos científicos 📄
* **Hugging Face Inference API**: Generación de imágenes con el modelo `black-forest-labs/FLUX.1-dev`. 📸
* **ChromaDB Cloud**: Almacenamiento persistente de vectores 💾
* **LangSmith**: Monitoreo y logging 📊

## 📁 Estructura del proyecto

```
PROYECTO_LLMS_05/
├── client/                                   # Contiene todos los archivos del frontend de la aplicación.
│   ├── static/                               # Archivos estáticos como CSS, JS e imágenes.
│   │   ├── css/                              # Hojas de estilo CSS.
│   │   │   └── styles.css                    # Hoja de estilos principal de la aplicación.
│   │   ├── generated_images/                 # Imágenes generadas por la IA.
│   │   │   ├── image_20250730193409_orig.png # Imagen original generada por el modelo.
│   │   │   └── image_20250730193409_w768.png # Versión redimensionada y optimizada de la imagen para la web.
│   │   ├── img/                              # Imágenes de la interfaz de usuario, como logos.
│   │   │   ├── logo-1.png                    # Logo principal de la aplicación.
│   │   │   └── logo-cgai.png                 # Otro logo o variante del logo.
│   │   └── js/                               # Archivos JavaScript para la interactividad del frontend.
│   │       └── main.js                       # Lógica JavaScript principal del frontend.
│   └── templates/                            # Plantillas HTML que el servidor renderiza.
│       ├── index.html                        # Página de inicio.
│       ├── login.html                        # Página de inicio de sesión.
│       ├── register.html                     # Página de registro.
│       └── science.html                      # Página relacionada con el contenido científico.
│
├── server/                                   # Contiene todos los archivos del backend de la aplicación.
│   ├── chroma_db/                            # Módulo para la base de datos vectorial ChromaDB.
│   │   └── connection_db.py                  # Script para manejar la conexión con ChromaDB.
│   ├── config/                               # Archivos de configuración del servidor.
│   │   └── settings.py                       # Carga y gestiona las variables de entorno y configuraciones.
│   ├── generators/                           # Módulos para la generación de contenido (texto, imágenes).
│   │   ├── image.py                          # Lógica para generar imágenes con la API de Hugging Face.
│   │   └── text.py                           # Lógica para generar texto con los modelos de Groq.
│   ├── models/                               # Definiciones de los modelos de datos de la aplicación.
│   │   ├── post.py                           # Modelo de datos para publicaciones/posts.
│   │   ├── science.py                        # Modelo de datos para contenido científico.
│   │   └── user.py                           # Modelo de datos para usuarios.
│   ├── prompts/                              # Almacena los prompts utilizados por los modelos de IA.
│   │   ├── prompts.py                        # Colección de prompts generales.
│   │   └── prompts_rag.py                    # Prompts específicos para el sistema RAG.
│   ├── RAG/                                  # Módulos relacionados con la Generación Aumentada por Recuperación.
│   │   ├── arxiv_processor.py                # Script para procesar y descargar artículos de ArXiv.
│   │   ├── rag_chain.py                      # Implementación de la cadena LangChain para RAG.
│   │   └── vector_db.py                      # Gestión de la base de datos vectorial para embeddings.
│   ├── routes/                               # Definición de las rutas (endpoints) de la API.
│   │   ├── auth.py                           # Rutas relacionadas con la autenticación de usuarios.
│   │   ├── content.py                        # Rutas para la gestión de contenido general.
│   │   └── science.py                        # Rutas específicas para el contenido científico.
│   ├── services/                             # Lógica de negocio de la aplicación.
│   │   ├── auth_service.py                   # Lógica para la autenticación de usuarios.
│   │   ├── content_service.py                # Lógica para la gestión y procesamiento de contenido.
│   │   └── science_service.py                # Lógica para las operaciones relacionadas con el contenido científico.
│   ├── utils/                                # Funciones de utilidad y herramientas auxiliares.
│   │   ├── cloudinary.py                     # Utilidades para la integración con Cloudinary.
│   │   ├── database.py                       # Conexión y operaciones con la base de datos principal (Supabase).
│   │   ├── dependencies.py                   # Funciones para la inyección de dependencias de FastAPI (ej. autenticación).
│   │   └── image_processor.py                # Función para redimensionar y optimizar imágenes.
│   ├── Dockerfile                            # Instrucciones para construir la imagen Docker del servidor.
│   └── main.py                               # Punto de entrada principal de la aplicación FastAPI.
│
├── docker-compose.yml                        # Define y orquesta los servicios Docker de la aplicación.
├── README.md                                 # Documentación principal del proyecto.
└── requirements.txt                          # Lista las dependencias de Python del proyecto.
```

## Instalación y Configuración 🚀

### Prerrequisitos ✨

  * **Docker** y **Docker Compose** (recomendado) o **Python 3.8+**
  * Cuentas en **Supabase**, **Groq**, **Cloudinary**, **ChromaDB Cloud** y **Hugging Face**.

-----

### Opción 1: Despliegue con Docker (Recomendado) 🐳

1.  Clonar el repositorio 📂

    ```bash
    git clone <repository-url>
    cd PROYECTO_LLMS_05
    ```

2.  Configurar variables de entorno 🔑

    Copiar `.env.example` a `.env` y completar:

    ```python
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

    # Image Generation (Hugging Face)
    HF_TOKEN=your_hugging_face_api_token_here

    # Coudinary
    CLOUDINARY_CLOUD_NAME=your_cloudinary_cloud_name_here
    CLOUDINARY_API_KEY=your_cloudinary_api_key_here
    CLOUDINARY_API_SECRET=your_cloudinary_api_secret_here

    # Chroma
    CHROMA_API_KEY='your_chroma_api_key_here'
    CHROMA_TENANT='your_chroma_tenant_here'
    CHROMA_DATABASE='your_chroma_database_here'
    ```

3.  Construir y ejecutar ▶️

    Para asegurar una reconstrucción limpia, se recomienda detener y eliminar los volúmenes antiguos antes de levantar los servicios.

    ```bash
    # Detener y eliminar contenedores, redes y volúmenes existentes
    docker-compose down -v

    # Construir las imágenes y levantar los servicios
    docker-compose up --build
    ```

    La aplicación estará disponible en `http://localhost:8000` 🌐

-----

### Opción 2: Instalación tradicional 💻

1.  Clonar el repositorio 📂

    ```bash
    git clone <repository-url>
    cd PROYECTO_LLMS_05
    ```

2.  Instalar dependencias 📦

    ```bash
    pip install -r requirements.txt
    ```

3.  Configurar variables de entorno 🔑

    (Usar la misma configuración que en la Opción 1)

4.  Ejecutar la aplicación 🚀

    ```bash
    uvicorn server.main:app --reload
    ```

-----

## Configurar base de datos en Supabase 📊

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

-----

## Uso de la API 🔌

### Autenticación 🔒

```http
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

### Generación de contenido ✍️

```http
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

-----

## Colaboradores 🤝

  * Orlando Alcalá
  * Andrea Alonso
  * Nhoeli Salazar
  * Juan Domingo

-----

## Contribuciones 💡

Las contribuciones son bienvenidas. Por favor:

1.  **Fork** el proyecto 🍴
2.  Crear una rama para tu feature (`git checkout -b feature/nueva-caracteristica`) 🌱
3.  **Commit** tus cambios (`git commit -m 'Agregar nueva característica'`) 💾
4.  **Push** a la rama (`git push origin feature/nueva-caracteristica`) ⬆️
5.  Abrir un **Pull Request** 📬
