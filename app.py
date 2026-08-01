import io
import os
import streamlit as st
from docx import Document
from docx.shared import Pt, Inches, RGBColor
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

# Diccionario de ejemplos automáticos según la asignatura seleccionada
EJEMPLOS_OBJETIVOS = {
    "Matemáticas": "Suma y resta de fracciones con distinto denominador",
    "Lengua y Literatura / Lenguaje": "Comprensión lectora y análisis de personajes en mitos grecolatinos",
    "Historia, Geografía y Ciencias Sociales": "Causas y consecuencias del proceso de Independencia de Chile",
    "Ciencias Naturales (Biología, Física, Química)": "Estructura de la célula eucariota y función de sus organelos",
    "Inglés": "Uso del presente simple y continuo para describir rutinas diarias",
    "Artes Visuales / Música": "Elementos del lenguaje visual: color, línea y textura en obras impresionistas",
    "Tecnología": "Diseño de un prototipo de solución a un problema medioambiental local",
    "Educación Física y Salud": "Desarrollo de cualidades físicas básicas mediante juegos colectivos",
    "Orientación": "Promoción del respeto y la resolución pacífica de conflictos en la comunidad escolar",
}


def generar_planificacion_ia(
    groq_api_key, nivel, asignatura, tipo_planificacion, enfoque, observaciones
):
    """Llama a la API de Groq para generar una planificación pedagógica detallada."""
    client = Groq(api_key=groq_api_key)

    prompt_sistema = """
    Eres un experto diseñador curricular y asesor pedagógico del sistema educativo chileno, con amplio conocimiento del Marco para la Buena Enseñanza, las Bases Curriculares del MINEDUC y los Decretos de Evaluación (ej. Decreto 67).

    Tu objetivo es redactar planificaciones pedagógicas altamente estructuradas, rigurosas, claras y listas para ser implementadas por los docentes en el aula.

    Asegúrate de incluir siempre:
    1. **Objetivo de Aprendizaje (OA)** y/o Habilidad principal adaptado al curso y asignatura específicos.
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


def crear_documento_word(
    nivel, asignatura, tipo_planificacion, enfoque, observaciones, contenido
):
    """Crea un archivo Word (.docx) formateado con la planificación."""
    doc = Document()

    # Título principal del documento
    p_titulo = doc.add_paragraph()
    run_titulo = p_titulo.add_run("PROPUESTA DE PLANIFICACIÓN PEDAGÓGICA")
    run_titulo.bold = True
    run_titulo.font.size = Pt(16)
    run_titulo.font.color.rgb = RGBColor(0, 51, 102)
    p_titulo.paragraph_format.space_after = Pt(12)

    # Tabla con metadatos de la planificación
    tabla = doc.add_table(rows=4, cols=2)
    tabla.style = "Table Grid"

    datos = [
        ("Nivel / Curso:", nivel),
        ("Asignatura:", asignatura),
        ("Tipo de Planificación:", tipo_planificacion),
        ("Tema / Enfoque:", enfoque),
    ]

    for i, (campo, valor) in enumerate(datos):
        cell_label = tabla.cell(i, 0)
        cell_value = tabla.cell(i, 1)

        p_label = cell_label.paragraphs[0]
        run_l = p_label.add_run(campo)
        run_l.bold = True
        run_l.font.size = Pt(10)

        p_val = cell_value.paragraphs[0]
        run_v = p_val.add_run(valor)
        run_v.font.size = Pt(10)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    if observaciones.strip():
        p_obs = doc.add_paragraph()
        run_o_title = p_obs.add_run("Consideraciones especiales: ")
        run_o_title.bold = True
        p_obs.add_run(observaciones)
        p_obs.paragraph_format.space_after = Pt(12)

    # Encabezado del contenido
    p_sub = doc.add_paragraph()
    run_sub = p_sub.add_run("Desarrollo de la Planificación")
    run_sub.bold = True
    run_sub.font.size = Pt(13)
    run_sub.font.color.rgb = RGBColor(0, 51, 102)
    p_sub.paragraph_format.space_after = Pt(8)

    # Agregar líneas de texto
    for linea in contenido.split("\n"):
        linea_str = linea.strip()
        if not linea_str:
            continue

        p = doc.add_paragraph()
        if linea_str.startswith("# "):
            run = p.add_run(linea_str.replace("# ", ""))
            run.bold = True
            run.font.size = Pt(14)
            run.font.color.rgb = RGBColor(0, 51, 102)
        elif linea_str.startswith("## "):
            run = p.add_run(linea_str.replace("## ", ""))
            run.bold = True
            run.font.size = Pt(12)
            run.font.color.rgb = RGBColor(0, 51, 102)
        elif linea_str.startswith("### "):
            run = p.add_run(linea_str.replace("### ", ""))
            run.bold = True
            run.font.size = Pt(11)
        elif linea_str.startswith("- ") or linea_str.startswith("* "):
            p.style = "List Bullet"
            texto_limpio = linea_str[2:].replace("**", "")
            p.add_run(texto_limpio)
        else:
            texto_limpio = linea_str.replace("**", "")
            p.add_run(texto_limpio)

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer


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

    # Obtener el ejemplo sugerido de acuerdo a la asignatura seleccionada
    ejemplo_sugerido = EJEMPLOS_OBJETIVOS.get(asignatura, "Escribe aquí el objetivo...")

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
            placeholder=f"Ej: {ejemplo_sugerido}",
            help=f"Sugerencia para {asignatura}: {ejemplo_sugerido}",
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
                f"Por favor ingresa un objetivo o contenido para la asignatura de **{asignatura}** antes de generar la planificación."
            )
        else:
            with st.spinner(
                f"Generando propuesta pedagógica de {asignatura} para {nivel}... Esto tomará unos segundos."
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

                    # Guardar en la sesión de Streamlit para que no se pierda al interactuar
                    st.session_state["resultado_planificacion"] = (
                        resultado_planificacion
                    )
                    st.session_state["datos_planificacion"] = {
                        "nivel": nivel,
                        "asignatura": asignatura,
                        "tipo": tipo_planificacion,
                        "enfoque": enfoque,
                        "observaciones": observaciones,
                    }
                    st.success("¡Planificación generada con éxito!")

                except Exception as e:
                    st.error(
                        f"Ocurrió un error al generar la planificación mediante IA: {e}"
                    )

    # Si ya hay un resultado generado en sesión, mostrarlo y ofrecer el botón de descarga
    if "resultado_planificacion" in st.session_state:
        st.markdown("### 📄 Propuesta Pedagógica")
        st.markdown(st.session_state["resultado_planificacion"])

        st.markdown("---")
        datos = st.session_state["datos_planificacion"]

        # Generar el archivo Word en memoria
        archivo_word = crear_documento_word(
            datos["nivel"],
            datos["asignatura"],
            datos["tipo"],
            datos["enfoque"],
            datos["observaciones"],
            st.session_state["resultado_planificacion"],
        )

        nombre_archivo = f"Planificacion_{datos['asignatura']}_{datos['nivel']}.docx".replace(
            " ", "_"
        )

        st.download_button(
            label="📥 Descargar Planificación en Word (.docx)",
            data=archivo_word,
            file_name=nombre_archivo,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            type="primary",
        )


def main():
    # Obtener la API Key desde los Secrets de Streamlit o del entorno
    groq_api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))

    # --- CARGAR LOGO DE SUTE CHILE EN LA BARRA LATERAL ---
    posibles_rutas_logo = [
        "logotiposute.jpg",
        "legislacion/logotiposute.jpg",
        "assets/logotiposute.jpg",
        "logotposute.jpg",
        "legislacion/logotposute.jpg",
    ]

    logo_encontrado = False
    for ruta in posibles_rutas_logo:
        if os.path.exists(ruta):
            st.sidebar.image(ruta, use_column_width=True)
            logo_encontrado = True
            break

    if not logo_encontrado:
        st.sidebar.info("ℹ️ Para ver el logo, asegúrate de que el archivo `logotiposute.jpg` esté subido a GitHub.")

    # Menú de navegación en la barra lateral
    st.sidebar.title("📌 Navegación")
    st.sidebar.markdown("---")

    opcion = st.sidebar.radio(
        "Ir a:",
        ["📝 Generador de Planificaciones", "⚖️ Asistente de Legislación Laboral"],
    )

    st.sidebar.markdown("---")
    st.sidebar.caption("🤖 **Planificador Docente v1.6**")
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
