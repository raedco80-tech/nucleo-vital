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
elif menu == "Escáner táctico Pro":
    # ==========================================
    # BASE DE DATOS MAESTRA UNIFICADA Y EXPANDIDA (V. DEFINITIVA)
    # ==========================================
    BASE_INGREDIENTES_MAESTRA = {
        # --- 1. PLATOS TÍPICOS Y CRIOLLOS ---
        "caja china": {"categoria": "Asado por Calor Radiante", "clasificacion": "Moderación Requerida", "dictamen": "Método de cocción superior a la fritura. Drena gran parte de la grasa pesada.", "recomendacion": "Acompañar con ensalada y evitar el exceso de piel (galleta).", "limite": "1 a 2 veces al mes.", "riesgo_cronico": "⚠️ CONSUMO EXCESIVO: El exceso de piel crocante eleva los triglicéridos y el colesterol LDL."},
        "chicharron": {"categoria": "Fritura Profunda de Cerdo", "clasificacion": "Precaución / Peligro Metabólico", "dictamen": "Altísima densidad calórica y grasas saturadas.", "recomendacion": "Acompañar con abundante sarsa criolla para ayudar a la digestión.", "limite": "Porción moderada 1 vez al mes.", "riesgo_cronico": "🚨 CONSUMO FRECUENTE: Obesidad, hígado graso agudo y riesgo de obstrucción arterial."},
        "carapulcra": {"categoria": "Guiso Tradicional Andino/Criollo", "clasificacion": "Moderación Requerida", "dictamen": "Nutritivo pero extremadamente denso en calorías. Si se combina con Sopa Seca, la carga calórica se duplica.", "recomendacion": "Servir porciones medidas.", "limite": "Plato fuerte ocasional (cada 15 días).", "riesgo_cronico": "🚨 CONSUMO FRECUENTE: Sobrecarga de carbohidratos que genera resistencia a la insulina."},
        "sopa seca": {"categoria": "Pasta Criolla (Carbohidrato Alto)", "clasificacion": "Precaución / Alto Índice Glucémico", "dictamen": "Aporta energía inmediata pero muy baja fibra.", "recomendacion": "Evitar comer en la noche. No repetir plato.", "limite": "Máximo 1 a 2 veces por mes.", "riesgo_cronico": "🚨 CONSUMO FRECUENTE: Picos crónicos de glucosa y predisposición a diabetes tipo 2."},
        "tamal": {"categoria": "Masa de Maíz con Manteca", "clasificacion": "Moderación Requerida", "dictamen": "La preparación tradicional exige altas cantidades de manteca de cerdo.", "recomendacion": "Evitar comerlo junto con pan.", "limite": "1 unidad (fin de semana).", "riesgo_cronico": "⚠️ CONSUMO FRECUENTE: Elevación de lípidos en sangre y riesgo de sobrepeso."},
        "bisteck": {"categoria": "Proteína Roja (Res)", "clasificacion": "Favorable / Moderación", "dictamen": "Excelente fuente de Hierro hemo, Zinc y vitaminas B.", "recomendacion": "Preparar a la plancha con mínimo aceite.", "limite": "2 a 3 veces por semana.", "riesgo_cronico": "⚠️ USO CRÓNICO: El abuso diario de carnes rojas se asocia a inflamación intestinal."},
        "lomo saltado": {"categoria": "Plato Tradicional Criollo", "clasificacion": "Moderación Requerida", "dictamen": "Buen aporte de proteínas pero altísimo en carbohidratos (arroz + papa) y mucho sodio.", "recomendacion": "Pedir con menos arroz y evitar tomarse todo el jugo.", "limite": "1 vez por semana o quincenal.", "riesgo_cronico": "⚠️ CONSUMO FRECUENTE: El exceso de sodio eleva la presión arterial."},
        "chancho al palo": {"categoria": "Asado Rústico a la Leña", "clasificacion": "Moderación Requerida", "dictamen": "Desengrasa la carne, pero el humo genera compuestos químicos.", "recomendacion": "Acompañar con ensalada y retirar partes quemadas.", "limite": "1 a 2 veces al mes.", "riesgo_cronico": "🚨 CONSUMO EXCESIVO: El humo impregna Hidrocarburos Aromáticos Policíclicos (HAP)."},
        "arroz con pato": {"categoria": "Guiso Tradicional Norteño", "clasificacion": "Precaución / Peligro Metabólico", "dictamen": "El arroz absorbe toda la grasa animal del pato y la cerveza del aderezo.", "recomendacion": "Retirar la piel antes de comer y controlar el arroz.", "limite": "1 a 2 veces al mes.", "riesgo_cronico": "🚨 CONSUMO FRECUENTE: Sobrecarga hepática (hígado graso)."},
        "arroz con pollo": {"categoria": "Plato Tradicional Criollo", "clasificacion": "Moderación Requerida", "dictamen": "Equilibrado si lleva buenas verduras, pero suele servirse con exceso de arroz.", "recomendacion": "Priorizar la pechuga y servir mitad arroz, mitad ensalada.", "limite": "1 vez a la semana.", "riesgo_cronico": "⚠️ CONSUMO EXCESIVO: Eleva los triglicéridos y el azúcar en la sangre."},
        "menestron": {"categoria": "Sopa Contundente", "clasificacion": "Favorable / Alto Valor Calórico", "dictamen": "Súper nutritivo pero hipercalórico por la combinación de fideos, papa y yuca.", "recomendacion": "Comer como plato único.", "limite": "Plato fuerte quincenal.", "riesgo_cronico": "🟢 USO CRÓNICO: Previene anemia, pero genera sobrepeso si se acompaña con segundo."},
        "sopa de mote": {"categoria": "Caldo Andino", "clasificacion": "Favorable / Moderación", "dictamen": "Alto aporte de colágeno y energía. Muy saciante.", "recomendacion": "Desgrasar el caldo antes de consumir.", "limite": "1 vez cada quince días.", "riesgo_cronico": "⚠️ CONSUMO FRECUENTE: Si no se desgrasa, eleva el colesterol LDL severamente."},
        "caldo de gallina": {"categoria": "Caldo Tradicional", "clasificacion": "Moderación Requerida", "dictamen": "El problema es la gran cantidad de grasa saturada que suelta la gallina vieja.", "recomendacion": "Exigir que se sirva desgrasado.", "limite": "Quincenal.", "riesgo_cronico": "🚨 CONSUMO FRECUENTE: Endurece las arterias (aterosclerosis)."},
        "papa rellena": {"categoria": "Fritura Criolla", "clasificacion": "Precaución / Peligro Metabólico", "dictamen": "Puré compactado rebozado y frito en abundante aceite.", "recomendacion": "Escurrir bien en papel absorbente.", "limite": "1 unidad ocasional.", "riesgo_cronico": "🚨 CONSUMO FRECUENTE: Altamente inflamatorio debido al aceite oxidado."},
        "rocoto relleno": {"categoria": "Plato Típico Arequipeño", "clasificacion": "Favorable / Moderación", "dictamen": "Gran aporte de vitaminas y proteína. El horneado es excelente cocción.", "recomendacion": "Acompañar con porción moderada de pastel de papa.", "limite": "Consumo regular permitido.", "riesgo_cronico": "⚠️ USO CRÓNICO: El picante extremo puede desencadenar gastritis erosiva en estómagos sensibles."},
        "seco de carne": {"categoria": "Guiso Criollo", "clasificacion": "Favorable / Nutritivo", "dictamen": "Los frejoles aportan fibra, el culantro es antioxidante y la carne da hierro.", "recomendacion": "Priorizar los frejoles y controlar el arroz.", "limite": "1 a 2 veces por semana.", "riesgo_cronico": "🟢 USO CRÓNICO: La fibra protege contra el cáncer de colon y regula el azúcar."},
        "pollo a la brasa": {"categoria": "Plato Tradicional (Asado)", "clasificacion": "Moderación Requerida", "dictamen": "Carne magra rica en proteínas, pero el pellejo y cremas son altos en grasas.", "recomendacion": "Comer la pechuga y dejar el pellejo.", "limite": "1 a 2 veces al mes.", "riesgo_cronico": "⚠️️ CONSUMO FRECUENTE: Partes carbonizadas vinculadas a irritación gástrica."},
        "broster": {"categoria": "Fritura Profunda", "clasificacion": "Precaución / Peligro Metabólico", "dictamen": "Absorbe grandes cantidades de aceite reutilizado.", "recomendacion": "Quitar el pellejo empanizado para reducir el daño.", "limite": "Máximo 1 vez al mes.", "riesgo_cronico": "🚨 CONSUMO FRECUENTE: Hipertensión y daño arterial agudo."},
        "ceviche": {"categoria": "Pescado Crudo Curado", "clasificacion": "Favorable / Nutritivo", "dictamen": "Pescado magro rico en Omega-3, limón y cebolla.", "recomendacion": "Consumir en lugares de extrema higiene.", "limite": "1 a 2 veces por semana.", "riesgo_cronico": "🟢 USO CRÓNICO: Fortalece el sistema inmunológico y la salud cardiovascular."},

        # --- 2. POSTRES Y DULCES ---
        "helado": {"categoria": "Postre Lácteo Ultraprocesado", "clasificacion": "Precaución / Alto en Azúcar", "dictamen": "Cremas comerciales con grasas hidrogenadas y alta sacarosa.", "recomendacion": "Preferir helados de hielo o paletas de pura fruta.", "limite": "1 bola pequeña ocasionalmente.", "riesgo_cronico": "🚨 CONSUMO FRECUENTE: Dispara los triglicéridos e hígado graso."},
        "mazamorra": {"categoria": "Postre Tradicional", "clasificacion": "Moderación Requerida", "dictamen": "Antioxidantes (maíz morado) opacados por exceso de harina de camote y azúcar.", "recomendacion": "Prepararla en casa con edulcorante natural.", "limite": "1 porción pequeña a la semana.", "riesgo_cronico": "⚠️ CONSUMO FRECUENTE: El exceso diario se almacena como grasa corporal."},
        "pay de manzana": {"categoria": "Repostería Horneada", "clasificacion": "Moderación Requerida", "dictamen": "Masa rica en margarina y azúcar refinada.", "recomendacion": "Comer solo el relleno y dejar los bordes gruesos.", "limite": "1 porción esporádica.", "riesgo_cronico": "🚨 CONSUMO FRECUENTE: Aumento de colesterol LDL y triglicéridos."},
        "pay de limon": {"categoria": "Repostería Horneada", "clasificacion": "Precaución / Alto en Azúcar", "dictamen": "Bomba de carbohidratos simples y leche condensada.", "recomendacion": "Consumir en celebraciones especiales.", "limite": "1 tajada pequeña al mes.", "riesgo_cronico": "🚨 CONSUMO FRECUENTE: Sobrecarga el páncreas rápidamente."},
        "torta": {"categoria": "Pastelería Dulce", "clasificacion": "Precaución / Peligro Metabólico", "dictamen": "Harinas refinadas, azúcares y cremas artificiales.", "recomendacion": "Exclusivo para cumpleaños.", "limite": "1 tajada esporádica.", "riesgo_cronico": "🚨 CONSUMO FRECUENTE: Daño cardiovascular crónico por grasas trans."},
        "torta helada": {"categoria": "Pastelería Mixta", "clasificacion": "Precaución / Peligro Metabólico", "dictamen": "Bizcochuelo, crema chantilly y gelatina azucarada.", "recomendacion": "Mantener porciones controladas.", "limite": "1 tajada esporádica.", "riesgo_cronico": "🚨 CONSUMO FRECUENTE: Genera resistencia a la insulina."},
        "leche asada": {"categoria": "Postre Lácteo/Huevo", "clasificacion": "Moderación Requerida", "dictamen": "Buena proteína, pero el caramelo añade mucha azúcar.", "recomendacion": "Hacerlo en casa controlando el azúcar.", "limite": "1 porción a la semana.", "riesgo_cronico": "⚠️ CONSUMO EXCESIVO: Incremento de la glucosa."},
        "crema volteada": {"categoria": "Postre Lácteo Denso", "clasificacion": "Precaución / Alto en Azúcar", "dictamen": "Usa leche condensada entera, triplicando su valor calórico.", "recomendacion": "Compartir la porción.", "limite": "1 porción pequeña ocasionalmente.", "riesgo_cronico": "🚨 CONSUMO FRECUENTE: Pico insulínico severo."},
        "gelatina": {"categoria": "Postre de Colágeno/Azúcar", "clasificacion": "Moderación Requerida", "dictamen": "Aporta azúcar y colorantes artificiales (como Tartrazina).", "recomendacion": "Buscar opciones 'Zero Azúcar'.", "limite": "Uso ocasional si tiene azúcar.", "riesgo_cronico": "⚠️ CONSUMO FRECUENTE: Colorantes asociados a hiperactividad infantil y azúcares a caries."},
        "churro": {"categoria": "Fritura de Repostería", "clasificacion": "Precaución / Peligro Metabólico Grave", "dictamen": "Harina frita, rellena de manjar y rebozada en azúcar.", "recomendacion": "Evitar por completo si se sufre de sobrepeso.", "limite": "Muy esporádicamente.", "riesgo_cronico": "🚨 CONSUMO FRECUENTE: Taponamiento arterial e hígado graso inmediato."},
        "paneton": {"categoria": "Panadería Dulce", "clasificacion": "Precaución / Peligro Metabólico", "dictamen": "Carbohidratos refinados, azúcar y manteca.", "recomendacion": "Postre de celebración esporádico.", "limite": "1 rebanada (100g) en temporada.", "riesgo_cronico": "🚨 CONSUMO FRECUENTE: Hígado graso y sobrepeso rápido."},

        # --- 3. ACEITES Y GRASAS ---
        "aceite vegetal": {"categoria": "Grasa Refinada", "clasificacion": "Moderación Requerida", "dictamen": "Alto en Omega-6 proinflamatorio.", "recomendacion": "Usar la mínima cantidad posible.", "limite": "Desechar después de freír.", "riesgo_cronico": "🚨 USO CRÓNICO: Promueve inflamación sistémica celular."},
        "aceite de coco": {"categoria": "Grasa Saturada Vegetal", "clasificacion": "Moderación Requerida", "dictamen": "Resiste bien el calor, pero sigue siendo grasa saturada.", "recomendacion": "No abusar.", "limite": "Máximo 1 cucharada diaria.", "riesgo_cronico": "⚠️ CONSUMO EXCESIVO: Puede elevar el colesterol LDL."},
        "aceite de oliva": {"categoria": "Grasa Saludable", "clasificacion": "Favorable / Cardioprotector", "dictamen": "Grasas monoinsaturadas saludables.", "recomendacion": "Usar crudo.", "limite": "2 a 3 cucharadas diarias.", "riesgo_cronico": "🟢 USO CRÓNICO: Previene infartos y protege el cerebro."},
        "manteca": {"categoria": "Grasa Saturada", "clasificacion": "Precaución / Peligro Cardiovascular", "dictamen": "Altísima densidad calórica.", "recomendacion": "Reemplazar por aceites vegetales líquidos.", "limite": "Uso ocasional.", "riesgo_cronico": "🚨 USO CRÓNICO: Formación de placas en las arterias (aterosclerosis)."},
        "margarina": {"categoria": "Grasa Vegetal Modificada", "clasificacion": "Precaución / Alerta Sanitaria", "dictamen": "Aceite vegetal hidrogenado (grasas trans).", "recomendacion": "Evitar por completo.", "limite": "Cero consumo regular.", "riesgo_cronico": "🚨 USO CRÓNICO: Daña el endotelio vascular y eleva riesgo cardíaco."},

        # --- 4. BEBIDAS Y SNACKS ---
        "coca": {"categoria": "Bebida Carbonatada", "clasificacion": "Precaución / Peligro Metabólico", "dictamen": "Sobrecarga de glucosa.", "recomendacion": "Sustituir por agua.", "limite": "Límite OMS: 25g de azúcares libres diarios.", "riesgo_cronico": "🚨 CONSUMO FRECUENTE: Resistencia a la insulina y obesidad severa."},
        "cafe": {"categoria": "Bebida Estimulante", "clasificacion": "Favorable / Dosis-Dependiente", "dictamen": "Rico en antioxidantes.", "recomendacion": "Tomar filtrado y sin azúcar.", "limite": "Máximo 3 a 4 tazas diarias.", "riesgo_cronico": "🟢 USO MODERADO: Protector hepático. 🚨 ABUSO CRÓNICO: Insomnio y gastritis."},
        "galleta": {"categoria": "Snack Procesado", "clasificacion": "Moderación Requerida", "dictamen": "Harinas refinadas y azúcares añadidos.", "recomendacion": "Consumo ocasional.", "limite": "Una porción esporádica.", "riesgo_cronico": "🚨 CONSUMO FRECUENTE: Picos de glucosa y aumento de colesterol LDL."},

        # --- 5. EMBUTIDOS Y LÁCTEOS ---
        "salchicha": {"categoria": "Embutido Cárnico", "clasificacion": "Precaución / Alerta Sanitaria", "dictamen": "Grasas saturadas, sodio y nitritos.", "recomendacion": "Priorizar carnes frescas.", "limite": "Máximo 1 vez por semana.", "riesgo_cronico": "🚨 CONSUMO FRECUENTE: Factor de riesgo para cáncer colorrectal."},
        "hot dog": {"categoria": "Embutido Cárnico", "clasificacion": "Precaución / Alerta Sanitaria", "dictamen": "Exceso de sodio industrial.", "recomendacion": "Hervir en lugar de freír.", "limite": "Máximo 1 a 2 unidades semanales.", "riesgo_cronico": "🚨 CONSUMO FRECUENTE: Riesgo de enfermedades cardiovasculares."},
        "queso": {"categoria": "Lácteo / Fermentado", "clasificacion": "Moderación Requerida", "dictamen": "Buena fuente de calcio, cuidado con el exceso de sodio.", "recomendacion": "Preferir quesos frescos y bajos en sal.", "limite": "1 a 2 rebanadas diarias.", "riesgo_cronico": "⚠️ CONSUMO EXCESIVO: Hipertensión arterial."},
        "leche": {"categoria": "Lácteo Base", "clasificacion": "Favorable / Nutritivo", "dictamen": "Aporte natural de calcio y proteínas.", "recomendacion": "Apto para dieta diaria si hay tolerancia.", "limite": "Porciones diarias según requerimiento.", "riesgo_cronico": "🟢 USO CRÓNICO: Fortalecimiento óseo preventivo."},
        "atun": {"categoria": "Conserva Marina", "clasificacion": "Favorable / Nutritivo", "dictamen": "Proteínas magras y Omega-3.", "recomendacion": "Preferir presentaciones 'en agua'.", "limite": "Máximo 2 a 3 latas por semana.", "riesgo_cronico": "⚠️ CONSUMO EXCESIVO: Riesgo de bioacumulación de mercurio."},

        # --- 6. HIGIENE Y QUÍMICOS ---
        "dental": {"categoria": "Higiene Bucal", "clasificacion": "Favorable / Seguro", "dictamen": "Fluoruro de sodio para endurecer el esmalte.", "recomendacion": "No tragar la espuma.", "limite": "Tamaño de una arveja por lavado.", "riesgo_cronico": "🟢 USO CRÓNICO: Previene la destrucción crónica del esmalte."},
        "aluminio": {"categoria": "Antitranspirante", "clasificacion": "Precaución / Monitoreo", "dictamen": "Bloquea conductos sudoríparos.", "recomendacion": "Alternar con opciones 'Zero Aluminio'.", "limite": "Máximo 1 aplicación diaria.", "riesgo_cronico": "🚨 USO CRÓNICO: Riesgo de neurotoxicidad."},
        "triclosan": {"categoria": "Antibacteriano", "clasificacion": "Precaución / Alerta Sanitaria", "dictamen": "Agente antimicrobiano de amplio espectro.", "recomendacion": "Evitar uso diario.", "limite": "No se recomienda.", "riesgo_cronico": "🚨 USO CRÓNICO: Alteración del sistema endocrino."},
        "hipoclorito de sodio": {"categoria": "Desinfectante (Lejía)", "clasificacion": "Peligro / Tóxico por Inhalación", "dictamen": "Gases corrosivos.", "recomendacion": "Jamás mezclar con otros químicos.", "limite": "Dilución estricta.", "riesgo_cronico": "🚨 EXPOSICIÓN CRÓNICA: Daño irreversible en mucosas respiratorias."}
    }

    # ==========================================
    # INTERFAZ DE USUARIO
    # ==========================================
    st.markdown("### 📷 y 🎙️ Escáner Táctico Pro - Análisis Integral")
    st.write("Sube la foto del producto y usa el dictado por voz para conocer su impacto toxicológico, límites seguros y alertas crónicas.")
    
    archivo_foto = st.file_uploader("1. Sube o toma la foto (Evidencia)", type=["jpg", "jpeg", "png", "webp"], key="foto_evidencia")
    if archivo_foto is not None:
        try:
            imagen_pil = Image.open(archivo_foto)
            imagen_pil.thumbnail((400, 400)) 
            st.image(imagen_pil, caption="Evidencia visual cargada")
        except Exception as err:
            st.error("Error al procesar la imagen.")

    st.markdown("---")
    st.markdown("#### 🎙️ Lector de Ingredientes y Alimentos")
    st.info("Toca aquí, presiona el micrófono 🎙️ de tu teclado y dicta los alimentos (Ej: arroz con pato, gelatina, chancho al palo).")
    
    ingredientes_texto = st.text_area("Ingresa los alimentos o ingredientes aquí:", height=100, placeholder="Ejemplo: arroz con pollo, helado, aluminio...")
    
    if st.button("🔍 Analizar Riesgo y Exposición"):
        if ingredientes_texto.strip() == "":
            st.warning("⚠️️ Por favor, dicta o escribe los elementos antes de analizar.")
        else:
            with st.spinner("Evaluando perfil toxicológico..."):
                texto_minusculas = ingredientes_texto.lower()
                componentes_hallados = []

                for clave, datos in BASE_INGREDIENTES_MAESTRA.items():
                    if clave in texto_minusculas:
                        datos_encontrados = datos.copy()
                        datos_encontrados["detectado"] = clave
                        componentes_hallados.append(datos_encontrados)

                st.markdown("---")
                st.subheader("📊 Reporte Oficial y Dosimetría Clínica")
                
                if len(componentes_hallados) > 0:
                    st.success(f"Se identificaron **{len(componentes_hallados)}** elementos:")
                    
                    for item in componentes_hallados:
                        with st.expander(f"📌 {item['detectado'].upper()} ({item['categoria']})", expanded=True):
                            clasif = item['clasificacion']
                            
                            if "Favorable" in clasif:
                                st.success(f"🟢 **Clasificación: {clasif}**")
                            elif "Peligro" in clasif or "Alerta" in clasif or "Metabólico" in clasif:
                                st.error(f"🔴 **Clasificación: {clasif}**")
                            else:
                                st.warning(f"🟡 **Clasificación: {clasif}**")
                            
                            st.write(f"**Análisis de Riesgo:** {item['dictamen']}")
                            st.write(f"**Recomendación de Uso:** {item['recomendacion']}")
                            st.write(f"**⚠️ Límite Seguro:** {item['limite']}")
                            st.markdown(f"**{item['riesgo_cronico']}**")
                else:
                    st.info("✅ **Análisis completado:** No se detectaron ingredientes críticos registrados.")
