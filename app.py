import re
import requests
import streamlit as st

st.set_page_config(
    page_title="Inscripción Talleres", page_icon="📝", layout="centered"
)

st.title("📝 Formulario de Inscripción a Talleres")
st.subheader("Encuentro Estudiantil de Alto Potencial")

POWER_AUTOMATE_URL = "https://4f10c0e245d2e70ca4e4448633670a.07.environment.api.powerplatform.com/powerautomate/automations/direct/cu/08/workflows/b102d09bd7684c489f9f9a4d422eb6eb/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=d0pWqfe49kB47jEU1WnjVsjF7bIztflpUvH3mz1IxxQ"

# Mapeo estricto de talleres por jornada
TALLERES_POR_JORNADA = {
    "Día 1: Secundaria (III Ciclo y Educación Diversificada)": [
        "Robótica Inicial",
        "Robótica Intermedia",
        "Talento Matemático Secundaria 1",
        "Talento Matemático Secundaria 2",
        "Recorrido Histórico por Medio del Arte",
        "Astronomía 1",
        "Astronomía 2",
    ],
    "Día 2: Primaria (I y II Ciclo)": [
        "Talento Matemático Primaria 1",
        "Talento Matemático Primaria 2",
        "Recorrido Histórico por Medio del Arte",
        "Astronomía 1",
        "Astronomía 2",
    ],
}

# 1. Selección de Jornada (fuera del formulario)
jornada = st.radio(
    "Seleccione la Jornada:",
    list(TALLERES_POR_JORNADA.keys()),
    key="jornada_radio",
)

opciones_talleres = TALLERES_POR_JORNADA[jornada]

# 2. Formulario principal
with st.form("form_inscripcion"):
    nombre = st.text_input("Nombre completo:")

    # Indicación explícita de formato para la cédula
    cedula = st.text_input(
        "Número de cédula:",
        placeholder="1203407684",
        help="Ingrese la cédula en formato de 9 dígitos continuos, sin guiones ni espacios.",
    )

    correo = st.text_input("Correo electrónico:")

    taller = st.selectbox(
        "Seleccione el Taller disponible:",
        opciones_talleres,
        key=f"taller_{jornada}",
    )

    submitted = st.form_submit_button("Completar Inscripción")

    if submitted:
        # Limpiar espacios accidentales al inicio o final
        cedula_clean = cedula.strip()

        # Validación de campos obligatorios
        if not nombre or not cedula_clean or not correo:
            st.error("Por favor completa todos los campos obligatorios.")

        # Validación estricta del formato de cédula (exactamente 9 números)
        elif not re.fullmatch(r"^\d{9}$", cedula_clean):
            st.error(
                "El formato de la cédula no es válido. Debe contener exactamente"
                " 9 dígitos numéricos sin guiones ni espacios (ejemplo:"
                " 1203407684)."
            )

        else:
            payload = {
                "nombre": nombre,
                "cedula": cedula_clean,
                "correo": correo,
                "jornada": jornada,
                "taller": taller,
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
