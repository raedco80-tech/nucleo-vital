from datetime import datetime, timedelta
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

# --- SISTEMA DE LICENCIAS (GUARDADO EN MEMORIA DE SESIÓN) ---
CLAVE_MAESTRA = "ADMIN_RAEDCO_2026"  # Tu contraseña secreta de administrador

# Inicializar la lista de licencias en la sesión para que no se borren al editar
if "licencias_db" not in st.session_state:
  st.session_state.licencias_db = {
      "NV-MASTER-2026": "2099-12-31",  # Tu llave maestra permanente
      "NV-OPERADOR-01": "2026-10-15",  # Llave de ejemplo con caducidad
  }


def verificar_acceso(token):
  if not token:
    return False, "Por favor ingrese una clave de acceso."

  # Verificar si es la clave maestra de administración
  if token == CLAVE_MAESTRA:
    return True, "MASTER"

  # Verificar si la clave existe en el sistema
  if token in st.session_state.licencias_db:
    fecha_exp_str = st.session_state.licencias_db[token]
    fecha_exp = datetime.strptime(fecha_exp_str, "%Y-%m-%d").date()
    hoy = datetime.now().date()

    if hoy <= fecha_exp:
      return True, "USUARIO"
    else:
      return (
          False,
          f"⚠️ La llave ingresada ha caducado el {fecha_exp_str}. Contacte al"
          " administrador.",
      )
  else:
    return False, "❌ Clave de acceso inválida o no autorizada."


# --- PERSISTENCIA AUTOMÁTICA EN EL DISPOSITIVO ---
query_params = st.query_params
token_guardado = query_params.get("token", None)

if "autenticado" not in st.session_state:
  st.session_state.autenticado = False
  st.session_state.tipo_usuario = None

  if token_guardado:
    valido, tipo = verificar_acceso(token_guardado)
    if valido:
      st.session_state.autenticado = True
      st.session_state.tipo_usuario = tipo

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
        "Ingrese su llave de autorización por única vez. Quedará registrada"
        " en su dispositivo."
    )
    token_ingresado = st.text_input("🔑 Llave de Acceso", type="password")

    if st.button("Validar y Recordar Dispositivo", use_container_width=True):
      valido, mensaje = verificar_acceso(token_ingresado)
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
  menu = st.sidebar.radio(
      "Seleccionar Modo", ["Centro de Mando", "Panel Maestro (Licencias)"]
  )
else:
  menu = "Centro de Mando"

if st.sidebar.button("🔒 Olvidar Dispositivo / Cerrar Sesión"):
  st.query_params.clear()
  st.session_state.autenticado = False
  st.session_state.tipo_usuario = None
  st.rerun()

# --- VISTA: PANEL MAESTRO (ADMINISTRACIÓN VISUAL) ---
if menu == "Panel Maestro (Licencias)":
  st.title("⚙️ Panel de Control Maestro - Gestión de Licencias")
  st.write(
      "Comandante, aquí puede administrar, extender o revocar las licencias de"
      " sus usuarios visualmente."
  )

  st.subheader("📋 Licencias Activas y Edición de Fechas")

  # Listar y permitir editar o borrar cada llave directamente
  for llave, exp_str in list(st.session_state.licencias_db.items()):
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
      st.write(f"🔑 **{llave}**")
    with col2:
      # Permitir cambiar la fecha directamente seleccionándola en un calendario visual
      fecha_actual_obj = datetime.strptime(exp_str, "%Y-%m-%d").date()
      nueva_fecha_obj = st.date_input(
          f"Expira ({llave})", value=fecha_actual_obj, key=f"date_{llave}"
      )
      # Actualizar si cambia la fecha
      st.session_state.licencias_db[llave] = nueva_fecha_obj.strftime(
          "%Y-%m-%d"
      )
    with col3:
      st.write("")
      st.write("")
      if llave != "NV-MASTER-2026":  # Evitar borrar tu llave maestra por accidente
        if st.button("🗑️ Revocar", key=f"del_{llave}"):
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

# --- VISTA: CENTRO DE MANDO ---
elif menu == "Centro de Mando":
  st.title("⚡ Núcleo Vital - Centro de Mando")
  st.markdown(
      "Estado del Sistema: <span style='color: #238636; font-weight: bold;'>●"
      " SEGURO Y OPERATIVO</span>",
      unsafe_allow_html=True,
  )

  st.warning("No hay alertas críticas en la zona monitoreada actualmente.")

  st.subheader("🛡️ Escudo Urbano (Inteligencia de Zonas)")
  st.write("Leyenda: 🟩 Seguro | 🟨 Precaución | 🟥 Crítico")

  zona_input = st.text_input(
      "Destino o zona a transitar:",
      placeholder="Ej. Mercado, Av. Principal...",
  )
  if st.button("Evaluar Ruta y Consolidar Memoria"):
    if zona_input:
      st.success(f"Analizando parámetros tácticos para la zona: {zona_input}")
    else:
      st.warning("Por favor ingrese una zona válida.")
