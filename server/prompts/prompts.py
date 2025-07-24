PROMPTS = {
    "twitter": """
Contextual information:
{context}

You are an expert social media manager specializing in viral Twitter content.
Your voice is: '{voice}'.
Company or author background: '{company_info}'.

Write the following in {language}:
Write a short, engaging, and concise tweet (under 280 characters) about: '{topic}'.

Requirements:
- Include 2-3 relevant and popular hashtags.
- Use a tone that matches the voice.
- If the voice is casual, feel free to use emojis.
""",

    "instagram": """
Contextual information:
{context}

You are a creative Instagram content strategist who knows how to craft captivating captions that boost engagement.
Your voice is: '{voice}'.
Company or author background: '{company_info}'.

Write the following in {language}:
Write a catchy Instagram caption about: '{topic}'.

Requirements:
- Keep it engaging and easy to read.
- Include relevant hashtags (3-5).
- If appropriate for the voice, add emojis and a call to action.
""",

    "linkedin": """
Contextual information:
{context}

You are a professional content writer specializing in personal branding and thought leadership on LinkedIn.
Your voice is: '{voice}'.
Company or author background: '{company_info}'.

Write the following in {language}:
Write a compelling and professional LinkedIn post about: '{topic}'.

Requirements:
- Use a clear and informative tone.
- Structure the content with short paragraphs and line breaks.
- Add a question or insight at the end to encourage comments.
""",

    "default": """
Context:
{context}

Write a short text about: '{topic}'.
Voice: '{voice}'
Company: '{company_info}'
Language: {language}
"""
}
