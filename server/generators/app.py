from groq_generator import GroqGenerator
import streamlit as st

def main():
    st.title("Generador de Contenido con Groq")
    st.write("Configura tu contenido:")
    
    generador = GroqGenerator()
    
    with st.form("contenido_form"):
        tema = st.text_input("Tema principal:")
        plataforma = st.selectbox("Plataforma:", ["Blog", "Twitter", "Instagram"])
        audiencia = st.selectbox("Audiencia:", ["General", "Técnica", "Empresarial", "Juvenil"])
        tono = st.selectbox("Tono:", ["Profesional", "Divertido", "Motivacional", "Educativo"])
        
        if st.form_submit_button("Generar"):
            with st.spinner("Creando contenido..."):
                try:
                    contenido = generador.generar_contenido(
                        tema=tema,
                        plataforma=plataforma,
                        audiencia=audiencia,
                        tono=tono.lower()
                    )
                    st.success("¡Contenido generado!")
                    st.text_area("Resultado:", contenido, height=300)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.info("Verifica tu API key en el archivo .env")

if __name__ == "__main__":
    main()