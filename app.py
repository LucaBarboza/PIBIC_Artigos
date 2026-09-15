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

/* Botão de Análise */
div.stButton > button:first-child {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 1.05rem !important;
    padding: 0.85rem 2rem !important;
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

/* ===================================================================== */
/* CHATBOT FLUTUANTE ESTILO ENIALABS / POPUP FLUTUANTE                   */
/* ===================================================================== */

/* Botão Launcher Circular Flutuante (Canto Inferior Direito) */
div[data-testid="stVerticalBlock"]:has(#floating-launcher-marker),
div[data-testid="element-container"]:has(#floating-launcher-marker),
div:has(> #floating-launcher-marker) {
    position: fixed !important;
    bottom: 24px !important;
    right: 24px !important;
    z-index: 999999 !important;
    width: auto !important;
    height: auto !important;
    margin: 0 !important;
    padding: 0 !important;
    border: none !important;
    background: transparent !important;
    box-shadow: none !important;
}

div:has(#floating-launcher-marker) button {
    width: 58px !important;
    height: 58px !important;
    min-width: 58px !important;
    min-height: 58px !important;
    border-radius: 50% !important;
    background: linear-gradient(135deg, #1E085A 0%, #3B0764 45%, #581C87 100%) !important;
    color: #FFFFFF !important;
    font-size: 1.55rem !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border: none !important;
    box-shadow: 0 8px 24px rgba(59, 7, 100, 0.45) !important;
    cursor: pointer !important;
    padding: 0 !important;
    margin: 0 !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

div:has(#floating-launcher-marker) button:hover {
    transform: scale(1.1) !important;
    box-shadow: 0 10px 30px rgba(88, 28, 135, 0.65) !important;
}

/* Janela Flutuante do Chatbot (Popup estilo EniaLabs) */
[data-testid="stVerticalBlockBorderWrapper"]:has(#floating-chat-window-marker) {
    position: fixed !important;
    bottom: 96px !important;
    right: 24px !important;
    width: 380px !important;
    max-width: calc(100vw - 36px) !important;
    height: 540px !important;
    max-height: calc(100vh - 120px) !important;
    background: #FFFFFF !important;
    border: 1.5px solid #D8B4FE !important;
    border-radius: 24px !important;
    box-shadow: 0 16px 40px -4px rgba(76, 29, 149, 0.22), 0 4px 16px rgba(0, 0, 0, 0.08) !important;
    padding: 1.1rem 1.15rem 1rem 1.15rem !important;
    margin-bottom: 0 !important;
    z-index: 999998 !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: hidden !important;
    animation: popupFadeIn 0.22s ease-out !important;
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

/* Pílulas de sugestão (estilo EniaLabs) */
.chat-pill-btn button {
    background: #FFFFFF !important;
    border: 1.2px solid #C084FC !important;
    border-radius: 9999px !important;
    color: #4C1D95 !important;
    font-size: 0.77rem !important;
    font-weight: 500 !important;
    padding: 0.38rem 0.8rem !important;
    box-shadow: none !important;
    width: 100% !important;
    line-height: 1.35 !important;
    white-space: normal !important;
    height: auto !important;
    text-align: left !important;
    margin-bottom: 0.4rem !important;
    transition: all 0.15s ease-in-out !important;
}

.chat-pill-btn button:hover {
    background: #FAF5FF !important;
    border-color: #9333EA !important;
    color: #3B0764 !important;
    box-shadow: 0 2px 8px rgba(168, 85, 247, 0.2) !important;
    transform: translateY(-1px) !important;
}

/* Input e botão no rodapé do popup */
div:has(#floating-chat-window-marker) div[data-testid="stTextInput"] {
    margin-bottom: 0 !important;
}

div:has(#floating-chat-window-marker) div[data-testid="stTextInput"] input {
    border-radius: 12px !important;
    border: 1.5px solid #D8B4FE !important;
    font-size: 0.84rem !important;
    padding: 0.5rem 0.75rem !important;
    background: #FFFFFF !important;
    color: #1E293B !important;
}

div:has(#floating-chat-window-marker) div[data-testid="stTextInput"] input:focus {
    border-color: #9333EA !important;
    box-shadow: 0 0 0 2px rgba(168, 85, 247, 0.25) !important;
}

div:has(#floating-chat-window-marker) .chat-send-btn button {
    background: #DDD6FE !important;
    color: #6D28D9 !important;
    border: none !important;
    border-radius: 12px !important;
    font-size: 1.25rem !important;
    font-weight: 800 !important;
    height: 40px !important;
    padding: 0 !important;
    box-shadow: none !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: all 0.2s ease !important;
}

div:has(#floating-chat-window-marker) .chat-send-btn button:hover {
    background: #C4B5FD !important;
    color: #4C1D95 !important;
    transform: scale(1.05) !important;
}

/* Botões do cabeçalho (reset e close) */
div:has(#floating-chat-window-marker) .chat-icon-btn button {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #64748B !important;
    font-size: 1.1rem !important;
    padding: 0 !important;
    height: 30px !important;
    width: 30px !important;
    border-radius: 8px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

div:has(#floating-chat-window-marker) .chat-icon-btn button:hover {
    background: #F1F5F9 !important;
    color: #0F172A !important;
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

    analisar_clicado = st.button("🚀 Fazer Análise do Artigo", use_container_width=True)

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

    # 1. TÍTULO TRADUZIDO
    with st.container(border=True):
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

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

    # 2. RESUMOS (Resumo Curto, Resumo, Resumo Traduzido, Resumo Completo)
    with st.container(border=True):
        st.markdown(
            """
            <div style="color: #2563EB; font-weight: 700; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.8rem;">
                Resumos
            </div>
            """,
            unsafe_allow_html=True,
        )

        tab_curto, tab_resumo, tab_trad, tab_comp = st.tabs([
            "Resumo Curto",
            "Resumo",
            "Resumo Traduzido",
            "Resumo Completo"
        ])

        with tab_curto:
            st.markdown(
                f"""
                <div style="background: #F0F7FF; border-left: 4px solid #2563EB; border-radius: 8px; padding: 1rem 1.2rem; margin: 0.6rem 0; color: #1E3A8A; font-size: 0.96rem; line-height: 1.65;">
                    {res.resumo_curto}
                </div>
                """,
                unsafe_allow_html=True,
            )

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

    # Chamada visual para o Assistente Flutuante
    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
    with st.container(border=True):
        col_banner_txt, col_banner_btn = st.columns([4, 1])
        with col_banner_txt:
            st.markdown(
                """
                <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <span style="font-size: 1.6rem;">💬</span>
                    <div>
                        <div style="font-weight: 800; font-size: 1rem; color: #1E085A;">
                            Dúvidas sobre o artigo? Converse com o assistente inteligente
                        </div>
                        <div style="font-size: 0.84rem; color: #64748B;">
                            Tire dúvidas específicas sobre metodologia, amostra e resultados via Gemini Long Context.
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col_banner_btn:
            if st.button("Abrir Chat 💬", key="btn_abrir_chat_banner", use_container_width=True):
                st.session_state["chat_widget_aberto"] = True
                st.rerun()

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
    st.download_button(
        label="📥 Baixar Relatório Completo em PDF",
        data=pdf_bytes,
        file_name=nome_arquivo_pdf,
        mime="application/pdf",
        use_container_width=True,
        key="btn_download_fim",
    )

# =====================================================================
# WIDGET FLUTUANTE DE CHAT (ESTILO ENIALABS / STRICT GROUNDING)
# =====================================================================

if "chat_widget_aberto" not in st.session_state:
    st.session_state["chat_widget_aberto"] = False

if "chat_historico" not in st.session_state:
    st.session_state["chat_historico"] = []

# Se o widget estiver aberto, desenha a janela popup estilo EniaLabs
if st.session_state["chat_widget_aberto"]:
    with st.container(border=True):
        st.markdown('<div id="floating-chat-window-marker"></div>', unsafe_allow_html=True)

        # 1. Cabeçalho do Chatbot
        c_title, c_reset, c_close = st.columns([7, 1, 1])
        with c_title:
            st.markdown(
                """
                <div style="font-weight: 800; font-size: 1.05rem; color: #0F172A; line-height: 1.2;">
                    EniaLabs <span style="font-size: 0.72rem; font-weight: 600; color: #6D28D9; background: #F3E8FF; padding: 2px 7px; border-radius: 6px; margin-left: 4px;">PIBIC</span>
                </div>
                <div style="font-size: 0.73rem; color: #64748B; margin-top: 3px; line-height: 1.35;">
                    Assistente do artigo científico. As respostas são geradas por IA e estritamente fundamentadas no PDF.
                </div>
                """,
                unsafe_allow_html=True,
            )
        with c_reset:
            st.markdown('<div class="chat-icon-btn">', unsafe_allow_html=True)
            if st.button("🔄", key="btn_popup_reset", help="Limpar conversa"):
                st.session_state["chat_historico"] = []
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with c_close:
            st.markdown('<div class="chat-icon-btn">', unsafe_allow_html=True)
            if st.button("✕", key="btn_popup_close", help="Fechar chat"):
                st.session_state["chat_widget_aberto"] = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<hr style='margin: 0.55rem 0 0.7rem 0 !important; opacity: 0.4;'>", unsafe_allow_html=True)

        # 2. Corpo do Chat (Scrollable)
        pergunta_para_enviar = None

        chat_body = st.container(height=310, border=False)
        with chat_body:
            # Se não há mensagens ainda, exibe as pílulas de sugestão estilo EniaLabs
            if not st.session_state["chat_historico"]:
                st.markdown(
                    """
                    <div style="color: #64748B; font-size: 0.78rem; margin-bottom: 0.6rem; line-height: 1.4;">
                        Tire dúvidas sobre o artigo ou selecione uma pergunta rápida:
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                sugestoes = [
                    ("Dá pra saber as limitações?", "Quais são as principais limitações, ressalvas ou ameaças à validade apontadas expressamente pelos autores no artigo?"),
                    ("Qual a metodologia e amostra?", "Como foi composta a metodologia da pesquisa, qual o tamanho e perfil da amostra e quais instrumentos de coleta foram adotados?"),
                    ("Quais os principais resultados?", "Quais foram os principais dados quantitativos, métricas estatísticas e resultados numéricos reportados no artigo?"),
                    ("Qual a fundamentação teórica?", "Qual o foco específico, hipótese de pesquisa e referencial teórico adotado pelos autores?"),
                    ("O que os autores concluíram?", "Quais foram as conclusões finais e implicações práticas apresentadas pelos autores?"),
                ]

                for idx, (label_sug, prompt_sug) in enumerate(sugestoes):
                    st.markdown('<div class="chat-pill-btn">', unsafe_allow_html=True)
                    if st.button(label_sug, key=f"sug_pill_{idx}", use_container_width=True):
                        pergunta_para_enviar = prompt_sug
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                # Exibe histórico de mensagens com estilo de balões elegante
                for msg in st.session_state["chat_historico"]:
                    if msg["role"] == "user":
                        st.markdown(
                            f"""
                            <div style="display: flex; justify-content: flex-end; margin-bottom: 0.6rem;">
                                <div style="background: linear-gradient(135deg, #4F46E5, #6D28D9); color: #FFFFFF; border-radius: 16px 16px 4px 16px; padding: 0.55rem 0.85rem; font-size: 0.82rem; max-width: 85%; line-height: 1.45; word-break: break-word;">
                                    {msg["content"]}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f"""
                            <div style="display: flex; justify-content: flex-start; margin-bottom: 0.6rem;">
                                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; color: #1E293B; border-radius: 16px 16px 16px 4px; padding: 0.6rem 0.85rem; font-size: 0.82rem; max-width: 90%; line-height: 1.5; word-break: break-word;">
                                    {msg["content"]}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

        # 3. Rodapé com formulário de envio (Input + botão com seta)
        with st.form(key="form_chat_popup", clear_on_submit=True):
            col_inp, col_btn = st.columns([5, 1])
            with col_inp:
                texto_digitado = st.text_input(
                    label="Pergunta",
                    placeholder="Pergunte sobre o artigo...",
                    label_visibility="collapsed",
                    key="input_popup_chat",
                )
            with col_btn:
                st.markdown('<div class="chat-send-btn">', unsafe_allow_html=True)
                btn_sub = st.form_submit_button("➔")
                st.markdown('</div>', unsafe_allow_html=True)

        if btn_sub and texto_digitado:
            pergunta_para_enviar = texto_digitado

        # 4. Processamento da pergunta com Strict Grounding e Long Context
        if pergunta_para_enviar:
            pdf_bytes_chat = st.session_state.get("pdf_bytes_atual")
            if not pdf_bytes_chat and uploaded_file is not None:
                pdf_bytes_chat = uploaded_file.getvalue()
                st.session_state["pdf_bytes_atual"] = pdf_bytes_chat

            if not pdf_bytes_chat:
                st.session_state["chat_historico"].append({"role": "user", "content": pergunta_para_enviar})
                st.session_state["chat_historico"].append({
                    "role": "assistant",
                    "content": "⚠️ Por favor, faça o upload e a análise de um PDF de artigo científico para iniciar a conversa.",
                })
                st.rerun()
            else:
                st.session_state["chat_historico"].append({"role": "user", "content": pergunta_para_enviar})
                with st.spinner("Consultando o documento integral via Gemini..."):
                    try:
                        nome_doc_chat = st.session_state.get("nome_artigo_analisado", "artigo.pdf")
                        resposta = responder_pergunta_artigo(
                            pdf_bytes=pdf_bytes_chat,
                            pergunta=pergunta_para_enviar,
                            historico_chat=st.session_state["chat_historico"][:-1],
                            nome_arquivo=nome_doc_chat,
                        )
                    except Exception as e:
                        resposta = f"❌ Ocorreu um erro ao consultar o artigo: {e}"

                    st.session_state["chat_historico"].append({"role": "assistant", "content": resposta})
                    st.rerun()

# 5. Botão Flutuante Launcher (Sempre visível no canto inferior direito)
with st.container():
    st.markdown('<div id="floating-launcher-marker"></div>', unsafe_allow_html=True)
    if st.button("💬", key="btn_floating_launcher", help="Abrir chat do artigo"):
        st.session_state["chat_widget_aberto"] = not st.session_state.get("chat_widget_aberto", False)
        st.rerun()
