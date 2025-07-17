from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from server.config import LLM_MODEL
from server.prompts.twitter import twitter_prompt
from server.prompts.blog import blog_prompt
from server.prompts.instagram import instagram_prompt
from server.prompts.linkedin import linkedin_prompt

llm = Ollama(model=LLM_MODEL, num_ctx=2048)

PROMPT_MAP = {
    "Twitter/X": twitter_prompt,
    "Blog": blog_prompt,
    "Instagram": instagram_prompt,
    "LinkedIn": linkedin_prompt,
}

def generate_content(tema: str, plataforma: str, audiencia: str, tono: str) -> str:
    prompt = PROMPT_MAP[plataforma]
    chain = LLMChain(prompt=prompt, llm=llm)
    respuesta = chain.run({
        "tema": tema,
        "audiencia": audiencia,
        "tono": tono
    })
    return respuesta
