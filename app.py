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
tab_calc, tab_guia = st.tabs(["🧮 Calculadora Bone-RADS", "📖 Guía: Márgenes y Periostio"])

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
# PESTAÑA 2: GUÍA ORIENTADORA (MÁRGENES Y REACCIÓN PERIÓSTICA)
# ==============================================================================
with tab_guia:
    st.header("📖 Guía de Orientación Diagnóstica")
    st.write("Consulte los criterios morfológicos del sistema modificado de **Lodwick-Madewell** y los patrones de **reacción perióstica** para realizar una clasificación certera.")

    st.markdown("---")

    # SECCIÓN MÁRGENES
    st.subheader("1. Clasificación de Márgenes (Lodwick-Madewell Modificado)")
    
    with st.expander("📌 **Grado IA: Geográfico con borde esclerótico (1 Ppto)**", expanded=True):
        st.write("""
        - **Características:** Lesión lítica con límites perfectamente definidos por un halo denso y esclerótico de hueso reactivo (zona de transición extremadamente estrecha).
        - **Significado Biológico:** Crecimiento muy lento e indolente que le permite al hueso huésped formar una barrera ósea madura.
        - **Ejemplos Típicos:** Fibroma no osificante (NOF), Quiste óseo simple, Encondroma maduro.
        """)

    with st.expander("📌 **Grado IB: Geográfico sin borde esclerótico (3 Ptos)**"):
        st.write("""
        - **Características:** Lesión lítica nítidamente demarcada, con borde cortante, pero **sin halo de esclerosis periférica**.
        - **Significado Biológico:** Lesión de crecimiento lento o moderado; el hueso no llega a formar un halo esclerótico denso pero mantiene delimitado el frente del tumor.
        - **Ejemplos Típicos:** Tumor de células gigantes, Quiste óseo aneurismático, Encondroma sin pared esclerótica.
        """)

    with st.expander("📌 **Grado II: Geográfico mal definido / Zona amplia de transición (5 Ptos)**"):
        st.write("""
        - **Características:** Lesión geográfica cuyos bordes no son nítidos; presenta una zona de transición ancha donde no es posible precisar exactamente el límite entre hueso sano y enfermo.
        - **Significado Biológico:** Crecimiento localmente agresivo o intermedio.
        - **Ejemplos Típicos:** Condrosarcoma de bajo grado, Fibroma desmoplásico, Osteoblastoma agresivo, Mieloma.
        """)

    with st.expander("📌 **Grado IIIA-C: No Geográfico / Permeativo / Cambiante (7 Ptos)**"):
        st.write("""
        - **IIIA (Cambio Activo):** Lesión previamente estable bien definida que desarrolla una zona permeable o mal definida (sugiere transformación maligna).
        - **IIIB (Carcomido / Permeativo):** Múltiples áreas líticas diminutas, agujeradas o permeantes que coalescen, con destrucción cortical masiva.
        - **IIIC (Oculto / Incalculable):** Avance tumoral medular rápido por el canal sin destrucción ósea visible inicial en radiografía.
        - **Ejemplos Típicos:** Osteosarcoma, Sarcoma de Ewing, Metástasis destructivas, Linfoma óseo.
        """)

    st.markdown("---")

    # SECCIÓN REACCIÓN PERIÓSTICA
    st.subheader("2. Patrones de Reacción Perióstica")

    col_no_agr, col_agr = st.columns(2)

    with col_no_agr:
        st.markdown("#### **No Agresiva (2 Ptos)**")
        st.write("""
        Indica procesos crónicos, indolentes o lentos donde el periostio tiene tiempo de formar hueso maduro:
        
        * **Capa Sólida / Continua:** Engrosamiento cortical corticalizado y homogéneo adyacente a la lesión.
        * **Remodelación / Neocorteza:** Expansión suave de la cortical donde el periostio forma una caparazón cortical delgada pero entera.
        """)

    with col_agr:
        st.markdown("#### **Agresiva (4 Ptos)**")
        st.write("""
        Indica avance tumoral rápido donde el ritmo del tumor sobrepasa la capacidad de reparación del periostio:
        
        * **Lamelar / Capas de cebolla:** Múltiples capas concéntricas interrumpidas (ej. Sarcoma de Ewing).
        * **Espiculada Paralela ("En cepillo" / *Hair-on-end*):** Espículas perpendiculares al eje cortical.
        * **Espiculada Divergente ("Sol Naciente" / *Sunburst*):** Espículas en abanico radiating hacia partes blandas.
        * **Triángulo de Codman:** Levantamiento agudo del periostio con rotura central por la masa tumoral.
        """)

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
