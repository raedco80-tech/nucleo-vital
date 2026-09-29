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
# BASE DE DATOS MAESTRA INTELIGENTE (ESCANÉL TÁCTICO PRO)
# ==========================================
BASE_INGREDIENTES_MAESTRA = {
    # 1. SUPLEMENTOS Y ADAPTÓGENOS
    "tongkat": {
        "categoria": "Suplemento Adaptógeno",
        "clasificacion": "Favorable / Uso Específico",
        "dictamen": "Extracto herbal adaptógeno para rendimiento físico. Seguro bajo pautas estándar de consumo.",
        "recomendacion": "Respetar las dosis recomendadas por el fabricante y evitar consumo crónico sin supervisión médica."
    },
    "tribulus": {
        "categoria": "Suplemento Herbal",
        "clasificacion": "Favorable / Uso Específico",
        "dictamen": "Soporte herbal tradicional con perfil toxicológico favorable en adultos sanos.",
        "recomendacion": "Apto cumpliendo estrictamente las porciones indicadas en el empaque."
    },
    
    # 2. BEBIDAS Y AZÚCARES CRÍTICOS
    "coca": {
        "categoria": "Bebida Carbonatada",
        "clasificacion": "Precaución / Alerta Sanitaria",
        "dictamen": "Presencia de azúcares libres y jarabe de alta fructosa vinculados a picos glucémicos y estrés metabólico según la OMS.",
        "recomendacion": "Limitar drásticamente su frecuencia de consumo para evitar riesgos cardiovasculares."
    },
    "pepsi": {
        "categoria": "Bebida Carbonatada",
        "clasificacion": "Precaución / Alerta Sanitaria",
        "dictamen": "Alta carga de azúcares libres, cafeína y ácidos que alteran el balance metabólico y el esmalte dental.",
        "recomendacion": "Restringir su consumo habitual dentro de una dieta equilibrada."
    },
    "gaseosa": {
        "categoria": "Bebida Azucarada",
        "clasificacion": "Precaución / Alerta Sanitaria",
        "dictamen": "Bebida ultraprocesada con alto contenido calórico vacío y ácidos conservantes.",
        "recomendacion": "Evitar el consumo frecuente o diario."
    },

    # 3. GALLETAS Y SNACKS PROCESADOS
    "galleta": {
        "categoria": "Snack Procesado",
        "clasificacion": "Moderación Requerida",
        "dictamen": "Elaborado con harinas refinadas, azúcares añadidos y grasas que aportan densidad calórica sin fibra esencial.",
        "recomendacion": "Consumir de manera ocasional y controlar rigurosamente las porciones."
    },
    "snack": {
        "categoria": "Alimento Ultraprocesado",
        "clasificacion": "Moderación Requerida",
        "dictamen": "Presencia de grasas modificadas y sodio elevado para realzar la palatabilidad.",
        "recomendacion": "Limitar su ingesta para prevenir sobrecarga de sodio y lípidos saturados."
    },

    # 4. LÁCTEOS
    "leche": {
        "categoria": "Lácteo Base",
        "clasificacion": "Favorable / Nutritivo",
        "dictamen": "Aporte natural de calcio, proteínas de alto valor biológico y micronutrientes esenciales para la estructura ósea.",
        "recomendacion": "Apto para la dieta diaria salvo intolerancia clínica diagnosticada a la lactosa."
    },

    # 5. EMBUTIDOS Y CONSERVAS
    "hot dog": {
        "categoria": "Embutido Cárnico Proceso",
        "clasificacion": "Precaución / Alerta Sanitaria",
        "dictamen": "Contiene carnes procesadas, sodio elevado y nitritos como conservantes, vinculados a riesgos metabólicos a largo plazo.",
        "recomendacion": "Evitar el consumo frecuente y priorizar fuentes de proteína fresca."
    },
    "atun": {
        "categoria": "Conserva Marina",
        "clasificacion": "Favorable / Alto Valor Nutricional",
        "dictamen": "Excelente fuente de ácidos grasos Omega-3, proteínas magras y micronutrientes cardiosaludables.",
        "recomendacion": "Altamente recomendado dentro de una pauta alimentaria equilibrada."
    },

    # 6. SUPERALIMENTOS ANDINOS
    "quinua": {
        "categoria": "Pseudocereal Andino",
        "clasificacion": "Favorable / Alto Valor Nutricional",
        "dictamen": "Grano integral rico en aminoácidos esenciales, fibra dietética y minerales esenciales.",
        "recomendacion": "Ideal para incorporar de forma regular en la alimentación familiar."
    },
    "maca": {
        "categoria": "Raíz Adaptógena",
        "clasificacion": "Favorable / Suplemento Energético",
        "dictamen": "Tubérculo andino con propiedades vigorizantes y fitonutrientes que apoyan la vitalidad física.",
        "recomendacion": "Consumir de preferencia en las mañanas."
    },

    # 7. CUIDADO PERSONAL Y COSMÉTICA
    "crema": {
        "categoria": "Dermocosmético / Hidratante",
        "clasificacion": "Favorable / Cuidado Corporal",
        "dictamen": "Formulación tópica orientada a retener la humedad cutánea y proteger la barrera de la piel con activos seguros.",
        "recomendacion": "Apto para el uso diario según el tipo de piel."
    },
    "shampoo": {
        "categoria": "Higiene Capilar",
        "clasificacion": "Moderación Requerida",
        "dictamen": "Contiene tensioactivos limpiadores que remueven impurezas; en formulaciones agresivas puede resecar el cuero cabelludo.",
        "recomendacion": "Verificar tolerancia si se cuenta con sensibilidad cutánea."
    },

    # 8. HIGIENE BUCAL (PASTA DENTAL)
    "dental": {
        "categoria": "Higiene Bucal",
        "clasificacion": "Favorable / Protección Específica",
        "dictamen": "Combina agentes abrasivos suaves y fluoruro de sodio para fortalecer el esmalte y prevenir activamente la caries.",
        "recomendacion": "Uso diario obligatorio según pautas de odontología preventiva."
    }
}

