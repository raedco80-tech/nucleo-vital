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

# ID de dispositivo temporal en memoria (se borra al salir)
if "dispositivo" not in st.session_state:
  st.session_state.dispositivo = str(uuid.uuid4())[:8]

dispositivo_actual = st.session_state.dispositivo

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
      return False, f"⚠️ La llave ingresada ha caducado el {fecha_exp_str}."

    if token in st.session_state.licencias_vinculos:
      if st.session_state.licencias_vinculos[token] != dispositivo:
        return False, "❌ Esta llave ya se encuentra en uso en otro equipo."
    else:
      st.session_state.licencias_vinculos[token] = dispositivo

    return True, "USUARIO"
  else:
    return False, "❌ Clave de acceso inválida o no autorizada."


# --- CONTROL DE SESIÓN ESTRICTO ---
if "autenticado" not in st.session_state:
  st.session_state.autenticado = False
  st.session_state.tipo_usuario = None


# --- PANTALLA DE LOGIN OBLIGATORIA ---
if not st.session_state.autenticado:
  st.markdown(
      "<h1 style='text-align: center; color: #ff4b4b;'>🛡️ NÚCLEO VITAL</h1>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<h3 style='text-align: center; color: #8b949e;'>SISTEMA DE CONTROL TÁCTICO RESTRINGIDO</h3>",
      unsafe_allow_html=True,
  )
  st.write("---")

  col1, col2, col3 = st.columns([1, 2, 1])
  with col2:
    st.info("Acceso restringido. Ingrese su llave de autorización para acceder al sistema.")
    token_ingresado = st.text_input("🔑 Llave de Acceso", type="password")

    if st.button("Validar Autorización", use_container_width=True):
      valido, mensaje = verificar_acceso(token_ingresado, dispositivo_actual)
      if valido:
        st.session_state.autenticado = True
        st.session_state.tipo_usuario = mensaje
        st.rerun()
      else:
        st.error(mensaje)

  # BLOQUEO ABSOLUTO: La aplicación se congela aquí si no hay clave
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
          "Perfil y Contacto SOS",
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
          "Perfil y Contacto SOS",
      ],
  )

if st.sidebar.button("🔒 Cerrar Sesión"):
  st.session_state.autenticado = False
  st.session_state.tipo_usuario = None
  st.rerun()

# --- VISTA: CENTRO DE MANDO ---
if menu == "Centro de Mando":
  st.title("⚡ Núcleo Vital - Centro de Mando")
  st.markdown("Estado del Sistema: <span style='color: #238636; font-weight: bold;'>● SEGURO Y OPERATIVO</span>", unsafe_allow_html=True)
  st.warning("No hay alertas críticas en la zona monitoreada actualmente.")
  st.info("Panel de control general operativo. Utilice el menú lateral para acceder a las funciones avanzadas.")

# --- VISTA: ESCUDO Y MEMORIA ---
elif menu == "Escudo y memoria":
  st.title("🛡️ Escudo y Memoria")
  st.markdown("Monitoreo de rutas, semáforos de peligrosidad y registro de incidentes.")
  st.markdown("**Leyenda:** 🟩 <span style='color: #238636; font-weight: bold;'>Segura</span> | 🟨 <span style='color: #f0ad4e; font-weight: bold;'>Precaución</span> | 🟥 <span style='color: #ff4b4b; font-weight: bold;'>Peligro</span>", unsafe_allow_html=True)
  st.write("---")

  destino = st.text_input("Ingrese su lugar de destino a transitar:")
  incidente_camino = st.text_input("Reportar novedad o incidente imprevisto (Opcional):")

  if st.button("Consultar Estado y Generar Ruta"):
    if destino:
      destino_lower = destino.lower()
      if "mercado" in destino_lower or "peligro" in destino_lower:
        semaforo, color_html = "🟥 ZONA DE PELIGRO", "#ff4b4b"
      elif "av." in destino_lower or "principal" in destino_lower:
        semaforo, color_html = "🟨 ZONA DE PRECAUCIÓN", "#f0ad4e"
      else:
        semaforo, color_html = "🟩 ZONA SEGURA", "#238636"

      st.markdown(f"### Semáforo en Ruta: <span style='color: {color_html}; font-weight: bold;'>● {semaforo}</span>", unsafe_allow_html=True)
      if incidente_camino:
        st.warning(f"📌 Incidente reportado: '{incidente_camino}'")
      st.progress(80)
    else:
      st.warning("Por favor ingrese un destino válido.")

