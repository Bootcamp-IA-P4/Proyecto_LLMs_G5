    prompt1 = twitter =(voice := os.getenv("PROMPT_VOICE", "fun, youth-focused, and eco-conscious"),
              company_info := os.getenv("COMPANY_INFO", "a startup designing stylish clothes from recycled materials"),languaje := os.getenv("PROMPT_LANGUAGE", "English"),
              topic :=os.getenv("PROMPT_TOPIC", "sustainable fashion for Gen Z"))
    prompt2 = instagram = (voice, company_info, languaje, topic)
    prompt3 = linkedin= (voice, company_info, languaje, topic)
    prompt4 = blog = (voice, company_info, languaje, topic)
    prompt5 = tiktok = (voice, company_info, languaje, topic)
    logger.info("✅ RAG inicializado correctamente")