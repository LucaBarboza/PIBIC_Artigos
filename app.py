import os
import streamlit as st
from src.gemini_analyzer import analisar_artigo_profundo, obter_api_key
from src.schemas import AnaliseArtigo
from src.pdf_generator import gerar_relatorio_pdf, sanitizar_nome_arquivo
from src.chat_module import responder_pergunta_artigo

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

/* Ocultar elementos padrão do Streamlit */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Container principal */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
    max-width: 880px !important;
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
    font-size: 1.05rem;
    line-height: 1.6;
    color: #475569;
    font-weight: 400;
    margin-bottom: 1.6rem;
}

/* Divisor sutil */
hr {
    border-color: #E2E8F0 !important;
    margin: 1.8rem 0 !important;
    opacity: 0.8 !important;
}

/* Box do Tutorial */
.tutorial-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    padding: 1.6rem 1.8rem;
    box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05), 0 2px 6px -1px rgba(15, 23, 42, 0.03);
    margin-bottom: 1.5rem;
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

/* Estilo do container de controle e cards */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF;
    border-radius: 18px !important;
    border: 1px solid #E2E8F0 !important;
    box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05) !important;
    padding: 1.8rem 1.8rem 2.2rem 1.8rem !important;
    margin-bottom: 2.2rem !important;
    overflow: visible !important;
}

.section-label {
    font-size: 0.92rem;
    font-weight: 700;
    color: #1E293B;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Botão Principal de Análise */
div[class*="st-key-btn_analisar_principal"] > button {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    padding: 0.85rem 2rem !important;
    border-radius: 12px !important;
    border: none !important;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35) !important;
    transition: all 0.2s ease-in-out !important;
    width: 100% !important;
}

div[class*="st-key-btn_analisar_principal"] > button:hover {
    background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%) !important;
    box-shadow: 0 6px 20px rgba(37, 99, 235, 0.45) !important;
    transform: translateY(-1px) !important;
}

/* Botões de Download de Relatório */
div[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1.8rem !important;
    border-radius: 12px !important;
    border: none !important;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.25) !important;
    transition: all 0.2s ease-in-out !important;
    width: 100% !important;
}

div[data-testid="stDownloadButton"] > button:hover {
    background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%) !important;
    box-shadow: 0 6px 18px rgba(37, 99, 235, 0.4) !important;
    transform: translateY(-1px) !important;
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
    margin-top: 0.6rem;
    margin-bottom: 0.6rem;
}

/* CARDS DE RESULTADOS */
.result-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 1.6rem;
    box-shadow: 0 4px 18px -2px rgba(15, 23, 42, 0.04);
    margin-bottom: 1.4rem;
}

.result-card-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 1.15rem;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 1rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid #F1F5F9;
}

.tldr-box {
    background: linear-gradient(135deg, #EFF6FF 0%, #EEF2FF 100%);
    border: 1px solid #BFDBFE;
    border-left: 4px solid #2563EB;
    border-radius: 12px;
    padding: 1.2rem;
    margin-top: 1rem;
    margin-bottom: 1rem;
    color: #1E3A8A;
    font-size: 0.95rem;
    line-height: 1.6;
}

.title-display {
    font-size: 1.25rem;
    font-weight: 700;
    color: #1E293B;
    margin-bottom: 0.4rem;
}

.title-sub {
    font-size: 0.95rem;
    color: #64748B;
    font-style: italic;
    margin-bottom: 0.8rem;
}

.qa-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1rem;
}

.qa-box {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 1.1rem;
    transition: border-color 0.2s;
}

.qa-box:hover {
    border-color: #CBD5E1;
}

.qa-title {
    font-size: 0.92rem;
    font-weight: 700;
    color: #1E293B;
    margin-bottom: 0.45rem;
    display: flex;
    align-items: center;
    gap: 0.45rem;
}

.qa-text {
    font-size: 0.9rem;
    color: #334155;
    line-height: 1.6;
    margin: 0;
}

