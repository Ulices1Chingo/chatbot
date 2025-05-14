import streamlit as st
from openai import OpenAI

# Título y descripción
st.title("🧮 Inteligencia Artificial para Teoremas Matemáticos")
st.write(
    "Este asistente especializado en matemáticas de pregrado puede ayudarte a encontrar y demostrar teoremas. "
    "Proporcione la contraseña de acceso para comenzar."
)

# Entrada para la contraseña
api_password = st.text_input("🔑 Contraseña de acceso", type="password")

# Verificar si se ingresó una contraseña
if not api_password:
    st.info("Por favor ingresa la contraseña para continuar.", icon="🗝️")
    st.stop()

# Crear cliente de OpenAI usando la contraseña ingresada como API key
client = OpenAI(api_key=api_password)

# Estado del chat con prompt especializado
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "Eres un experto en matemáticas de pregrado que conoce todos los teoremas, lemas, "
                "corolarios y definiciones de las materias de pregrado. Además, debes demostrar todo "
                "formalmente. Proporciona las definiciones clave involucradas en el teorema. "
                "Si lo que se menciona no es verdad, proporciona un contraejemplo. "
                "Si te preguntan sobre cualquier otro tema, responde: 'No conozco sobre ese tema'"
            )
        }
    ]

# Mostrar historial del chat (omitimos el mensaje del sistema)
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada de chat
if prompt := st.chat_input("Escribe tu pregunta sobre teoremas matemáticos..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Respuesta del modelo con streaming
        with st.spinner("🧠 Pensando..."):
            stream = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=st.session_state.messages,
                stream=True
            )

            # Mostrar y guardar respuesta
            with st.chat_message("assistant"):
                response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})

    except Exception as e:
        st.error(f"❌ Error al consultar la API: {e}")