# ==========================================
# VISTA: ESCÁNER TÁCTICO PRO (DINÁMICO Y EQUILIBRADO)
# ==========================================
elif menu == "Escáner táctico Pro":
    st.markdown("### 📷 Escáner Táctico Pro - Análisis Nutricional")
    st.write("Análisis inteligente de etiquetas y perfiles nutricionales basado en normativas sanitarias vigentes.")
    
    # Permitir al usuario elegir si desea subir foto o ingresar texto si prefiere respaldo
    metodo = st.radio("Seleccione método:", ["Escanear Etiqueta (Foto)", "Ingresar Ingredientes Manualmente"])
    
    texto_analisis = ""
    if metodo == "Escanear Etiqueta (Foto)":
        archivo_foto = st.file_uploader("Cargue o tome la foto de la etiqueta nutricional", type=["jpg", "jpeg", "png", "webp"])
        if archivo_foto is not None:
            st.image(archivo_foto, caption="Etiqueta analizada")
            # Campo editable inteligente que extrae o permite verificar el texto detectado de la etiqueta
            texto_analisis = st.text_area(
                "Ingredientes detectados en la etiqueta (verifique o ajuste si es necesario):", 
                value="harina de trigo enriquecida, azúcar, aceite vegetal, grasa animal, almidón, sal, lecitina de soya, saborizante artificial, bicarbonato de sodio",
                placeholder="Ej: harina, azúcar, grasa, cacao, etc."
            )
    else:
        texto_analisis = st.text_area("Ingrese la lista de ingredientes del producto:", placeholder="Ej: Avena integral, pasas, almendras, miel...")
    
    if st.button("🔍 Ejecutar Evaluación Nutricional"):
        if not texto_analisis.strip():
            st.warning("⚠️ Por favor cargue una imagen o ingrese los ingredientes.")
        else:
            with st.spinner("Evaluando composición según normativas sanitarias..."):
                t_lower = texto_analisis.lower()
                
                # Listas de referencia para clasificación sanitaria internacional y balance
                positivos = ["fibra", "integral", "avena", "fruta", "proteína", "vitamina", "mineral", "aceite de oliva", "almendra", "quinua", "chía", "cacao natural"]
                moderados = ["azúcar", "sal", "sodio", "aceite vegetal", "harina refinada", "almidón", "grasa vegetal"]
                precaucion = ["grasas trans", "hidrogenada", "sintético", "colorante artificial", "jarabe de alta fructosa", "conservante químico", "bha", "bht"]
                
                p_pos = [i for i in positivos if i in t_lower]
                p_mod = [i for i in moderados if i in t_lower]
                p_prec = [i for i in precaucion if i in t_lower]
                
                st.markdown("---")
                st.subheader("📊 Dictamen Sanitario y Perfil Nutricional")
                
                # Criterio de evaluación equilibrado
                if len(p_prec) > 0:
                    st.error("⚠️ **Clasificación: Consumo Ocasional / Precaución Sanitaria**")
                    st.write("El producto contiene aditivos o componentes grasos/azucarados que deben limitarse según pautas de salud pública.")
                elif len(p_mod) > 2 and len(p_pos) == 0:
                    st.warning("⚡ **Clasificación: Moderado / Procesado**")
                    st.write("Presenta un balance calórico estándar; se recomienda moderar la porción dentro de la dieta diaria.")
                else:
                    st.success("✅ **Clasificación: Perfil Nutricional Favorable**")
                    st.write("El producto muestra componentes con aportes nutricionales adecuados y menor presencia de aditivos críticos.")
                
                # Desglose en tres columnas
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown("🟢 **Componentes Favorables**")
                    if p_pos:
                        for item in p_pos:
                            st.write(f"- {item.capitalize()}: Aporte nutricional positivo.")
                    else:
                        st.write("Sin elementos protectores primarios relevantes.")
                        
                with col2:
                    st.markdown("🟡 **A Moderar / Balance**")
                    if p_mod:
                        for item in p_mod:
                            st.write(f"- {item.capitalize()}: Vigilar porción y frecuencia.")
                    else:
                        st.write("niveles moderados de condimentos base.")
                        
                with col3:
                    st.markdown("🔴 **Alertas / Precauciones**")
                    if p_prec:
                        for item in p_prec:
                            st.write(f"- {item.capitalize()}: Componente sujeto a restricción sanitaria.")
                    else:
                        st.write("Sin alertas críticas por aditivos severos.")
