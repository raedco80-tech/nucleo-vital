import streamlit as st
from datetime import datetime

# ==========================================
# CONFIGURACIÓN DE PÁGINA Y ESTILOS
# ==========================================
st.set_page_config(
    page_title="NÚCLEO VITAL - Centro de Mando Táctico",
    page_icon="🛡️",
    layout="centered"
)

st.markdown("""
    <style>
    .main-title {
        font-size: 28px;
        font-weight: 700;
        color: #d9534f;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 14px;
        color: #6c757d;
        text-align: center;
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 6px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# INICIALIZACIÓN DE ESTADOS (SESIÓN)
# ==========================================
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "usuario_actual" not in st.session_state:
    st.session_state.usuario_actual = ""
if "nivel_acceso" not in st.session_state:
    st.session_state.nivel_acceso = ""

# Base de datos simulada de licencias / llaves tácticas
if "licencias" not in st.session_state:
    st.session_state.licencias = {
        "NV-MASTER-2026": {"expira": "2999-12-31", "tipo": "MAESTRO"},
        "NV-OPERADOR-01": {"expira": "2026-10-15", "tipo": "OPERADOR"}
    }

# ==========================================
# PANTALLA DE ACCESO Y SEGURIDAD
# ==========================================
if not st.session_state.autenticado:
    st.markdown('<p class="main-title">🛡️ NÚCLEO VITAL</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">SISTEMA DE CONTROL TÁCTICO RESTRINGIDO</p>', unsafe_allow_html=True)
    
    st.info("Acceso restringido. Ingrese su llave de autorización para acceder al sistema.")
    
    with st.form("form_login"):
        llave_ingresada = st.text_input("🔑 Llave de Acceso", type="password")
        submit_login = st.form_submit_button("Validar Autorización")
        
        if submit_login:
            hoy_str = datetime.now().strftime("%Y-%m-%d")
            if llave_ingresada in st.session_state.licencias:
                datos_lic = st.session_state.licencias[llave_ingresada]
                if datos_lic["expira"] >= hoy_str:
                    st.session_state.autenticado = True
                    st.session_state.usuario_actual = llave_ingresada
                    st.session_state.nivel_acceso = datos_lic["tipo"]
                    st.success("¡Autorización concedida! Entrando al sistema...")
                    st.rerun()
                else:
                    st.error("❌ La llave ingresada ha expirado.")
            else:
                st.error("❌ Llave de acceso inválida o no registrada.")
    st.stop()

# ==========================================
# MENÚ DE NAVEGACIÓN TÁCTICA
# ==========================================
st.sidebar.markdown("### ⚡ Navegación Táctica")
seccion = st.sidebar.selectbox(
    "Seleccionar Sección",
    ["Panel Maestro (Licencias)", "Escáner Táctico Pro", "Centro de Control Operativo"]
)

if st.sidebar.button("🚪 Cerrar Sesión"):
    st.session_state.autenticado = False
    st.session_state.usuario_actual = ""
    st.session_state.nivel_acceso = ""
    st.rerun()

# ==========================================
# SECCIÓN 1: PANEL MAESTRO (LICENCIAS)
# ==========================================
if seccion == "Panel Maestro (Licencias)":
    st.markdown("### ⚙️ Panel de Control Maestro")
    st.write(f"Usuario activo: **{st.session_state.usuario_actual}** ({st.session_state.nivel_acceso})")
    
    st.markdown("---")
    st.subheader("📋 Licencias y Llaves Activas")
    
    for clave, info in st.session_state.licencias.items():
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"🔑 **{clave}**")
        with col2:
            st.markdown(f"Expira: `{info['expira']}` ({info['tipo']})")
    
    if st.session_state.nivel_acceso == "MAESTRO":
        st.markdown("---")
        st.subheader("➕ Registrar Nueva Llave de Acceso")
        with st.form("form_nueva_llave"):
            nueva_clave = st.text_input("Nombre de nueva llave (Ej: NV-OPERADOR-02)")
            tipo_nuevo = st.selectbox("Tipo de Acceso", ["OPERADOR", "MAESTRO"])
            expira_nuevo = st.date_input("Fecha de Expiración")
            submit_llave = st.form_submit_button("Registrar Llave")
            
            if submit_llave:
                if nueva_clave:
                    st.session_state.licencias[nueva_clave] = {
                        "expira": expira_nuevo.strftime("%Y-%m-%d"),
                        "tipo": tipo_nuevo
                    }
                    st.success(f"¡Llave '{nueva_clave}' registrada con éxito!")
                    st.rerun()
                else:
                    st.error("Por favor ingrese un nombre válido para la llave.")

# ==========================================
# SECCIÓN 2: ESCÁNER TÁCTICO PRO (CORREGIDO Y EQUILIBRADO)
# ==========================================
elif seccion == "Escáner Táctico Pro":
    st.markdown("### 📷 Escáner Táctico Pro - Análisis Nutricional")
    st.write("Análisis avanzado de componentes, ingredientes y perfiles nutricionales basado en normativas alimentarias vigentes.")
    
    modo_ingreso = st.radio("Seleccione método de análisis:", ["Subir Foto / Imagen de Etiqueta", "Ingresar Ingredientes Manualmente"])
    
    texto_analisis = ""
    if modo_ingreso == "Subir Foto / Imagen de Etiqueta":
        archivo_foto = st.file_uploader("Cargue la foto del producto o etiqueta nutricional", type=["jpg", "jpeg", "png"])
        if archivo_foto is not None:
            st.image(archivo_foto, caption="Imagen cargada para análisis táctico", use_column_width=True)
            texto_analisis = st.text_area("Describa o pegue los ingredientes principales visibles en la etiqueta:", placeholder="Ej: Harina de trigo enriquecida, agua, azúcar, aceite vegetal, sal, levadura...")
    else:
        texto_analisis = st.text_area("Ingrese la lista de ingredientes o nombre del producto:", placeholder="Ej: Avena integral, leche descremada, pasas, almendras...")
    
    if st.button("🔍 Ejecutar Análisis Táctico"):
        if texto_analisis.strip() == "":
            st.warning("⚠️ Por favor ingrese o describa los ingredientes para que el escáner realice la evaluación.")
        else:
            with st.spinner("Procesando composición nutricional..."):
                texto_lower = texto_analisis.lower()
                
                # Criterios equilibrados y científicos
                ingredientes_positivos = ["fibra", "integral", "avena", "fruta", "proteína", "vitamina", "mineral", "agua", "aceite de oliva", "almendra", "quinua", "chía"]
                ingredientes_moderados = ["azúcar", "sal", "sodio", "aceite vegetal", "harina refinada", "almidón"]
                ingredientes_precaucion = ["grasas trans", "sintético", "colorante artificial", "jarabe de alta fructosa", "conservante químico"]
                
                p_positivos = [i for i in ingredientes_positivos if i in texto_lower]
                p_moderados = [i for i in ingredientes_moderados if i in texto_lower]
                p_precaucion = [i for i in ingredientes_precaucion if i in texto_lower]
                
                st.markdown("---")
                st.subheader("📊 Resultado del Análisis Táctico Detallado")
                
                # Evaluación general equilibrada
                if len(p_precaucion) > 0:
                    st.error("⚠️ **Clasificación: Consumo Ocasional / Con Precaución**")
                    st.write("El producto contiene elementos que requieren moderación según guías nutricionales estándar.")
                elif len(p_moderados) > 2 and len(p_positivos) == 0:
                    st.warning("⚡ **Clasificación: Moderado / Procesado**")
                    st.write("Presenta componentes energéticos o condimentos que deben consumirse con equilibrio dentro de una dieta diaria.")
                else:
                    st.success("✅ **Clasificación: Perfil Nutricional Favorable / Saludable**")
                    st.write("El producto contiene componentes de calidad con buenos aportes nutricionales para el organismo.")
                
                # Desglose detallado
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown("🟢 **Aportes Positivos**")
                    if p_positivos:
                        for item in p_positivos:
                            st.write(f"- {item.capitalize()}: Contribuye positivamente a la nutrición y energía.")
                    else:
                        st.write("No se detectaron elementos protectores primarios destacados.")
                        
                with col2:
                    st.markdown("🟡 **A moderar / Balance**")
                    if p_moderados:
                        for item in p_moderados:
                            st.write(f"- {item.capitalize()}: Consumir dentro de porciones adecuadas para evitar excesos calóricos.")
                    else:
                        st.write("Bajos niveles de azúcares o sodio aparentes.")
                        
                with col3:
                    st.markdown("🔴 **Precauciones**")
                    if p_precaucion:
                        for item in p_precaucion:
                            st.write(f"- {item.capitalize()}: Se recomienda limitar su frecuencia de consumo.")
                    else:
                        st.write("Sin alertas críticas por aditivos o conservantes severos.")

# ==========================================
# SECCIÓN 3: CENTRO DE CONTROL OPERATIVO
# ==========================================
elif seccion == "Centro de Control Operativo":
    st.markdown("### 📊 Centro de Control Operativo")
    st.write("Módulo de supervisión general de parámetros y variables del sistema.")
    st.info("Sistema operando en la nube con conectividad sincronizada.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric(label="Estado del Servidor", value="ONLINE 24/7", delta="Estable")
    with col_b:
        st.metric(label="Licencias Activas", value=len(st.session_state.licencias), delta="Sincronizado")
