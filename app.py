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

# ----------------- EXIBIÇÃO COM OS NOMES EXATOS -----------------
if "resultado_analise" in st.session_state and st.session_state["resultado_analise"] is not None:
    res: AnaliseArtigo = st.session_state["resultado_analise"]
    nome_doc = st.session_state.get("nome_artigo_analisado", "Artigo")

    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

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
            <div style="color: #2563EB; font-weight: 700; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 1rem;">
                Perguntas Fundamentais que o Artigo Respondeu
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_1, col_2 = st.columns(2)

        with col_1:
            st.markdown(
                f"""
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.1rem; margin-bottom: 1rem;">
                    <div style="font-weight: 700; font-size: 0.92rem; color: #0F172A; margin-bottom: 0.45rem;">
                        Novidades do artigo
                    </div>
                    <p style="color: #334155; font-size: 0.88rem; line-height: 1.6; margin: 0;">{pf.novidades_do_artigo}</p>
                </div>

                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.1rem; margin-bottom: 1rem;">
                    <div style="font-weight: 700; font-size: 0.92rem; color: #0F172A; margin-bottom: 0.45rem;">
                        O que foi apresentado tá bem fundamentado
                    </div>
                    <p style="color: #334155; font-size: 0.88rem; line-height: 1.6; margin: 0;">{pf.fundamentacao}</p>
                </div>

                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.1rem;">
                    <div style="font-weight: 700; font-size: 0.92rem; color: #0F172A; margin-bottom: 0.45rem;">
                        Qualidade do artigo
                    </div>
                    <p style="color: #334155; font-size: 0.88rem; line-height: 1.6; margin: 0;">{pf.qualidade_artigo}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_2:
            st.markdown(
                f"""
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.1rem; margin-bottom: 1rem;">
                    <div style="font-weight: 700; font-size: 0.92rem; color: #0F172A; margin-bottom: 0.45rem;">
                        Assunto principal
                    </div>
                    <p style="color: #334155; font-size: 0.88rem; line-height: 1.6; margin: 0;">{pf.assunto_principal}</p>
                </div>

                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.1rem; margin-bottom: 1rem;">
                    <div style="font-weight: 700; font-size: 0.92rem; color: #0F172A; margin-bottom: 0.45rem;">
                        Foco
                    </div>
                    <p style="color: #334155; font-size: 0.88rem; line-height: 1.6; margin: 0;">{pf.foco}</p>
                </div>

                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.1rem;">
                    <div style="font-weight: 700; font-size: 0.92rem; color: #0F172A; margin-bottom: 0.45rem;">
                        Foco teórico
                    </div>
                    <p style="color: #334155; font-size: 0.88rem; line-height: 1.6; margin: 0;">{pf.foco_teorico}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

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
            "ABNT (Associação Brasileira de Normas Técnicas)": {
                "valor": refs.abnt,
                "chave": "ABNT",
                "escopo": "Onde impera: TCCs, dissertações, teses, relatórios técnicos e periódicos nacionais da maioria das universidades brasileiras.",
            },
            "APA (American Psychological Association)": {
                "valor": refs.apa,
                "chave": "APA",
                "escopo": "Onde impera: Psicologia, Educação, Administração, Ciências Sociais Aplicadas e submissões para periódicos internacionais (ou nacionais indexados internacionalmente, como Scielo e Redalyc).",
            },
            "Vancouver": {
                "valor": refs.vancouver,
                "chave": "Vancouver",
                "escopo": "Onde impera: Medicina, Enfermagem, Odontologia, Farmácia e Ciências da Saúde em geral.",
            },
            "IEEE (Institute of Electrical and Electronics Engineers)": {
                "valor": refs.ieee,
                "chave": "IEEE",
                "escopo": "Onde impera: Engenharia Elétrica, Eletrônica, Ciência da Computação, Robótica e Telecomunicações.",
            },
            "Chicago": {
                "valor": refs.chicago,
                "chave": "Chicago",
                "escopo": "Onde impera: Usado pontualmente em História, Filosofia e Belas Artes, especialmente pelo uso intensivo de notas de rodapé explicativas e bibliografia ao final.",
            },
            "MLA (Modern Language Association)": {
                "valor": refs.mla,
                "chave": "MLA",
                "escopo": "Onde impera: Predominante em estudos de Letras, Linguística e Literatura voltados a publicações em línguas estrangeiras.",
            },
        }

        alguma_norma_exibida = False
        for nome_norma, info in normas_info.items():
            if info["valor"]:
                alguma_norma_exibida = True
                st.markdown(
                    f"""
                    <div style="margin-top: 1rem; margin-bottom: 0.3rem;">
                        <span style="background: #DBEAFE; color: #1E40AF; font-weight: 700; font-size: 0.82rem; padding: 0.25rem 0.65rem; border-radius: 6px;">
                            {nome_norma}
                        </span>
                        <div style="font-size: 0.82rem; color: #64748B; margin-top: 0.35rem; line-height: 1.4;">
                            {info['escopo']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.code(info["valor"], language="markdown")

        if not alguma_norma_exibida:
            st.info("Nenhuma referência selecionada para exibição.")
