import streamlit as datetime, hashlib
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

# --- SISTEMA DE LICENCIAS Y CONTROL DE ACCESO ---
# Base de datos simulada de licencias (Clave: Fecha de Expiración en formato YYYY-MM-DD)
# Puedes modificar o añadir llaves aquí fácilmente.
LICENCIAS_VALIDAS = {
    "NV-MASTER-2026": "2099-12-31",  # Tu llave maestra permanente
    "NV-OPERADOR-01": "2026-10-15",  # Ejemplo de llave para un usuario con caducidad
}

CLAVE_MAESTRA = "ADMIN_RAEDCO_2026"  # Contraseña secreta solo para ti (Administrador)


def verificar_acceso(token):
  if not token:
    return False, "Por favor ingrese una clave de acceso."

  # Verificar si es la clave maestra de administración
  if token == CLAVE_MAESTRA:
    return True, "MASTER"

  # Verificar si la clave existe en el sistema
  if token in LICENCIAS_VALIDAS:
    fecha_exp_str = LICENCIAS_VALIDAS[token]
    fecha_exp = datetime.strptime(fecha_exp_str, "%Y-%m-%d").date()
    hoy = datetime.now().date()

    if hoy <= fecha_exp:
      return True, "USUARIO"
    else:
      return (
          False,
          f"⚠️ La clave ingresada ha caducado el {fecha_exp_str}. Contacte al"
          " administrador.",
      )
  else:
    return False, "❌ Clave de acceso inválida o no autorizada."


# Inicializar estado de sesión
if "autenticado" not in st.session_state:
  st.session_state.autenticado = False
  st.session_state.tipo_usuario = None

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
        "Acceso protegido. Introduzca su llave de autorización proporcionada"
        " por el comando central."
    )
    token_ingresado = st.text_input("🔑 Llave de Acceso", type="password")

    if st.button("Validar Credenciales", use_container_width=True):
      valido, mensaje = verificar_acceso(token_ingresado)
      if valido:
        st.session_state.autenticado = True
        st.session_state.tipo_usuario = mensaje
        st.rerun()
      else:
        st.error(mensaje)

  st.stop()  # Detiene la ejecución aquí si no está autenticado

# --- APLICACIÓN PRINCIPAL (UNA VEZ AUTORIZADO) ---
st.sidebar.title("⚡ Navegación Táctica")

# Si el usuario es el Administrador (Master), habilitar panel de control de llaves
if st.session_state.tipo_usuario == "MASTER":
  menu = st.sidebar.radio(
      "Seleccionar Modo", ["Centro de Mando", "Panel Maestro (Licencias)"]
  )
else:
  menu = "Centro de Mando"

if st.sidebar.button("🔒 Cerrar Sesión"):
  st.session_state.autenticado = False
  st.session_state.tipo_usuario = None
  st.rerun()

# --- VISTA: PANEL MAESTRO (SOLO PARA TI) ---
if menu == "Panel Maestro (Licencias)":
  st.title("⚙️ Panel de Control Maestro - Gestión de Licencias")
  st.write(
      "Bienvenido, Comandante. Aquí puede supervisar y controlar los accesos"
      " autorizados."
  )

  st.subheader("📋 Licencias Activas en el Sistema")
  for llave, exp in LICENCIAS_VALIDAS.items():
    st.write(f"- **Llave:** `{llave}` | **Expira:** `{exp}`")

  st.markdown("---")
  st.subheader("➕ Generar Nueva Llave Temporal")
  nueva_llave = st.text_input("Nombre de la nueva llave (Ej: NV-CLIENTE-02)")
  dias_validez = st.number_input(
      "Días de vigencia antes de caducar", min_value=1, max_value=365, value=30
  )

  if st.button("Registrar y Activar Llave"):
    if nueva_llave:
      nueva_fecha = (datetime.now().date() + timedelta(days=int(dias_validez))).strftime(
          "%Y-m-d"
      )
      LICENCIAS_VALIDAS[nueva_llave] = nueva_fecha
      st.success(
          f"¡Llave '{nueva_llave}' creada con éxito! Expira el {nueva_fecha}."
      )
    else:
      st.error("Ingrese un nombre válido para la llave.")

# --- VISTA: CENTRO DE MANDO (APLICACIÓN PRINCIPAL) ---
elif menu == "Centro de Mando":
  st.title("⚡ Núcleo Vital - Centro de Mando")
  st.markdown(
      "Estado del Sistema: <span style='color: #238636; font-weight: bold;'>●"
      " SEGURO Y OPERATIVO</span>",
      unsafe_allow_html=True,
  )

  # Alerta de ejemplo
  st.warning("No hay alertas críticas en la zona monitoreada actualmente.")

  # Tu interfaz táctica habitual
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