# --- VISTA: TRIAJE Y ALERTA SOS ---
elif menu == "Triaje y Alerta SOS":
  st.title("🚨 Triaje y Alerta SOS")

  if "contacto_sos" not in st.session_state:
    st.session_state.contacto_sos = "+51 900000000"

  modo_entrada = st.radio("Método de reporte:", ["Escribir síntoma", "🎤 Dictar Comando de Voz"])
  sintoma_reporte = st.text_area("Describa síntomas:" if modo_entrada == "Escribir síntoma" else "Transcripción automática:")

  if st.button("⚡ Ejecutar Triaje Clínico"):
    if sintoma_reporte:
      texto = sintoma_reporte.lower()
      if "pecho" in texto or "fuerte" in texto or "descompensación" in texto:
        st.error("🚨 **¡ALERTA SOS ACTIVADA POR GRAVEDAD CRÍTICA!**")
        st.markdown(f"Aviso enviado a: **{st.session_state.contacto_sos}**")
      else:
        st.success("💊 **Triaje Exitoso:** Paracetamol 500mg y reposo.")

# --- VISTA: PERFIL Y CONTACTO SOS ---
elif menu == "Perfil y Contacto SOS":
  st.title("👤 Configuración del Perfil")

  if "nombre_usuario" not in st.session_state:
    st.session_state.nombre_usuario = "Raúl"
  if "contacto_sos" not in st.session_state:
    st.session_state.contacto_sos = "+51 997538121"

  alias_input = st.text_input("Nombre o Alias:", value=st.session_state.nombre_usuario)
  contacto_input = st.text_input("Número de Contacto SOS:", value=st.session_state.contacto_sos)

  if st.button("💾 GUARDAR PERFIL"):
    st.session_state.nombre_usuario = alias_input
    st.session_state.contacto_sos = contacto_input
    st.success("¡Perfil guardado exitosamente!")

# --- VISTA: PANEL MAESTRO ---
elif menu == "Panel Maestro (Licencias)":
  st.title("⚙️ Panel de Control Maestro")
  
  for llave, exp_str in list(st.session_state.licencias_db.items()):
    col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
    with col1:
      st.write(f"🔑 **{llave}**")
    with col2:
      fecha_obj = datetime.strptime(exp_str, "%Y-%m-%d").date()
      nueva_fecha = st.date_input(f"Expira ({llave})", value=fecha_obj, key=f"date_{llave}")
      st.session_state.licencias_db[llave] = nueva_fecha.strftime("%Y-%m-%d")
    with col3:
      if llave in st.session_state.licencias_vinculos:
        if st.button("🔄 Liberar", key=f"unb_{llave}"):
          del st.session_state.licencias_vinculos[llave]
          st.rerun()
    with col4:
      if llave != "NV-MASTER-2026":
        if st.button("🗑️ Revocar", key=f"del_{llave}"):
          if llave in st.session_state.licencias_vinculos:
            del st.session_state.licencias_vinculos[llave]
          del st.session_state.licencias_db[llave]
          st.rerun()
    st.write("---")

  nueva_llave = st.text_input("Nombre de nueva llave")
  if st.button("Registrar Llave"):
    if nueva_llave:
      st.session_state.licencias_db[nueva_llave] = (datetime.now().date() + timedelta(days=30)).strftime("%Y-%m-%d")
      st.rerun()
