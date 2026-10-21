import streamlit as st

st.set_page_config(page_title="II Encuentro Estudiantil UADTC", page_icon="👋", layout="centered")

try:
    st.image("logo_uadtc.png", width=220)
except Exception:
    pass

st.title("Segundo Encuentro Nacional Estudiantil de Alto Potencial")
st.subheader("Nuestro potencial transforma el mañana")
st.markdown("---")

st.markdown("### Bienvenido al Portal de Inscripciones")
st.write("Por favor seleccione la jornada correspondiente a su nivel educativo en el menú lateral izquierdo o mediante los botones a continuación:")

col1, col2 = st.columns(2)

with col1:
    st.info("**Secundaria (III Ciclo y Diversificada)**")
    st.write("📅 Martes 3 de Diciembre")
    st.page_link("pages/1_Secundaria_3_Dic.py", label="Ir a Formulario de Secundaria", icon="📝")

with col2:
    st.info("**Primaria (I y II Ciclo)**")
    st.write("📅 Miércoles 4 de Diciembre")
    st.page_link("pages/2_Primaria_4_Dic.py", label="Ir a Formulario de Primaria", icon="📝")
