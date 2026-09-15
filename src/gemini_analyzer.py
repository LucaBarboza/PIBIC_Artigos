import os
from typing import List, Callable, Optional
import streamlit as st
from google import genai
from google.genai import types

from src.schemas import (
    IdentificacaoEMetadados,
    SintesesDoArtigo,
    PerguntasFundamentais,
    AnaliseArtigo,
)


def obter_api_key() -> str:
    """
    Recupera a chave da API do Gemini prioritariamente dos Secrets do Streamlit Cloud
    e secundariamente das variáveis de ambiente locais.
    """
    try:
        if "GEMINI_API_KEY" in st.secrets:
            key = st.secrets["GEMINI_API_KEY"]
            if key and key.strip() and not key.startswith("sua_chave"):
                return key.strip()
    except Exception:
        pass

    env_key = os.environ.get("GEMINI_API_KEY")
    if env_key and env_key.strip():
        return env_key.strip()

    raise ValueError(
        "Chave da API do Gemini não configurada! "
        "Adicione a chave 'GEMINI_API_KEY' nos Secrets do Streamlit Cloud "
        "ou no arquivo '.streamlit/secrets.toml'."
    )


def _chamar_gemini_com_fallback(
    client: genai.Client,
    pdf_part: types.Part,
    prompt: str,
    schema,
    system_instruction: str,
    modelo_preferido: str = "gemini-3.5-flash-lite",
):
    """
    Executa chamada ao Gemini com Structured Output e fallback de modelo caso o 3.5 não esteja liberado.
    """
    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=schema,
        temperature=0.2,
        system_instruction=system_instruction,
    )

    modelos = [modelo_preferido, "gemini-3.1-flash-lite"]
    ultimo_erro = None

    for modelo in modelos:
        try:
            response = client.models.generate_content(
                model=modelo,
                contents=[pdf_part, prompt],
                config=config,
            )
            if response.text:
                return schema.model_validate_json(response.text)
        except Exception as e:
            ultimo_erro = e
            continue

    raise RuntimeError(f"Erro ao processar com os modelos Gemini: {ultimo_erro}")