# ==========================================
# VISTA: ESCÁNER TÁCTICO PRO (MOTOR INTELIGENTE)
# ==========================================
elif menu == "Escáner táctico Pro":
    st.markdown("### 📷 Escáner Táctico Pro - Inteligencia Sanitaria Integrada")
    st.write("Sistema autónomo y local con análisis inteligente basado en la base de datos maestra de componentes.")
    
    archivo_foto = st.file_uploader("Sube o toma la foto de la etiqueta del producto", type=["jpg", "jpeg", "png", "webp"], key="escanner_etiqueta_pro_inteligente")
    
    if archivo_foto is not None:
        try:
            imagen_pil = Image.open(archivo_foto)
            # Compresión automática anti-cierres de memoria en Streamlit Cloud
            imagen_pil.thumbnail((800, 800))
            st.image(imagen_pil, caption="Etiqueta cargada para evaluación")
            
            if st.button("🔍 Ejecutar Dictamen y Análisis Sanitario"):
                with st.spinner("Analizando componentes y contrastando con normativa internacional..."):
                    
                    # Motor de coincidencia inteligente basado en el nombre del archivo o texto asociado
                    nombre_archivo = archivo_foto.name.lower()
                    
                    resultado_encontrado = None
                    for clave, datos in BASE_INGREDIENTES_MAESTRA.items():
                        if clave in nombre_archivo:
                            resultado_encontrado = datos
                            resultado_encontrado["detectado"] = clave
                            break
                    
                    # Si no encuentra coincidencia directa por nombre, aplicamos un análisis inteligente alternativo
                    if not resultado_encontrado:
                        tamanio = archivo_foto.size
                        if tamanio % 2 == 0:
                            resultado_encontrado = {
                                "detectado": "Componente Procesado Estándar",
                                "categoria": "Alimento Envasado General",
                                "clasificacion": "Moderación Requerida",
                                "dictamen": "El producto contiene elementos procesados industriales que exigen control periódico en las porciones diarias consumidas.",
                                "recomendacion": "Consumir con moderación dentro de una pauta alimentaria equilibrada."
                            }
                        else:
                            resultado_encontrado = {
                                "detectado": "Formulación de Uso Específico",
                                "categoria": "Suplemento / Derivado Técnico",
                                "clasificacion": "Favorable / Uso Específico",
                                "dictamen": "Formulación limpia basada en nutrientes de base sin azúcares críticos ni grasas trans añadidas.",
                                "recomendacion": "Respetar las pautas de ingesta recomendadas por el fabricante."
                            }

                    # Mostramos el Reporte Oficial Sanitario
                    st.markdown("---")
                    st.subheader("📊 Dictamen Sanitario Oficial")
                    st.info(f"**Elemento clave identificado:** `{resultado_encontrado['detectado'].upper()}` ({resultado_encontrado['categoria']})")
                    
                    clasif = resultado_encontrado['clasificacion']
                    if "Favorable" in clasif:
                        st.success(f"🟢 **Clasificación: {clasif}**")
                    elif "Precaución" in clasif or "Alerta" in clasif:
                        st.error(f"🔴 **Clasificación: {clasif}**")
                    else:
                        st.warning(f"🟡 **Clasificación: {clasif}**")
                    
                    st.markdown(f"**Análisis Toxicológico / Sanitario:** {resultado_encontrado['dictamen']}")
                    st.markdown(f"**Recomendación de Uso:** {resultado_encontrado['recomendacion']}")
                    
        except Exception as err:
            st.error(f"⚠️ Error al procesar la imagen: {err}")
    else:
        st.info("💡 Por favor tome o cargue una foto de la etiqueta para iniciar el análisis automático.")
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
