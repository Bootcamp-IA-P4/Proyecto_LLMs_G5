from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from server.config import LLM_MODEL
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

llm = Ollama(model=LLM_MODEL, num_ctx=2048)

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

def generate_content(tema: str, plataforma: str, audiencia: str, tono: str):
    prompt = PROMPT_MAP[plataforma]
    chain = LLMChain(prompt=prompt, llm=llm)
    texto = chain.run({
        "tema": tema,
        "audiencia": audiencia,
        "tono": tono
    })
    # Generar la imagen
    imagen_bytes = generate_image_stability(tema, plataforma, audiencia, tono)
    # Lógica para insertar la imagen según la plataforma
    if plataforma == "Instagram":
        return imagen_bytes, texto  # Imagen primero, luego texto
    else:
        return texto, imagen_bytes  # Texto primero, luego imagen
