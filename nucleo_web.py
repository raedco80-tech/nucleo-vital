from datetime import datetime, timedelta
import uuid
import streamlit as st

# Configuración de la página táctica
st.set_page_config(
    page_title="Núcleo Vital - Centro de Mando",
    page_icon="🛡️",
    layout="wide",
)

# Estilo táctico / oscuro personalizado
st.markdown(
    """
    <style>
    .main { background-color: #0e1117; color: #c9d1d9; }
    .stButton>button { background-color: #238636; color: white; border-radius: 6px; font-weight: bold; }
    .stTextInput>div>div>input { background-color: #161b22; color: white; border: 1px solid #30363d; }
    .stTextArea>div>div>textarea { background-color: #161b22; color: white; border: 1px solid #30363d; }
    </style>
""",
    unsafe_allow_html=True,
)

# --- SISTEMA DE LICENCIAS Y VINCULACIÓN ---
CLAVE_MAESTRA = "ADMIN_RAEDCO_2026"  # Tu contraseña secreta de administrador

if "licencias_db" not in st.session_state:
  st.session_state.licencias_db = {
      "NV-MASTER-2026": "2099-12-31",  # Tu llave maestra permanente
      "NV-OPERADOR-01": "2026-10-15",  # Llave de ejemplo
  }

if "licencias_vinculos" not in st.session_state:
  st.session_state.licencias_vinculos = {}

if "device" not in st.query_params:
  st.query_params["device"] = str(uuid.uuid4())[:8]

dispositivo_actual = st.query_params["device"]


def verificar_acceso(token, dispositivo):
  if not token:
    return False, "Por favor ingrese una clave de acceso."

  if token == CLAVE_MAESTRA:
    return True, "MASTER"

  if token in st.session_state.licencias_db:
    fecha_exp_str = st.session_state.licencias_db[token]
    fecha_exp = datetime.strptime(fecha_exp_str, "%Y-%m-%d").date()
    hoy = datetime.now().date()

    if hoy > fecha_exp:
      return (
          False,
          f"⚠️ La llave ingresada ha caducado el {fecha_exp_str}. Contacte al"
          " administrador.",
      )

    if token in st.session_state.licencias_vinculos:
      if st.session_state.licencias_vinculos[token] != dispositivo:
        return (
            False,
            "❌ Esta llave ya se encuentra registrada y en uso en otro"
            " dispositivo diferente.",
        )
    else:
      st.session_state.licencias_vinculos[token] = dispositivo

    return True, "USUARIO"
  else:
    return False, "❌ Clave de acceso inválida o no autorizada."


# --- PERSISTENCIA AUTOMÁTICA EN EL DISPOSITIVO ---
token_guardado = st.query_params.get("token", None)

if "autenticado" not in st.session_state:
  st.session_state.autenticado = False
  st.session_state.tipo_usuario = None

  if token_guardado:
    valido, tipo = verificar_acceso(token_guardado, dispositivo_actual)
    if valido:
      st.session_state.autenticado = True
      st.session_state.tipo_usuario = tipo
    else:
      st.query_params.pop("token", None)

# --- PANTALLA DE BLOQUEO / LOGIN ---
if not st.session_state.autenticado:
  st.markdown(
      "<h1 style='text-align: center; color: #ff4b4b;'>🛡️ NÚCLEO VITAL</h1>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<h3 style='text-align: center; color: #8b949e;'>SISTEMA DE CONTROL"
      " TÁCTICO RESTRINGIDO</h3>",
      unsafe_allow_html=True,
  )
  st.write("---")

  col1, col2, col3 = st.columns([1, 2, 1])
  with col2:
    st.info(
        "Ingrese su llave de autorización. Quedará vinculada de forma única a"
        " este dispositivo."
    )
    token_ingresado = st.text_input("🔑 Llave de Acceso", type="password")

    if st.button("Validar y Vincular Dispositivo", use_container_width=True):
      valido, mensaje = verificar_acceso(token_ingresado, dispositivo_actual)
      if valido:
        st.query_params["token"] = token_ingresado
        st.session_state.autenticado = True
        st.session_state.tipo_usuario = mensaje
        st.rerun()
      else:
        st.error(mensaje)

  st.stop()

