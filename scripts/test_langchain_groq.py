"""
Script simple para probar LangChain con diferentes modelos Groq
"""

import os
import time
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq

# Lista de modelos compatibles con Groq (puedes añadir más si Groq los soporta)
AVAILABLE_MODELS = [
    "llama3-8b-8192",
    "mixtral-8x7b-32768",
    "gemma-7b-it"
]

def check_groq_key():
    """Verifica si la API key de Groq está configurada"""
    return bool(os.getenv("GROQ_API_KEY"))

def get_models():
    """Devuelve la lista de modelos disponibles"""
    return [{"name": model} for model in AVAILABLE_MODELS]

def generate_text(model, prompt):
    """Genera texto con un modelo específico usando LangChain y Groq"""
    try:
        print(f"🤖 Generando con {model}...")
        start_time = time.time()

        llm = ChatGroq(model_name=model, temperature=0.7)
        response = llm.invoke([HumanMessage(content=prompt)])

        end_time = time.time()
        print(f"✅ Generado en {end_time - start_time:.2f} segundos")
        return response.content
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    print("🔍 Probando LangChain con Groq...\n")

    # Verificar API Key
    if not check_groq_key():
        print("❌ GROQ_API_KEY no está configurada. Exporta tu clave con:")
        print("   export GROQ_API_KEY='tu_api_key'")
        return

    print("✅ API Key detectada!")

    # Obtener modelos disponibles
    models = get_models()
    if not models:
        print("❌ No hay modelos disponibles.")
        return

    print(f"\n📋 Modelos disponibles:")
    for i, model in enumerate(models, 1):
        print(f"  {i}. {model['name']}")

    print("\n¿Quieres probar todos los modelos? (y/n): ")
    choice = input().lower()
    if choice != 'y':
        print("Introduce los números de los modelos a probar (ej: 1, 3): ")
        selected = input().split(',')
        models = [models[int(i)-1] for i in selected if i.strip().isdigit()]

    # Prompts de prueba
    test_prompts = [
        "Escribe un tweet sobre inteligencia artificial",
        "Explica qué es Python en 2 párrafos",
        "Crea un titular para un blog sobre tecnología"
    ]

    print(f"\n🧪 Comparando modelos con diferentes prompts...")

    # Probar cada prompt con todos los modelos
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n{'='*60}")
        print(f"📝 PROMPT {i}: {prompt}")
        print(f"{'='*60}")

        for model in models:
            model_name = model['name']
            print(f"\n🎯 Modelo: {model_name}")
            print("-" * 40)

            result = generate_text(model_name, prompt)
            if result:
                print(f"🤖 Respuesta:\n{result}")
            else:
                print("❌ Error generando respuesta")

            print("-" * 40)

if __name__ == "__main__":
    main()
