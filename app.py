import streamlit as st
import os
from dotenv import load_dotenv

# Importar el módulo de legislación laboral desde la carpeta
try:
    from legislacion.pagina_legislacion import mostrar_seccion_legislacion
    LEGISLACION_DISPONIBLE = True
except ImportError:
    LEGISLACION_DISPONIBLE = False

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración inicial de la página
st.set_page_config(
    page_title="Planificador y Asistente Docente",
    page_icon="📚",
    layout="wide"
)


def mostrar_seccion_planificaciones():
    """Módulo del Generador de Planificaciones de Clase."""
    st.title("📝 Generador de Planificaciones de Clase")
    st.write("Diseña planificaciones alineadas con los estándares y bases curriculares del MINEDUC.")
    st.markdown("---")

    # Contenedor principal de selección de parámetros
    col1, col2 = st.columns(2)
    with col1:
        nivel = st.selectbox(
            "Selecciona el Nivel / Curso:",
            ["1° a 6° Básico", "7° y 8° Básico", "1° a 4° Medio"]
        )
        asignatura = st.selectbox(
            "Selecciona la Asignatura:",
            ["Matemáticas", "Lenguaje y Comunicación", "Historia", "Ciencias Naturales", "Artes / Tecnología"]
        )
    
    with col2:
        tipo_planificacion = st.selectbox(
            "Tipo de Planificación:",
            ["Clase a Clase (90 min)", "Unidad Didáctica", "Anual"]
        )
        enfoque = st.text_input("Objetivo o Contenido Específico:", placeholder="Ej: Suma y resta de fracciones homogéneas")

    st.markdown("### 📋 Estructura de la Clase")
    st.info("Configura los detalles del objetivo de aprendizaje (OA) para generar la propuesta.")

    if st.button("Generar Planificación con IA", type="primary"):
        if not enfoque.strip():
            st.warning("Por favor ingresa un objetivo o contenido específico antes de generar.")
        else:
            with st.spinner("Generando planificación pedagógica..."):
                st.success("Planificación estructurada correctamente.")
                st.markdown(f"""
                #### 🎯 Propuesta de Clase: {enfoque}
                * **Nivel:** {nivel} | **Asignatura:** {asignatura} | **Formato:** {tipo_planificacion}
                
                ---
                ##### 1. Inicio (15 min)
                * **Activación de conocimientos previos:** Preguntas guiadas sobre el contenido clave.
                * **Presentación del objetivo:** Declaración clara de la meta de la sesión.

                ##### 2. Desarrollo (60 min)
                * **Explicación modelada:** Presentación conceptual con apoyos visuales y concretos.
                * **Práctica guiada:** Resolución de actividades en parejas o pequeños grupos.
                * **Práctica independiente:** Trabajo en guía individual de ejercitación.

                ##### 3. Cierre (15 min)
                * **Sistematización:** Ticket de salida para evaluar la comprensión del objetivo.
                """)


def main():
    # Menú de navegación en la barra lateral
    st.sidebar.title("📌 Navegación")
    st.sidebar.markdown("---")
    
    opcion = st.sidebar.radio(
        "Ir a:",
        [
            "📝 Generador de Planificaciones", 
            "⚖️ Asistente de Legislación Laboral"
        ]
    )

    st.sidebar.markdown("---")
    st.sidebar.caption("🤖 **Planificador Docente v1.0**")
    st.sidebar.caption("Chile — Marco MINEDUC & Normativa Laboral")

    # Renderizado condicional según la selección del usuario
    if opcion == "📝 Generador de Planificaciones":
        mostrar_seccion_planificaciones()
        
    elif opcion == "⚖️ Asistente de Legislación Laboral":
        if LEGISLACION_DISPONIBLE:
            mostrar_seccion_legislacion()
        else:
            st.error("⚠️ No se encontró el módulo `legislacion/pagina_legislacion.py`. Asegúrate de que la carpeta y el archivo existan en GitHub.")


if __name__ == "__main__":
    main()
