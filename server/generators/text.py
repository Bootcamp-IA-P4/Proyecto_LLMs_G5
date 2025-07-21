from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from server.config import LLM_MODEL, OLLAMA_BASE_URL
from server.prompts.twitter import twitter_prompt
from server.prompts.blog import blog_prompt
from server.prompts.instagram import instagram_prompt
from server.prompts.linkedin import linkedin_prompt
from server.prompts.facebook import facebook_prompt
from server.prompts.tiktok import tiktok_prompt
from server.prompts.youtube import youtube_prompt
from server.prompts.threads import threads_prompt
from server.prompts.snapchat import snapchat_prompt
from server.prompts.pinterest import pinterest_prompt
from server.prompts.reddit import reddit_prompt
from server.prompts.telegram import telegram_prompt
from server.prompts.whatsapp import whatsapp_prompt
from server.prompts.bluesky import bluesky_prompt
from server.prompts.mastodon import mastodon_prompt
from server.prompts.medium import medium_prompt
from server.prompts.tumblr import tumblr_prompt
from server.generators.image import generate_image_stability
import os
import openai

PROMPT_MAP = {
    "Twitter/X": twitter_prompt,
    "Blog": blog_prompt,
    "Instagram": instagram_prompt,
    "LinkedIn": linkedin_prompt,
    "Facebook": facebook_prompt,
    "TikTok": tiktok_prompt,
    "YouTube": youtube_prompt,
    "Threads": threads_prompt,
    "Snapchat": snapchat_prompt,
    "Pinterest": pinterest_prompt,
    "Reddit": reddit_prompt,
    "Telegram": telegram_prompt,
    "WhatsApp Channels": whatsapp_prompt,
    "Bluesky": bluesky_prompt,
    "Mastodon": mastodon_prompt,
    "Medium": medium_prompt,
    "Tumblr": tumblr_prompt,
}

def generate_content(tema: str, plataforma: str, audiencia: str, tono: str, llm_provider: str):
    prompt = PROMPT_MAP[plataforma]
    # Generar texto con el motor seleccionado (local o cloud)
    if llm_provider == "Ollama (local)":
        model = os.getenv("LLM_MODEL", "gemma:2b")
        chain = LLMChain(prompt=prompt, llm=Ollama(model=model, base_url=os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")))
        texto = chain.run({"tema": tema, "audiencia": audiencia, "tono": tono})
    elif llm_provider == "Groq API (cloud)":
        model = os.getenv("GROQ_MODEL", "llama-3-70b-8192")
        openai.api_key = os.getenv("GROQ_API_KEY")
        openai.api_base = "https://api.groq.com/openai/v1"
        prompt_str = prompt.format(tema=tema, audiencia=audiencia, tono=tono)
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt_str}]
        )
        texto = response.choices[0].message.content
    else:
        raise ValueError("Proveedor LLM no soportado")

    # Generar imagen
    imagen_bytes = generate_image_stability(tema, plataforma, audiencia, tono)
    if plataforma == "Instagram":
        return imagen_bytes, texto
    else:
        return texto, imagen_bytes
