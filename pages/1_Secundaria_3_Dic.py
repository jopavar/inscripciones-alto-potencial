import streamlit as st
import requests

st.set_page_config(
    page_title="Inscripción Secundaria - II Encuentro Nacional",
    page_icon="🎓",
    layout="centered"
)

st.title("II Encuentro Nacional Estudiantil de Alto Potencial")
st.subheader("Jornada de Secundaria — Jueves 3 de diciembre de 2026")
st.markdown("**Sede:** Universidad Latina de Costa Rica, Sede San Pedro")

st.divider()

# ==============================================================================
# BLOQUEO DE INSCRIPCIONES PARA SECUNDARIA
# Para reactivar el formulario, elimina o comenta las siguientes dos líneas:
# ==============================================================================
st.warning("🔒 Las inscripciones para la jornada de Secundaria (3 de diciembre) se encuentran cerradas.")
st.stop()

# ==============================================================================
# CÓDIGO DEL FORMULARIO (Inactivo mientras st.stop() esté presente arriba)
# ==============================================================================
WEBHOOK_URL = st.secrets.get("WEBHOOK_URL", "")

TALLERES_SECUNDARIA = [
    "Taller de Robótica (Principiantes): Mentes en código: IA en acción",
    "Taller de Robótica (Intermedio): Laboratorio de inventos: ¡Cocodrilos con circuitos!",
    "Matletas en Acción (Educación Diversificada): El Arte del razonamiento matemático en el mundo Olímpico",
    "Matletas en Acción (III Ciclo): El Arte del razonamiento matemático en el mundo Olímpico",
    "Realidad Virtual (III Ciclo): Creando soluciones juntos",
    "Astrofísica (III Ciclo y Educación Diversificada): ¡Descubre los secretos del Universo!"
]

if "taller_secundaria" not in st.session_state:
    st.session_state.taller_secundaria = TALLERES_SECUNDARIA[0]

taller_seleccionado = st.selectbox(
    "Seleccione el Taller disponible:",
    options=TALLERES_SECUNDARIA,
    key="taller_secundaria"
)

with st.form("form_inscripcion_secundaria"):
    nombre = st.text_input("Nombre completo del estudiante:")
    cedula = st.text_input("Número de cédula (sin guiones ni espacios):")
    correo = st.text_input("Correo electrónico de contacto:")
    
    submitted = st.form_submit_button("Completar Inscripción")

    if submitted:
        if not nombre.strip() or not cedula.strip() or not correo.strip():
            st.error("Por favor, complete todos los campos obligatorios.")
        elif not WEBHOOK_URL:
            st.error("Error de configuración: No se encontró la URL del servicio de registro.")
        else:
            payload = {
                "nombre": nombre.strip(),
                "cedula": cedula.strip(),
                "correo": correo.strip(),
                "taller": taller_seleccionado.strip(),
                "jornada": "Jueves 3 de diciembre: Secundaria"
            }
            
            with st.spinner("Procesando inscripción..."):
                try:
                    response = requests.post(WEBHOOK_URL, json=payload, timeout=30)
                    if response.status_code == 200:
                        st.success("¡Inscripción realizada con éxito! Revise su correo electrónico para confirmar los detalles.")
                    elif response.status_code == 409:
                        st.warning(response.text or "El estudiante ya se encuentra inscrito o el taller alcanzó su cupo máximo.")
                    else:
                        st.error(f"Error al procesar la solicitud: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error de conexión con el servidor: {e}")
