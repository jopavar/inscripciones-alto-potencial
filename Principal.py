import streamlit as st

st.set_page_config(
    page_title="II Encuentro Estudiantil UADTC",
    page_icon="👋",
    layout="centered"
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

st.markdown("---")

st.markdown("### Bienvenido al Portal Oficial de Inscripciones")
st.write(
    "Por favor seleccione la jornada correspondiente al nivel educativo del"
    " estudiante:"
)

col1, col2 = st.columns(2)

with col1:
    st.info("**Secundaria (III Ciclo y Diversificada)**")
    st.write("📅 Jueves 3 de Diciembre")
    st.page_link("pages/1_Secundaria_3_Dic.py", label="Ir a Formulario de Secundaria", icon="📝")

with col2:
    st.info("**Primaria (I y II Ciclo)**")
    st.write("📅 Viernes 4 de Diciembre")
    st.page_link("pages/2_Primaria_4_Dic.py", label="Ir a Formulario de Primaria", icon="📝")
