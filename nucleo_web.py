from datetime import datetime, timedelta
import uuid
import streamlit as st
from PIL import Image
# Configuración de la página táctica
st.set_page_config(
    page_title="Núcleo Vital - Centro de Mando",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo táctico / oscuro personalizado
st.markdown(
    """
    <style>
    .main { background-color: #0e1117; color: #c9d1d9; }
    .stButton>button { background-color: #238636; color: white; border-radius: 8px; font-weight: bold; height: 65px !important; font-size: 18px !important; margin-bottom: 5px; border: 2px solid #3fb950; }
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
    import csv
    import urllib.request

    if not token:
        return False, "Por favor ingrese una clave de acceso."

    # Conexión global a la bóveda de Google Sheets
    sheet_id = "1xVHT-PoTz_M7zu8Dlzqi6DGTQ86zow1qeBxNIGzAHJ8"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

    try:
        response = urllib.request.urlopen(url)
        lines = [l.decode('utf-8') for l in response.readlines()]
        reader = csv.reader(lines)
        next(reader) # Saltar cabecera

        for row in reader:
            if len(row) >= 3:
                clave_db = row[1].strip()
                estado_db = row[2].strip()

                if token == clave_db:
                    if estado_db.upper() == "ACTIVO":
                        # Se descarga el nombre y el contacto SIN IMPORTAR si es admin o usuario
                        st.session_state.nombre_usuario = row[0].strip()
                        st.session_state.contacto_sos = row[3].strip() if len(row) >= 4 else ""
                        
                        # Verifica si es el admin para darle su panel especial
                        if token == CLAVE_MAESTRA:
                            return True, "MASTER"
                        else:
                            return True, "USUARIO"
                    else:
                        return False, "⚠️ Esta clave ha sido desactivada."
        
        return False, "❌ Clave incorrecta o no registrada en el sistema."

    except Exception as e:
        return False, f"⚠️ Error de enlace satelital con la base maestra."


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
 # Inicializar memoria de pantalla si no existe
        if 'menu_actual' not in st.session_state:
            st.session_state['menu_actual'] = "Centro de Mando"

        st.sidebar.markdown("### ⚡ Navegación Táctica")

        # Botones táctiles anchos (use_container_width=True hace que ocupen todo el ancho)
        if st.sidebar.button("📊 Centro de Mando", use_container_width=True):
            st.session_state['menu_actual'] = "Centro de Mando"
            
        if st.sidebar.button("🛡️ Escudo y memoria", use_container_width=True):
            st.session_state['menu_actual'] = "Escudo y memoria"
            
        if st.sidebar.button("📷 Escáner táctico Pro", use_container_width=True):
            st.session_state['menu_actual'] = "Escáner táctico Pro"
            
        if st.sidebar.button("🚑 Triaje y Alerta SOS", use_container_width=True):
            st.session_state['menu_actual'] = "Triaje y Alerta SOS"
            
        if st.sidebar.button("👤 Perfil y Contacto SOS", use_container_width=True):
            st.session_state['menu_actual'] = "Perfil y Contacto SOS"

        # Conectar el botón presionado con el resto de tu código
        menu = st.session_state['menu_actual']

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
                
                st.markdown(f"### Semáforo en Ruta: <span style='color: {color_html}; font-weight: bold;'>{semaforo}</span>", unsafe_allow_html=True)
                st.success(f"📍 Destino fijado: **{destino}**")
                
                ruta_gps = destino.replace(" ", "+")
                enlace_mapa = f"https://www.google.com/maps/dir/?api=1&destination={ruta_gps}"
                
                st.markdown(f"""
                <a href="{enlace_mapa}" target="_blank" style="text-decoration: none;">
                    <button style="background-color: #1f6feb; color: white; border-radius: 8px; font-weight: bold; height: 60px; width: 100%; font-size: 18px; border: 2px solid #388bfd; cursor: pointer; margin-top: 10px; margin-bottom: 10px;">
                        🛰️ INICIAR NAVEGACIÓN GPS (GOOGLE MAPS)
                    </button>
                </a>
                """, unsafe_allow_html=True)
                
                if incidente_camino:
                    st.warning(f"📌 Incidente reportado en bitácora: '{incidente_camino}'")
                    
                st.progress(100)
            else:
                st.warning("Por favor ingrese un destino válido.")
# --- VISTA: ESCÁNER TÁCTICO PRO ---
elif menu == "Escáner táctico Pro":
        st.title("🔎 Escáner táctico Pro")
        st.write("Analice alimentos, bebidas o productos de cuidado personal.")

        producto_scan = st.text_input("Ingrese el nombre del producto (ej. Ajinomen, Shampoo):")

        if st.button("Ejecutar Análisis Médico"):
            if producto_scan:
                termino = producto_scan.lower().strip()
                
                sheet_id = "1xVHT-PoTz_M7zu8Dlzqi6DGTQ86zow1qeBxNIGzAHJ8"
                gid_escaner = "400163944"
                
                url_escaner = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid_escaner}"

                encontrado = False
                try:
                    import urllib.request
                    import csv
                    response = urllib.request.urlopen(url_escaner)
                    lines = [l.decode('utf-8') for l in response.readlines()]
                    reader = csv.reader(lines)
                    next(reader) # Saltar la cabecera

                    for row in reader:
                        if len(row) >= 5:
                            nombre_db = row[0].strip()
                            if termino in nombre_db.lower():
                                encontrado = True
                                ingredientes = row[1]
                                uso_cronico = row[2]
                                recomendacion = row[3]
                                clasificacion = row[4]

                                st.subheader(f"🏷 Producto Identificado: {nombre_db}")
                                
                                if "Peligro" in clasificacion:
                                    st.error(f"🔴 **Clasificación:** {clasificacion}")
                                elif "Alerta" in clasificacion:
                                    st.warning(f"🟡 **Clasificación:** {clasificacion}")
                                else:
                                    st.success(f"🟢 **Clasificación:** {clasificacion}")
                                
                                st.write(f"**🧪 Componentes Críticos:** {ingredientes}")
                                st.write(f"**⚠️ Impacto por Uso Crónico:** {uso_cronico}")
                                st.info(f"💡 **Recomendación Táctica:** {recomendacion}")
                                break # Detener búsqueda al encontrar coincidencia

                    if not encontrado:
                        st.success("✅ **Estado:** Producto no registrado en alertas rojas primarias.")
                        st.markdown("### 📊 Reporte Preventivo de Consumo General")
                        st.write("**Composición:** Si es un producto procesado o químico, la ausencia de toxinas graves no significa que sea inofensivo a largo plazo.")
                        st.warning("⚠️ **Precaución de Uso Crónico:**")
                        st.write("- **Sobrecarga Metabólica/Dérmica:** El uso diario de procesados (o químicos en la piel) obliga al cuerpo a filtrar conservantes, generando fatiga celular.")
                        st.info("💡 **Regla Táctica:** Apto estrictamente para uso ocasional. Priorice alimentos naturales y productos libres de parabenos/sulfatos.")

                except Exception as e:
                    st.error("⚠️ Error de enlace satelital con la base de datos médica.")
            else:
                st.warning("Por favor ingrese un producto para iniciar el escaneo.")
elif menu == "Triaje y Alerta SOS":
        st.title("🚨 Triaje y Alerta SOS")

        if "contacto_sos" not in st.session_state:
            st.session_state.contacto_sos = "+51 900000000"

        st.write("Ingrese el malestar o accidente para recibir asistencia médica inmediata:")
        
        sintoma_reporte = st.text_input("Describa el síntoma (ej. fiebre alta, dolor de cabeza, corte):")

        if st.button("⚡ Ejecutar Triaje Clínico"):
            if sintoma_reporte:
                termino = sintoma_reporte.lower().strip()
                
                sheet_id = "1xVHT-PoTz_M7zu8Dlzqi6DGTQ86zow1qeBxNIGzAHJ8"
                gid_triaje = "1008699611" 
                url_triaje = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid_triaje}"
                
                encontrado = False
                try:
                    import urllib.request
                    import csv
                    response = urllib.request.urlopen(url_triaje)
                    lines = [l.decode('utf-8') for l in response.readlines()]
                    reader = csv.reader(lines)
                    next(reader) # Saltar la cabecera

                    for row in reader:
                        if len(row) >= 5:
                            sintoma_db = row[0].strip()
                            if termino in sintoma_db.lower():
                                encontrado = True
                                gravedad = row[1].strip().upper()
                                primeros_aux = row[2].strip()
                                medicina = row[3].strip()
                                alerta_sos = row[4].strip().upper()

                                st.subheader(f"🩺 Evaluación para: {sintoma_db}")
                                
                                if "GRAVE" in gravedad:
                                    st.error(f"⚠️ **NIVEL DE GRAVEDAD:** {gravedad}")
                                elif "MODERADO" in gravedad:
                                    st.warning(f"🟡 **NIVEL DE GRAVEDAD:** {gravedad}")
                                else:
                                    st.success(f"🟢 **NIVEL DE GRAVEDAD:** {gravedad}")
                                
                                st.info(f"**🛠️ Instrucciones de Primeros Auxilios:** {primeros_aux}")
                                st.write(f"**💊 Medicina Básica Sugerida:** {medicina}")
                                
                                if alerta_sos == "SI":
                                    st.error("🚨 **ACCIÓN CRÍTICA REQUERIDA:** Riesgo alto detectado. Por favor, desplácese hacia abajo y active la Alerta SOS de inmediato.")
                                break

                    if not encontrado:
                        st.warning("⚠️ Síntoma no registrado con exactitud. Si considera que es una emergencia real, active el SOS en la parte inferior.")

                except Exception as e:
                    st.error("⚠️ Error de enlace con la base médica de Triaje.")
            else:
                st.warning("Por favor ingrese un síntoma para analizar.")
                
        st.markdown("---")
                        
        import streamlit.components.v1 as components
                        
        numero_wsp = st.session_state.contacto_sos.replace("+", "").replace(" ", "")
                        sintoma_seguro = sintoma_reporte.replace("'", "").replace('"', "")
                        
                        # --- EXTRACCIÓN GPS CALIBRADA EN ALTA PRECISIÓN ---
                        codigo_gps = f"""
                        <script>
                        function enviarSOS() {{
                            if (navigator.geolocation) {{
                                var opcionesGPS = {{
                                    enableHighAccuracy: true,
                                    timeout: 15000,
                                    maximumAge: 0
                                }};
                                
                                navigator.geolocation.getCurrentPosition(function(position) {{
                                    var lat = position.coords.latitude;
                                    var lon = position.coords.longitude;
                                    var mapa = "https://www.google.com/maps?q=" + lat + "," + lon;
                                    var mensaje = "🚨 ALERTA SOS CRÍTICA 🚨 Paciente reporta: {sintoma_seguro}. Ubicación exacta GPS: " + mapa;
                                    var url = "https://wa.me/{numero_wsp}?text=" + encodeURIComponent(mensaje);
                                    window.open(url, "_blank");
                                }}, function(error) {{
                                    alert("⚠️ El GPS está tardando. Por favor, acércate a una ventana o sal al patio para que la tablet detecte los satélites.");
                                }}, opcionesGPS);
                            }} else {{
                                alert("El dispositivo no soporta funciones de GPS.");
                            }}
                        }}
                        </script>
                        <button onclick="enviarSOS()" style="background-color: #25D366; color: white; border-radius: 8px; font-weight: bold; height: 60px; width: 100%; font-size: 18px; border: 2px solid #128C7E; cursor: pointer; margin-top: 10px; font-family: sans-serif;">
                            🛰️ EXTRAER GPS EXACTO Y ENVIAR ALERTA
                        </button>
                        """
                        components.html(codigo_gps, height=85)
                    else:
                        st.success("💊 **Triaje Exitoso:** Proceda con observación de rutina.")
                else:
                    st.warning("⚠️ Faltan datos: Por favor, describa los síntomas.")

        # --- VISTA: PERFIL Y CONTACTO SOS ---
elif menu == "Perfil y Contacto SOS":
        st.title("👤 Configuración del Perfil")
            
        st.info("🔒 Perfil gestionado por el Administrador central.")
        nombre_db = st.session_state.get("nombre_usuario", "Usuario")
        contacto_db = st.session_state.get("contacto_sos", "No registrado")
        
        st.text_input("Nombre / Rol (Solo lectura):", value=nombre_db, disabled=True)
        st.text_input("Número de Contacto SOS:", value=contacto_db, disabled=True)
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
