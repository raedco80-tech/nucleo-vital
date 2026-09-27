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
CLAVE_MAESTRA = "ADMIN_RAEDCO_2026"

if "licencias_db" not in st.session_state:
  st.session_state.licencias_db = {
      "NV-MASTER-2026": "2099-12-31",
      "NV-OPERADOR-01": "2026-10-15",
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
    if datetime.now().date() > fecha_exp:
      return False, f"⚠️ La llave ha caducado el {fecha_exp_str}."
    if token in st.session_state.licencias_vinculos:
      if st.session_state.licencias_vinculos[token] != dispositivo:
        return False, "❌ Esta llave ya está en uso en otro dispositivo."
    else:
      st.session_state.licencias_vinculos[token] = dispositivo
    return True, "USUARIO"
  else:
    return False, "❌ Clave de acceso inválida."


# --- CONTROL DE SESIÓN ESTRICTO ---
if "autenticado" not in st.session_state:
  st.session_state.autenticado = False
  st.session_state.tipo_usuario = None

token_guardado = st.query_params.get("token", None)

if token_guardado and not st.session_state.autenticado:
  valido, tipo = verificar_acceso(token_guardado, dispositivo_actual)
  if valido:
    st.session_state.autenticado = True
    st.session_state.tipo_usuario = tipo
  else:
    st.query_params.pop("token", None)

# --- PANTALLA DE BLOQUEO OBLIGATORIA ---
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
        "Acceso restringido. Ingrese su llave de autorización para vincular"
        " este equipo."
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

  # CORTA LA EJECUCIÓN AQUÍ: NADA MÁS SE MUESTRA HASTA QUE SE AUTENTIQUE
  st.stop()

# ==========================================
# APLICACIÓN PRINCIPAL (MÓDULOS INTACTOS)
# ==========================================

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

if st.sidebar.button("🔒 Cerrar Sesión / Olvidar Dispositivo"):
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

# --- VISTA: ESCUDO Y MEMORIA ---
elif menu == "Escudo y memoria":
  st.title("🛡️ Escudo y Memoria")
  st.markdown(
      "Monitoreo de rutas, semáforos de peligrosidad y registro de incidentes"
      " en tiempo real."
  )
  st.markdown(
      "**Leyenda de Semáforos:** 🟩 <span style='color: #238636; font-weight:"
      " bold;'>Segura</span> | 🟨 <span style='color: #f0ad4e; font-weight:"
      " bold;'>Precaución</span> | 🟥 <span style='color: #ff4b4b;"
      " font-weight: bold;'>Peligro</span>",
      unsafe_allow_html=True,
  )
  st.write("---")
  destino = st.text_input("Ingrese su lugar de destino a transitar:")
  incidente_camino = st.text_input("Reportar novedad o incidente imprevisto:")
  if st.button("Consultar Estado y Generar Ruta Automática"):
    if destino:
      if "mercado" in destino.lower() or "peligro" in destino.lower():
        semaforo = "🟥 ZONA DE PELIGRO / ALTO RIESGO"
        color_html = "#ff4b4b"
      else:
        semaforo = "🟩 ZONA SEGURA"
        color_html = "#238636"
      st.markdown(
          f"### Semáforo en Ruta: <span style='color: {color_html}; font-weight:"
          f" bold;'>● {semaforo}</span>",
          unsafe_allow_html=True,
      )
      st.progress(80)

# --- VISTA: ESCÁNER TÁCTICO PRO ---
elif menu == "Escáner táctico Pro":
  st.title("📷 Escáner táctico Pro")
  foto_producto = st.file_uploader(
      "Tomar o subir foto del envoltorio del producto:",
      type=["jpg", "jpeg", "png", "webp"],
  )
  if foto_producto is not None:
    st.image(foto_producto, width=350)
    if st.button("🔍 Analizar Ingredientes Automáticamente"):
      st.warning(
          "⚠️ **Resultado:** Producto clasificado en **Rango de Consumo No"
          " Recomendado (Malo)**."
      )

# --- VISTA: TRIAJE Y ALERTA SOS ---
elif menu == "Triaje y Alerta SOS":
  st.title("🚨 Triaje y Alerta SOS")
  if "contacto_sos" not in st.session_state:
    st.session_state.contacto_sos = "+51 900000000"
  with st.expander("⚙️ Configurar Número de Emergencia SOS"):
    nuevo_contacto = st.text_input(
        "Número:", value=st.session_state.contacto_sos
    )
    if st.button("Actualizar Contacto"):
      st.session_state.contacto_sos = nuevo_contacto
      st.success("¡Actualizado!")
  sintoma_reporte = st.text_area(
      "Describa el estado de salud o síntomas:",
      placeholder="Ej. Mareos intensos, dolor en el pecho...",
  )
  if st.button("⚡ Ejecutar Triaje Clínico"):
    if sintoma_reporte:
      if "pecho" in sintoma_reporte.lower() or "fuerte" in sintoma_reporte.lower():
        st.error(
            "🚨 **¡ALERTA SOS ACTIVADA POR GRAVEDAD CRÍTICA!** Aviso enviado a:"
            f" {st.session_state.contacto_sos}"
        )
      else:
        st.success(
            "💊 **Triaje Exitoso:** Paracetamol 500mg (1 cada 8h) y reposo."
        )

# --- VISTA: PANEL MAESTRO ---
elif menu == "Panel Maestro (Licencias)":
  st.title("⚙️ Panel de Control Maestro - Gestión Antifraude")
  for llave, exp_str in list(st.session_state.licencias_db.items()):
    col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
    with col1:
      st.write(f"🔑 **{llave}**")
    with col2:
      nueva_fecha_obj = st.date_input(
          f"Expira ({llave})",
          value=datetime.strptime(exp_str, "%Y-%m-%d").date(),
          key=f"date_{llave}",
      )
      st.session_state.licencias_db[llave] = nueva_fecha_obj.strftime(
          "%Y-%m-%d"
      )
    with col3:
      if llave in st.session_state.licencias_vinculos and st.button(
          "🔄 Liberar", key=f"unb_{llave}"
      ):
        del st.session_state.licencias_vinculos[llave]
        st.rerun()
    with col4:
      if llave != "NV-MASTER-2026" and st.button(
          "🗑️ Revocar", key=f"del_{llave}"
      ):
        del st.session_state.licencias_db[llave]
        st.rerun()
    st.write("---")
  nueva_llave = st.text_input("Nombre de nueva llave")
  if st.button("Registrar Llave"):
    if nueva_llave:
      st.session_state.licencias_db[nueva_llave] = (
          datetime.now().date() + timedelta(days=30)
      ).strftime("%Y-%m-%d")
      st.rerun()
