import re
import requests
import streamlit as st

st.set_page_config(
    page_title="Inscripción Secundaria - 3 Diciembre",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed" 
)

st.markdown(
    """
    <style>
        [data-testid="sidebar-nav-items"] {display: none !important;}
        [data-testid="collapsedControl"] {display: none !important;}
        section[data-testid="stSidebar"] {display: none !important;}
    </style>
    """,
    unsafe_allow_html=True
)

col_titulo, col_logo = st.columns([3, 1])

with col_titulo:
    st.title("Segundo Encuentro Nacional Estudiantil de Alto Potencial")
    st.subheader("Nuestro potencial transforma el mañana")

with col_logo:
    try:
        st.image("logo_uadtc.png", use_container_width=True)
    except Exception:
        pass

st.markdown("### 📅 Inscripción: Jueves 3 de Diciembre")
st.info("**Población Objetivo:** III Ciclo y Educación Diversificada (Secundaria)")
st.markdown("---")

POWER_AUTOMATE_URL = "https://4f10c0e245d2e70ca4e4448633670a.07.environment.api.powerplatform.com/powerautomate/automations/direct/cu/08/workflows/b102d09bd7684c489f9f9a4d422eb6eb/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=d0pWqfe49kB47jEU1WnjVsjF7bIztflpUvH3mz1IxxQ"

TALLERES_SECUNDARIA = [
    "Taller de Robótica: Mentes en código: IA en acción",
    "Taller de Robótica: Laboratorio de inventos: ¡Cocodrilos con circuitos! ",
    "Matletas en Acción (III Ciclo): El Arte del razonamiento matemático en el mundo Olímpico",
    "Matletas en Acción (Educación Diversificada): El Arte del razonamiento matemático en el mundo Olímpico",
    "Realidad Virtual (III Ciclo): Creando soluciones juntos",
    "Astronomía: ¡Descubre los secretos del Universo!",
]

# 1. EL SELECTBOX SE U BICA FUERA DEL FORMULARIO PARA REGISTRAR EL CAMBIO DE INMEDIATO
taller_seleccionado = st.selectbox(
    "Seleccione el Taller disponible:", 
    TALLERES_SECUNDARIA,
    index=None,
    placeholder="-- Seleccione un taller de la lista --",
    key="taller_secundario_state"
)

# 2. FORMULARIO ÚNICAMENTE PARA LOS CAMPOS DE TEXTO Y EL BOTÓN
with st.form("form_secundaria"):
    nombre = st.text_input("Nombre completo del estudiante:")
    cedula = st.text_input(
        "Número de cédula (9 dígitos sin guiones ni espacios):",
        placeholder="153650125"
    )
    correo = st.text_input("Correo electrónico de contacto:")
    
    submitted = st.form_submit_button("Completar Inscripción")

    if submitted:
        cedula_clean = cedula.strip()

        if not taller_seleccionado:
            st.error("Por favor seleccione un taller antes de continuar.")
        elif not nombre or not cedula_clean or not correo:
            st.error("Por favor completa todos los campos obligatorios.")
        elif not re.fullmatch(r"^\d{9}$", cedula_clean):
            st.error("El formato de la cédula debe contener exactamente 9 dígitos numéricos sin guiones ni espacios.")
        else:
            payload = {
                "nombre": nombre,
                "cedula": cedula_clean,
                "correo": correo,
                "jornada": "Jueves 3 de diciembre: Secundaria",
                "taller": taller_seleccionado,
            }

            with st.spinner("Procesando inscripción..."):
                try:
                    response = requests.post(POWER_AUTOMATE_URL, json=payload)
                    if response.status_code == 200:
                        st.success(f"¡Inscripción realizada con éxito! Taller registrado: {taller_seleccionado}")
                    else:
                        st.error(f"Error al procesar la solicitud: {response.text}")
                except Exception as e:
                    st.error(f"Error de conexión con el servidor: {e}")
