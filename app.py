import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Calculadora y Guía ACR Bone-RADS",
    page_icon="🦴",
    layout="centered"
)

st.title("🦴 Sistema ACR Bone-RADS")
st.caption("Estratificación de riesgo de lesiones óseas en radiografía convencional (Caracciolo et al., 2023)")

# Pestañas principales de la App
tab_calc, tab_guia = st.tabs(["🧮 Calculadora Bone-RADS", "📖 Guía Visual (Figuras 1-5)"])

# ==============================================================================
# PESTAÑA 1: CALCULADORA INTERACTIVA
# ==============================================================================
with tab_calc:
    st.subheader("Estratificación del Riesgo")
    st.write("Seleccione las características morfológicas y clínicas observadas en el estudio radiológico.")

    # Opción para Bone-RADS 0
    es_incompleto = st.checkbox("⚠️ La lesión no se puede evaluar completamente (Ej. localización en esqueleto axial en Rx o estudio técnico inadecuado)")

    if es_incompleto:
        st.error("### Clasificación: **Bone-RADS 0** (Estudio Incompleto)")
        st.warning("**Recomendación:** Se requieren estudios adicionales de imagen (TC o RM) para caracterizar adecuadamente la lesión.")
    else:
        st.markdown("### 1. Criterios Radiológicos y Clínicos")

        # Margen
        margen = st.selectbox(
            "Bordes de la Lesión (Margen):",
            options=[
                ("Ninguno / Esclerosis difusa sin margen lítico claro", 0),
                ("IA: Geográfico bien definido con borde esclerótico", 1),
                ("IB: Geográfico bien definido sin borde esclerótico", 3),
                ("II: Geográfico con zona de transición ancha / mal definido", 5),
                ("III: No geográfico (carcomido / permeativo) o en cambio activo", 7)
            ],
            format_func=lambda x: x[0]
        )

        # Reacción Perióstica
        periostio = st.selectbox(
            "Reacción Perióstica:",
            options=[
                ("Ausente", 0),
                ("No agresiva (sólida, continua, engrosamiento cortical)", 2),
                ("Agresiva (multilamelada/capas de cebolla, espiculada, triángulo de Codman)", 4)
            ],
            format_func=lambda x: x[0]
        )

        # Erosión Endóstica
        erosion = st.selectbox(
            "Erosión Endóstica (Scalloping):",
            options=[
                ("Leve (ausente o < 25% del grosor cortical)", 0),
                ("Moderada (25% - 50% del grosor cortical)", 1),
                ("Profunda (> 50% del grosor cortical)", 2)
            ],
            format_func=lambda x: x[0]
        )

        # Fractura Patológica
        fractura = st.radio(
            "¿Presenta Fractura Patológica?",
            options=[("No", 0), ("Sí", 2)],
            format_func=lambda x: x[0],
            horizontal=True
        )

        # Masa de Tejidos Blandos
        m_blandos = st.radio(
            "¿Presenta Masa de Tejidos Blandos Extraósea?",
            options=[("No", 0), ("Sí", 4)],
            format_func=lambda x: x[0],
            horizontal=True
        )

        # Antecedente Oncológico
        cancer_previo = st.radio(
            "¿Tiene Antecedente de Cáncer Primario Conocido?",
            options=[("No", 0), ("Sí", 2)],
            format_func=lambda x: x[0],
            horizontal=True
        )

        # Cálculo de Puntuación
        puntuacion_total = margen[1] + periostio[1] + erosion[1] + fractura[1] + m_blandos[1] + cancer_previo[1]

        st.markdown("---")
        st.markdown("### 2. Clasificación y Recomendación")

        # Categorías Bone-RADS
        if puntuacion_total <= 2:
            categoria = "Bone-RADS 1"
            riesgo = "Riesgo Muy Bajo (< 2% Malignidad)"
            color = "green"
            manejo = "Si es asintomática: Alta o seguimiento de rutina.\nSi es sintomática: Valorar TC/RM o evaluación por ortopedia."
        elif puntuacion_total <= 4:
            categoria = "Bone-RADS 2"
            riesgo = "Riesgo Bajo (2% - 10% Malignidad)"
            color = "blue"
            manejo = "Seguimiento radiográfico a corto plazo (3 a 6 meses), o TC/RM para confirmar benignidad."
        elif puntuacion_total <= 6:
            categoria = "Bone-RADS 3"
            riesgo = "Riesgo Intermedio (10% - 50% Malignidad)"
            color = "orange"
            manejo = "Interconsulta con Oncología Ortopédica. Estudio avanzado con TC, RM o Gammagrafía y valoración de biopsia."
        else:
            categoria = "Bone-RADS 4"
            riesgo = "Riesgo Alto (> 50% Malignidad)"
            color = "red"
            manejo = "Maligno hasta demostrar lo contrario. Derivación urgente a Oncología Ortopédica, biopsia y estadificación."

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Puntuación Total", value=f"{puntuacion_total} pts")
        with col2:
            st.metric(label="Categoría", value=categoria)

        st.markdown(f"### Estimación: **:{color}[{riesgo}]**")
        st.info(f"**Conducta Recomendada:**\n\n{manejo}")


