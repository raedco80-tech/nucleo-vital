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
    # BASE DE DATOS INTERNA (AUTOCONTENIDA)
    # ==========================================
    BASE_INGREDIENTES_MAESTRA = {
        # 1. SUPLEMENTOS Y BEBIDAS
        "tongkat": {"categoria": "Suplemento", "clasificacion": "Favorable", "dictamen": "Adaptógeno para rendimiento físico.", "recomendacion": "Respetar dosis."},
        "tribulus": {"categoria": "Suplemento Herbal", "clasificacion": "Favorable / Uso Específico", "dictamen": "Soporte herbal tradicional. Seguro en adultos sanos.", "recomendacion": "Apto cumpliendo porciones."},
        "coca": {"categoria": "Bebida Carbonatada", "clasificacion": "Precaución / Alerta Sanitaria", "dictamen": "Alta carga de azúcares libres y jarabe de alta fructosa.", "recomendacion": "Limitar drásticamente."},
        "pepsi": {"categoria": "Bebida Carbonatada", "clasificacion": "Precaución / Alerta Sanitaria", "dictamen": "Alta en azúcares, ácidos y cafeína.", "recomendacion": "Restringir consumo habitual."},
        "gaseosa": {"categoria": "Bebida Azucarada", "clasificacion": "Precaución / Alerta Sanitaria", "dictamen": "Bebida ultraprocesada, calorías vacías.", "recomendacion": "Evitar consumo frecuente."},
        
        # 2. ALIMENTOS Y SNACKS
        "galleta": {"categoria": "Snack Procesado", "clasificacion": "Moderación Requerida", "dictamen": "Harinas refinadas y azúcares añadidos.", "recomendacion": "Consumo ocasional."},
        "snack": {"categoria": "Ultraprocesado", "clasificacion": "Moderación Requerida", "dictamen": "Exceso de sodio y grasas modificadas.", "recomendacion": "Limitar ingesta."},
        "leche": {"categoria": "Lácteo Base", "clasificacion": "Favorable / Nutritivo", "dictamen": "Aporte natural de calcio y proteínas.", "recomendacion": "Apto para dieta diaria."},
        "hot dog": {"categoria": "Embutido Cárnico", "clasificacion": "Precaución / Alerta Sanitaria", "dictamen": "Carnes procesadas con nitritos y exceso de sodio.", "recomendacion": "Evitar consumo frecuente."},
        "atun": {"categoria": "Conserva Marina", "clasificacion": "Favorable / Nutritivo", "dictamen": "Fuente de Omega-3 y proteínas.", "recomendacion": "Altamente recomendado."},
        "quinua": {"categoria": "Cereal Andino", "clasificacion": "Favorable / Nutritivo", "dictamen": "Rico en aminoácidos esenciales.", "recomendacion": "Consumo regular."},
        "maca": {"categoria": "Raíz Adaptógena", "clasificacion": "Favorable / Energético", "dictamen": "Tubérculo con propiedades vigorizantes.", "recomendacion": "Preferente en mañanas."},

        # 3. HIGIENE Y COSMÉTICA
        "crema": {"categoria": "Dermocosmético", "clasificacion": "Favorable / Seguro", "dictamen": "Retiene la humedad cutánea.", "recomendacion": "Apto para uso diario."},
        "shampoo": {"categoria": "Higiene Capilar", "clasificacion": "Moderación Requerida", "dictamen": "Contiene tensioactivos que pueden resecar.", "recomendacion": "Verificar tolerancia."},
        "dental": {"categoria": "Higiene Bucal", "clasificacion": "Favorable / Seguro", "dictamen": "Abrasivos suaves y fluoruro para el esmalte.", "recomendacion": "Uso diario obligatorio."},
        "aluminio": {"categoria": "Antitranspirante", "clasificacion": "Precaución / Monitoreo", "dictamen": "Bloquea conductos sudoríparos. Posible acumulación.", "recomendacion": "Alternar con desodorantes libres de aluminio."},
        "triclosan": {"categoria": "Antibacteriano", "clasificacion": "Precaución / Alerta Sanitaria", "dictamen": "Asociado a alteración endocrina y resistencia bacteriana.", "recomendacion": "Evitar productos que lo contengan."},
        "alcohol denat": {"categoria": "Solvente Cosmético", "clasificacion": "Moderación Requerida", "dictamen": "Seca rápido pero irrita pieles sensibles.", "recomendacion": "Evitar en piel atópica."},
        "parabenos": {"categoria": "Conservante", "clasificacion": "Precaución / Monitoreo", "dictamen": "Asociados a disrupción endocrina leve.", "recomendacion": "Buscar opciones 'Libre de parabenos'."},
        "fragancia": {"categoria": "Aromatizante", "clasificacion": "Moderación Requerida", "dictamen": "Puede contener alérgenos que causan dermatitis.", "recomendacion": "Vigilar reacciones en la piel."},

        # 4. BEBÉS E INFANTIL
        "cocamidopropil betaina": {"categoria": "Limpiador Suave", "clasificacion": "Favorable / Seguro", "dictamen": "Tensioactivo derivado del coco, ideal para piel sensible.", "recomendacion": "Excelente para higiene infantil."},
        "fenoxietanol": {"categoria": "Conservante Cosmético", "clasificacion": "Precaución / Monitoreo", "dictamen": "Usado en toallitas húmedas. Puede irritar pieles muy delicadas.", "recomendacion": "Evitar uso excesivo en zonas irritadas."},

        # 5. LIMPIEZA DEL HOGAR Y GARAJE
        "hipoclorito de sodio": {"categoria": "Desinfectante (Lejía)", "clasificacion": "Peligro / Tóxico por Inhalación", "dictamen": "Altamente corrosivo. Sus gases irritan las vías respiratorias.", "recomendacion": "Usar con guantes, diluido y en áreas ventiladas. NO mezclar."},
        "amonio cuaternario": {"categoria": "Antibacteriano de Superficies", "clasificacion": "Moderación Requerida", "dictamen": "Eficaz desinfectante, pero causa dermatitis por contacto directo.", "recomendacion": "Mantener lejos de niños y enjuagar superficies."},
        "acido sulfonico": {"categoria": "Detergente Fuerte", "clasificacion": "Precaución / Irritante", "dictamen": "Desengrasante que destruye la barrera natural de las manos.", "recomendacion": "Usar guantes de goma obligatoriamente."},
        "ftalatos": {"categoria": "Plastificante / Fragancia", "clasificacion": "Precaución / Alerta Sanitaria", "dictamen": "Disruptor endocrino común en ambientadores sintéticos.", "recomendacion": "Ventilar bien los espacios cerrados."},
        "metanol": {"categoria": "Solvente Industrial", "clasificacion": "Peligro / Altamente Tóxico", "dictamen": "Alcohol industrial que se absorbe por la piel.", "recomendacion": "Manipular con equipo de protección estricto."}
    }

    # ==========================================
    # INTERFAZ DE USUARIO: ESCÁNER TÁCTICO PRO
    # ==========================================
    st.markdown("### 📷 y 🎙️ Escáner Táctico Pro - Análisis por Voz y Texto")
    st.write("Sube la imagen del producto como registro y usa el dictado por voz o teclado para analizar los ingredientes reales.")
    
    # 1. Carga de imagen (Evidencia visual)
    archivo_foto = st.file_uploader("1. Sube o toma la foto del producto", type=["jpg", "jpeg", "png", "webp"], key="foto_evidencia")
    if archivo_foto is not None:
        try:
            imagen_pil = Image.open(archivo_foto)
            imagen_pil.thumbnail((400, 400)) # Compresión de seguridad
            st.image(imagen_pil, caption="Evidencia visual cargada")
        except Exception as err:
            st.error("Error al procesar la imagen.")

    st.markdown("---")
    
    # 2. Ingreso por voz/texto
    st.markdown("#### 🎙️ Lector de Ingredientes")
    st.info("Escribe los ingredientes o usa el **micrófono de tu teclado** para dictarlos rápidamente.")
    
    ingredientes_texto = st.text_area("Ingresa los ingredientes aquí:", height=100, placeholder="Ejemplo: Contiene agua, aluminio, triclosán, metanol...")
    
    if st.button("🔍 Analizar Ingredientes Reales"):
        if ingredientes_texto.strip() == "":
            st.warning("⚠️ Por favor, dicta o escribe algunos ingredientes antes de analizar.")
        else:
            with st.spinner("Analizando componentes toxicológicos..."):
                texto_minusculas = ingredientes_texto.lower()
                componentes_hallados = []

                # Búsqueda de coincidencias
                for clave, datos in BASE_INGREDIENTES_MAESTRA.items():
                    if clave in texto_minusculas:
                        datos_encontrados = datos.copy()
                        datos_encontrados["detectado"] = clave
                        componentes_hallados.append(datos_encontrados)

                # Despliegue de Resultados
                st.markdown("---")
                st.subheader("📊 Reporte Sanitario Oficial")
                
                if len(componentes_hallados) > 0:
                    st.success(f"Se identificaron **{len(componentes_hallados)}** componentes clave:")
                    
                    for item in componentes_hallados:
                        with st.expander(f"📌 {item['detectado'].upper()} ({item['categoria']})", expanded=True):
                            clasif = item['clasificacion']
                            
                            # Asignación de semáforo
                            if "Favorable" in clasif:
                                st.success(f"🟢 **Clasificación: {clasif}**")
                            elif "Peligro" in clasif or "Alerta" in clasif:
                                st.error(f"🔴 **Clasificación: {clasif}**")
                            else:
                                st.warning(f"🟡 **Clasificación: {clasif}**")
                            
                            st.write(f"**Dictamen:** {item['dictamen']}")
                            st.write(f"**Recomendación:** {item['recomendacion']}")
                else:
                    st.info("✅ **Análisis completado:** No se detectaron ingredientes críticos o tóxicos en el texto ingresado. El producto posee una formulación no registrada en la base de alertas.")
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
