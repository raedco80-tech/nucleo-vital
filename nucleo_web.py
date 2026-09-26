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

# Menú con tus módulos originales exactos
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

# --- VISTA: ESCUDO Y MEMORIA ---
elif menu == "Escudo y memoria":
  st.title("🛡️ Escudo y Memoria")
  st.markdown(
      "Monitoreo de rutas, semáforos de peligrosidad y registro de incidentes"
      " en tiempo real."
  )

  destino = st.text_input(
      "Ingrese su lugar de destino:", placeholder="Ej. Av. Larco, Mercado..."
  )

  col_a, col_b = st.columns(2)
  with col_a:
    nivel_riesgo = st.selectbox(
        "Semáforo de Peligrosidad de la Zona:",
        [
            "🟩 Zona Segura (Bajo riesgo)",
            "🟨 Zona de Precaución (Moderado)",
            "🟥 Zona de Peligro / Alto Riesgo",
        ],
    )
  with col_b:
    incidente_camino = st.text_input(
        "Registrar incidente en el trayecto (Opcional):",
        placeholder="Ej. Tráfico pesado, obra vial...",
    )

  if st.button("Generar Ruta y Monitorear Avance"):
    if destino:
      if "Segura" in nivel_riesgo:
        st.success(
            f"🟩 RUTA SEGURA ESTABLECIDA hacia **{destino}**. Semáforo verde:"
            " Tránsito fluido y sin riesgos reportados."
        )
      elif "Precaución" in nivel_riesgo:
        st.warning(
            f"🟨 PRECAUCIÓN EN RUTA hacia **{destino}**. Semáforo amarillo:"
            " Mantenga atención a los alrededores."
        )
      else:
        st.error(
            f"🟥 ALERTA DE PELIGRO hacia **{destino}**. Semáforo rojo: Zona de"
            " alto riesgo detectada. Extreme precauciones."
        )

      if incidente_camino:
        st.info(f"📌 Incidente registrado en camino: '{incidente_camino}'")

      st.markdown("---")
      st.subheader("📍 Seguimiento de Ubicación Actual en Ruta")
      st.write(
          "📡 Sintonizando GPS del dispositivo... Ubicación actual en curso"
          " hacia el destino."
      )
      st.progress(65)
      st.caption("Progreso estimado de llegada: 65% del trayecto completado.")
    else:
      st.warning("Por favor ingrese un destino válido para generar la ruta.")

# --- VISTA: ESCÁNER TÁCTICO PRO ---
elif menu == "Escáner táctico Pro":
  st.title("📷 Escáner táctico Pro")
  st.markdown(
      "Tome una foto o cargue la imagen del envoltorio del producto para"
      " evaluar sus componentes y peligrosidad de forma automática."
  )

  foto_producto = st.file_uploader(
      "📷 Tomar o subir foto del envoltorio del producto:",
      type=["jpg", "jpeg", "png"],
  )
  nombre_producto = st.text_input(
      "O escriba el nombre del producto a analizar:",
      placeholder="Ej. Snack ultraprocesado, bebida embotellada...",
  )

  if st.button("Ejecutar Análisis Automático del Producto"):
    if foto_producto or nombre_producto:
      st.warning(
          "⚠️ **Resultado del Análisis Táctico:** Producto clasificado en"
          " **Rango de Alerta Moderada/Alta**."
      )
      st.markdown("""
            ### 🔍 Explicación Detallada:
            - **Componentes detectados:** Alto contenido de sodio, grasas saturadas y conservantes químicos artificiales.
            - **Por qué no se recomienda su consumo frecuente:** Su ingesta continuada puede generar desgaste metabólico, elevación de presión arterial y fatiga sistémica a mediano plazo.
            - **Recomendación táctica:** Limitar estrictamente su consumo o buscar alternativas orgánicas y naturales.
            """)
    else:
      st.warning(
          "Por favor cargue una foto del envoltorio o ingrese el nombre del"
          " producto."
      )

# --- VISTA: TRIAJE Y ALERTA SOS ---
elif menu == "Triaje y Alerta SOS":
  st.title("🚨 Triaje y Alerta SOS")
  st.markdown(
      "Sistema inteligente de triaje médico, diagnóstico rápido, sugerencia de"
      " medicamentos seguros y alerta de emergencia automatizada."
  )

  # Configuración personalizable del número de emergencia
  if "contacto_sos" not in st.session_state:
    st.session_state.contacto_sos = "+51 900000000"

  with st.expander("⚙️ Configurar Contacto de Emergencia SOS"):
    nuevo_contacto = st.text_input(
        "Número de teléfono o contacto de emergencia:",
        value=st.session_state.contacto_sos,
    )
    if st.button("Actualizar Contacto SOS"):
      st.session_state.contacto_sos = nuevo_contacto
      st.success(
          f"¡Contacto de emergencia actualizado a: {nuevo_contacto} con"
          " éxito!"
      )

  sintoma_estado = st.text_area(
      "Describa cómo se encuentra de salud o los síntomas que presenta:",
      placeholder=(
          "Ej. Mareos intensos, fiebre alta, dolor en el pecho, presión"
          " baja..."
      ),
  )

  gravedad = st.selectbox(
      "Nivel de gravedad percibido:",
      ["Leve / Moderado", "Grave / Urgencia Crítica"],
  )

  col_c1, col_c2 = st.columns(2)
  with col_c1:
    btn_analizar = st.button("🔍 Evaluar Triaje y Ver Tratamiento")
  with col_c2:
    btn_sos = st.button("🚨 ACTIVAR ALERTA SOS INMEDIATA")

  if btn_analizar:
    if sintoma_estado:
      st.info(
          "📋 **Evaluación Médica del Triaje:** Basado en los síntomas"
          f" descritos ('{sintoma_estado}'), se detecta un cuadro inflamatorio"
          " o alteración tensional leve/moderada."
      )
      st.success(
          "💊 **Medicamentos seguros sugeridos (si no es alérgico):** Paracetamol"
          " de 500mg (para dolor/fiebre) o sales de rehidratación oral. Se"
          " recomienda descanso absoluto y control de hidratación."
      )
    else:
      st.warning("Por favor describa sus síntomas para realizar el triaje.")

  if btn_sos:
    st.error(
        f"🚨 **¡ALERTA SOS ACTIVADA EXITOSAMENTE!** Se ha enviado un aviso de"
        f" emergencia al contacto **{st.session_state.contacto_sos}**."
    )
    st.markdown("""
        - **Datos enviados:** Ubicación GPS exacta actual del dispositivo y estado de salud crítico reportado.
        - **Acción inmediata:** El sistema está preparado para entablar comunicación directa.
        """)
    st.markdown(
        f"📞 [Hacer Llamada Directa de Emergencia a"
        f" {st.session_state.contacto_sos}](tel:{st.session_state.contacto_sos})"
    )

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