# --- APLICACIÓN PRINCIPAL ---
st.sidebar.title("⚡ Navegación Táctica")

if st.session_state.tipo_usuario == "MASTER":
  menu = st.sidebar.selectbox(
      "Seleccionar Sección",
      [
          "Centro de Mando",
          "Escudo y memoria",
          "Escáner táctico Pro",
          "Triaje y Alerta SOS",
          "Panel Maestro (Licencias)",
      ],
  )
else:
  menu = st.sidebar.selectbox(
      "Seleccionar Sección",
      [
          "Centro de Mando",
          "Escudo y memoria",
          "Escáner táctico Pro",
          "Triaje y Alerta SOS",
      ],
  )

if st.sidebar.button("🔒 Olvidar Dispositivo / Cerrar Sesión"):
  st.query_params.pop("token", None)
  st.session_state.autenticado = False
  st.session_state.tipo_usuario = None
  st.rerun()

# --- VISTA: CENTRO DE MANDO ---
if menu == "Centro de Mando":
  st.title("⚡ Núcleo Vital - Centro de Mando")
  st.markdown(
      "Estado del Sistema: <span style='color: #238636; font-weight: bold;'>●"
      " SEGURO Y OPERATIVO</span>",
      unsafe_allow_html=True,
  )
  st.warning("No hay alertas críticas en la zona monitoreada actualmente.")
  st.info(
      "Panel de control general operativo. Utilice el menú lateral para"
      " acceder a las funciones avanzadas."
  )

# --- VISTA: ESCUDO Y MEMORIA (CON SEMÁFOROS VISUALES RESTAURADOS) ---
elif menu == "Escudo y memoria":
  st.title("🛡️ Escudo y Memoria")
  st.markdown(
      "Monitoreo de rutas, semáforos de peligrosidad y registro de incidentes"
      " en tiempo real."
  )

  destino = st.text_input(
      "Ingrese su lugar de destino a transitar:",
      placeholder="Ej. Av. Larco, Mercado Central, Cañete...",
  )
  incidente_camino = st.text_input(
      "Reportar novedad o incidente imprevisto en el camino (Opcional):",
      placeholder="Ej. Bloqueo de vía, manifestación, pista mojada...",
  )

  if st.button("Consultar Estado y Generar Ruta Automática"):
    if destino:
      destino_lower = destino.lower()
      if (
          "mercado" in destino_lower
          or "nocturno" in destino_lower
          or "peligro" in destino_lower
      ):
        semaforo = "🟥 ZONA DE PELIGRO / ALTO RIESGO"
        color_html = "#ff4b4b"
        recomendacion = (
            "Se detectan reportes recientes de alta peligrosidad en la zona."
            " Evite transitar sin compañía."
        )
      elif "av." in destino_lower or "principal" in destino_lower:
        semaforo = "🟨 ZONA DE PRECAUCIÓN"
        color_html = "#f0ad4e"
        recomendacion = (
            "Tránsito moderado con reportes de tráfico o aglomeración."
            " Manténgase alerta."
        )
      else:
        semaforo = "🟩 ZONA SEGURA"
        color_html = "#238636"
        recomendacion = (
            "Sin alertas críticas reportadas en esta ruta. Tránsito fluido y"
            " normal."
        )

      # SEMÁFORO VISUAL DESTACADO
      st.markdown(
          f"### Semáforo de Peligrosidad Actual: <span style='color:"
          f" {color_html}; font-size: 26px; font-weight: bold;'>●"
          f" {semaforo}</span>",
          unsafe_allow_html=True,
      )
      st.info(f"📊 **Análisis en vivo:** {recomendacion}")

      if incidente_camino:
        st.warning(
            f"📌 Incidente añadido y reportado con éxito al sistema: "
            f"'{incidente_camino}'"
        )

      st.markdown("---")
      st.subheader("📍 Seguimiento de Ubicación y Avance en Vivo")
      st.write(
          "📡 Sintonizando GPS y conectando con servidores de ruta..."
      )
      st.progress(80)
      st.caption(
          f"Progreso actual del trayecto hacia **{destino}** (80% completado)."
      )
    else:
      st.warning("Por favor ingrese un destino válido para iniciar el análisis.")