.norma-container {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 1.1rem;
    margin-bottom: 1.2rem;
}

.norma-badge {
    display: inline-block;
    padding: 0.25rem 0.65rem;
    border-radius: 6px;
    background: #DBEAFE;
    color: #1E40AF;
    font-weight: 700;
    font-size: 0.8rem;
    margin-bottom: 0.4rem;
}

.norma-scope {
    font-size: 0.82rem;
    color: #64748B;
    line-height: 1.4;
    margin-bottom: 0.6rem;
}

/* =========================================================================
   WIDGET FLUTUANTE DE CHAT (FAB + POPUP PIXEL-PERFECT)
   ========================================================================= */

/* 1. Botão Flutuante Circular (FAB) - Mais para a esquerda, próximo ao corpo do app */
div[class*="st-key-floating_chat_fab"] {
    position: fixed !important;
    bottom: 28px !important;
    right: max(24px, calc(50vw - 440px + 14px)) !important;
    z-index: 999999 !important;
    width: 58px !important;
    height: 58px !important;
    padding: 0 !important;
    margin: 0 !important;
    background: transparent !important;
    border: none !important;
}

div[class*="st-key-floating_chat_fab"] button {
    width: 58px !important;
    height: 58px !important;
    min-width: 58px !important;
    min-height: 58px !important;
    max-width: 58px !important;
    max-height: 58px !important;
    border-radius: 50% !important;
    background: linear-gradient(135deg, #1E40AF 0%, #2563EB 100%) !important;
    color: #FFFFFF !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 8px 24px rgba(37, 99, 235, 0.45) !important;
    border: 2px solid rgba(255, 255, 255, 0.25) !important;
    padding: 0 !important;
    margin: 0 !important;
    cursor: pointer !important;
    transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.2s ease !important;
}

div[class*="st-key-floating_chat_fab"] button:hover {
    transform: scale(1.08) !important;
    box-shadow: 0 12px 30px rgba(37, 99, 235, 0.6) !important;
}

div[class*="st-key-floating_chat_fab"] button:active {
    transform: scale(0.95) !important;
}

div[class*="st-key-floating_chat_fab"] button span[data-testid="stIconMaterial"] {
    font-size: 1.65rem !important;
    color: #FFFFFF !important;
    line-height: 1 !important;
    margin: 0 !important;
}

/* 2. Janela Flutuante do Chat (Card Pop-up) - Alinhada com o botão e o corpo */
div[class*="st-key-floating_chat_card"] {
    position: fixed !important;
    bottom: 96px !important;
    right: max(24px, calc(50vw - 440px + 14px)) !important;
    width: 385px !important;
    max-width: calc(100vw - 48px) !important;
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 20px !important;
    box-shadow: 0 20px 45px -8px rgba(15, 23, 42, 0.22), 0 8px 16px -4px rgba(15, 23, 42, 0.08) !important;
    z-index: 999998 !important;
    padding: 1.15rem 1.2rem !important;
    animation: popupFadeIn 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

@keyframes popupFadeIn {
    from {
        opacity: 0;
        transform: translateY(14px) scale(0.96);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

/* Remove caixas/bordas duplas do container de rolagem interno */
div[class*="st-key-floating_chat_card"] [data-testid="stVerticalBlockBorderWrapper"] {
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    background: transparent !important;
}

/* 3. Botões do Cabeçalho do Chat (Reset e Fechar - Foto 2 Aprimorada) */
div[class*="st-key-chat_header_btn_"] {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
}

div[class*="st-key-chat_header_btn_"] button {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 8px !important;
    color: #475569 !important;
    width: 32px !important;
    height: 32px !important;
    min-width: 32px !important;
    min-height: 32px !important;
    max-width: 32px !important;
    max-height: 32px !important;
    padding: 0 !important;
    margin: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.05) !important;
    transition: all 0.15s ease !important;
}

div[class*="st-key-chat_header_btn_"] button:hover {
    background: #F1F5F9 !important;
    background-color: #F1F5F9 !important;
    color: #0F172A !important;
    border-color: #CBD5E1 !important;
    box-shadow: 0 2px 5px rgba(15, 23, 42, 0.08) !important;
    transform: none !important;
}

div[class*="st-key-chat_header_btn_"] button span[data-testid="stIconMaterial"] {
    font-size: 1.15rem !important;
    color: #475569 !important;
    line-height: 1 !important;
    margin: 0 !important;
}

div[class*="st-key-chat_header_btn_"] button:hover span[data-testid="stIconMaterial"] {
    color: #0F172A !important;
}

/* 4. Pílulas de Sugestão de Perguntas (Chips Delicados) */
div[class*="st-key-floating_chat_card"] div[class*="st-key-pill_"] button {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 9999px !important;
    color: #334155 !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    padding: 0.45rem 0.95rem !important;
    text-align: left !important;
    line-height: 1.35 !important;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04) !important;
    margin-bottom: 0.45rem !important;
    width: 100% !important;
    transition: all 0.15s ease-in-out !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
}

div[class*="st-key-floating_chat_card"] div[class*="st-key-pill_"] button:hover {
    background: #EFF6FF !important;
    background-color: #EFF6FF !important;
    border-color: #3B82F6 !important;
    color: #1D4ED8 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 3px 10px rgba(37, 99, 235, 0.12) !important;
}

div[class*="st-key-floating_chat_card"] div[class*="st-key-pill_"] button p {
    color: inherit !important;
    font-size: inherit !important;
    font-weight: inherit !important;
    margin: 0 !important;
    padding: 0 !important;
    text-align: left !important;
}

/* 5. Rodapé: Formulário, Input e Botão de Envio */
div[class*="st-key-floating_chat_card"] [data-testid="stForm"] {
    border: none !important;
    padding: 0.3rem 0 0 0 !important;
    margin: 0 !important;
    background: transparent !important;
}

/* Ocultar 'Press Enter to submit form' que sobrepõe a digitação */
[data-testid="InputInstructions"],
div[class*="st-key-floating_chat_card"] [data-testid="InputInstructions"] {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}

div[class*="st-key-floating_chat_card"] [data-testid="stTextInput"] {
    margin: 0 !important;
    padding: 0 !important;
}

div[class*="st-key-floating_chat_card"] input[type="text"] {
    border-radius: 12px !important;
    border: 1px solid #CBD5E1 !important;
    font-size: 0.85rem !important;
    height: 40px !important;
    background: #F8FAFC !important;
    color: #0F172A !important;
    padding: 0 0.85rem !important;
    transition: all 0.15s ease !important;
}

div[class*="st-key-floating_chat_card"] input[type="text"]:focus {
    border-color: #2563EB !important;
    background: #FFFFFF !important;
    box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.15) !important;
}

div[class*="st-key-floating_chat_card"] [data-testid="stFormSubmitButton"] {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin: 0 !important;
    padding: 0 !important;
    height: 40px !important;
}

div[class*="st-key-floating_chat_card"] [data-testid="stFormSubmitButton"] button {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
    color: #FFFFFF !important;
    border-radius: 12px !important;
    height: 40px !important;
    width: 40px !important;
    min-height: 40px !important;
    min-width: 40px !important;
    max-width: 40px !important;
    padding: 0 !important;
    margin: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
    border: none !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}

div[class*="st-key-floating_chat_card"] [data-testid="stFormSubmitButton"] button:hover {
    background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%) !important;
    transform: scale(1.05) !important;
    box-shadow: 0 6px 16px rgba(37, 99, 235, 0.45) !important;
}

