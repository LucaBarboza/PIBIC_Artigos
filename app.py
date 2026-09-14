import os
import streamlit as st
from src.gemini_analyzer import analisar_artigo_pdf, obter_api_key
from src.schemas import AnaliseArtigo

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

/* Estilo do container de controle */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF;
    border-radius: 18px !important;
    border: 1px solid #E2E8F0 !important;
    box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05) !important;
    padding: 1.2rem !important;
    margin-bottom: 1.5rem;
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

/* ESTILIZAÇÃO DAS ABAS (TABS) E RESULTADOS */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 2px solid #E2E8F0;
    padding-bottom: 6px;
    margin-bottom: 1.5rem;
}

.stTabs [data-baseweb="tab"] {
    padding: 9px 18px !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    font-size: 0.92rem !important;
    color: #64748B !important;
    background-color: #F8FAFC !important;
    border: 1px solid #E2E8F0 !important;
    transition: all 0.2s ease !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: #1E293B !important;
    border-color: #CBD5E1 !important;
}

.stTabs [aria-selected="true"] {
    color: #2563EB !important;
    background: #EFF6FF !important;
    border-color: #BFDBFE !important;
    box-shadow: 0 2px 6px rgba(37, 99, 235, 0.1) !important;
}

/* Header do Artigo Analisado */
.article-header {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 1.6rem;
    box-shadow: 0 4px 18px -2px rgba(15, 23, 42, 0.04);
    margin-bottom: 1.6rem;
}

.article-title-pt {
    font-size: 1.4rem;
    font-weight: 800;
    color: #0F172A;
    line-height: 1.35;
    margin-bottom: 0.4rem;
}

.article-title-orig {
    font-size: 0.95rem;
    color: #64748B;
    font-style: italic;
    line-height: 1.4;
    margin-bottom: 0.8rem;
}

/* TL;DR Box */
.tldr-card {
    background: linear-gradient(135deg, #F0F9FF 0%, #EEF2FF 100%);
    border: 1px solid #BAE6FD;
    border-left: 4px solid #0284C7;
    border-radius: 12px;
    padding: 1.3rem;
    margin-bottom: 1.5rem;
}

.tldr-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.8rem;
    font-weight: 700;
    color: #0369A1;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 0.4rem;
}

.tldr-text {
    font-size: 0.96rem;
    color: #0C4A6E;
    line-height: 1.65;
    margin: 0;
}

/* Card de Perguntas Fundamentais */
.qa-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 1.2rem;
    height: 100%;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
    margin-bottom: 1rem;
    transition: transform 0.15s, border-color 0.15s;
}

.qa-card:hover {
    border-color: #93C5FD;
    transform: translateY(-2px);
}

.qa-header {
    font-size: 0.92rem;
    font-weight: 700;
    color: #1E293B;
    display: flex;
    align-items: center;
    gap: 0.45rem;
    margin-bottom: 0.5rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #F1F5F9;
}

.qa-content {
    font-size: 0.88rem;
    color: #334155;
    line-height: 1.6;
    margin: 0;
}

/* Referências */
.ref-block {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 1.3rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
}

.ref-badge {
    display: inline-block;
    padding: 0.25rem 0.65rem;
    border-radius: 6px;
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    color: #1D4ED8;
    font-weight: 700;
    font-size: 0.82rem;
    margin-bottom: 0.35rem;
}

