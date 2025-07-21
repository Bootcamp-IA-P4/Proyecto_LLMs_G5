from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
dotenv_path = os.path.join(project_root, ".env")

load_dotenv(dotenv_path=dotenv_path)


try:  
    from server.prompts.prompts import PROMPTS
except ImportError:
    print("No se encontró el archivo, usaremos el prompt por defecto")
    PROMPTS = {"default": "Write  {topic}"}



def generate_text(topic: str, platform: str, model_name: str = "llama3-8b-8192", voice: str = "a neutral and informative assistant", company_info: str = "", language: str = "en") -> str:
    print(f"Generating text for '{platform}' with the model '{model_name}'" )
    LANG_MAP = {
    "es" : "Spanish",
    "en" : "English",
    "fr" : "French",
    "it" : "Italian"
    }

    language_full = LANG_MAP.get(language.lower(), "English")
    try:
        llm = ChatGroq(model=model_name, temperature=0.7)
        prompt_template_string = PROMPTS.get(platform.lower(), PROMPTS["default"])
        prompt_template = ChatPromptTemplate.from_template(prompt_template_string)
        chain = prompt_template | llm
        response = chain.invoke({"topic": topic, "voice": voice, "company_info": company_info, "language": language_full})
        print("Generated text:")
        return response.content
    except Exception as e:
        print(f"Error generating text: {e}")
        return "Error generating text" 