div[class*="st-key-floating_chat_card"] [data-testid="stFormSubmitButton"] button span[data-testid="stIconMaterial"] {
    color: #FFFFFF !important;
    font-size: 1.25rem !important;
    margin: 0 !important;
    line-height: 1 !important;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ----------------- CAPA DO APP -----------------
st.markdown(
    """
    <h1 class="hero-title">Analisador Inteligente de Artigos Científicos</h1>
    <p class="hero-subtitle">
        Acelere sua revisão bibliográfica e fichamento acadêmico. Faça upload do PDF de qualquer artigo 
        e receba uma <b>análise estruturada e profunda via Google Gemini 3.5 Flash-Lite</b>: síntese em múltiplos níveis, 
        avaliação metodológica, respostas às perguntas fundamentais e referências normatizadas.
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
                <div class="step-title">Selecione Normas</div>
                <div class="step-desc">Escolha quais normas bibliográficas deseja gerar (ABNT, APA, IEEE, etc.).</div>
            </div>
            <div class="tutorial-step">
                <div class="step-num">3</div>
                <div class="step-title">Inicie a Análise</div>
                <div class="step-desc">O Gemini 3.5 Flash-Lite realiza a leitura multimodal e o fichamento estruturado.</div>
            </div>
            <div class="tutorial-step">
                <div class="step-num">4</div>
                <div class="step-title">Copie & Estude</div>
                <div class="step-desc">Consulte os resumos, perguntas metodológicas e copie as referências em 1 clique.</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# ----------------- ÁREA DE INTERAÇÃO (UPLOAD + CONTROLES + BOTÃO) -----------------
with st.container(border=True):
    st.markdown('<div class="section-label"><span>📤</span> 1. Selecionar Arquivo do Artigo (PDF)</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        label="Arraste e solte o arquivo PDF do artigo científico aqui",
        type=["pdf"],
        help="Selecione um arquivo PDF de artigo científico para análise completa.",
        label_visibility="collapsed",
    )

    if uploaded_file is not None:
        file_size_mb = uploaded_file.size / (1024 * 1024)
        st.markdown(
            f"""
            <div class="file-info-badge">
                <span>📄 <b>{uploaded_file.name}</b> ({file_size_mb:.2f} MB)</span>
                <span>✅ PDF carregado</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div style="margin-top: 1.2rem;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label"><span>📚</span> 2. Normas Bibliográficas Desejadas</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        cb_abnt = st.checkbox("ABNT", value=True)
        cb_apa = st.checkbox("APA", value=False)
    with col2:
        cb_vancouver = st.checkbox("Vancouver", value=False)
        cb_ieee = st.checkbox("IEEE", value=False)
    with col3:
        cb_chicago = st.checkbox("Chicago", value=False)
        cb_mla = st.checkbox("MLA", value=False)

    normas_selecionadas = []
    if cb_abnt:
        normas_selecionadas.append("ABNT")
    if cb_apa:
        normas_selecionadas.append("APA")
    if cb_vancouver:
        normas_selecionadas.append("Vancouver")
    if cb_ieee:
        normas_selecionadas.append("IEEE")
    if cb_chicago:
        normas_selecionadas.append("Chicago")
    if cb_mla:
        normas_selecionadas.append("MLA")

    st.markdown('<div style="margin-top: 1.2rem;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label"><span>⚡</span> 3. Processamento da IA</div>', unsafe_allow_html=True)

    analisar_clicado = st.button("🚀 Fazer Análise do Artigo", key="btn_analisar_principal", use_container_width=True)

# ----------------- EXECUÇÃO DA ANÁLISE COM GEMINI (PIPELINE EM 3 ETAPAS) -----------------
if analisar_clicado:
    if uploaded_file is None:
        st.warning("⚠️ Por favor, faça o upload de um arquivo PDF antes de iniciar a análise.")
    else:
        try:
            # Validar existência da chave
            _ = obter_api_key()

            progress_bar = st.progress(0.0)
            status_placeholder = st.empty()

            def atualizar_progresso(pct: float, msg: str):
                progress_bar.progress(pct)
                status_placeholder.info(f"⏳ **{msg}**")

            pdf_bytes = uploaded_file.getvalue()
            resultado = analisar_artigo_profundo(
                pdf_bytes=pdf_bytes,
                normas_selecionadas=normas_selecionadas,
                nome_arquivo=uploaded_file.name,
                progresso_callback=atualizar_progresso,
            )

            progress_bar.empty()
            status_placeholder.empty()

            # Salvar no session_state para manter persistente
            st.session_state["resultado_analise"] = resultado
            st.session_state["nome_artigo_analisado"] = uploaded_file.name
            st.session_state["normas_processadas"] = normas_selecionadas
            st.session_state["pdf_bytes_atual"] = pdf_bytes
            st.session_state["chat_historico"] = []
            st.success("✨ Análise científica aprofundada concluída com sucesso!")

        except ValueError as ve:
            st.error(f"🔑 **Erro de Credencial:** {ve}")
            st.info(
                "💡 **Como configurar no Streamlit Cloud:**\n\n"
                "1. Abra seu painel no Streamlit Cloud.\n"
                "2. Vá em **Settings** -> **Secrets**.\n"
                "3. Insira:\n```toml\nGEMINI_API_KEY = \"sua_chave_aqui\"\n```"
            )
        except Exception as e:
            st.error(f"❌ Ocorreu um erro durante o processamento do artigo: {e}")

# ----------------- EXIBIÇÃO COM OS NOMES EXATOS -----------------
if "resultado_analise" in st.session_state and st.session_state["resultado_analise"] is not None:
    res: AnaliseArtigo = st.session_state["resultado_analise"]
    nome_doc = st.session_state.get("nome_artigo_analisado", "artigo.pdf")

    # Recuperação ou salvaguarda de pdf_bytes_atual para o chat
    if "pdf_bytes_atual" not in st.session_state and uploaded_file is not None:
        st.session_state["pdf_bytes_atual"] = uploaded_file.getvalue()

    # Cálculo estimado de tempo de leitura economizado
    palavras_artigo_est = max(4000, len(res.resumo_completo.split()) * 12)
    tempo_minutos = max(20, round(palavras_artigo_est / 180))

    # Tags de palavras-chave formatadas como badges modernos
    pills_html = ""
    if getattr(res, "palavras_chave", None):
        pills_html = " ".join([
            f'<span style="display: inline-block; background: #EEF2F6; border: 1px solid #CBD5E1; color: #1E293B; font-size: 0.8rem; font-weight: 600; padding: 0.25rem 0.65rem; border-radius: 9999px; margin-right: 0.35rem; margin-bottom: 0.35rem;">#{tag}</span>'
            for tag in res.palavras_chave
        ])
    else:
        pills_html = '<span style="color: #94A3B8; font-size: 0.85rem;">Não identificadas</span>'

    area_texto = getattr(res, "area_conhecimento", "Geral / Multidisciplinar")

    # PAINEL DE METADADOS CIENTÍFICOS
    with st.container(border=True):
        st.markdown(
            f"""
            <div style="display: flex; flex-wrap: wrap; gap: 1.5rem; justify-content: space-between; align-items: flex-start;">
                <div style="flex: 1; min-width: 220px;">
                    <div style="font-size: 0.75rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em;">
                        ⏱️ Tempo de Leitura Economizado
                    </div>
                    <div style="font-size: 1.35rem; font-weight: 800; color: #0F172A; margin-top: 0.2rem;">
                        ~{tempo_minutos} min <span style="font-size: 0.82rem; font-weight: 500; color: #10B981;">(leitura crítica + fichamento)</span>
                    </div>
                </div>
                <div style="flex: 1; min-width: 220px;">
                    <div style="font-size: 0.75rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em;">
                        🏷️ Grande Área / Subárea
                    </div>
                    <div style="font-size: 1.05rem; font-weight: 700; color: #2563EB; margin-top: 0.2rem;">
                        {area_texto}
                    </div>
                </div>
            </div>
            <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid #F1F5F9;">
                <div style="font-size: 0.75rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.45rem;">
                    🔑 Palavras-chave do Artigo
                </div>
                <div>{pills_html}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='margin-top: 1.2rem;'></div>", unsafe_allow_html=True)

    # Geração do relatório em PDF em memória
    pdf_bytes = gerar_relatorio_pdf(res, nome_doc)
    nome_arquivo_pdf = sanitizar_nome_arquivo(nome_doc)

    st.download_button(
        label="📥 Baixar Relatório Completo em PDF",
        data=pdf_bytes,
        file_name=nome_arquivo_pdf,
        mime="application/pdf",
        use_container_width=True,
        help="Baixe o relatório diagramado com o fichamento analítico completo e referências.",
    )

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

    # 1. TÍTULO (TRADUZIDO OU ORIGINAL)
    with st.container(border=True):
        if res.titulo_traduzido:
            st.markdown(
                """
                <div style="color: #2563EB; font-weight: 700; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.4rem;">
                    Título Traduzido
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                f"""
                <h2 style="font-size: 1.4rem; font-weight: 800; color: #0F172A; line-height: 1.35; margin: 0 0 0.5rem 0;">
                    {res.titulo_traduzido}
                </h2>
                <div style="color: #64748B; font-size: 0.92rem;">
                    <b>Título Original:</b> <i>{res.titulo_original}</i>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div style="color: #2563EB; font-weight: 700; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.4rem;">
                    Título do Artigo
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                f"""
                <h2 style="font-size: 1.4rem; font-weight: 800; color: #0F172A; line-height: 1.35; margin: 0 0 0.5rem 0;">
                    {res.titulo_original}
                </h2>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

    # 2. RESUMOS (Resumo SEMPRE em primeiro lugar; Resumo Traduzido apenas se existir)
    with st.container(border=True):
        st.markdown(
            """
            <div style="color: #2563EB; font-weight: 700; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.8rem;">
                Resumos
            </div>
            """,
            unsafe_allow_html=True,
        )

        if res.resumo_traduzido:
            tab_resumo, tab_trad, tab_curto, tab_comp = st.tabs([
                "Resumo",
                "Resumo Traduzido",
                "Resumo Curto",
                "Resumo Completo"
            ])

            with tab_resumo:
                st.markdown(
                    f"<div style='color: #334155; line-height: 1.7; font-size: 0.95rem; padding: 0.6rem 0;'>{res.resumo_original}</div>",
                    unsafe_allow_html=True,
                )

            with tab_trad:
                st.markdown(
                    f"<div style='color: #334155; line-height: 1.7; font-size: 0.95rem; padding: 0.6rem 0;'>{res.resumo_traduzido}</div>",
                    unsafe_allow_html=True,
                )

            with tab_curto:
                st.markdown(
                    f"""
                    <div style="background: #F0F7FF; border-left: 4px solid #2563EB; border-radius: 8px; padding: 1rem 1.2rem; margin: 0.6rem 0; color: #1E3A8A; font-size: 0.96rem; line-height: 1.65;">
                        {res.resumo_curto}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with tab_comp:
                st.markdown(
                    f"<div style='color: #1E293B; line-height: 1.8; font-size: 0.95rem; padding: 0.6rem 0;'>{res.resumo_completo}</div>",
                    unsafe_allow_html=True,
                )
        else:
            tab_resumo, tab_curto, tab_comp = st.tabs([
                "Resumo",
                "Resumo Curto",
                "Resumo Completo"
            ])

            with tab_resumo:
                st.markdown(
                    f"<div style='color: #334155; line-height: 1.7; font-size: 0.95rem; padding: 0.6rem 0;'>{res.resumo_original}</div>",
                    unsafe_allow_html=True,
                )

            with tab_curto:
                st.markdown(
                    f"""
                    <div style="background: #F0F7FF; border-left: 4px solid #2563EB; border-radius: 8px; padding: 1rem 1.2rem; margin: 0.6rem 0; color: #1E3A8A; font-size: 0.96rem; line-height: 1.65;">
                        {res.resumo_curto}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with tab_comp:
                st.markdown(
                    f"<div style='color: #1E293B; line-height: 1.8; font-size: 0.95rem; padding: 0.6rem 0;'>{res.resumo_completo}</div>",
                    unsafe_allow_html=True,
                )

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

    # 3. PERGUNTAS FUNDAMENTAIS QUE O ARTIGO RESPONDEU
    pf = res.perguntas_fundamentais
    with st.container(border=True):
        st.markdown(
            """
            <div style="color: #2563EB; font-weight: 700; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 1.2rem;">
                Perguntas Fundamentais que o Artigo Respondeu
            </div>
            """,
            unsafe_allow_html=True,
        )

        perguntas_lista = [
            ("Novidades do artigo", pf.novidades_do_artigo),
            ("O que foi apresentado tá bem fundamentado", pf.fundamentacao),
            ("Qualidade do artigo", pf.qualidade_artigo),
            ("Assunto principal", pf.assunto_principal),
            ("Foco", pf.foco),
            ("Foco teórico", pf.foco_teorico),
        ]

        for titulo_p, texto_p in perguntas_lista:
            st.markdown(
                f"""
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.2rem 1.4rem; margin-bottom: 1.2rem;">
                    <div style="font-weight: 700; font-size: 0.95rem; color: #0F172A; margin-bottom: 0.5rem;">
                        {titulo_p}
                    </div>
                    <div style="color: #334155; font-size: 0.92rem; line-height: 1.7;">
                        {texto_p}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<div style='margin-bottom: 0.8rem;'></div>", unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

    # 4. REFERÊNCIA
    with st.container(border=True):
        st.markdown(
            """
            <div style="color: #2563EB; font-weight: 700; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.8rem;">
                Referência
            </div>
            """,
            unsafe_allow_html=True,
        )

        refs = res.referencias

        normas_info = {
            "ABNT": refs.abnt,
            "APA": refs.apa,
            "Vancouver": refs.vancouver,
            "IEEE": refs.ieee,
            "Chicago": refs.chicago,
            "MLA": refs.mla,
        }

        alguma_norma_exibida = False
        for nome_norma, valor in normas_info.items():
            if valor:
                alguma_norma_exibida = True
                st.markdown(
                    f"""
                    <div style="margin-top: 1rem; margin-bottom: 0.4rem;">
                        <span style="background: #DBEAFE; color: #1E40AF; font-weight: 700; font-size: 0.85rem; padding: 0.25rem 0.65rem; border-radius: 6px;">
                            {nome_norma}
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.code(valor, language="markdown")

        if not alguma_norma_exibida:
            st.info("Nenhuma referência selecionada para exibição.")

    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    st.download_button(
        label="📥 Baixar Relatório Completo em PDF",
        data=pdf_bytes,
        file_name=nome_arquivo_pdf,
        mime="application/pdf",
        use_container_width=True,
        key="btn_download_fim",
    )

    # =========================================================================
    # CHATBOT FLUTUANTE (FAB + POPUP NO CANTO INFERIOR DIREITO)
    # Abre e fecha exclusivamente ao clicar no botão flutuante ou no botão '✕'
    # =========================================================================
    is_chat_aberto = st.session_state.get("chat_widget_aberto", False)

    # 1. Botão Flutuante Circular (FAB)
    fab_icon = ":material/close:" if is_chat_aberto else ":material/chat:"
    fab_help = "Fechar chat" if is_chat_aberto else "Pergunte ao Artigo (Chat)"

    if st.button("", icon=fab_icon, key="floating_chat_fab", help=fab_help):
        st.session_state["chat_widget_aberto"] = not is_chat_aberto
        st.rerun()

    # 2. Janela Flutuante do Chat (Card Pop-up) - APENAS quando aberta
    if is_chat_aberto:
        with st.container(key="floating_chat_card"):
            # Cabeçalho do Card Pop-up
            col_tit, col_act1, col_act2 = st.columns([7.4, 0.9, 0.9], vertical_alignment="center")
            with col_tit:
                st.markdown(
                    """
                    <div style="font-size: 0.98rem; font-weight: 800; color: #0F172A; line-height: 1.25;">
                        Pergunte ao Artigo
                    </div>
                    <div style="font-size: 0.74rem; color: #64748B; margin-top: 2px;">
                        Assistente científico • Strict Grounding
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with col_act1:
                if st.button("", icon=":material/refresh:", key="chat_header_btn_clear", help="Reiniciar conversa"):
                    st.session_state["chat_historico"] = []
                    st.rerun()
            with col_act2:
                if st.button("", icon=":material/close:", key="chat_header_btn_close", help="Fechar chat"):
                    st.session_state["chat_widget_aberto"] = False
                    st.rerun()

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

            if "chat_historico" not in st.session_state:
                st.session_state["chat_historico"] = []

            # Área de Rolagem para Conteúdo (Sugestões ou Histórico)
            pergunta_clicada = None
            with st.container(height=300):
                if not st.session_state["chat_historico"]:
                    st.markdown(
                        """
                        <div style="font-size: 0.76rem; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 0.5rem;">
                            💡 Sugestões rápidas:
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    if st.button("⚠️ Quais as limitações apontadas?", key="pill_limitacoes", use_container_width=True):
                        pergunta_clicada = "Quais são as principais limitações, ameaças à validade ou ressalvas apontadas expressamente pelos autores no artigo?"
                    if st.button("🔬 Metodologia e tamanho da amostra?", key="pill_metodologia", use_container_width=True):
                        pergunta_clicada = "Como foi composta a metodologia da pesquisa, qual o tamanho e perfil da amostra e quais instrumentos de coleta foram adotados?"
                    if st.button("📊 Principais resultados e métricas?", key="pill_resultados", use_container_width=True):
                        pergunta_clicada = "Quais foram os principais dados quantitativos, métricas estatísticas e resultados numéricos reportados no artigo?"
                    if st.button("🎯 Qual a hipótese central e objetivo?", key="pill_objetivo", use_container_width=True):
                        pergunta_clicada = "Qual a hipótese central formulada e qual o objetivo primário investigado no trabalho?"
                else:
                    for msg in st.session_state["chat_historico"]:
                        avatar = "🧑‍🔬" if msg["role"] == "user" else "🤖"
                        with st.chat_message(msg["role"], avatar=avatar):
                            st.markdown(msg["content"])

            # Formulário de Envio no Rodapé do Card
            with st.form(key="form_chat_popup", clear_on_submit=True):
                col_inp, col_send = st.columns([5.3, 1], vertical_alignment="center")
                with col_inp:
                    pergunta_texto = st.text_input(
                        "Mensagem",
                        placeholder="Pergunte sobre o artigo...",
                        label_visibility="collapsed",
                    )
                with col_send:
                    btn_enviar = st.form_submit_button("", icon=":material/arrow_forward:")

            pergunta_final = pergunta_clicada or (pergunta_texto if btn_enviar and pergunta_texto.strip() else None)

            if pergunta_final:
                st.session_state["chat_historico"].append({"role": "user", "content": pergunta_final})
                with st.spinner("Consultando o PDF via Gemini Long Context..."):
                    try:
                        pdf_bytes_chat = st.session_state.get("pdf_bytes_atual")
                        if not pdf_bytes_chat and uploaded_file is not None:
                            pdf_bytes_chat = uploaded_file.getvalue()

                        if not pdf_bytes_chat:
                            resposta = "⚠️ Arquivo do artigo não encontrado na memória. Por favor, reenvie o PDF para habilitar o chat."
                        else:
                            resposta = responder_pergunta_artigo(
                                pdf_bytes=pdf_bytes_chat,
                                pergunta=pergunta_final,
                                historico_chat=st.session_state["chat_historico"][:-1],
                                nome_arquivo=nome_doc,
                            )
                    except Exception as chat_err:
                        resposta = f"❌ Ocorreu um erro ao consultar o artigo: {chat_err}"

                st.session_state["chat_historico"].append({"role": "assistant", "content": resposta})
                st.rerun()
