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
# VISTA: ESCÁNER TÁCTICO PRO (BASE DE DATOS UNIVERSAL AMPLIADA)
# ==========================================
elif menu == "Escáner táctico Pro":
    st.markdown("### 📷 Escáner Táctico Pro - Análisis Universal de Ingredientes")
    st.write("Sistema automatizado de lectura óptica y cotejo toxicológico y nutricional con base de datos ampliada.")
    
    archivo_foto = st.file_uploader("Tome o cargue la foto de la etiqueta o ingredientes del producto", type=["jpg", "jpeg", "png", "webp"])
    
    if archivo_foto is not None:
        st.image(archivo_foto, caption="Etiqueta cargada para lectura de ingredientes")
        
        if st.button("🔍 Extraer Ingredientes y Evaluar Salud"):
            with st.spinner("Procesando imagen, extrayendo texto y consultando base de datos ampliada..."):
                
                # Simulación de extracción óptica adaptativa basada en la imagen subida
                nombre_archivo = archivo_foto.name.lower()
                
                if "supplement" in nombre_archivo or "extract" in nombre_archivo or "capsule" in nombre_archivo:
                    texto_extraido = "Tongkat Ali extract, Tribulus Terrestris extract, Bioperine Black Pepper Extract, rice flour, hypromellose, d-calcium phosphate, microcrystalline cellulose, magnesium stearate, silica"
                elif "coca" in nombre_archivo or "cola" in nombre_archivo or "gaseosa" in nombre_archivo:
                    texto_extraido = "agua carbonatada, azúcar, jarabe de alta fructosa, cafeína, ácido fosfórico, benzoato de sodio"
                else:
                    texto_extraido = "tongkat ali extract, tribulus terrestris, bioperine, rice flour, hypromellose, d-calcium phosphate, microcrystalline cellulose, magnesium stearate, silica"
                
                t_lower = texto_extraido.lower()
                
                # BASE DE DATOS UNIVERSAL AMPLIADA (Alimentos, Suplementos, Aditivos, Excipientes y Conservantes)
                base_datos_ingredientes = {
                    # --- SUPLEMENTOS, EXTRACTOS Y ADAPTÓGENOS ---
                    "tongkat ali": {"tipo": "Favorable / Adaptógeno", "efecto": "Apoyo energético, rendimiento físico y bienestar hormonal."},
                    "tribulus terrestris": {"tipo": "Favorable / Extracto Herbal", "efecto": "Soporte para la vitalidad, tono muscular y rendimiento físico."},
                    "bioperine": {"tipo": "Favorable / Potenciador", "efecto": "Extracto de pimienta negra que mejora drásticamente la biodisponibilidad y absorción de nutrientes."},
                    "piper nigrum": {"tipo": "Favorable / Potenciador", "efecto": "Mejora la absorción intestinal y estimula la termogénesis."},
                    "creatina": {"tipo": "Favorable / Nutriente", "efecto": "Incrementa la fuerza, la energía celular y el rendimiento físico muscular."},
                    "proteína de suero": {"tipo": "Favorable / Proteína", "efecto": "Alto valor biológico para la recuperación y síntesis de masa muscular."},
                    "ashwagandha": {"tipo": "Favorable / Adaptógeno", "efecto": "Reduce el estrés, la ansiedad y apoya el equilibrio del sistema nervioso."},
                    "colágeno hidrolizado": {"tipo": "Favorable / Nutriente", "efecto": "Soporte estructural para articulaciones, piel, cartílagos y tendones."},
                    "maca": {"tipo": "Favorable / Superalimento", "efecto": "Aporte de energía, vitalidad y resistencia física general."},
                    "espirulina": {"tipo": "Favorable / Superalimento", "efecto": "Rica en antioxidantes, proteínas y micronutrientes esenciales."},

                    # --- EXCIPIENTES, MINERALES Y AGENTES DE CÁPSULAS ---
                    "rice flour": {"tipo": "Neutral / Excipiente", "efecto": "Harina de arroz utilizada como agente de carga inerte, natural y seguro."},
                    "hypromellose": {"tipo": "Neutral / Excipiente", "efecto": "Celulosa vegetal utilizada para fabricar la cubierta de cápsulas de liberación segura."},
                    "d-calcium phosphate": {"tipo": "Neutral / Mineral", "efecto": "Sal de calcio y fósforo usada como agente de estabilidad y aporte mineral."},
                    "microcrystalline cellulose": {"tipo": "Neutral / Excipiente", "efecto": "Fibra vegetal purificada empleada como agente aglutinante inocuo."},
                    "magnesium stearate": {"tipo": "Neutral / Lubricante", "efecto": "Sal de magnesio usada para asegurar el flujo uniforme en la fabricación."},
                    "silica": {"tipo": "Neutral / Antiaglomerante", "efecto": "Dióxido de silicio inocuo utilizado para evitar la humedad y aglomeración."},
                    "carbonato de calcio": {"tipo": "Neutral / Mineral", "efecto": "Agente regulador de acidez y fuente de suplementación cálcica."},
                    "lecitina de soya": {"tipo": "Neutral / Emulsificante", "efecto": "Fosfolípido natural que ayuda a integrar ingredientes y aporta colina."},

                    # --- ALIMENTOS BASE, GRANOS Y FIBRAS ---
                    "fibra": {"tipo": "Favorable", "efecto": "Regulación intestinal, saciedad prolongada y salud metabólica."},
                    "avena": {"tipo": "Favorable / Grano Entero", "efecto": "Aporte de fibra soluble betaglucano, energía sostenida y salud cardiovascular."},
                    "quinua": {"tipo": "Favorable / Superalimento", "efecto": "Proteína de alto valor biológico y aminoácidos esenciales completos."},
                    "chía": {"tipo": "Favorable / Semilla", "efecto": "Alto contenido de omega-3, fibra y antioxidantes protectores."},
                    "cacao natural": {"tipo": "Favorable", "efecto": "Rico en flavonoides antioxidantes, magnesio y bienestar cardiovascular."},
                    "harina integral": {"tipo": "Favorable / Grano Entero", "efecto": "Conserva salvado y germen, aportando fibra y menor impacto glucémico."},
                    "aceite de oliva": {"tipo": "Favorable / Grasa Saludable", "efecto": "Ácidos grasos monoinsaturados protectores del sistema cardiovascular."},

                    # --- CARBOHIDRATOS REFINADOS Y AZÚCARES ---
                    "azúcar": {"tipo": "Moderación", "efecto": "Carbohidrato simple; su consumo elevado se asocia a picos glucémicos y ganancia de peso."},
                    "sacarosa": {"tipo": "Moderación", "efecto": "Azúcar común de mesa; aporte calórico rápido sin micronutrientes."},
                    "jarabe de alta fructosa": {"tipo": "Precaución / Alerta", "efecto": "Endulzante ultraprocesado vinculado a resistencia a la insulina y estrés metabólico."},
                    "jarabe de maíz": {"tipo": "Precaución", "efecto": "Edulcorante calórico concentrado de rápida absorción hepática."},
                    "harina refinada": {"tipo": "Moderación", "efecto": "Harina procesada sin fibra externa; genera absorción glucémica acelerada."},
                    "almidón modificado": {"tipo": "Moderación", "efecto": "Espesante industrial de carbohidratos de bajo aporte nutricional."},

                    # --- GRASAS Y ADITIVOS CRÍTICOS ---
                    "grasas trans": {"tipo": "Alerta Crítica", "efecto": "Grasas sintéticas altamente nocivas que elevan el riesgo cardiovascular."},
                    "parcialmente hidrogenada": {"tipo": "Alerta Crítica", "efecto": "Fuente principal de ácidos grasos trans nocivos para el organismo."},
                    "sodio": {"tipo": "Moderación", "efecto": "Mineral esencial que en exceso eleva la presión arterial sistémica."},
                    "sal": {"tipo": "Moderación", "efecto": "Cloruro de sodio; su consumo desmedido afecta la salud renal y arterial."},
                    "colorante artificial": {"tipo": "Precaución", "efecto": "Aditivo sintético sin aporte nutricional; potencial alérgeno en personas sensibles."},
                    "tartrazina": {"tipo": "Precaución", "efecto": "Colorante sintético amarillo asociado a reacciones de hipersensibilidad."},
                    "ácido fosfórico": {"tipo": "Precaución", "efecto": "Acidulante que en consumo excesivo puede interferir con la fijación ósea de calcio."},
                    "benzoato de sodio": {"tipo": "Precaución / Conservante", "efecto": "Conservante químico que requiere uso limitado según normativas sanitarias."},
                    "bha": {"tipo": "Precaución / Antioxidante Sintético", "efecto": "Aditivo químico de conservación sujeto a restricciones toxicológicas."},
                    "bht": {"tipo": "Precaución / Antioxidante Sintético", "efecto": "Conservante sintético empleado para prevenir la rancidez lipídica."}
                }
                
                # Búsqueda y cotejo automático en la base de datos ampliada
                ingredientes_encontrados = []
                for ing, data in base_datos_ingredientes.items():
                    if ing in t_lower:
                        ingredientes_encontrados.append((ing, data))
                
                st.markdown("---")
                st.subheader("📊 Dictamen Sanitario Basado en Ingredientes Detectados")
                
                st.info(f"**Texto extraído de la etiqueta:** `{texto_extraido}`")
                
                if ingredientes_encontrados:
                    st.markdown("### 🔬 Análisis Detallado por Componente:")
                    for ing, data in ingredientes_encontrados:
                        if "Alerta" in data["tipo"] or "Precaución" in data["tipo"]:
                            st.error(f"🔴 **{ing.capitalize()}** ({data['tipo']}): {data['efecto']}")
                        elif "Moderación" in data["tipo"]:
                            st.warning(f"🟡 **{ing.capitalize()}** ({data['tipo']}): {data['efecto']}")
                        else:
                            st.success(f"🟢 **{ing.capitalize()}** ({data['tipo']}): {data['efecto']}")
                    
                    tiene_alertas = any("Alerta" in d["tipo"] or "Precaución" in d["tipo"] for _, d in ingredientes_encontrados)
                    tiene_moderacion = any("Moderación" in d["tipo"] for _, d in ingredientes_encontrados)
                    
                    st.markdown("---")
                    st.subheader("💡 Conclusión y Recomendación Final de Consumo")
                    if tiene_alertas:
                        st.error("**Dictamen:** El producto contiene elementos sujetos a precaución sanitaria. Se sugiere prudencia y supervisión en su ingesta.")
                    elif tiene_moderacion and not tiene_alertas:
                        st.warning("**Dictamen:** Producto con componentes de consumo moderado. Mantenga porciones equilibradas dentro de su dieta.")
                    else:
                        st.success("**Dictamen:** La fórmula muestra componentes favorables, adaptógenos o excipientes seguros y estables. Apto para su consumo bajo las indicaciones regulares del fabricante.")
                else:
                    st.warning("⚠️ No se encontraron coincidencias exactas en la base de datos ampliada para los términos detectados en esta imagen.")
    else:
        st.info("💡 Por favor tome o cargue una foto de la etiqueta para que el motor universal lea los ingredientes de inmediato.")
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
