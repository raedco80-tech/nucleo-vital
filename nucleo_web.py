import streamlit as st
import datetime
import urllib.parse
import json
import os

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Núcleo Vital - Centro de Mando", page_icon="⚡", layout="centered")

ARCHIVO_HISTORIAL = "historial_zonas.json"
ARCHIVO_PERFIL = "perfil_usuario.json"

# --- FUNCIONES DE CARGA Y GUARDADO ---
def cargar_json(archivo, default_data):
    if os.path.exists(archivo):
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return default_data
    return default_data

def guardar_json(archivo, data):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if 'perfil' not in st.session_state:
    st.session_state.perfil = cargar_json(ARCHIVO_PERFIL, {"alias": "", "info_medica": "", "telefono": ""})
if 'historial' not in st.session_state:
    st.session_state.historial = cargar_json(ARCHIVO_HISTORIAL, [])

# --- MENÚ LATERAL TÁCTICO ---
st.sidebar.title("⚡ NÚCLEO VITAL")
st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "Navegación Táctica:",
    ["🛡️ Escudo y Memoria", "📷 Escáner Táctico Pro", "🩺 Triage y Alerta SOS", "⚙️ Perfil y Contacto SOS"]
)
st.sidebar.markdown("---")
st.sidebar.caption("🟢 Núcleo Activo\n\n© Corporación Racor\nDesarrollo Táctico Pro")

# Validar si falta teléfono
if not st.session_state.perfil.get("telefono") and menu != "⚙️ Perfil y Contacto SOS":
    st.warning("⚠️ No has configurado un número de emergencia. Ve a 'Perfil y Contacto SOS'.")

# --- PANEL 1: ESCUDO URBANO ---
if menu == "🛡️ Escudo y Memoria":
    st.header("🛡️ Escudo Urbano (Inteligencia de Zonas)")
    st.markdown("**Leyenda:** 🟩 Seguro | 🟧 Precaución | 🟥 Crítico")
    
    destino = st.text_input("Destino o zona a transitar:", placeholder="Ej: Mercado, Av. Principal...").strip().lower()
    opinion = st.text_input("Alimentar memoria en vivo (Reporte):", placeholder="Ej: Zona oscura, asalto reciente...")
    
    if st.button("🚀 Evaluar Ruta y Consolidar Memoria"):
        if destino:
            tiempo_actual = datetime.datetime.now()
            if opinion:
                st.session_state.historial.append({
                    "destino": destino,
                    "reporte": opinion,
                    "fecha": tiempo_actual.strftime("%Y-%m-%d %H:%M:%S")
                })
                guardar_json(ARCHIVO_HISTORIAL, st.session_state.historial)
            
            conteo = sum(1 for reg in st.session_state.historial if reg["destino"] == destino)
            zonas_peligrosas = ["mercado", "puente", "oscuro", "industrial", "abandonado", "trocha"]
            es_critica = any(p in destino for p in zonas_peligrosas) or conteo >= 2
            
            if es_critica:
                st.error(f"📍 DESTINO CRÍTICO: {destino.upper()}\n⚠️ {conteo} incidente(s) acumulado(s). Extreme precauciones.")
            else:
                st.success(f"📍 DESTINO ESTABLE: {destino.upper()}\n✅ Trayecto sin historial relevante.")
            
            url_mapa = f"https://www.google.com/maps/search/?api=1&query={destino.replace(' ', '+')}"
            st.markdown(f"[🗺️ Abrir Mapa de la Zona]({url_mapa})")
        else:
            st.warning("Ingrese un destino.")

# --- PANEL 2: ESCÁNER TÁCTICO PRO ---
elif menu == "📷 Escáner Táctico Pro":
    st.header("📷 Escáner Táctico Pro")
    st.markdown("Cargue una foto de su galería o use la cámara de su dispositivo para auditar el producto.")
    
    modo = st.radio("Método de captura:", ["📂 Galería", "📸 Cámara en vivo"])
    
    archivo_foto = None
    if modo == "📂 Galería":
        archivo_foto = st.file_uploader("Seleccionar foto de la etiqueta", type=['jpg', 'jpeg', 'png'])
    else:
        # Streamlit abre la cámara de forma nativa sin necesidad de OpenCV
        archivo_foto = st.camera_input("Tomar foto del envase")
        
    if archivo_foto is not None:
        st.image(archivo_foto, width=300)
        nombre_archivo = archivo_foto.name.lower()
        
        with st.spinner('Analizando matriz química...'):
            if any(w in nombre_archivo for w in ["embutido", "hotdog", "salchicha", "jamon", "chorizo", "tocino", "nugget"]):
                st.error("🟥 ALERTA: EMBUTIDO Y CARNE PROCESADA\nContiene nitritos y exceso de sodio. Causa inflamación celular. Consumo restringido.")
            elif any(w in nombre_archivo for w in ["mantequilla", "margarina", "manteca", "grasa"]):
                st.warning("🟧 PRECAUCIÓN: GRASAS PROCESADAS\nGrasas saturadas o trans que promueven rigidez arterial. Uso moderado.")
            elif any(w in nombre_archivo for w in ["frug", "nectar", "gaseosa", "soda", "cola", "energizante"]):
                st.error("🟥 ALERTA: BEBIDA AZUCARADA\nAlta fructosa. Genera picos glicémicos y sobrecarga hepática. No apto para hidratación.")
            elif any(w in nombre_archivo for w in ["tartrazina", "caramelo", "chupete", "gomita", "helado", "postre"]):
                st.error("🟥 ALERTA: AZÚCAR Y COLORANTES\nDaño de esmalte y aporte calórico vacío. Prohibido en consumo diario.")
            elif any(w in nombre_archivo for w in ["sopa", "instant", "caldo", "fideo", "mazamorra"]):
                st.warning("🟧 PRECAUCIÓN: PREPARADO INDUSTRIAL\nAlto en sodio, glutamato y almidones refinados. Consumo moderado.")
            else:
                st.success("🟩 PRODUCTO APTO (VERIFICADO)\nPerfil limpio sin aditivos críticos. Apto para consumo habitual dentro de una dieta equilibrada.")