# ==============================================================================
# PESTAÑA 2: GUÍA VISUAL ORIENTADORA (FIGURAS 1 A 5)
# ==============================================================================
with tab_guia:
    st.header("📖 Guía de Orientación Diagnóstica")
    st.write("Consulte los criterios morfológicos del consenso ACR para caracterizar los márgenes y la reacción perióstica.")

    st.markdown("---")

    # FIGURA 1: MÁRGENES
    st.subheader("1. Márgenes de la Lesión (Lodwick-Madewell Modificado)")
    try:
        st.image("assets/figura1.png", caption="Figura 1: Sistema modificado de Lodwick-Madewell para la gradación de márgenes (IA, IB, II, IIIA, IIIB, IIIC).", use_container_width=True)
    except Exception:
        st.warning("⚠️ *Cargue 'figura1.png' en la carpeta 'assets/' para ver el diagrama.*")

    with st.expander("📌 **Detalles de Clasificación de Márgenes**"):
        st.write("""
        * **IA (1 Pto):** Geográfico, bien definido con borde esclerótico periférico.
        * **IB (3 Ptos):** Geográfico, bien definido sin borde esclerótico.
        * **II (5 Ptos):** Geográfico, mal definido / zona amplia de transición.
        * **IIIA-C (7 Ptos):** No geográfico, carcomido/permeativo o con cambio activo de comportamiento.
        """)

    st.markdown("---")

    # FIGURAS 2 Y 3: REMODELACIÓN Y PERIOSTIO
    st.subheader("2. Remodelación Ósea y Reacción Perióstica Inicial")
    
    col_f2, col_f3 = st.columns(2)
    with col_f2:
        try:
            st.image("assets/figura2.png", caption="Figura 2: Patrones no agresivos de remodelación cortical (a: lisa, b: tabicada, c: lobulada).", use_container_width=True)
        except Exception:
            st.info("💡 *Cargue 'figura2.png'*")
    with col_f3:
        try:
            st.image("assets/figura3.png", caption="Figura 3: Patrones con corteza intacta (a: capa sólida, b: Triángulo de Codman, c: lamelar/cebolla).", use_container_width=True)
        except Exception:
            st.info("💡 *Cargue 'figura3.png'*")

    st.markdown("---")

    # FIGURAS 4 Y 5: PATRONES AGRESIVOS Y COMPLEJOS
    st.subheader("3. Patrones Periósticos Agresivos y Mixtos")
    
    col_f4, col_f5 = st.columns(2)
    with col_f4:
        try:
            st.image("assets/figura4.png", caption="Figura 4: Patrones agresivos (a: espiculado paralelo / hair-on-end, b: divergente / sunburst).", use_container_width=True)
        except Exception:
            st.info("💡 *Cargue 'figura4.png'*")
    with col_f5:
        try:
            st.image("assets/figura5.png", caption="Figura 5: Patrones mixtos/complejos (a: espiculado con Codman, b: lamelar y paralelo).", use_container_width=True)
        except Exception:
            st.info("💡 *Cargue 'figura5.png'*")

# ==============================================================================
# FOOTER Y REFERENCIA BIBLIOGRÁFICA
# ==============================================================================
st.markdown("---")
st.subheader("📚 Referencia Bibliográfica")
st.markdown("""
> Caracciolo, J., Ali, S., Chang, C. Y., Degnan, A., Flemming, D., Henderson, E. R., Kransdorf, M., Letson, G., & Murphey, M. (2023). **Bone Tumor Risk Stratification and Management System: A Consensus Guideline from the ACR Bone Reporting and Data System Committee**. *Journal of the American College of Radiology: JACR*, 20(11), 1134–1147.  
> 🔗 **DOI:** [https://doi.org/10.1016/j.jacr.2023.07.017](https://doi.org/10.1016/j.jacr.2023.07.017)
""")

st.caption("Aviso legal: Esta herramienta es puramente de apoyo educativo y clínico, no reemplaza el criterio ni la interpretación médica profesional.")
