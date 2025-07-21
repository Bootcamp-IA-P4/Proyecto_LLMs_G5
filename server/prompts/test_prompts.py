from prompts import PROMPTS

def test_prompt(prompt_key: str, topic: str, persona: str):
    prompt = PROMPTS[prompt_key].format(topic=topic, persona=persona)
    print(f"=== TESTING {prompt_key.upper()} ===")
    print("Prompt completo:\n", prompt)
    print("\nSalida esperada:")
    print("-"*50)
    # Aquí iría la conexión real al LLM (usando Groq/OpenAI)
    # print(generar_texto(prompt))  # Mock para pruebas
    print("<Este sería el texto generado>")
    print("-"*50)

# Ejemplo de prueba
test_prompt(
    prompt_key="linkedin_post",
    topic="remote work productivity",
    persona="HR expert, data-driven tone, for startup founders"
)