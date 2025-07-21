import streamlit as st
from server.generators.text import generate_content

def create_page():
    """
    Crea y gestiona la página de la interfaz de usuario con Streamlit.
    """
    st.title(" Generador Automático de Contenido")
    st.caption(f"Una PoC para Digital Content usando LLMs locales (Modelo: phi-3)")

    temas_sugeridos = [
        "Inteligencia Artificial y automatización",
        "Sostenibilidad y cambio climático",
        "Economía digital y criptomonedas",
        "Salud mental y bienestar",
        "Política internacional y geopolítica",
        "Innovación educativa",
        "Deportes y grandes eventos (JJOO, Mundiales)",
        "Cultura pop y tendencias virales",
        "Ciencia y exploración espacial",
        "Emprendimiento y startups",
        "Otro..."
    ]

    with st.form("content_form"):
        tema_seleccionado = st.selectbox("Selecciona un tema o elige 'Otro...' para escribir uno:", temas_sugeridos)
        tema = tema_seleccionado
        if tema_seleccionado == "Otro...":
            tema = st.text_input("Escribe tu tema personalizado:", "")

        plataforma = st.selectbox("¿Para qué plataforma?", [
            "Blog", "Twitter/X", "Instagram", "LinkedIn", "Facebook", "TikTok", "YouTube", "Threads", "Snapchat", "Pinterest", "Reddit", "Telegram", "WhatsApp Channels", "Bluesky", "Mastodon", "Medium", "Tumblr"
        ])

        audiencia = st.selectbox("¿A quién va dirigido?", ["Público General", "Expertos en Tecnología", "Niños", "Inversores"])

        tono = st.selectbox("¿Qué tono debe tener?", ["Informal", "Profesional", "Divertido", "Divulgativo"])

        submitted = st.form_submit_button("✨ Generar Contenido")

    if submitted:
        with st.spinner(" Pensando y generando... Esto puede tardar un poco."):
            resultado = generate_content(
                tema=tema,
                plataforma=plataforma,
                audiencia=audiencia,
                tono=tono
            )
            # resultado puede ser (imagen_bytes, texto) o (texto, imagen_bytes)
            if plataforma == "Instagram":
                imagen_bytes, texto = resultado
                st.image(imagen_bytes, caption="Imagen generada por IA", use_column_width=True)
                st.subheader("✅ Contenido Generado")
                st.markdown(texto)
            else:
                texto, imagen_bytes = resultado
                st.subheader("✅ Contenido Generado")
                st.markdown(texto)
                st.image(imagen_bytes, caption="Imagen generada por IA", use_column_width=True) 