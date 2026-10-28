import re
import requests
import streamlit as st

# Configuración de página e intencionalidad de colapsar la barra lateral
st.set_page_config(
    page_title="Inscripción Primaria - 4 Diciembre",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Inyección CSS para ocultar completamente la barra de navegación lateral
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

# Encabezado con título a la izquierda y logo a la derecha
col_titulo, col_logo = st.columns([3, 1])

with col_titulo:
    st.title("Segundo Encuentro Nacional Estudiantil de Alto Potencial")
    st.subheader("Nuestro potencial transforma el mañana")

with col_logo:
    try:
        st.image("logo_uadtc.png", use_container_width=True)
    except Exception:
        pass

st.markdown("### 📅 Inscripción: Viernes 4 de Diciembre")
st.info("**Población Objetivo:** I y II Ciclo (Primaria)")
st.markdown("---")

POWER_AUTOMATE_URL = "https://4f10c0e245d2e70ca4e4448633670a.07.environment.api.powerplatform.com/powerautomate/automations/direct/cu/08/workflows/b102d09bd7684c489f9f9a4d422eb6eb/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=d0pWqfe49kB47jEU1WnjVsjF7bIztflpUvH3mz1IxxQ"

TALLERES_PRIMARIA = [
    "Taller de Robótica: Pequeños Inventores, Grandes Robots ",
    "Taller de Robótica: Código Secreto: Misiones Robóticas",
    "Taller de Matemática (I Ciclo): Exploradores de Números y Secretos Matemáticos",
    "Taller de Matemática (II Ciclo): ¡Desafío mental: juegos, enigmas y estrategias!",
    "Explorando el cuerpo humano: Realidad Virtual, Creación 3D, Ciencias y Artes (Primaria)",
    "Astronomía (II Ciclo): ¡Vamos a conocer otros mundos!",
]

taller_seleccionado = st.selectbox("Seleccione el Taller disponible:", TALLERES_PRIMARIA)

with st.form("form_primaria"):
    nombre = st.text_input("Nombre completo del estudiante:")
    cedula = st.text_input(
        "Número de cédula (9 dígitos sin guiones ni espacios):",
        placeholder="153650125"
    )
    correo = st.text_input("Correo electrónico de contacto:")
    
    submitted = st.form_submit_button("Completar Inscripción")

    if submitted:
        cedula_clean = cedula.strip()

        if not nombre or not cedula_clean or not correo:
            st.error("Por favor completa todos los campos obligatorios.")
        elif not re.fullmatch(r"^\d{9}$", cedula_clean):
            st.error("El formato de la cédula debe contener exactamente 9 dígitos numéricos sin guiones ni espacios.")
        else:
            payload = {
                "nombre": nombre,
                "cedula": cedula_clean,
                "correo": correo,
                "jornada": "Viernes 4 de diciembre: Primaria",
                "taller": taller_seleccionado,
            }

            with st.spinner("Procesando inscripción..."):
                try:
                    response = requests.post(POWER_AUTOMATE_URL, json=payload)
                    if response.status_code == 200:
                        st.success("¡Inscripción realizada con éxito! Se ha enviado un correo de confirmación.")
                    else:
                        st.error(f"Error al procesar la solicitud: {response.text}")
                except Exception as e:
                    st.error(f"Error de conexión con el servidor: {e}")
