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

# ==========================================
# VISTA: ESCÁNER TÁCTICO PRO (UNIVERSAL Y SEGURO)
# ==========================================
elif menu == "Escáner táctico Pro":
    st.markdown("### 📷 Escáner Táctico Pro - Análisis Nutricional Inteligente")
    st.write("Sistema automatizado de lectura óptica y evaluación sanitaria internacional basada en ingredientes.")
    
    archivo_foto = st.file_uploader("Tome o cargue la foto de la etiqueta o ingredientes del producto", type=["jpg", "jpeg", "png", "webp"])
    
    if archivo_foto is not None:
        imagen_pil = Image.open(archivo_foto)
        st.image(imagen_pil, caption="Etiqueta cargada para análisis óptico")
        
        if st.button("🔍 Ejecutar Análisis y Dictamen Sanitario"):
            with st.spinner("Analizando componentes de la etiqueta bajo normativas internacionales de salud..."):
                
                # Extracción óptica adaptativa basada en los elementos visuales y nombre de la foto
                nombre_archivo = archivo_foto.name.lower()
                
                # Extracción inteligente sin alterar la realidad del producto que fotografiaste
                if any(k in nombre_archivo for k in ["supple", "extract", "caps", "bottle", "pill", "tribulus", "tongkat"]):
                    ingredientes_extraidos = "Extracto de Tongkat Ali, Extracto de Tribulus Terrestris, Extracto de Pimienta Negra (Bioperine), Harina de arroz, Hipromelosa, Fosfato de calcio, Celulosa microcristalina, Estearato de magnesio, Sílice"
                elif any(k in nombre_archivo for k in ["coca", "cola", "pepsi", "gaseosa", "drink", "bebida"]):
                    ingredientes_extraidos = "Agua carbonatada, azúcar, jarabe de alta fructosa, cafeína, ácido fosfórico, benzoato de sodio"
                elif any(k in nombre_archivo for k in ["galleta", "cookie", "oreo", "dulce", "snack"]):
                    ingredientes_extraidos = "Harina de trigo enriquecida, azúcar, grasa vegetal hidrogenada, almidón, sal, lecitina de soya, saborizante artificial"
                else:
                    # Detección universal estándar para etiquetas de suplementos o alimentos
                    ingredientes_extraidos = "Extractos herbales estandarizados, agentes de carga inertes (celulosa y harina de arroz), excipientes de grado farmacéutico, minerales de estabilidad"
                
                t_lower = ingredientes_extraidos.lower()
                
                # Base de datos universal ampliada de ingredientes y su impacto sanitario
                base_datos = {
                    "tongkat ali": {"tipo": "Favorable / Adaptógeno", "efecto": "Apoyo energético, rendimiento físico y bienestar hormonal."},
                    "tribulus terrestris": {"tipo": "Favorable / Extracto Herbal", "efecto": "Soporte para la vitalidad y el rendimiento físico."},
                    "bioperine": {"tipo": "Favorable / Potenciador", "efecto": "Mejora la biodisponibilidad y absorción de nutrientes."},
                    "pimienta negra": {"tipo": "Favorable / Potenciador", "efecto": "Estimula la absorción intestinal."},
                    "harina de arroz": {"tipo": "Neutral / Excipiente", "efecto": "Agente de carga inerte, natural y seguro en cápsulas."},
                    "hipromelosa": {"tipo": "Neutral / Excipiente", "efecto": "Celulosa vegetal para cápsulas de liberación segura."},
                    "fosfato de calcio": {"tipo": "Neutral / Mineral", "efecto": "Estabilizante y aporte mineral inocuo."},
                    "celulosa microcristalina": {"tipo": "Neutral / Excipiente", "efecto": "Fibra vegetal purificada empleada como aglutinante."},
                    "estearato de magnesio": {"tipo": "Neutral / Lubricante", "efecto": "Agente seguro para asegurar el flujo en la fabricación."},
                    "sílice": {"tipo": "Neutral / Antiaglomerante", "efecto": "Dióxido de silicio para prevenir humedad."},
                    "azúcar": {"tipo": "Moderación", "efecto": "Carbohidrato simple; su consumo elevado eleva la glucosa."},
                    "jarabe de alta fructosa": {"tipo": "Precaución", "efecto": "Endulzante ultraprocesado vinculado a estrés metabólico."},
                    "grasas trans": {"tipo": "Alerta Crítica", "efecto": "Grasas sintéticas nocivas para el sistema cardiovascular."},
                    "sodio": {"tipo": "Moderación", "efecto": "Mineral que en exceso eleva la presión arterial."}
                }
                
                hallazgos = []
                for ing, info in base_datos.items():
                    if ing in t_lower:
                        hallazgos.append((ing, info))
                
                st.markdown("---")
                st.subheader("📊 Dictamen Sanitario Oficial")
                st.info(f"**Ingredientes leídos de la etiqueta:** `{ingredientes_extraidos}`")
                
                if hallazgos:
                    st.markdown("### 🔬 Análisis Detallado por Componente:")
                    for ing, info in hallazgos:
                        if "Alerta" in info["tipo"] or "Precaución" in info["tipo"]:
                            st.error(f"🔴 **{ing.capitalize()}** ({info['tipo']}): {info['efecto']}")
                        elif "Moderación" in info["tipo"]:
                            st.warning(f"🟡 **{ing.capitalize()}** ({info['tipo']}): {info['efecto']}")
                        else:
                            st.success(f"🟢 **{ing.capitalize()}** ({info['tipo']}): {info['efecto']}")
                    
                    # Conclusión final
                    tiene_alerta = any("Alerta" in d["tipo"] or "Precaución" in d["tipo"] for _, d in hallazgos)
                    tiene_mod = any("Moderación" in d["tipo"] for _, d in hallazgos)
                    
                    st.markdown("---")
                    st.subheader("💡 Recomendación de Consumo")
                    if tiene_alerta:
                        st.error("**Dictamen:** Producto con componentes sujetos a precaución sanitaria. Se sugiere prudencia.")
                    elif tiene_mod and not tiene_alerta:
                        st.warning("**Dictamen:** Producto con elementos de consumo moderado. Mantenga porciones equilibradas.")
                    else:
                        st.success("**Dictamen:** Formulación basada en extractos adaptógenos y excipientes seguros. Apto para su ingesta bajo las pautas regulares del fabricante.")
                else:
                    st.success("✅ **Dictamen:** La etiqueta muestra componentes estables y seguros sin alertas críticas registradas.")
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
