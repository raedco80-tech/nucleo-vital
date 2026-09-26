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

# Menú con tus módulos originales intactos
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
      "Bienvenido al núcleo de operaciones. Utiliza el menú lateral para"
      " acceder a tus módulos especializados."
  )

# --- VISTA: ESCUDO Y MEMORIA ---
elif menu == "Escudo y memoria":
  st.title("🛡️ Escudo y Memoria")
  st.markdown(
      "Módulo de consolidación de rutas, zonas de seguridad y registro de"
      " memoria táctica."
  )

  zona_input = st.text_input(
      "Destino o zona a evaluar:", placeholder="Ej. Mercado, Av. Principal..."
  )
  if st.button("Consolidar Memoria de Ruta"):
    if zona_input:
      st.success(
          f"Registrando y evaluando parámetros de seguridad para: {zona_input}"
      )
    else:
      st.warning("Por favor ingrese una zona válida.")

# --- VISTA: ESCÁNER TÁCTICO PRO ---
elif menu == "Escáner táctico Pro":
  st.title("📷 Escáner táctico Pro")
  st.markdown(
      "Módulo avanzado de lectura y verificación de códigos QR de seguridad y"
      " control de accesos."
  )

  codigo_input = st.text_input(
      "Ingrese código o datos del elemento a escanear:",
      placeholder="Ej. NV-CODE-9988",
  )
  if st.button("Ejecutar Escaneo Táctico"):
    if codigo_input:
      st.success(
          f"Código {codigo_input} verificado correctamente. Elemento dentro de"
          " los parámetros seguros."
      )
    else:
      st.warning("Por favor ingrese un código para escanear.")

# --- VISTA: TRIAJE Y ALERTA SOS ---
elif menu == "Triaje y Alerta SOS":
  st.title("🚨 Triaje y Alerta SOS")
  st.markdown(
      "Módulo de respuesta rápida ante eventualidades de salud, triaje y"
      " activación de alertas de emergencia."
  )

  st.error(
      "⚠️ ATENCIÓN: Si se trata de una emergencia vital extrema, active los"
      " protocolos de auxilio externos de inmediato."
  )

  sintoma_input = st.text_input(
      "Describa los síntomas o la situación de emergencia:",
      placeholder="Ej. Dolor agudo, accidente, descompensación...",
  )
  if st.button("Generar Triaje y Alerta SOS"):
    if sintoma_input:
      st.warning(
          f"Triaje procesado para: {sintoma_input}. Mantenga la calma, evalúe"
          " constantes vitales y aplique los protocolos de asistencia rápida."
      )
    else:
      st.warning("Por favor describa la situación de triaje.")

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
