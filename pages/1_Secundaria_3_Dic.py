import base64
import re
from pathlib import Path

import requests
import streamlit as st


def logo_base64(nombre_archivo):
    """Busca el logo y lo devuelve codificado en base64 (o None si no existe)."""
    aqui = Path(__file__).resolve().parent
    for ruta in (aqui / nombre_archivo, aqui.parent / nombre_archivo, Path.cwd() / nombre_archivo):
        if ruta.exists():
            return base64.b64encode(ruta.read_bytes()).decode()
    return None


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

# ENCABEZADO: logos a la misma altura (MEP a la izquierda, UADTC a la derecha) y título centrado
ALTURA_LOGO = 110  # píxeles; cambia este valor para agrandar o reducir ambos logos

mep_b64 = logo_base64("logo_mep.png")
uadtc_b64 = logo_base64("logo_uadtc.png")

img_mep = f'<img src="data:image/png;base64,{mep_b64}" style="height:{ALTURA_LOGO}px;">' if mep_b64 else ""
img_uadtc = f'<img src="data:image/png;base64,{uadtc_b64}" style="height:{ALTURA_LOGO}px;">' if uadtc_b64 else ""

st.markdown(
    f"""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.5rem;">
        {img_mep}
        {img_uadtc}
    </div>
    <div style="text-align:center; margin-bottom:1rem;">
        <h1 style="font-size:2.1rem; line-height:1.25; margin:0; padding:0;">
            Segundo Encuentro Nacional Estudiantil de Alto Potencial
        </h1>
        <p style="font-size:1.25rem; font-style:italic; color:#555; margin:0.6rem 0 0 0;">
            Nuestro potencial transforma el mañana
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

if not mep_b64:
    st.warning("No se encontró el archivo logo_mep.png en el repositorio.")
if not uadtc_b64:
    st.warning("No se encontró el archivo logo_uadtc.png en el repositorio.")

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

# 1. EL SELECTBOX SE UBICA FUERA DEL FORMULARIO PARA REGISTRAR EL CAMBIO DE INMEDIATO
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
                    response = requests.post(POWER_AUTOMATE_URL, json=payload, timeout=30)
                    if response.status_code == 200:
                        st.success(f"¡Inscripción realizada con éxito! Taller registrado: {taller_seleccionado}")
                    else:
                        st.error(f"Error al procesar la solicitud: {response.text}")
                except Exception as e:
                    st.error(f"Error de conexión con el servidor: {e}")