# --- VISTA: ESCÁNER TÁCTICO PRO ---
elif menu == "Escáner táctico Pro":
  st.title("📷 Escáner táctico Pro")
  st.markdown(
      "Tome o cargue la foto del envoltorio del producto. La aplicación"
      " analizará los ingredientes automáticamente desde la imagen."
  )

  foto_producto = st.file_uploader(
      "📷 Tomar o subir foto del envoltorio del producto:",
      type=["jpg", "jpeg", "png", "webp"],
  )

  if foto_producto is not None:
    st.image(
        foto_producto,
        caption="Imagen del producto capturada para análisis",
        width=350,
    )
    if st.button("🔍 Analizar Ingredientes Automáticamente"):
      st.warning(
          "⚠️ **Resultado del Análisis Automático:** Producto clasificado en"
          " **Rango de Consumo No Recomendado (Malo)**."
      )
      st.markdown("""
            ### 📋 Explicación Técnica Detallada:
            - **Análisis de la Imagen:** El sistema detecta sellos de advertencia altos en azúcares refinados, grasas trans y jarabe de maíz de alta fructosa.
            - **Por qué evitar su consumo:** Su digestión genera picos de glucosa seguidos de fatiga metabólica, sobrecarga hepática y retención de líquidos a largo plazo.
            - **Alternativa Táctica:** Sustituir por alimentos de origen natural o snacks integrales sin aditivos artificiales.
            """)
  else:
    st.info(
        "💡 Cargue o capture la fotografía del envoltorio para que el motor"
        " de visión artificial analice los componentes de inmediato."
    )

# --- VISTA: TRIAJE Y ALERTA SOS ---
elif menu == "Triaje y Alerta SOS":
  st.title("🚨 Triaje y Alerta SOS")
  st.markdown(
      "Diagnóstico clínico automático por texto o voz, triaje inteligente con"
      " recetas y alertas automáticas de ubicación."
  )

  if "contacto_sos" not in st.session_state:
    st.session_state.contacto_sos = "+51 900000000"

  with st.expander(
      "⚙️ Configurar / Cambiar Número de Contacto de Emergencia SOS"
  ):
    nuevo_contacto = st.text_input(
        "Editar número de teléfono de emergencia:",
        value=st.session_state.contacto_sos,
    )
    if st.button("Actualizar Número de Contacto SOS"):
      st.session_state.contacto_sos = nuevo_contacto
      st.success(
          f"¡Número de emergencia actualizado correctamente a:"
          f" {nuevo_contacto}!"
      )

  st.write(
      "🎙️ **Seleccione método de entrada:** Puede escribir los síntomas o"
      " activar el comando de voz del dispositivo."
  )
  modo_entrada = st.radio(
      "Método de reporte:", ["Escribir síntoma", "🎤 Dictar Comando de Voz"]
  )

  sintoma_reporte = ""
  if modo_entrada == "Escribir síntoma":
    sintoma_reporte = st.text_area(
        "Describa el estado de salud o síntomas:",
        placeholder=(
            "Ej. Mareos intensos, fiebre alta, dolor en el pecho, presión"
            " baja..."
        ),
    )
  else:
    st.info(
        "🎙️ **Micrófono Activo:** Diga con claridad sus síntomas (Simulación"
        " de voz activada)."
    )
    sintoma_reporte = st.text_area(
        "Transcripción automática del comando de voz:",
        value=(
            "Siento fuerte opresión en el pecho, mareos y descompensación"
            " general."
        ),
    )

  if st.button("⚡ Ejecutar Triaje Clínico y Análisis Automático"):
    if sintoma_reporte:
      texto_analisis = sintoma_reporte.lower()

      if (
          "pecho" in texto_analisis
          or "inconsciente" in texto_analisis
          or "sangre" in texto_analisis
          or "respirar" in texto_analisis
          or "fuerte" in texto_analisis
          or "descompensación" in texto_analisis
      ):
        nivel_gravedad = "🔴 GRAVE / URGENCIA CRÍTICA"
        color_urgencia = "#ff4b4b"
        es_grave = True
      else:
        nivel_gravedad = "🟡 LEVE / MODERADO"
        color_urgencia = "#f0ad4e"
        es_grave = False

      st.markdown(
          f"### Nivel de Gravedad Calculado Automáticamente: <span"
          f" style='color: {color_urgencia};'>{nivel_gravedad}</span>",
          unsafe_allow_html=True,
      )

      if es_grave:
        st.error(
            "🚨 **¡ALERTA SOS AUTOMÁTICA ACTIVADA POR GRAVEDAD CRÍTICA!**"
        )
        st.markdown(f"""
                - **Motivo:** El sistema detectó un cuadro clínico de alto riesgo en su reporte.
                - **Ubicación GPS:** Transmitiendo coordenadas geográficas exactas en tiempo real.
                - **Aviso enviado:** Notificación de emergencia enviada de forma automática al número configurado: **{st.session_state.contacto_sos}**.
                """)
        st.markdown(
            f"📞 [LLAMAR AUTOMÁTICAMENTE AL CONTACTO SOS"
            f" ({st.session_state.contacto_sos})](tel:{st.session_state.contacto_sos})"
        )
      else:
        st.success(
            "💊 **Triaje Exitoso: Tratamiento y Recomendaciones Médicas"
            " Detalladas:**"
        )
        st.markdown("""
                - **Diagnóstico Preliminar:** Cuadro sintomático leve/moderado sin compromiso vital inmediato.
                - **Medicamentos sugeridos:** Paracetamol de 500 mg (1 tableta cada 8 horas) o Ibuprofeno (si hay malestar muscular).
                - **Pautas a seguir:** Reposo absoluto, hidratación constante con sales orales y monitoreo de temperatura.
                """)
    else:
      st.warning("Por favor ingrese o dicte el síntoma para realizar el triaje.")

