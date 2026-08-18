import os
import streamlit as st
from groq import Groq

def obtener_groq_client():
    """Obtiene la clave de la API de Groq desde los Secrets de Streamlit o variables de entorno."""
    api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))
    if api_key:
        return Groq(api_key=api_key)
    return None

def consultar_legislacion_ia(client, pregunta):
    """Consulta al modelo de IA sobre la legislación laboral docente en Chile."""
    prompt_sistema = """
    Eres un abogado especialista en Derecho Laboral Educacional y legislación docente en Chile.
    Tienes un conocimiento profundo del Estatuto Docente (Decreto con Fuerza de Ley N° 1 de 1996), el Código del Trabajo de Chile, la Ley de Inclusión, y los Decretos y Reglamentos del Ministerio de Educación (MINEDUC).

    Tu objetivo es responder las consultas de los profesores, asistentes de la educación y trabajadores de la educación de manera clara, rigurosa, orientadora y sindicalmente solidarizada.

    Asegúrate de:
    1. Citar explícitamente los artículos pertinentes cuando corresponda (ej. "Según el Artículo 69 del Estatuto Docente...").
    2. Explicar los derechos de manera comprensible sin tecnicismos excesivos.
    3. Entregar recomendaciones o pasos concretos que el trabajador puede seguir ante una vulneración o duda laboral.
    4. Mantener una postura de resguardo de los derechos laborales.
    """

    # Intentamos primero con llama-3.1-70b-versatile y luego con llama-3.3-70b-specdec
    try:
        respuesta = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": pregunta},
            ],
            temperature=0.3,
            max_tokens=2500,
        )
        return respuesta.choices[0].message.content
    except Exception:
        respuesta = client.chat.completions.create(
            model="llama-3.3-70b-specdec",
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": pregunta},
            ],
            temperature=0.3,
            max_tokens=2500,
        )
        return respuesta.choices[0].message.content

def mostrar_seccion_legislacion():
    """Interfaz principal del Asistente de Legislación Laboral."""
    st.title("⚖️ Asistente de Legislación Laboral Docente")
    st.write("Resuelve tus dudas sobre el Estatuto Docente, Código del Trabajo y normativa educacional en Chile.")

    with st.expander("💡 **¿Qué puedes consultar aquí?**", expanded=False):
        st.markdown(
            """
            * **Derechos Laborales:** Horas lectivas vs. no lectivas, permiso administrativo, licencias médicas, causales de despido.
            * **Estatuto Docente:** Carrera Docente, bonos, asignación de dirección, titularidad de horas, evaluaciones y sumarios.
            * **Código del Trabajo:** Contratación, finiquito, fueros, horas extraordinarias y descansos.
            """
        )

    st.markdown("---")

    # Preguntas frecuentes rápidas
    st.markdown("#### 📌 Consultas frecuentes rápidas:")
    col_q1, col_q2, col_q3 = st.columns(3)

    pregunta_rapida = None
    with col_q1:
        if st.button("⏱️ ¿Proporción de horas lectivas y no lectivas?"):
            pregunta_rapida = "¿Cuál es la proporción legal entre horas lectivas y no lectivas según el Estatuto Docente en Chile?"
    with col_q2:
        if st.button("📋 ¿Días de permiso administrativo?"):
            pregunta_rapida = "¿Cuántos días de permiso administrativo corresponden al año a un docente y cómo se gestionan?"
    with col_q3:
        if st.button("📝 ¿Causales de término de contrato?"):
            pregunta_rapida = "¿Cuáles son las causales legales para el término de contrato de un docente en el sector municipal y particular subvencionado?"

    st.markdown("---")

    # Área de texto para ingresar la pregunta
    pregunta_usuario = st.text_area(
        "Escribe tu consulta jurídica o laboral aquí:",
        value=pregunta_rapida if pregunta_rapida else "",
        placeholder="Ej: ¿Cuánto debiera recibir de sueldo un director de escuela básica o qué asignaciones le corresponden según la Ley de Carrera Docente?",
        height=120,
    )

    if st.button("🔍 Consultar al Asistente Jurídico", type="primary"):
        client = obtener_groq_client()

        if not client:
            st.error("⚠️ No se detectó la clave de Groq API (`GROQ_API_KEY`). Verifica la configuración en los Secrets de Streamlit.")
        elif not pregunta_usuario.strip():
            st.warning("Por favor ingresa o selecciona una pregunta antes de consultar.")
        else:
            with st.spinner("Consultando la normativa laboral educacional chilena... Esto tomará unos segundos."):
                try:
                    respuesta = consultar_legislacion_ia(client, pregunta_usuario)
                    
                    st.markdown("### 🏛️ Respuesta de la Asesoría Jurídica")
                    st.markdown(
                        f'<div style="background-color: #FFFFFF; padding: 25px; border-radius: 12px; border: 1px solid #E2E8F0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); margin-bottom: 20px;">{respuesta}</div>',
                        unsafe_allow_html=True,
                    )
                except Exception as e:
                    st.error(f"Ocurrió un error al consultar el servicio de IA: {e}")
