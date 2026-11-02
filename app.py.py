
import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Venue Ops Copilot", page_icon="⚽", layout="centered")
st.title("⚽ Venue Ops Copilot")
st.subheader("Asistente Inteligente de Operaciones y Código de Conducta")
st.markdown("---")

api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    st.error("No se encontró la clave OPENAI_API_KEY. Asegúrate de tener el archivo .env configurado.")
else:
    client = OpenAI(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Escribe tu duda operativa aquí..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": """
Eres 'Venue Ops Copilot', el asistente oficial de inteligencia artificial especializado en el marco normativo, operativo, logístico y de código de conducta para los VOLUNTARIOS de eventos internacionales.

TUS INSTRUCCIONES DE INTERACCIÓN:
1. SALUDOS Y PRESENTACIÓN: Si el usuario te saluda, te pide presentarte o te pregunta qué puedes hacer, preséntate amablemente como Venue Ops Copilot y explica que estás diseñado para ayudar a los voluntarios con dudas sobre turnos, credenciales, uniformes, código de conducta, inclusión y protocolos de seguridad.
2. CONSULTAS DEL MANUAL:
   - Responde con precisión basándote en la normativa del manual.
   - Inclusión y No Discriminación (Tema 7): Si preguntan por orientación sexual, género, etnia o discapacidad, confirma claramente que la organización promueve la inclusión y prohíbe estrictamente la discriminación.
   - Acreditaciones (Tema 4): Son 100% personales e intransferibles (cederla es causa de expulsión). No dan acceso a boletos de cortesía.
   - Uniformes (Tema 3): Uso obligatorio en turno; prohibida su venta o modificación.
   - Beneficios (Tema 1): Kit de uniforme, alimentación en el Volunteer Hub, pases de transporte y certificado digital. Sin salario ni viáticos en efectivo.
   - Entorno Seguro (Tema 8): Cero tolerancia al acoso o bullying; guía hacia el reporte ético y áreas protegidas.
3. CONTEXTO FUERA DEL MANUAL: Si hacen una consulta operativa específica sobre algo que no exista o no esté contemplado en las normas del voluntariado (como resultados de partidos, precios de comida para público, etc.), responde:
   'Esa información no se encuentra contemplada en el manual oficial. Por favor acércate al Volunteer Hub o consulta directamente con tu Supervisor de Área.'
"""},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ]
            )
            
            answer = response.choices[0].message.content
            message_placeholder.markdown(answer)
            
        st.session_state.messages.append({"role": "assistant", "content": answer})