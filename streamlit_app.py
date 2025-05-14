import streamlit as st
from openai import OpenAI
import os

st.title("Inteligencia Artificial para encontrar teoremas de matemáticas")

# Solicitar contraseña de API
api_password = st.text_input("Ingrese la contraseña del API:", type="password")

# Contraseña correcta (deberías usar un método más seguro en producción)
CORRECT_PASSWORD = "password123"  # Cambia esto por una contraseña segura

if api_password:
    if api_password == CORRECT_PASSWORD:
        try:
            # Configurar el cliente de OpenAI
            client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            
            st.markdown("Escribe de qué se trata el teorema de matemáticas especificando el área relacionada de pregrado." \
                       "La IA solo responde preguntas relacionadas al tema.")

            question = st.text_input("Escribe tu pregunta:")

            prompt = ("Eres un experto en matemáticas de pregrado que conoce todos los teoremas, lemas, corolarios y definiciones"
                    " de las materias de pregrado. Además, debes de demostrarlo formalmente. También, debes de proveer las definiciones "
                    "claves que involucran en el teorema. Si lo que se menciona no es verdad proporciona un contraejemplo."
                    "Si te preguntan sobre cualquier otro tema, responde: 'No conozco sobre ese tema'"
            )

            if question:
                with st.spinner("Pensando..."):
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": prompt},
                            {"role": "user", "content": question}
                        ]
                    )
                    st.success("Respuesta:")
                    st.markdown(response.choices[0].message.content)
        
        except Exception as e:
            st.error(f"Error al conectar con la API: {str(e)}")
    else:
        st.error("Contraseña incorrecta. Por favor, ingrese la contraseña válida.")
else:
    st.warning("Por favor, ingrese la contraseña del API para continuar.")
