
import streamlit as st
from server.generators.text import generate_content

def create_page():
    """
    Crea y gestiona la página de la interfaz de usuario con Streamlit.
    """
    st.title(" Generador Automático de Contenido")
    st.caption(f"Una PoC para Digital Content usando LLMs locales (Modelo: phi-3)")

    # Formulario para que el usuario introduzca la información
    with st.form("content_form"):
        tema = st.text_input("¿Sobre qué tema quieres escribir?", "Inteligencia Artificial Generativa")

        plataforma = st.selectbox("¿Para qué plataforma?", ["Blog", "Twitter/X", "Instagram", "LinkedIn"])

        audiencia = st.selectbox("¿A quién va dirigido?", ["Público General", "Expertos en Tecnología", "Niños", "Inversores"])

        tono = st.selectbox("¿Qué tono debe tener?", ["Informal", "Profesional", "Divertido", "Divulgativo"])

        submitted = st.form_submit_button("✨ Generar Contenido")

    # Lógica de generación al enviar el formulario
    if submitted:
        with st.spinner(" Pensando y generando... Esto puede tardar un poco."):
            respuesta = generate_content(
                tema=tema,
                plataforma=plataforma,
                audiencia=audiencia,
                tono=tono
            )
            st.subheader("✅ Contenido Generado")
            st.markdown(respuesta)
