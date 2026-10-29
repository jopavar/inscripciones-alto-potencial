with st.form("form_secundaria"):
    # Se agrega key="taller_sec_key"
    taller_seleccionado = st.selectbox(
        "Seleccione el Taller disponible:", 
        TALLERES_SECUNDARIA,
        key="taller_sec_key"
    )
    
    nombre = st.text_input("Nombre completo del estudiante:")
    cedula = st.text_input("Número de cédula (9 dígitos sin guiones ni espacios):", placeholder="153650125")
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
                "jornada": "Jueves 3 de diciembre: Secundaria",
                # LEER DIRECTAMENTE DESDE SESSION STATE
                "taller": st.session_state["taller_sec_key"],
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