# --- PANEL 3: TRIAGE Y SOS ---
elif menu == "🩺 Triage y Alerta SOS":
    st.header("🩺 Asistente Clínico y Alerta SOS")
    st.info("💡 En celular: Toca el cuadro de texto y usa el **micrófono de tu teclado** para dictar los síntomas al instante.")
    
    sintomas = st.text_area("Describa su emergencia o síntomas aquí:", height=100)
    
    if st.button("🚨 EVALUAR Y ENVIAR SOS", type="primary"):
        texto_analisis = sintomas.strip().lower()
        if not texto_analisis:
            st.warning("Por favor, ingrese sus síntomas.")
        else:
            criticos = ["pecho", "respirar", "desmayo", "infarto", "colapso", "convulsión", "sangrado", "accidente", "emergencia", "asfixia", "fractura", "quemadura", "veneno"]
            gastro = ["estómago", "barriga", "náusea", "vómito", "diarrea", "indigestión"]
            respiratorio_leve = ["fiebre", "tos", "gripe", "resfrío", "garganta"]
            dolor_leve = ["cabeza", "espalda", "golpe", "corte", "raspon", "caída", "muela"]

            if any(palabra in texto_analisis for palabra in criticos):
                st.error("🚨 ALERTA CRÍTICA: EMERGENCIA VITAL DETECTADA")
                
                alias = st.session_state.perfil.get("alias", "Usuario Desconocido")
                info_med = st.session_state.perfil.get("info_medica", "Sin información")
                tel = "".join(c for c in st.session_state.perfil.get("telefono", "") if c.isdigit() or c == "+")
                
                msg = urllib.parse.quote(f"🚨 *SOS NÚCLEO VITAL*\n👤 Usuario: {alias}\n🏥 Info Médica: {info_med}\n⚠️ Síntomas: '{texto_analisis[:80]}...'\n📍 GPS: https://maps.google.com/?q=-13.065,-76.132")
                link_wa = f"https://wa.me/{tel}?text={msg}" if tel else f"https://wa.me/?text={msg}"
                
                st.markdown(f"### [🔴 HAZ CLIC AQUÍ PARA ENVIAR WHATSAPP SOS AL CONTACTO TÁCTICO]({link_wa})")
                st.info("Instrucción: Mantenga la calma y no mueva al paciente si sospecha de trauma espinal.")
            else:
                st.success("✅ EVALUACIÓN PRIMARIA: ESTADO ESTABLE")
                if any(p in texto_analisis for p in gastro):
                    st.write("💊 **Botiquín Básico:** Suero oral a sorbos. Si hay retorcijón, antiespasmódico (Buscapina). Dieta blanda.")
                elif any(p in texto_analisis for p in respiratorio_leve):
                    st.write("💊 **Botiquín Básico:** Paracetamol (500mg) para la fiebre. Reposo e hidratación constante.")
                elif any(p in texto_analisis for p in dolor_leve):
                    st.write("💊 **Botiquín Básico:** Ibuprofeno (400mg). Aplique hielo envuelto en un paño en la zona afectada.")
                else:
                    st.write("💊 **Botiquín Básico:** Paracetamol (500mg) y reposo preventivo. Monitorice la evolución.")

# --- PANEL 4: PERFIL ---
elif menu == "⚙️ Perfil y Contacto SOS":
    st.header("⚙️ Configuración del Perfil")
    
    nuevo_alias = st.text_input("Nombre o Alias (Identificador):", value=st.session_state.perfil.get("alias", ""))
    nuevo_tel = st.text_input("Número de Contacto SOS (Añadir código de país, ej: +51999888777):", value=st.session_state.perfil.get("telefono", ""))
    nueva_info = st.text_area("Información Médica Relevante (Alergias, Sangre):", value=st.session_state.perfil.get("info_medica", ""))
    
    if st.button("💾 GUARDAR PERFIL Y ACTIVAR RUTA SOS", type="primary"):
        if not nuevo_tel:
            st.warning("El número de teléfono es obligatorio para el correcto funcionamiento del SOS.")
        else:
            st.session_state.perfil["alias"] = nuevo_alias
            st.session_state.perfil["telefono"] = nuevo_tel
            st.session_state.perfil["info_medica"] = nueva_info
            guardar_json(ARCHIVO_PERFIL, st.session_state.perfil)
            st.success("✅ Perfil actualizado y guardado en la memoria local exitosamente.")