def analisar_artigo_profundo(
    pdf_bytes: bytes,
    nome_arquivo: str = "artigo.pdf",
    progresso_callback: Optional[Callable[[float, str], None]] = None,
    modelo_preferido: str = "gemini-3.5-flash-lite",
) -> AnaliseArtigo:
    """
    Pipeline particionado em 3 requisições especializadas para garantir máxima
    profundidade analítica e fichamento denso sem compressão de texto.
    """
    api_key = obter_api_key()
    client = genai.Client(api_key=api_key)
    pdf_part = types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf")

    # -------------------------------------------------------------
    # ETAPA 1: Identificação Bibliográfica e Metadados
    # -------------------------------------------------------------
    if progresso_callback:
        progresso_callback(
            0.15,
            "🔍 Etapa 1/3: Extraindo identificação bibliográfica, autores e metadados..."
        )

    prompt_etapa1 = f"""
Você é um especialista em catalogação acadêmica e análise de publicações científicas.
Analise as primeiras páginas, cabeçalhos, rodapés e metadados do artigo em PDF ('{nome_arquivo}').

TAREFAS OBRIGATÓRIAS:
1. Extraia o Título Original do artigo exatamente como impresso.
2. 'titulo_traduzido': Tradução técnica primorosa do título para o Português brasileiro culto.
   REGRA OBRIGATÓRIA: Se o título original do artigo JÁ estiver em Português, NÃO traduza e defina 'titulo_traduzido' estritamente como null.
3. Extraia o Resumo (Abstract) original na íntegra.
4. Identifique a Grande Área e Subárea do Conhecimento Científico a que o estudo pertence.
5. Extraia de 3 a 5 Palavras-Chave conceituais essenciais em Português que melhor caracterizam o estudo.
6. Identifique a 'densidade_tecnica' do artigo: responda estritamente com 'baixa', 'media' ou 'alta'.
   - 'baixa': ensaios, artigos de revisão narrativa ou ciências humanas com leitura fluida e discursiva.
   - 'media': estudos empíricos e experimentais convencionais com dados e gráficos padrão.
   - 'alta': pesada em equações matemáticas, modelos estatísticos avançados, algoritmos complexos ou física/química teórica.
"""

    sys_etapa1 = (
        "Você é um catalogador acadêmico sênior com máxima precisão em "
        "metadados bibliográficos, identificação de autoria, periódicos e áreas do conhecimento científico."
    )

    dados_etapa1: IdentificacaoEMetadados = _chamar_gemini_com_fallback(
        client=client,
        pdf_part=pdf_part,
        prompt=prompt_etapa1,
        schema=IdentificacaoEMetadados,
        system_instruction=sys_etapa1,
        modelo_preferido=modelo_preferido,
    )

    # -------------------------------------------------------------
    # ETAPA 2: Sínteses em Múltiplos Níveis e Fichamento Analítico Denso
    # -------------------------------------------------------------
    if progresso_callback:
        progresso_callback(
            0.50,
            "📖 Etapa 2/3: Elaborando sínteses executivas e fichamento analítico aprofundado..."
        )

    prompt_etapa2 = f"""
Você é um pesquisador sênior elaborando um fichamento analítico aprofundado do artigo '{nome_arquivo}'.

ATENÇÃO: NÃO SEJA CONCISO. PROIBIDAS RESPOSTAS TELEGRÁFICAS OU SUPERFICIAIS.
Este fichamento é para suporte a Iniciação Científica (PIBIC), TCC ou Dissertação.

TAREFAS OBRIGATÓRIAS:
1. 'resumo_curto': Síntese executiva densa (TL;DR) em 2 a 3 frases densas (problema, método e achado central) em Português.
2. 'resumo_traduzido': Tradução acadêmica fluente e impecável do resumo original para o português brasileiro formal.
   REGRA OBRIGATÓRIA: Se o resumo original do artigo JÁ estiver em Português, NÃO traduza e defina 'resumo_traduzido' estritamente como null.
3. 'resumo_completo': FICHAMENTO ANALÍTICO EXTENSO (Mínimo de 4 a 6 parágrafos substanciais):
   - Detalhe o problema de pesquisa, contexto e motivação científica.
   - Descreva pormenorizadamente a metodologia, desenhos experimentais, variáveis, arquiteturas ou métodos teóricos.
   - Apresente os resultados quantitativos/qualitativos específicos alcançados, tabelas e métricas principais.
   - Explique a discussão e a conclusão dos autores sobre os impactos do trabalho.
"""

    sys_etapa2 = (
        "Você é um orientador de pesquisa acadêmica renomado. Sua escrita é rica, técnica, densa, "
        "estruturada e exaustiva. Você não poupa detalhes metodológicos e resultados."
    )

    dados_etapa2: SintesesDoArtigo = _chamar_gemini_com_fallback(
        client=client,
        pdf_part=pdf_part,
        prompt=prompt_etapa2,
        schema=SintesesDoArtigo,
        system_instruction=sys_etapa2,
        modelo_preferido=modelo_preferido,
    )

    # -------------------------------------------------------------
    # ETAPA 3: Avaliação Crítica e Perguntas Fundamentais Aprofundadas
    # -------------------------------------------------------------
    if progresso_callback:
        progresso_callback(
            0.80,
            "🔬 Etapa 3/3: Conduzindo avaliação crítica e dissecando as perguntas fundamentais..."
        )

    prompt_etapa3 = f"""
Você é um parecerista científico de periódico internacional Qualis A1 avaliando com rigor o artigo '{nome_arquivo}'.

ATENÇÃO: Cada uma das 6 perguntas fundamentais DEVE ser respondida de forma substancial e aprofundada, com múltiplos parágrafos, citando argumentos, dados e procedimentos concretos extraídos do texto do artigo. Respostas curtas de 1 ou 2 linhas serão REJEITADAS.

PERGUNTAS A RESPONDER:
1. 'novidades_do_artigo': Quais as inovações concretas, dados inéditos, novos algoritmos ou diferenciais que este trabalho traz em relação ao estado da arte? (Mínimo 2 parágrafos densos).
2. 'fundamentacao': O que foi apresentado tá bem fundamentado? Avalie com rigor crítico se as evidências empíricas, dados estatísticos, amostras ou deduções teóricas realmente sustentam as conclusões ou se há lacunas e extrapolações. (Mínimo 2 parágrafos analíticos).
3. 'qualidade_artigo': Qual o veredito sobre a qualidade acadêmica global? Avalie clareza, rigor metodológico, reprodutibilidade, relevância e explicitação de limitações. (Mínimo 2 parágrafos).
4. 'assunto_principal': Identifique o grande tema e a lacuna da literatura enfrentada pelos pesquisadores.
5. 'foco': Explique com clareza a hipótese central, pergunta norteadora e objetivo específico do estudo.
6. 'foco_teorico': Mapeie as teorias fundamentais, autores seminais, escolas de pensamento e modelos conceituais que sustentam o artigo.
"""

    sys_etapa3 = (
        "Você é um avaliador de artigos de revistas de alto impacto (Nature, IEEE, Science, Scielo). "
        "Sua análise é crítica, criteriosa, altamente analítica e sem superficialidade."
    )

    dados_etapa3: PerguntasFundamentais = _chamar_gemini_com_fallback(
        client=client,
        pdf_part=pdf_part,
        prompt=prompt_etapa3,
        schema=PerguntasFundamentais,
        system_instruction=sys_etapa3,
        modelo_preferido=modelo_preferido,
    )

    if progresso_callback:
        progresso_callback(1.0, "✨ Análise científica concluída com sucesso!")

    # Consolidação final do objeto unificado
    return AnaliseArtigo(
        titulo_original=dados_etapa1.titulo_original,
        titulo_traduzido=dados_etapa1.titulo_traduzido,
        resumo_original=dados_etapa1.resumo_original,
        resumo_curto=dados_etapa2.resumo_curto,
        resumo_traduzido=dados_etapa2.resumo_traduzido,
        resumo_completo=dados_etapa2.resumo_completo,
        perguntas_fundamentais=dados_etapa3,
        area_conhecimento=dados_etapa1.area_conhecimento,
        palavras_chave=dados_etapa1.palavras_chave,
        densidade_tecnica=getattr(dados_etapa1, "densidade_tecnica", "media") or "media",
    )
