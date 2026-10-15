import re
import requests
import streamlit as st

st.set_page_config(
    page_title="Inscripción Talleres", page_icon="📝", layout="centered"
)

# Encabezado oficial del evento
st.title("Segundo Encuentro Nacional Estudiantil de Alto Potencial")
st.subheader("Nuestro potencial transforma el mañana")
st.caption("📝 Formulario de Inscripción a Talleres")
st.markdown("---")

POWER_AUTOMATE_URL = "https://4f10c0e245d2e70ca4e4448633670a.07.environment.api.powerplatform.com/powerautomate/automations/direct/cu/08/workflows/b102d09bd7684c489f9f9a4d422eb6eb/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=d0pWqfe49kB47jEU1WnjVsjF7bIztflpUvH3mz1IxxQ"

# Distribución de talleres por jornada
TALLERES_POR_JORNADA = {
    "Día 1: Secundaria (III Ciclo y Educación Diversificada)": [
        "Taller de Robótica: Nivel Inicial",
        "Taller de Robótica: Nivel Intermedio",
        "Matletas en Acción (III Ciclo): El Arte del razonamiento matemático en el mundo Olímpico",
        "Matletas en Acción (Educación Diversificada): El Arte del razonamiento matemático en el mundo Olímpico",
        "Recorrido Histórico por Medio del Arte",
        "Astronomía: ¡Descubre los secretos del Universo!",
    ],
    "Día 2: Primaria (I y II Ciclo)": [
        "Robótica Inicial",
        "Robótica Intermedia",
        "Taller de Matemática para I Ciclo: ¡Aventuras con los números!",
        "Taller de Matemática para II Ciclo: ¡Desafío mental: juegos, enigmas y estrategias!",
        "Recorrido Histórico por Medio del Arte",
        "Astronomía: ¡Vamos a conocer otros mundos!",
    ],
}

# 1. Selección de Jornada (fuera del formulario)
jornada = st.radio(
    "Seleccione la Jornada:",
    list(TALLERES_POR_JORNADA.keys()),
    key="jornada_radio",
)

# 2. Selección del Taller filtrado según la jornada activa
opciones_talleres = TALLERES_POR_JORNADA[jornada]
taller_seleccionado = st.selectbox(
    "Seleccione el Taller disponible:",
    opciones_talleres,
    key=f"taller_{jornada}",
)

# 3. Formulario principal para la recolección de datos
with st.form("form_inscripcion"):
    nombre = st.text_input("Nombre completo:")

    cedula = st.text_input(
        "Número de cédula (Formato de 9 dígitos sin guiones ni espacios, ej."
        " 153650125):",
        placeholder="153650125",
    )

    correo = st.text_input("Correo electrónico:")

    submitted = st.form_submit_button("Completar Inscripción")

    if submitted:
        cedula_clean = cedula.strip()

        if not nombre or not cedula_clean or not correo:
            st.error("Por favor completa todos los campos obligatorios.")

        elif not re.fullmatch(r"^\d{9}$", cedula_clean):
            st.error(
                "El formato de la cédula no es válido. Debe ingresar"
                " exactamente 9 dígitos numéricos sin guiones ni espacios"
                " (ejemplo: 153650125)."
            )

        else:
            payload = {
                "nombre": nombre,
                "cedula": cedula_clean,
                "correo": correo,
                "jornada": jornada,
                "taller": taller_seleccionado,
            }

            with st.spinner("Procesando inscripción..."):
                try:
                    response = requests.post(POWER_AUTOMATE_URL, json=payload)
                    if response.status_code == 200:
                        st.success(
                            "¡Inscripción realizada con éxito! Se ha enviado"
                            " un correo de confirmación."
                        )
                    else:
                        st.error(
                            f"Error al procesar la solicitud: {response.text}"
                        )
                except Exception as e:
                    st.error(
                        f"Ocurrió un error al conectar con el servidor: {e}"
                    )
