"""
Script simple para probar Ollama con diferentes modelos
"""

import requests
import json
import time

OLLAMA_URL = "http://localhost:11434"

def check_ollama():
    """Verifica si Ollama está corriendo"""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/version", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_models():
    """Obtiene lista de modelos disponibles"""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags")
        if response.status_code == 200:
            return response.json().get("models", [])
        return []
    except:
        return []

def generate_text(model, prompt):
    """Genera texto con un modelo específico"""
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        print(f"🤖 Generando con {model}...")
        start_time = time.time()
        
        response = requests.post(f"{OLLAMA_URL}/api/generate", json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            end_time = time.time()
            
            print(f"✅ Generado en {end_time - start_time:.2f} segundos")
            return result.get("response", "")
        else:
            print(f"❌ Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    print("🔍 Probando Ollama...\n")
    
    # Verificar si Ollama está corriendo
    if not check_ollama():
        print("❌ Ollama no está corriendo. Ejecuta 'ollama serve' primero.")
        return
    
    print("✅ Ollama está corriendo!")
    
    # Obtener modelos disponibles
    models = get_models()
    if not models:
        print("❌ No hay modelos disponibles. Descarga uno con 'ollama pull llama3.2:3b'")
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