elif menu == "Triaje y Alerta SOS":
            st.title("🚨 Triaje y Alerta SOS")
            
            if "contacto_sos" not in st.session_state:
                st.session_state.contacto_sos = "+51 900000000"
                
            modo_entrada = st.radio("Método de reporte:", ["Escribir síntoma", "Dictar Comando de Voz"])
            sintoma_reporte = st.text_area("Describa síntomas:" if modo_entrada == "Escribir síntoma" else "Transcripción de voz...")
            
            if st.button("⚡ Ejecutar Triaje Clínico"):
                if sintoma_reporte:
                    texto = sintoma_reporte.lower()
                    if "pecho" in texto or "fuerte" in texto or "descompensación" in texto:
                        st.error("🚨 **¡ALERTA SOS ACTIVADA POR GRAVEDAD CRÍTICA!**")
                        
                        # --- BOTÓN TÁCTICO DE WHATSAPP CON CONTACTO DINÁMICO ---
                        mensaje = f"🚨 ALERTA SOS CRÍTICA 🚨 Paciente reporta: {sintoma_reporte}. Requiere asistencia inmediata. A continuación envío mi ubicación en tiempo real:"
                        mensaje_url = mensaje.replace(" ", "%20")
                        numero_wsp = st.session_state.contacto_sos.replace("+", "").replace(" ", "")
                        enlace_wsp = f"https://wa.me/{numero_wsp}?text={mensaje_url}"
                        
                        st.markdown(f"""
                        <a href="{enlace_wsp}" target="_blank" style="text-decoration: none;">
                            <button style="background-color: #25D366; color: white; border-radius: 8px; font-weight: bold; height: 60px; width: 100%; font-size: 18px; border: 2px solid #128C7E; cursor: pointer; margin-top: 10px;">
                                💬 ENVIAR ALERTA Y UBICACIÓN A WHATSAPP
                            </button>
                        </a>
                        """, unsafe_allow_html=True)
                    else:
                        st.success("💊 **Triaje Exitoso:** Proceda con observación de rutina.")
                else:
                    st.warning("Por favor, describa los síntomas.")

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
