import streamlit as st
import os

# Configuração da página
st.set_page_config(
    page_title="PIBIC AI - Analisador de Artigos Científicos",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Injeção de CSS customizado elegante e moderno
CUSTOM_CSS = """
<style>
/* Importação de fontes modernas do Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #0F172A;
}

/* Ocultar elementos desnecessários da barra superior */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Container principal com espaçamento refinado */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
    max-width: 860px !important;
}

/* Badges e Tags */
.academic-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.35rem 0.9rem;
    border-radius: 9999px;
    background: linear-gradient(135deg, rgba(37, 99, 235, 0.08) 0%, rgba(79, 70, 229, 0.12) 100%);
    border: 1px solid rgba(59, 130, 246, 0.25);
    color: #1D4ED8;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    margin-bottom: 1rem;
    text-transform: uppercase;
}

/* Header & Capa */
.hero-title {
    font-size: 2.5rem !important;
    font-weight: 800 !important;
    line-height: 1.15 !important;
    letter-spacing: -0.03em !important;
    background: linear-gradient(135deg, #0F172A 30%, #2563EB 70%, #4F46E5 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.8rem !important;
}

.hero-subtitle {
    font-size: 1.1rem;
    line-height: 1.6;
    color: #475569;
    font-weight: 400;
    margin-bottom: 1.8rem;
}

/* Box do Tutorial */
.tutorial-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    padding: 1.6rem 1.8rem;
    box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05), 0 2px 6px -1px rgba(15, 23, 42, 0.03);
    margin-bottom: 2.2rem;
    position: relative;
    overflow: hidden;
}

.tutorial-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 5px;
    height: 100%;
    background: linear-gradient(180deg, #2563EB, #7C3AED);
}

.tutorial-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 1.15rem;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 1.2rem;
}

.tutorial-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1rem;
}

.tutorial-step {
    background: #F8FAFC;
    border: 1px solid #EDF2F7;
    border-radius: 12px;
    padding: 1rem;
    transition: all 0.2s ease-in-out;
}

.tutorial-step:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.08);
    border-color: #BFDBFE;
}

.step-num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    border-radius: 6px;
    background: #2563EB;
    color: #FFFFFF;
    font-size: 0.78rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.step-title {
    font-size: 0.88rem;
    font-weight: 600;
    color: #1E293B;
    margin-bottom: 0.25rem;
}

.step-desc {
    font-size: 0.78rem;
    color: #64748B;
    line-height: 1.4;
}

/* Área de Upload e Ações */
.action-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    padding: 1.8rem;
    box-shadow: 0 8px 30px rgba(15, 23, 42, 0.04);
    margin-bottom: 2rem;
}

.section-label {
    font-size: 0.92rem;
    font-weight: 700;
    color: #1E293B;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Estilo do botão primário */
div.stButton > button:first-child {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.75rem 2rem !important;
    border-radius: 12px !important;
    border: none !important;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35) !important;
    transition: all 0.2s ease-in-out !important;
    width: 100% !important;
}

div.stButton > button:first-child:hover {
    background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%) !important;
    box-shadow: 0 6px 20px rgba(37, 99, 235, 0.45) !important;
    transform: translateY(-1px) !important;
}

/* Customização do File Uploader */
[data-testid="stFileUploader"] {
    background: #F8FAFC;
    border: 2px dashed #CBD5E1;
    border-radius: 14px;
    padding: 1rem;
    transition: border-color 0.2s;
}

[data-testid="stFileUploader"]:hover {
    border-color: #3B82F6;
}

.file-info-badge {
    background: #ECFDF5;
    border: 1px solid #A7F3D0;
    color: #065F46;
    padding: 0.6rem 1rem;
    border-radius: 10px;
    font-size: 0.88rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 0.8rem;
    margin-bottom: 1rem;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ----------------- CAPA DO APP -----------------
st.markdown(
    """
    <div class="academic-badge">
        <span>🔬</span> PIBIC • Pesquisa & Iniciação Científica
    </div>
    <h1 class="hero-title">Analisador Inteligente de Artigos Científicos</h1>
    <p class="hero-subtitle">
        Acelere sua revisão bibliográfica e fichamento acadêmico. Faça upload do PDF de qualquer artigo 
        e receba uma <b>análise estruturada e profunda via Google Gemini</b>: síntese em múltiplos níveis, 
        avaliação metodológica, pontos fundamentais respondidos e referências pré-formatadas nas 
        principais normas acadêmicas do mundo.
    </p>
    """,
    unsafe_allow_html=True,
)

# ----------------- BOX DE TUTORIAL -----------------
st.markdown(
    """
    <div class="tutorial-card">
        <div class="tutorial-header">
            <span>💡</span> Como utilizar este aplicativo
        </div>
        <div class="tutorial-grid">
            <div class="tutorial-step">
                <div class="step-num">1</div>
                <div class="step-title">Suba o Artigo</div>
                <div class="step-desc">Faça upload de qualquer PDF científico (em português, inglês ou outro idioma).</div>
            </div>
            <div class="tutorial-step">
                <div class="step-num">2</div>
                <div class="step-title">Inicie a Análise</div>
                <div class="step-desc">Clique no botão de análise para enviar o documento de forma nativa ao Gemini.</div>
            </div>
            <div class="tutorial-step">
                <div class="step-num">3</div>
                <div class="step-title">Explore os Dados</div>
                <div class="step-desc">Consulte resumos traduzidos, rigor teórico e referências (ABNT, APA, IEEE, etc.).</div>
            </div>
            <div class="tutorial-step">
                <div class="step-num">4</div>
                <div class="step-title">Baixe o Relatório</div>
                <div class="step-desc">Exporte todo o fichamento completo em um arquivo pronto para seu TCC ou projeto.</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------- ÁREA DE INTERAÇÃO (UPLOAD + BOTÃO) -----------------
st.markdown('<div class="action-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label"><span>📤</span> 1. Selecionar Arquivo do Artigo</div>', unsafe_allow_html=True)

# Input de subir PDF
uploaded_file = st.file_uploader(
    label="Arraste e solte o arquivo PDF do artigo científico aqui",
    type=["pdf"],
    help="Selecione um arquivo PDF de artigo científico para análise completa.",
    label_visibility="visible",
)

if uploaded_file is not None:
    file_size_mb = uploaded_file.size / (1024 * 1024)
    st.markdown(
        f"""
        <div class="file-info-badge">
            <span>📄 <b>{uploaded_file.name}</b> ({file_size_mb:.2f} MB)</span>
            <span>✅ Pronto para análise</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div style="margin-top: 1.2rem;"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label"><span>⚡</span> 2. Processamento da IA</div>', unsafe_allow_html=True)

# Botão fazer análise
analisar_clicado = st.button("🚀 Fazer Análise do Artigo", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Feedback da ação do usuário (Placeholder para Etapa 2)
if analisar_clicado:
    if uploaded_file is None:
        st.warning("⚠️ Por favor, faça o upload de um arquivo PDF antes de iniciar a análise.")
    else:
        st.info(
            f"🔄 Artigo **{uploaded_file.name}** recebido com sucesso!\n\n"
            "*(A extração multimodal e o processamento estruturado com Gemini API serão conectados na Etapa 2)*"
        )