.ref-scope {
    font-size: 0.82rem;
    color: #64748B;
    margin-bottom: 0.8rem;
    line-height: 1.4;
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
        cb_abnt = st.checkbox("ABNT", value=True, help="Associação Brasileira de Normas Técnicas (TCCs e periódicos brasileiros)")
        cb_apa = st.checkbox("APA", value=False, help="American Psychological Association (Sociais e periódicos internacionais)")
    with col2:
        cb_vancouver = st.checkbox("Vancouver", value=False, help="Padrão biomédico e Ciências da Saúde")
        cb_ieee = st.checkbox("IEEE", value=False, help="Engenharias, Computação e Robótica")
    with col3:
        cb_chicago = st.checkbox("Chicago", value=False, help="História, Filosofia e Belas Artes")
        cb_mla = st.checkbox("MLA", value=False, help="Letras, Linguística e Literatura")

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

# ----------------- EXECUÇÃO DA ANÁLISE COM GEMINI -----------------
if analisar_clicado:
    if uploaded_file is None:
        st.warning("⚠️ Por favor, faça o upload de um arquivo PDF antes de iniciar a análise.")
    else:
        try:
            # Validar existência da chave
            _ = obter_api_key()

            with st.spinner("🔍 Analisando artigo com Gemini 3.5 Flash-Lite (leitura multimodal e estruturação científica)..."):
                pdf_bytes = uploaded_file.getvalue()
                resultado = analisar_artigo_pdf(
                    pdf_bytes=pdf_bytes,
                    normas_selecionadas=normas_selecionadas,
                    nome_arquivo=uploaded_file.name,
                )
                # Salvar no session_state para manter persistente
                st.session_state["resultado_analise"] = resultado
                st.session_state["nome_artigo_analisado"] = uploaded_file.name
                st.session_state["normas_processadas"] = normas_selecionadas
                st.success("✨ Análise científica concluída com sucesso!")

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

# ----------------- EXIBIÇÃO EM ABAS E LAYOUT REFINADO -----------------
if "resultado_analise" in st.session_state and st.session_state["resultado_analise"] is not None:
    res: AnaliseArtigo = st.session_state["resultado_analise"]
    nome_doc = st.session_state.get("nome_artigo_analisado", "Artigo Científico")

    st.markdown("<br>", unsafe_allow_html=True)

    # 1. HEADER DO ARTIGO ANALISADO
    st.markdown(
        f"""
        <div class="article-header">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.6rem;">
                <span class="ref-badge">✅ Análise Acadêmica Concluída</span>
                <span style="font-size: 0.8rem; color: #64748B;">📄 {nome_doc}</span>
            </div>
            <div class="article-title-pt">{res.titulo_traduzido}</div>
            <div class="article-title-orig">Original: {res.titulo_original}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 2. NAVEGAÇÃO POR ABAS MODERNAS
    tab_resumo, tab_perguntas, tab_fichamento, tab_referencias = st.tabs([
        "📌 Síntese & Resumos",
        "🔬 Rigor & Perguntas",
        "📖 Fichamento Completo",
        "📚 Referências Normatizadas"
    ])

    # ABA 1: SÍNTESE E RESUMOS
    with tab_resumo:
        # TL;DR em Destaque
        st.markdown(
            f"""
            <div class="tldr-card">
                <div class="tldr-badge">⚡ Síntese Executiva (TL;DR)</div>
                <p class="tldr-text">{res.resumo_curto}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("#### 📄 Texto do Resumo (Abstract)")
        subtab_trad, subtab_orig = st.tabs(["🇧🇷 Resumo Traduzido (Português)", "🇺🇸 Resumo Original (Idioma do Artigo)"])
        
        with subtab_trad:
            with st.container(border=True):
                st.markdown(res.resumo_traduzido)

        with subtab_orig:
            with st.container(border=True):
                st.markdown(res.resumo_original)

    # ABA 2: RIGOR E PERGUNTAS FUNDAMENTAIS
    with tab_perguntas:
        pf = res.perguntas_fundamentais
        col_esq, col_dir = st.columns(2)

        with col_esq:
            st.markdown(
                f"""
                <div class="qa-card">
                    <div class="qa-header"><span>🎯</span> Assunto Principal & Lacuna</div>
                    <p class="qa-content">{pf.assunto_principal}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                f"""
                <div class="qa-card">
                    <div class="qa-header"><span>🔍</span> Foco & Hipótese de Pesquisa</div>
                    <p class="qa-content">{pf.foco}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                f"""
                <div class="qa-card">
                    <div class="qa-header"><span>🧠</span> Foco Teórico & Epistemologia</div>
                    <p class="qa-content">{pf.foco_teorico}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_dir:
            st.markdown(
                f"""
                <div class="qa-card">
                    <div class="qa-header"><span>🚀</span> Novidades & Contribuições Inéditas</div>
                    <p class="qa-content">{pf.novidades_do_artigo}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                f"""
                <div class="qa-card">
                    <div class="qa-header"><span>⚖️</span> Rigor da Fundamentação & Evidências</div>
                    <p class="qa-content">{pf.fundamentacao}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                f"""
                <div class="qa-card">
                    <div class="qa-header"><span>📊</span> Qualidade Metodológica & Limitações</div>
                    <p class="qa-content">{pf.qualidade_artigo}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ABA 3: FICHAMENTO COMPLETO
    with tab_fichamento:
        st.markdown("#### 📖 Síntese Aprofundada e Estruturada")
        with st.container(border=True):
            st.markdown(res.resumo_completo)

    # ABA 4: REFERÊNCIAS NORMATIZADAS
    with tab_referencias:
        refs = res.referencias
        st.markdown("#### 📚 Referências Bibliográficas Pré-Formatadas")
        st.caption("Clique no botão de cópia no canto superior direito de cada bloco para colar diretamente no seu documento.")

        normas_info = {
            "ABNT": {
                "valor": refs.abnt,
                "nome_completo": "ABNT NBR 6023 (Associação Brasileira de Normas Técnicas)",
                "escopo": "<b>Onde impera:</b> TCCs, dissertações, teses, relatórios técnicos e periódicos nacionais da maioria das universidades brasileiras.",
            },
            "APA": {
                "valor": refs.apa,
                "nome_completo": "APA 7ª Edição (American Psychological Association)",
                "escopo": "<b>Onde impera:</b> Psicologia, Educação, Administração, Ciências Sociais Aplicadas e submissões para periódicos internacionais (ou nacionais indexados, ex: SciELO).",
            },
            "Vancouver": {
                "valor": refs.vancouver,
                "nome_completo": "Vancouver (International Committee of Medical Journal Editors)",
                "escopo": "<b>Onde impera:</b> Medicina, Enfermagem, Odontologia, Farmácia e Ciências da Saúde em geral.",
            },
            "IEEE": {
                "valor": refs.ieee,
                "nome_completo": "IEEE (Institute of Electrical and Electronics Engineers)",
                "escopo": "<b>Onde impera:</b> Engenharia Elétrica, Eletrônica, Ciência da Computação, Robótica e Telecomunicações.",
            },
            "Chicago": {
                "valor": refs.chicago,
                "nome_completo": "Chicago Manual of Style (Autor-Data)",
                "escopo": "<b>Onde impera:</b> História, Filosofia e Belas Artes, especialmente pelo uso intensivo de notas explicativas e bibliografia final.",
            },
            "MLA": {
                "valor": refs.mla,
                "nome_completo": "MLA 9ª Edição (Modern Language Association)",
                "escopo": "<b>Onde impera:</b> Estudos de Letras, Linguística e Literatura voltados a publicações em línguas estrangeiras.",
            },
        }

        alguma_norma_exibida = False
        for sigla, info in normas_info.items():
            if info["valor"]:
                alguma_norma_exibida = True
                st.markdown(
                    f"""
                    <div class="ref-block">
                        <span class="ref-badge">{info['nome_completo']}</span>
                        <div class="ref-scope">{info['escopo']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.code(info["valor"], language="markdown")

        if not alguma_norma_exibida:
            st.info("Nenhuma norma bibliográfica foi selecionada no momento da análise.")
