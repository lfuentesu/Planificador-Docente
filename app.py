import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Cargar variables de entorno si existen localmente
load_dotenv()

# Importar el módulo de legislación laboral desde la carpeta
try:
    from legislacion.pagina_legislacion import mostrar_seccion_legislacion

    LEGISLACION_DISPONIBLE = True
except ImportError:
    LEGISLACION_DISPONIBLE = False

# Configuración inicial de la página
st.set_page_config(
    page_title="Planificador y Asistente Docente", page_icon="📚", layout="wide"
)


def generar_planificacion_ia(
    groq_api_key, nivel, asignatura, tipo_planificacion, enfoque, observaciones
):
    """Llama a la API de Groq para generar una planificación pedagógica detallada."""
    client = Groq(api_key=groq_api_key)

    prompt_sistema = """
    Eres un experto diseñador curricular y asesor pedagógico del sistema educativo chileno, con amplio conocimiento del Marco para la Buena Enseñanza, las Bases Curriculares del MINEDUC y los Decretos de Evaluación (ej. Decreto 67).

    Tu objetivo es redactar planificaciones pedagógicas altamente estructuradas, rigurosas, claras y listas para ser implementadas por los docentes en el aula.

    Asegúrate de incluir siempre:
    1. **Objetivo de Aprendizaje (OA)** y/o Habilidad principal adaptado al curso específico.
    2. **Indicadores de Evaluación** específicos.
    3. **Estructura de la Clase:**
       - **Inicio (15 min):** Activación de conocimientos previos, conflicto cognitivo y declaración del objetivo.
       - **Desarrollo (60 min):** Modelaje, práctica guiada y práctica independiente con actividades concretas.
       - **Cierre (15 min):** Síntesis de aprendizajes y ticket de salida/evaluación formativa.
    4. **Sugerencia de Diversificación (DUA):** Adecuaciones para atender a la diversidad en el aula.
    5. **Recursos Sugeridos.**

    Usa un formato Markdown limpio, profesional y bien organizado con encabezados y viñetas.
    """

    prompt_usuario = f"""
    Genera una propuesta de planificación con los siguientes parámetros:
    - **Nivel / Curso Específico:** {nivel}
    - **Asignatura:** {asignatura}
    - **Tipo de Planificación:** {tipo_planificacion}
    - **Tema / Objetivo Específico:** {enfoque}
    - **Consideraciones adicionales:** {observaciones if observaciones else "Ninguna especificada"}
    """

    respuesta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt_usuario},
        ],
        temperature=0.4,
        max_tokens=2200,
    )

    return respuesta.choices[0].message.content


def mostrar_seccion_planificaciones(groq_api_key):
    """Módulo del Generador de Planificaciones de Clase impulsado por IA."""
    st.title("📝 Generador de Planificaciones de Clase (IA)")
    st.write(
        "Diseña planificaciones pedagógicas completas alineadas con los estándares del MINEDUC usando Inteligencia Artificial."
    )
    st.markdown("---")

    # Contenedor principal de selección de parámetros
    col1, col2 = st.columns(2)
    with col1:
        nivel = st.selectbox(
            "Selecciona el Nivel / Curso:",
            [
                # Educación Parvularia
                "Prekínder (NT1)",
                "Kínder (NT2)",
                # Educación Básica
                "1° Básico",
                "2° Básico",
                "3° Básico",
                "4° Básico",
                "5° Básico",
                "6° Básico",
                "7° Básico",
                "8° Básico",
                # Educación Media
                "1° Medio",
                "2° Medio",
                "3° Medio (Formación General)",
                "3° Medio (TTP / Técnico Profesional)",
                "4° Medio (Formación General)",
                "4° Medio (TTP / Técnico Profesional)",
                # Educación de Adultos
                "EPJA / Educación de Adultos",
            ],
        )
        asignatura = st.selectbox(
            "Selecciona la Asignatura:",
            [
                "Matemáticas",
                "Lengua y Literatura / Lenguaje",
                "Historia, Geografía y Ciencias Sociales",
                "Ciencias Naturales (Biología, Física, Química)",
                "Inglés",
                "Artes Visuales / Música",
                "Tecnología",
                "Educación Física y Salud",
                "Orientación",
            ],
        )

    with col2:
        tipo_planificacion = st.selectbox(
            "Tipo de Planificación:",
            [
                "Clase a Clase (90 minutos)",
                "Unidad Didáctica (2 a 4 semanas)",
                "Planificación Anual (Visión General)",
            ],
        )
        enfoque = st.text_input(
            "Objetivo o Contenido Específico:",
            placeholder="Ej: Suma y resta de fracciones homogéneas / Análisis de mitos grecolatinos",
        )

    observaciones = st.text_area(
        "Contexto o necesidades específicas (Opcional):",
        placeholder="Ej: Incluir trabajo colaborativo en parejas, priorizar evaluación formativa, considerar estudiantes con DUA...",
        height=80,
    )

    st.markdown("---")

    if st.button("🚀 Generar Planificación con IA", type="primary"):
        if not groq_api_key:
            st.error(
                "⚠️ No se detectó la clave de Groq API. Asegúrate de tener configurado `GROQ_API_KEY` en los Secrets de Streamlit."
            )
        elif not enfoque.strip():
            st.warning(
                "Por favor ingresa un objetivo o contenido específico antes de generar la planificación."
            )
        else:
            with st.spinner(
                "Generando propuesta pedagógica con Llama 3.3... Esto tomará unos segundos."
            ):
                try:
                    resultado_planificacion = generar_planificacion_ia(
                        groq_api_key,
                        nivel,
                        asignatura,
                        tipo_planificacion,
                        enfoque,
                        observaciones,
                    )
                    st.success("¡Planificación generada con éxito!")
                    st.markdown("### 📄 Propuesta Pedagógica")
                    st.markdown(resultado_planificacion)
                except Exception as e:
                    st.error(
                        f"Ocurrió un error al generar la planificación mediante IA: {e}"
                    )


def main():
    # Obtener la API Key desde los Secrets de Streamlit o del entorno
    groq_api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))

    # Menú de navegación en la barra lateral
    st.sidebar.title("📌 Navegación")
    st.sidebar.markdown("---")

    opcion = st.sidebar.radio(
        "Ir a:",
        ["📝 Generador de Planificaciones", "⚖️ Asistente de Legislación Laboral"],
    )

    st.sidebar.markdown("---")
    st.sidebar.caption("🤖 **Planificador Docente v1.1**")
    st.sidebar.caption("Chile — Marco MINEDUC & Normativa Laboral")

    # Renderizado condicional según la selección del usuario
    if opcion == "📝 Generador de Planificaciones":
        mostrar_seccion_planificaciones(groq_api_key)

    elif opcion == "⚖️ Asistente de Legislación Laboral":
        if LEGISLACION_DISPONIBLE:
            mostrar_seccion_legislacion()
        else:
            st.error(
                "⚠️ No se encontró el módulo `legislacion/pagina_legislacion.py`. Asegúrate de que la carpeta y el archivo existan en GitHub."
            )


if __name__ == "__main__":
    main()
