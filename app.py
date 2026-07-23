import streamlit as st
import json
import os
from io import BytesIO
from docx import Document
from docx.shared import Pt, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Configuración de la página
st.set_page_config(
    page_title="Planificador Curricular Solidario",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para la interfaz
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    
    .title-container {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 1.8rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .title-container h1 { color: white !important; margin-bottom: 0.3rem; font-size: 2.1rem; }
    .title-container p { color: #e0e6ed !important; font-size: 1.05rem; margin: 0; }

    .pacto-container {
        background-color: #eef2f7;
        border-left: 5px solid #2a5298;
        padding: 1rem 1.2rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
    }

    .section-header {
        color: #1e3c72;
        font-weight: bold;
        font-size: 1.25rem;
        margin-bottom: 0.8rem;
    }

    .print-btn {
        width: 100%;
        background-color: #e63946;
        color: white;
        padding: 0.75rem 1rem;
        border: none;
        border-radius: 8px;
        font-size: 1.05rem;
        cursor: pointer;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Logo si existe
if os.path.exists("logosute.jpg"):
    col_logo, _ = st.columns([1, 4])
    with col_logo:
        st.image("logosute.jpg", width=110)

# Banner del Título Principal
st.markdown("""
    <div class="title-container">
        <h1>📝 Planificador Curricular Inteligente</h1>
        <p>Red Colaborativa de Apoyo Pedagógico para la Educación Básica</p>
    </div>
""", unsafe_allow_html=True)

# Mensaje de Mística y Pacto Solidario
st.markdown("""
    <div class="pacto-container">
        <h4 style="margin:0 0 5px 0; color:#1e3c72;">🤝 Compromiso de Solidaridad Docente</h4>
        <p style="margin:0; font-size:0.95rem; color:#333;">
            Esta es una herramienta comunitaria y fraterna. Al compartir y guardar tus planificaciones, estás enriqueciendo el banco colectivo de clases para apoyar a otros profesores de todo el país. <b>La educación pública la construimos entre todos.</b>
        </p>
    </div>
""", unsafe_allow_html=True)

# Manual Integrado
with st.expander("❓ GUÍA RÁPIDA DE USO / TUTORIAL PASO A PASO (Clic aquí)", expanded=False):
    st.markdown("""
    ### 📖 ¿Cómo usar este Planificador en 5 pasos sencillos?
    
    1. **Seleccionar Asignatura y Nivel:** Elija la materia (1° a 8° Básico) y el Objetivo de Aprendizaje (OA).
    2. **Ajustar Profundización:** Deslice el control para seleccionar el nivel cognitivo (*Inicial, Intermedio o Avanzado*).
    3. **Personalizar el Contenido:** Modifique libremente las cajas de Inicio, Desarrollo, Cierre, DUA y Recursos.
    4. **Editar Material del Estudiante:** Redacte las actividades para la Guía y el Ticket de Salida.
    5. **Descargar y Compartir:** Genere sus 3 documentos Word (.docx) e incorpore la clase al banco colaborativo.
    """)

# Funciones de datos
def cargar_curriculum():
    if os.path.exists("curriculum.json"):
        with open("curriculum.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def guardar_curriculum(datos):
    with open("curriculum.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

def cargar_historial():
    if os.path.exists("historial_planificaciones.json"):
        with open("historial_planificaciones.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_historial(historial):
    with open("historial_planificaciones.json", "w", encoding="utf-8") as f:
        json.dump(historial, f, ensure_ascii=False, indent=4)

curriculum = cargar_curriculum()

# BARRA LATERAL
st.sidebar.header("🛠️ Herramientas del Taller")

if st.sidebar.button("🔄 Reiniciar / Nueva Clase", use_container_width=True):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("➕ Agregar Nuevo OA a la Bodega")

with st.sidebar.expander("Ingresar nuevo Objetivo"):
    asig_nueva = st.text_input("Asignatura:")
    curso_nuevo = st.text_input("Curso:")
    oa_nuevo = st.text_input("Código / Descripción del OA:")
    ini_nuevo = st.text_area("Inicio por defecto:", value="Activación de conocimientos previos y motivación.")
    des_nuevo = st.text_area("Desarrollo por defecto:", value="Exposición guiada y práctica de ejercicios.")
    cie_nuevo = st.text_area("Cierre por defecto:", value="Síntesis de ideas clave y evaluación formativa.")
    ind_nuevo = st.text_area("Indicador por defecto:", value="Demuestra comprensión mediante resolución de problemas.")

    if st.button("💾 Guardar OA en Bodega"):
        if asig_nueva and curso_nuevo and oa_nuevo:
            if asig_nueva not in curriculum: curriculum[asig_nueva] = {}
            if curso_nuevo not in curriculum[asig_nueva]: curriculum[asig_nueva][curso_nuevo] = []
            
            curriculum[asig_nueva][curso_nuevo].append({
                "oa": oa_nuevo, "inicio": ini_nuevo, "desarrollo": des_nuevo,
                "cierre": cie_nuevo, "indicador": ind_nuevo
            })
            guardar_curriculum(curriculum)
            st.sidebar.success("¡Objetivo agregado con éxito!")
            st.rerun()

# Banco Colaborativo en Barra Lateral
st.sidebar.markdown("---")
st.sidebar.subheader("🗄️ Banco Colaborativo de Clases")
historial = cargar_historial()

if historial:
    with st.sidebar.expander(f"Ver Clases Compartidas ({len(historial)})"):
        for item in reversed(historial):
            st.markdown(f"**{item['fecha']}** | {item['asignatura']} ({item['curso']})")
            st.caption(f"📌 {item.get('unidad','Unidad 1')} — {item.get('num_sesion','Clase 1')}")
            st.caption(f"Docente: {item['profesor']}")
            st.caption(f"OA: {item['oa'][:45]}...")
            st.markdown("---")
else:
    st.sidebar.info("Sé el primero en compartir una clase con la comunidad.")

if not curriculum:
    st.error("No se encontró el archivo 'curriculum.json'.")
else:
    st.markdown('<div class="section-header">📌 1. Selección Curricular Base</div>', unsafe_allow_html=True)
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        asignatura_sel = st.selectbox("Asignatura:", list(curriculum.keys()))
    with col_c2:
        curso_sel = st.selectbox("Curso / Nivel:", list(curriculum[asignatura_sel].keys()))
    
    lista_oas = curriculum[asignatura_sel][curso_sel]
    opciones_oa = [item["oa"] for item in lista_oas]
    oa_sel_texto = st.selectbox("Objetivo de Aprendizaje (OA):", opciones_oa)
    datos_oa = next(item for item in lista_oas if item["oa"] == oa_sel_texto)

    st.markdown("---")

    st.markdown('<div class="section-header">⚙️ 2. Identificación y Contexto de la Clase</div>', unsafe_allow_html=True)
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        fecha_clase = st.date_input("Fecha programada para la clase:")
        nombre_profesor = st.text_input("Nombre del Docente:", value="Profesor(a)")
    with col_f2:
        tiempo_clase = st.text_input("Duración Estimada:", value="90 minutos (2 horas pedagógicas)")
        unidad_didactica = st.text_input("Unidad Didáctica / Mes:", value="Unidad 1")

    num_sesion = st.text_input("Número de Clase / Sesión dentro de la Unidad:", value="Clase N° 1")

    nivel_dificultad = st.select_slider(
        "📊 Nivel de Profundización Cognitiva:",
        options=["Inicial / Reforzamiento", "Intermedio / Estándar", "Avanzado / Desafío"],
        value="Intermedio / Estándar"
    )

    texto_inicio = datos_oa["inicio"]
    texto_desarrollo = datos_oa["desarrollo"]
    texto_cierre = datos_oa["cierre"]

    if nivel_dificultad == "Inicial / Reforzamiento":
        texto_inicio += " (Enfoque de nivelación: repasar conceptos previos con apoyo pictórico)."
        texto_desarrollo += " (Paso a paso guiado con modelaje en pizarra y apoyo directo)."
        texto_cierre += " (Verificación directa del concepto clave y síntesis verbal)."
    elif nivel_dificultad == "Avanzado / Desafío":
        texto_inicio += " (Desafío inicial: planteamiento de problema lógico para reflexionar)."
        texto_desarrollo += " (Resolución autónoma, fundamentación de procedimientos y comparación de estrategias)."
        texto_cierre += " (Pregunta de transferencia para aplicar en situaciones inéditas)."

    oat_sugerido = "Demostrar una actitud de esfuerzo, perseverancia y rigor en la realización de trabajos."
    if "Matemática" in asignatura_sel: oat_sugerido = "Manifestar una actitud de curiosidad e interés por las matemáticas."
    elif "Lenguaje" in asignatura_sel: oat_sugerido = "Demostrar interés por la lectura y la comunicación reflexiva."

    st.markdown("---")

    st.markdown('<div class="section-header">📝 3. Secuencia Didáctica (Momentos de la Clase)</div>', unsafe_allow_html=True)
    oat_editable = st.text_area("🌱 Objetivo de Aprendizaje Transversal (OAT) / Actitud:", value=oat_sugerido, height=80)
    inicio_editable = st.text_area("🕐 1. INICIO - Activación y Motivación:", value=texto_inicio, height=110)
    desarrollo_editable = st.text_area("⚙️ 2. DESARROLLO - Práctica Guiada e Independiente:", value=texto_desarrollo, height=130)
    cierre_editable = st.text_area("⏱️ 3. CIERRE - Síntesis y Evaluación Formativa:", value=texto_cierre, height=110)

    st.markdown("---")

    st.markdown('<div class="section-header">🛠️ 4. Soportes, DUA y Evaluación</div>', unsafe_allow_html=True)
    recursos_sugeridos = "Texto escolar, cuaderno de la asignatura, pizarra y plumones."
    dua_sugerido = "Proporcionar instrucciones claras y fraccionadas. Monitorear activamente el trabajo en los puestos."

    indicador_editable = st.text_area("🎯 Indicador de Logro Esperado:", value=datos_oa["indicador"], height=80)
    recursos_editable = st.text_area("📦 Recursos Didácticos Requeridos:", value=recursos_sugeridos, height=80)
    dua_editable = st.text_area("💡 Estrategias DUA / Diversificación:", value=dua_sugerido, height=80)
    instrumento_editable = st.text_area("📋 Instrumento / Tipo de Evaluación Formativa:", value="Ticket de Salida y Pauta de Cotejo / Observación Directa.", height=80)
    obs_editable = st.text_area("✏️ Bitácora / Observaciones del Docente:", value="Sin observaciones previas. Registrar ajustes o imprevistos de la sesión aquí.", height=80)

    st.markdown("---")

    st.markdown('<div class="section-header">📄 5. Material Impreso para el Estudiante</div>', unsafe_allow_html=True)
    guia_p1 = st.text_area("📝 Pregunta 1 (Práctica Guiada):", value="Actividad 1: Responde brevemente el concepto principal abordado en el desarrollo.", height=70)
    guia_p2 = st.text_area("✏️ Pregunta 2 (Práctica Independiente):", value="Actividad 2: Aplica lo aprendido resolviendo la siguiente situación en tu cuaderno.", height=70)
    guia_ticket = st.text_area("🎟️ Ticket de Salida:", value="TICKET DE SALIDA: Escribe en 2 líneas lo más importante que aprendiste hoy.", height=70)

    # GENERACIÓN DE DOCUMENTOS WORD
    # 1. PLANIFICACIÓN
    doc = Document()
    for section in doc.sections:
        section.top_margin = Cm(2.5); section.bottom_margin = Cm(2.5)
        section.left_margin = Cm(2.5); section.right_margin = Cm(2.5)

    style_normal = doc.styles['Normal']
    font_normal = style_normal.font; font_normal.name = 'Calibri'; font_normal.size = Pt(11)

    if os.path.exists("logosute.jpg"):
        p_logo = doc.add_paragraph(); p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.add_run().add_picture("logosute.jpg", width=Inches(1.2))

    p_titulo = doc.add_paragraph(); p_titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_titulo.add_run("PLANIFICACIÓN DE AULA SEMANAL").font.bold = True
    
    p_sub = doc.add_paragraph(); p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.add_run("Documento Técnico Pedagógico - Licencia Educativa Libre").italic = True
    
    doc.add_paragraph("\n")
    tabla = doc.add_table(rows=8, cols=2); tabla.style = 'Table Grid'
    
    celdas = [
        ("Docente:", nombre_profesor), ("Fecha de Aplicación:", str(fecha_clase)),
        ("Duración / N° Sesión:", f"{tiempo_clase} — {num_sesion}"), ("Unidad / Mes:", unidad_didactica),
        ("Asignatura / Nivel:", f"{asignatura_sel} — {curso_sel}"), ("Nivel de Profundización:", nivel_dificultad),
        ("Objetivo Priorizado:", oa_sel_texto), ("Actitud / OAT:", oat_editable)
    ]
    for i, (campo, valor) in enumerate(celdas):
        row = tabla.rows[i]
        row.cells[0].paragraphs[0].add_run(campo).bold = True
        row.cells[1].paragraphs[0].add_run(valor)
            
    doc.add_paragraph("\n")
    doc.add_heading("I. Secuencia Didáctica de la Sesión", level=1)
    doc.add_paragraph().add_run("• INICIO:\n").bold = True; doc.paragraphs[-1].add_run(inicio_editable)
    doc.add_paragraph().add_run("• DESARROLLO:\n").bold = True; doc.paragraphs[-1].add_run(desarrollo_editable)
    doc.add_paragraph().add_run("• CIERRE:\n").bold = True; doc.paragraphs[-1].add_run(cierre_editable)
    
    doc.add_paragraph("\n")
    doc.add_heading("II. Recursos y Materiales Pedagógicos", level=1)
    doc.add_paragraph().add_run("Materiales seleccionados: ").bold = True; doc.paragraphs[-1].add_run(recursos_editable)
    
    doc.add_paragraph("\n")
    doc.add_heading("III. Diversificación de la Enseñanza (DUA)", level=1)
    doc.add_paragraph().add_run("Estrategias de atención a la diversidad: ").bold = True; doc.paragraphs[-1].add_run(dua_editable)
    
    doc.add_paragraph("\n")
    doc.add_heading("IV. Estrategia de Evaluación Formativa", level=1)
    doc.add_paragraph().add_run("• Indicador de Logro: ").bold = True; doc.paragraphs[-1].add_run(indicador_editable)
    doc.add_paragraph().add_run("• Instrumento: ").bold = True; doc.paragraphs[-1].add_run(instrumento_editable)

    doc.add_paragraph("\n")
    doc.add_heading("V. Observaciones y Bitácora Docente", level=1)
    doc.add_paragraph().add_run("Notas de aplicación: ").bold = True; doc.paragraphs[-1].add_run(obs_editable)
    
    b_documento = BytesIO(); doc.save(b_documento); b_documento.seek(0)

    # 2. GUÍA ESTUDIANTE
    doc_guia = Document()
    for section in doc_guia.sections:
        section.top_margin = Cm(2.0); section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(2.0); section.right_margin = Cm(2.0)

    if os.path.exists("logosute.jpg"):
        p_logo_g = doc_guia.add_paragraph(); p_logo_g.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo_g.add_run().add_picture("logosute.jpg", width=Inches(1.0))

    p_tg = doc_guia.add_paragraph(); p_tg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tg.add_run(f"GUÍA DE TRABAJO Y EVALUACIÓN FORMATIVA\n{asignatura_sel.upper()} — {curso_sel.upper()}\n({unidad_didactica} - {num_sesion})").font.bold = True

    doc_guia.add_paragraph("\n")
    t_est = doc_guia.add_table(rows=2, cols=2); t_est.style = 'Table Grid'
    t_est.rows[0].cells[0].paragraphs[0].add_run("Nombre del Estudiante: ").bold = True
    t_est.rows[0].cells[1].paragraphs[0].add_run(f"Fecha: {fecha_clase}").bold = True
    t_est.rows[1].cells[0].paragraphs[0].add_run(f"Docente: {nombre_profesor}").bold = True
    t_est.rows[1].cells[1].paragraphs[0].add_run(f"Curso: {curso_sel}").bold = True

    doc_guia.add_paragraph("\n")
    p_oa_est = doc_guia.add_paragraph()
    p_oa_est.add_run("🎯 Objetivo de Aprendizaje: ").bold = True; p_oa_est.add_run(oa_sel_texto)

    doc_guia.add_paragraph("\n--- DESARROLLO DE LA GUÍA ---")
    p_g1 = doc_guia.add_paragraph(); p_g1.add_run("1. ").bold = True; p_g1.add_run(guia_p1)
    for _ in range(4): doc_guia.add_paragraph("_________________________________________________________________________________")

    doc_guia.add_paragraph("\n")
    p_g2 = doc_guia.add_paragraph(); p_g2.add_run("2. ").bold = True; p_g2.add_run(guia_p2)
    for _ in range(4): doc_guia.add_paragraph("_________________________________________________________________________________")

    doc_guia.add_paragraph("\n---------------------------------------------------------------------------------")
    p_tick_title = doc_guia.add_paragraph(); p_tick_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tick_title.add_run("✂️ TICKET DE SALIDA (Para entregar al finalizar la clase)").bold = True

    p_tick_body = doc_guia.add_paragraph(); p_tick_body.add_run(guia_ticket)
    for _ in range(3): doc_guia.add_paragraph("_________________________________________________________________________________")

    b_guia = BytesIO(); doc_guia.save(b_guia); b_guia.seek(0)

    # 3. PAUTA DE COTEJO
    doc_pauta = Document()
    for section in doc_pauta.sections:
        section.top_margin = Cm(2.0); section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(2.0); section.right_margin = Cm(2.0)

    if os.path.exists("logosute.jpg"):
        p_logo_p = doc_pauta.add_paragraph(); p_logo_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo_p.add_run().add_picture("logosute.jpg", width=Inches(1.0))

    p_tp = doc_pauta.add_paragraph(); p_tp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tp.add_run(f"PAUTA DE COTEJO Y EVALUACIÓN FORMATIVA\n{asignatura_sel.upper()} — {curso_sel.upper()}\n({unidad_didactica} - {num_sesion})").font.bold = True

    doc_pauta.add_paragraph("\n")
    t_est_p = doc_pauta.add_table(rows=2, cols=2); t_est_p.style = 'Table Grid'
    t_est_p.rows[0].cells[0].paragraphs[0].add_run("Estudiante: ").bold = True
    t_est_p.rows[0].cells[1].paragraphs[0].add_run(f"Fecha: {fecha_clase}").bold = True
    t_est_p.rows[1].cells[0].paragraphs[0].add_run(f"Docente: {nombre_profesor}").bold = True
    t_est_p.rows[1].cells[1].paragraphs[0].add_run(f"Curso: {curso_sel}").bold = True

    doc_pauta.add_paragraph("\n")
    p_oa_p = doc_pauta.add_paragraph(); p_oa_p.add_run("🎯 Objetivo Evaluado: ").bold = True; p_oa_p.add_run(oa_sel_texto)

    doc_pauta.add_paragraph("\n")
    tabla_rub = doc_pauta.add_table(rows=5, cols=4); tabla_rub.style = 'Table Grid'
    encabezados = ["Criterio de Evaluación", "Logrado (3 pts)", "En Desarrollo (2 pts)", "Por Lograr (1 pt)"]
    for j, enc in enumerate(encabezados): tabla_rub.rows[0].cells[j].paragraphs[0].add_run(enc).bold = True

    criterios = [
        ("1. Comprensión Conceptual", "Explica con claridad el concepto principal del OA.", "Demuestra comprensión parcial; requiere apoyo.", "Presenta confusiones en conceptos básicos."),
        ("2. Aplicación Práctica", "Resuelve la guía de ejercicios de manera autónoma.", "Resuelve la mayoría con mediación del docente.", "No logra resolver los ejercicios."),
        ("3. Actitud y Trabajo (OAT)", "Demuestra rigor, perseverancia y respeto continuo.", "Mantiene atención a ratos o requiere llamados.", "Muestra desinterés o interrumpe."),
        ("4. Ticket de Salida", "Sintetiza la lección de forma pertinente.", "Responde el ticket de forma incompleta.", "No entrega el ticket de salida.")
    ]
    for i, (crit, log, dev, por) in enumerate(criterios, start=1):
        row = tabla_rub.rows[i]
        row.cells[0].paragraphs[0].add_run(crit).bold = True
        row.cells[1].paragraphs[0].add_run(log)
        row.cells[2].paragraphs[0].add_run(dev)
        row.cells[3].paragraphs[0].add_run(por)

    doc_pauta.add_paragraph("\n")
    t_res = doc_pauta.add_table(rows=1, cols=2); t_res.style = 'Table Grid'
    t_res.rows[0].cells[0].paragraphs[0].add_run("Puntaje Total Obtenido: _______ / 12 pts").bold = True
    t_res.rows[0].cells[1].paragraphs[0].add_run("Calificación / Formato: ____________").bold = True

    b_pauta = BytesIO(); doc_pauta.save(b_pauta); b_pauta.seek(0)

    # SECCIÓN DE DESCARGA Y GUARDADO
    st.markdown("---")
    st.markdown('<div class="section-header">📥 6. Descarga y Compartir en el Banco Colaborativo</div>', unsafe_allow_html=True)
    
    if st.button("🤝 Compartir esta Clase en el Banco Colaborativo", use_container_width=True):
        historial.append({
            "fecha": str(fecha_clase), "profesor": nombre_profesor, "asignatura": asignatura_sel,
            "curso": curso_sel, "unidad": unidad_didactica, "num_sesion": num_sesion,
            "nivel": nivel_dificultad, "oa": oa_sel_texto, "inicio": inicio_editable,
            "desarrollo": desarrollo_editable, "cierre": cierre_editable
        })
        guardar_historial(historial)
        st.success("¡Gracias por colaborar! Tu clase ha sido agregada al Banco Colaborativo de la comunidad.")
        st.rerun()

    st.markdown("\n")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button("💾 Planificación (.docx)", b_documento, f"Planificacion_{asignatura_sel.replace(' ','')}_{curso_sel.replace(' ','')}.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
    with col2:
        st.download_button("📄 Guía + Ticket (.docx)", b_guia, f"GuiaEstudiante_{asignatura_sel.replace(' ','')}_{curso_sel.replace(' ','')}.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
    with col3:
        st.download_button("📊 Pauta Cotejo (.docx)", b_pauta, f"PautaCotejo_{asignatura_sel.replace(' ','')}_{curso_sel.replace(' ','')}.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)

    st.markdown("\n")
    st.components.v1.html('<button class="print-btn" onclick="window.parent.print()">🖨️ Imprimir / Vista Previa en Pantalla</button>', height=60)