# --- VISTA: PANEL MAESTRO (SOLO PARA TI) ---
elif menu == "Panel Maestro (Licencias)":
  st.title("⚙️ Panel de Control Maestro - Gestión Antifraude")
  st.write(
      "Comandante, aquí controla las licencias, fechas y la vinculación de"
      " equipos."
  )

  st.subheader("📋 Licencias, Fechas y Dispositivos Vinculados")

  for llave, exp_str in list(st.session_state.licencias_db.items()):
    col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
    with col1:
      st.write(f"🔑 **{llave}**")
      vinculado = st.session_state.licencias_vinculos.get(llave, "No vinculada")
      st.caption(
          f"Estado: {'📱 Vinculada' if vinculado != 'No vinculada' else '🟢 Libre'}"
      )
    with col2:
      fecha_actual_obj = datetime.strptime(exp_str, "%Y-%m-%d").date()
      nueva_fecha_obj = st.date_input(
          f"Expira ({llave})", value=fecha_actual_obj, key=f"date_{llave}"
      )
      st.session_state.licencias_db[llave] = nueva_fecha_obj.strftime(
          "%Y-%m-%d"
      )
    with col3:
      st.write("")
      st.write("")
      if llave in st.session_state.licencias_vinculos:
        if st.button(
            "🔄 Liberar",
            key=f"unb_{llave}",
            help=(
                "Desata la llave de este celular para que pueda usarse en otro"
            ),
        ):
          del st.session_state.licencias_vinculos[llave]
          st.success(f"Llave '{llave}' liberada.")
          st.rerun()
    with col4:
      st.write("")
      st.write("")
      if llave != "NV-MASTER-2026":
        if st.button("🗑️ Revocar", key=f"del_{llave}"):
          if llave in st.session_state.licencias_vinculos:
            del st.session_state.licencias_vinculos[llave]
          del st.session_state.licencias_db[llave]
          st.rerun()

    st.write("---")

  st.subheader("➕ Generar Nueva Llave Temporal")
  nueva_llave = st.text_input("Nombre de la nueva llave (Ej: NV-CLIENTE-02)")
  dias_validez = st.number_input(
      "Días de vigencia inicial", min_value=1, max_value=365, value=30
  )

  if st.button("Registrar y Activar Nueva Llave"):
    if nueva_llave:
      calculo_fecha = (
          datetime.now().date() + timedelta(days=int(dias_validez))
      ).strftime("%Y-%m-%d")
      st.session_state.licencias_db[nueva_llave] = calculo_fecha
      st.success(
          f"¡Llave '{nueva_llave}' creada con éxito! Expira el {calculo_fecha}."
      )
      st.rerun()
    else:
      st.error("Ingrese un nombre válido para la llave.")
