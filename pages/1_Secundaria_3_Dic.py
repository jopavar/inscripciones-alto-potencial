import re
import requests
import streamlit as st

st.set_page_config(
    page_title="Inscripción Secundaria - 3 Diciembre",
    page_icon="📝",
    layout="centered"
)

try:
    st.image("logo_uadtc.png", width=200)
except Exception:
    pass

st.title("Segundo Encuentro Nacional Estudiantil de Alto Potencial")
st.subheader("Nuestro potencial transforma el mañana")
st.markdown("### 📅 Inscripción: Martes 3 de Diciembre")
st.info("**Población:** III Ciclo y Educación Diversificada (Secundaria)")
st.markdown("---")

POWER_AUTOMATE_URL = "https://4f10c0e245d2e70ca4e4448633670a.07.environment.api.powerplatform.com/powerautomate/automations/direct/cu/08/workflows/b102d09bd7684c489f9f9a4d422eb6eb/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=d0pWqfe49kB47jEU1WnjVsjF7bIztflpUvH3mz1IxxQ"

TALLERES_SECUNDARIA = [
    "Taller de Robótica: Nivel Inicial",
    "Taller de Robótica: Nivel Intermedio",
    "Matletas en Acción (III Ciclo): El Arte del razonamiento matemático en el mundo Olímpico",
    "Matletas en Acción (Educación Diversificada): El Arte del razonamiento matemático en el mundo Olímpico",
    "Recorrido Histórico por Medio del Arte",
    "Astronomía: ¡Descubre los secretos del Universo!",
]

taller_seleccionado = st.selectbox("Seleccione el Taller disponible:", TALLERES_SECUNDARIA)

with st.form("form_secundaria"):
    nombre = st.text_input("Nombre completo del estudiante:")
    cedula = st.text_input("Número de cédula (9 dígitos sin guiones ni espacios):", placeholder="153650125")
    correo = st.text_input("Correo electrónico de contacto:")
    
    submitted = st.form_submit_button("Completar Inscripción")

    if submitted:
        cedula_clean = cedula.strip()

        if not nombre or not cedula_clean or not correo:
            st.error("Por favor completa todos los campos obligatorios.")
        elif not re.fullmatch(r"^\d{9}$", cedula_clean):
            st.error("El formato de la cédula debe contener exactamente 9 dígitos numéricos.")
        else:
            payload = {
                "nombre": nombre,
                "cedula": cedula_clean,
                "correo": correo,
                "jornada": "Martes 3 de diciembre: Secundaria",
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
                    st.error(f"Error de conexión: {e}")
