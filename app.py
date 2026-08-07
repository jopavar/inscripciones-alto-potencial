import streamlit as st
import requests

st.set_page_config(page_title="Inscripción Talleres", page_icon="📝", layout="centered")

st.title("📝 Formulario de Inscripción a Talleres")
st.subheader("Encuentro Estudiantil de Alto Potencial")

POWER_AUTOMATE_URL = "https://4f10c0e245d2e70ca4e4448633670a.07.environment.api.powerplatform.com/powerautomate/automations/direct/cu/08/workflows/b102d09bd7684c489f9f9a4d422eb6eb/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=d0pWqfe49kB47jEU1WnjVsjF7bIztflpUvH3mz1IxxQ"

# 1. Selección de Jornada fuera del formulario para permitir filtrado dinámico
jornada = st.radio(
    "Seleccione la Jornada:",
    [
        "Día 1: Secundaria (III Ciclo y Educación Diversificada)",
        "Día 2: Primaria (I y II Ciclo)"
    ]
)

# 2. Filtrado dependiente según la jornada elegida
if "Secundaria" in jornada:
    opciones_talleres = [
        "Robótica Inicial",
        "Robótica Intermedia",
        "Talento Matemático Secundaria 1",
        "Talento Matemático Secundaria 2",
        "Recorrido Histórico por Medio del Arte",
        "Astronomía 1",
        "Astronomía 2"
    ]
else:
    opciones_talleres = [
        "Talento Matemático Primaria 1",
        "Talento Matemático Primaria 2",
        "Recorrido Histórico por Medio del Arte",
        "Astronomía 1",
        "Astronomía 2"
    ]

# 3. Formulario principal
with st.form("form_inscripcion"):
    nombre = st.text_input("Nombre completo:")
    cedula = st.text_input("Número de cédula:")
    correo = st.text_input("Correo electrónico:")
    
    taller = st.selectbox("Seleccione el Taller disponible para la jornada:", opciones_talleres)
    
    submitted = st.form_submit_button("Completar Inscripción")
    
    if submitted:
        if not nombre or not cedula or not correo:
            st.error("Por favor completa todos los campos obligatorios.")
        else:
            payload = {
                "nombre": nombre,
                "cedula": cedula,
                "correo": correo,
                "jornada": jornada,
                "taller": taller
            }
            
            with st.spinner("Procesando inscripción..."):
                try:
                    response = requests.post(POWER_AUTOMATE_URL, json=payload)
                    if response.status_code == 200:
                        st.success("¡Inscripción realizada con éxito! Se ha enviado un correo de confirmación.")
                    else:
                        st.error(f"Error al procesar la solicitud: {response.text}")
                except Exception as e:
                    st.error(f"Ocurrió un error al conectar con el servidor: {e}")
