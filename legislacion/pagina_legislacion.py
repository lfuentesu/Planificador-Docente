import streamlit as st
import os
from groq import Groq


def mostrar_seccion_legislacion():
    st.title("⚖️ Asistente de Legislación Laboral Educativa")
    st.write(
        "Consultas orientadas al marco normativo docente y de asistentes de la educación en Chile."
    )
    st.markdown("---")

    # Intentar obtener la API Key de los Secrets de Streamlit o del entorno
    groq_api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))

    # Barra lateral o campo para ingresar/verificar la API Key
    with st.sidebar:
        st.subheader("🔑 Configuración de Clave API")
        if not groq_api_key:
            groq_api_key = st.text_input(
                "Ingresa tu Groq API Key:",
                type="password",
                help="Consíguela en console.groq.com",
            )
        else:
            st.success("Clave API de Groq detectada correctamente.")

    # Pestañas con la información de resumen normativo
    tab1, tab2, tab3 = st.tabs(
        ["💬 Consulta Normativa", "📚 Marco Legal Principal", "🛡️ Resguardo y Derechos"]
    )

    with tab1:
        st.subheader("Haz tu consulta legal o laboral")
        st.info(
            "Ejemplo: *¿Cuáles son los plazos para el descanso maternal?* o *¿Qué dice el Estatuto Docente sobre la titularidad de horas?*"
        )

        pregunta = st.text_area(
            "Escribe la situación o duda legal aquí:",
            height=120,
            placeholder="Describe brevemente los hechos o la norma sobre la que deseas consultar...",
        )

        if st.button("Consultar Asistente Legal", type="primary"):
            if not groq_api_key:
                st.error(
                    "⚠️ Se requiere una API Key de Groq para responder consultas. Por favor ingrésala en la barra lateral."
                )
            elif not pregunta.strip():
                st.warning("Por favor ingresa una pregunta o consulta antes de enviar.")
            else:
                with st.spinner("Analizando marco legal chileno con Llama 3.3..."):
                    try:
                        client = Groq(api_key=groq_api_key)

                        prompt_sistema = """
                        Eres un experto abogado especialista en Derecho Laboral Educacional de Chile.
                        Tus respuestas deben ser fundamentadas rigurosamente en la legislación chilena vigente:
                        - Estatuto Docente (DFL N° 1) y Carrera Docente (Ley N° 20.903).
                        - Estatuto de Asistentes de la Educación (Ley N° 21.109).
                        - Código del Trabajo de Chile.
                        - Ley Karin (Ley N° 21.643) y Ley TEA (Ley N° 21.545).
                        - Dictámenes relevantes de la Dirección del Trabajo (DT) y Contraloría General de la República (CGR).
                        
                        Entrega explicaciones claras, amables, estructuradas y con orientación práctica para los profesionales de la educación.
                        """

                        respuesta = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[
                                {"role": "system", "content": prompt_sistema},
                                {"role": "user", "content": pregunta},
                            ],
                            temperature=0.3,
                            max_tokens=1500,
                        )

                        st.markdown("### 📄 Dictamen y Orientación Sugerida")
                        st.markdown(respuesta.choices[0].message.content)

                    except Exception as e:
                        st.error(f"Ocurrió un error al consultar el servicio de IA: {e}")

    with tab2:
        st.markdown("### 📜 Normativa Clave en Educación")
        st.markdown(
            """
        * **Estatuto Docente (DFL 1):** Rige los derechos, deberes, jornada laboral y asignaciones de los profesionales de la educación.
        * **Ley N° 20.903 (Carrera Docente):** Establece el sistema de desarrollo profesional docente, tramos y horas no lectivas.
        * **Ley N° 21.109 (Asistentes de la Ed.):** Regula el marco contractual, categorías y derechos de los asistentes de la educación.
        * **Código del Trabajo:** Aplica de forma supletoria en el sector particular subvencionado y administración delegada.
        """
        )

    with tab3:
        st.markdown("### 🛡️ Protección de Derechos Laborales")
        st.markdown(
            """
        * **Ley Karin (N° 21.643):** Protocolos de prevención y sanción ante acoso laboral, sexual y violencia en el trabajo.
        * **Protección a la Maternidad:** Artículos 194 y siguientes del Código del Trabajo (fuero, permiso postnatal e indemnizaciones).
        * **Principio de Confianza Legítima:** Aplicable en el sector público tras renovaciones sucesivas de contratas.
        """
        )
