from datetime import datetime, timedelta
import uuid
import streamlit as st
from PIL import Image
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

elif menu == "Escáner táctico Pro":
    # ==========================================
    # BASE DE DATOS INTERNA CON ALERTAS CRÓNICAS
    # ==========================================
    BASE_INGREDIENTES_MAESTRA = {
        # 1. HIGIENE Y COSMÉTICA
        "aluminio": {
            "categoria": "Antitranspirante", "clasificacion": "Precaución / Monitoreo", 
            "dictamen": "Bloquea conductos sudoríparos. Se absorbe por la piel.", 
            "recomendacion": "Alternar con opciones 'Zero Aluminio'.",
            "limite": "Máximo 1 aplicación diaria.",
            "riesgo_cronico": "🚨 USO CRÓNICO: Riesgo de neurotoxicidad por acumulación de metales pesados en el cuerpo humano y sospecha de alteración en tejido mamario a largo plazo."
        },
        "triclosan": {
            "categoria": "Antibacteriano", "clasificacion": "Precaución / Alerta Sanitaria", 
            "dictamen": "Agente antimicrobiano de amplio espectro.", 
            "recomendacion": "Buscar jabones de glicerina pura.",
            "limite": "No se recomienda para uso diario.",
            "riesgo_cronico": "🚨 USO CRÓNICO: Alteración del sistema endocrino (desajustes hormonales) y fomento de cepas de bacterias súper-resistentes en la piel."
        },
        "parabenos": {
            "categoria": "Conservante", "clasificacion": "Precaución / Monitoreo", 
            "dictamen": "Actúan como estrógenos débiles en el organismo.", 
            "recomendacion": "Buscar opciones 'Libre de parabenos'.",
            "limite": "Evitar lociones de cuerpo entero que los contengan.",
            "riesgo_cronico": "🚨 USO CRÓNICO: Acumulación estrogénica que puede interferir con el desarrollo hormonal normal a lo largo de los años."
        },
        "dental": {
            "categoria": "Higiene Bucal", "clasificacion": "Favorable / Seguro", 
            "dictamen": "Fluoruro de sodio y abrasivos para endurecer el esmalte.", 
            "recomendacion": "No tragar la espuma tras el cepillado.",
            "limite": "Una porción del tamaño de una arveja por lavado.",
            "riesgo_cronico": "🟢 USO CRÓNICO: Si no se ingiere, es totalmente seguro y previene la destrucción crónica del esmalte dental (caries profundas)."
        },

        # 2. ALIMENTOS Y BEBIDAS
        "coca": {
            "categoria": "Bebida Carbonatada", "clasificacion": "Precaución / Peligro Metabólico", 
            "dictamen": "Sobrecarga de glucosa y jarabe de alta fructosa.", 
            "recomendacion": "Sustituir por agua carbonatada sin azúcar.",
            "limite": "Límite OMS: 25g de azúcares libres diarios.",
            "riesgo_cronico": "🚨 CONSUMO FRECUENTE: Desarrollo directo de resistencia a la insulina, diabetes tipo 2, esteatosis hepática (hígado graso) y obesidad severa."
        },
        "gaseosa": {
            "categoria": "Bebida Azucarada", "clasificacion": "Precaución / Peligro Metabólico", 
            "dictamen": "Agua carbonatada con exceso de azúcares y colorantes.", 
            "recomendacion": "Evitar su consumo regular.",
            "limite": "Límite OMS: 25g de azúcares libres diarios.",
            "riesgo_cronico": "🚨 CONSUMO FRECUENTE: Descalcificación ósea por ácido fosfórico, daño al esmalte dental y alto riesgo de síndrome metabólico."
        },
        "hot dog": {
            "categoria": "Embutido Cárnico", "clasificacion": "Precaución / Alerta Sanitaria", 
            "dictamen": "Contiene nitritos y exceso de sodio industrial.", 
            "recomendacion": "Hervir en lugar de freír para reducir la reacción química.",
            "limite": "Máximo 1 a 2 unidades semanales.",
            "riesgo_cronico": "🚨 CONSUMO FRECUENTE: Clasificado por la OMS como factor de riesgo para desarrollar cáncer colorrectal crónico, además de generar hipertensión arterial."
        },
        "atun": {
            "categoria": "Conserva Marina", "clasificacion": "Favorable / Nutritivo", 
            "dictamen": "Proteínas magras y Omega-3.", 
            "recomendacion": "Preferir presentaciones 'en agua'.",
            "limite": "Máximo 2 a 3 latas por semana.",
            "riesgo_cronico": "⚠️ CONSUMO EXCESIVO: El consumo diario (más de 4 latas semanales) puede generar bioacumulación de mercurio, causando fatiga, temblores y daño neurológico leve."
        },
        "galleta": {
            "categoria": "Snack Dulce", "clasificacion": "Moderación Requerida", 
            "dictamen": "Harinas refinadas sin fibra y grasas hidrogenadas.", 
            "recomendacion": "Consumir rara vez y en porciones chicas.",
            "limite": "Una porción esporádica a la semana.",
            "riesgo_cronico": "🚨 CONSUMO FRECUENTE: Picos crónicos de glucosa, aumento de colesterol LDL (malo) y riesgo de daño cardiovascular temprano."
        }
    }

    # ==========================================
    # INTERFAZ DE USUARIO: ESCÁNER TÁCTICO PRO
    # ==========================================
    st.markdown("### 📷 y 🎙️ Escáner Táctico Pro - Análisis por Voz y Texto")
    st.write("Sube la foto del producto y dicta los ingredientes para conocer su impacto toxicológico a largo plazo.")
    
    archivo_foto = st.file_uploader("1. Sube o toma la foto del producto", type=["jpg", "jpeg", "png", "webp"], key="foto_evidencia")
    if archivo_foto is not None:
        try:
            imagen_pil = Image.open(archivo_foto)
            imagen_pil.thumbnail((400, 400)) 
            st.image(imagen_pil, caption="Evidencia visual cargada")
        except Exception as err:
            st.error("Error al procesar la imagen.")

    st.markdown("---")
    st.markdown("#### 🎙️ Lector de Ingredientes")
    st.info("Toca aquí, presiona el micrófono 🎙️ de tu teclado y dicta los ingredientes (Ej: coca, galleta, aluminio, triclosan).")
    
    ingredientes_texto = st.text_area("Ingresa los ingredientes aquí:", height=100, placeholder="Dicta los ingredientes...")
    
    if st.button("🔍 Analizar Riesgo Crónico"):
        if ingredientes_texto.strip() == "":
            st.warning("⚠️ Por favor, dicta o escribe algunos ingredientes antes de analizar.")
        else:
            with st.spinner("Evaluando consecuencias de salud a largo plazo..."):
                texto_minusculas = ingredientes_texto.lower()
                componentes_hallados = []

                for clave, datos in BASE_INGREDIENTES_MAESTRA.items():
                    if clave in texto_minusculas:
                        datos_encontrados = datos.copy()
                        datos_encontrados["detectado"] = clave
                        componentes_hallados.append(datos_encontrados)

                st.markdown("---")
                st.subheader("📊 Reporte de Toxicidad e Impacto")
                
                if len(componentes_hallados) > 0:
                    st.success(f"Se identificaron **{len(componentes_hallados)}** componentes clave:")
                    
                    for item in componentes_hallados:
                        with st.expander(f"📌 {item['detectado'].upper()} ({item['categoria']})", expanded=True):
                            clasif = item['clasificacion']
                            
                            if "Favorable" in clasif:
                                st.success(f"🟢 **Clasificación: {clasif}**")
                            elif "Peligro" in clasif or "Alerta" in clasif or "Metabólico" in clasif:
                                st.error(f"🔴 **Clasificación: {clasif}**")
                            else:
                                st.warning(f"🟡 **Clasificación: {clasif}**")
                            
                            st.write(f"**Análisis:** {item['dictamen']}")
                            st.write(f"**Recomendación:** {item['recomendacion']}")
                            st.write(f"**⚠️ Límite Seguro:** {item['limite']}")
                            
                            # NUEVA ALERTA DE RIESGO CRÓNICO
                            st.markdown(f"**{item['riesgo_cronico']}**")
                else:
                    st.info("✅ **Análisis completado:** No se detectaron ingredientes críticos. Aparentemente es de uso libre, pero mantén la prudencia con las cantidades.")
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
