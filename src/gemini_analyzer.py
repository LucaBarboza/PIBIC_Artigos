import os
from typing import List
import streamlit as st
from google import genai
from google.genai import types

from src.schemas import AnaliseArtigo

# Prompt de Sistema rigoroso e acadêmico
SYSTEM_INSTRUCTION = """
Você é um revisor acadêmico sênior, cientista experiente e avaliador de periódicos com qualificação internacional Qualis A1.
Sua missão é analisar o artigo científico em PDF fornecido de forma minuciosa, crítica, fidedigna e aprofundada.

DIRETRIZES FUNDAMENTAIS:
1. LEITURA COMPLETA E MULTIMODAL:
   Analise o documento integralmente, incluindo título, autores, afiliações, resumo (abstract), introdução, 
   fundamentação teórica, procedimentos metodológicos, tabelas, gráficos, discussão, conclusões e notas de rodapé.

2. EXTRAÇÃO BIBLIOGRÁFICA FIDEDIGNA:
   Identifique com precisão cirúrgica os dados de publicação do artigo:
   - Sobrenome e prenome de todos os autores.
   - Título exato do artigo e subtítulo (se houver).
   - Nome completo e correto do periódico científico ou anais de conferência onde foi publicado.
   - Cidade de publicação (se indicada), volume, número/fascículo, páginas inicial e final, mês e ano.
   - Código DOI oficial (Digital Object Identifier) ou link permanente de acesso.
   Formate as referências nas normas solicitadas pelo usuário seguindo à risca as regras de cada manual (ABNT, APA, Vancouver, IEEE, Chicago, MLA).
   Para qualquer norma NÃO selecionada pelo usuário, defina o respectivo campo estritamente como nulo (None/null).

3. RIGOR ANALÍTICO E CRÍTICO:
   - Não forneça respostas genéricas, superficiais ou vagas.
   - Na análise de fundamentação e qualidade metodológica, aponte a consistência das evidências empíricas, adequação amostral, validade estatística ou matemática, limitações metodológicas transparentes e viéses potenciais.
   - Destaque com clareza as novidades e diferenciais do trabalho em relação ao estado da arte.

4. IDIOMA E TERMINOLOGIA:
   - As traduções e sínteses devem estar em Português brasileiro formal, culto e estritamente adequado ao jargão acadêmico da área do estudo (engenharia, saúde, exatas, humanas, etc.).
   - O resumo original deve preservar o idioma original da publicação.
"""


def obter_api_key() -> str:
    """
    Recupera a chave da API do Gemini prioritariamente dos Secrets do Streamlit Cloud
    e secundariamente das variáveis de ambiente locais.
    """
    # 1. Tentar Streamlit Secrets (Streamlit Cloud ou .streamlit/secrets.toml)
    try:
        if "GEMINI_API_KEY" in st.secrets:
            key = st.secrets["GEMINI_API_KEY"]
            if key and key.strip() and not key.startswith("sua_chave"):
                return key.strip()
    except Exception:
        pass

    # 2. Tentar variável de ambiente do sistema
    env_key = os.environ.get("GEMINI_API_KEY")
    if env_key and env_key.strip():
        return env_key.strip()

    raise ValueError(
        "Chave da API do Gemini não configurada! "
        "Adicione a chave 'GEMINI_API_KEY' nos Secrets do Streamlit Cloud "
        "ou no arquivo '.streamlit/secrets.toml'."
    )


def analisar_artigo_pdf(
    pdf_bytes: bytes,
    normas_selecionadas: List[str],
    nome_arquivo: str = "artigo.pdf",
    modelo_preferido: str = "gemini-3.5-flash-lite",
) -> AnaliseArtigo:
    """
    Envia os bytes do PDF diretamente ao Google Gemini com Structured Output (Pydantic),
    gerando o fichamento completo do artigo nas normas selecionadas.
    """
    api_key = obter_api_key()
    client = genai.Client(api_key=api_key)

    # Criação do objeto Part com os bytes do PDF
    pdf_part = types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf")

    # Prompt instrucional informando as normas selecionadas
    normas_txt = ", ".join(normas_selecionadas) if normas_selecionadas else "Nenhuma"
    prompt_usuario = (
        f"Por favor, realize a análise acadêmica completa e profunda do artigo em anexo ('{nome_arquivo}').\n\n"
        f"NORMAS BIBLIOGRÁFICAS SOLICITADAS PELO USUÁRIO: [{normas_txt}].\n"
        "INSTRUÇÃO OBRIGATÓRIA PARA REFERÊNCIAS:\n"
        "- Gere a referência completa e formatada APENAS para as normas listadas acima.\n"
        "- Para todas as normas que NÃO estejam nessa lista, retorne o campo correspondente como null/None.\n"
        "Preencha todos os demais campos da análise com profundidade analítica, rigor científico e linguagem acadêmica."
    )

    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=AnaliseArtigo,
        temperature=0.2,
        system_instruction=SYSTEM_INSTRUCTION,
    )

    modelos_para_tentar = [modelo_preferido, "gemini-2.5-flash"]

    ultimo_erro = None
    for modelo in modelos_para_tentar:
        try:
            response = client.models.generate_content(
                model=modelo,
                contents=[pdf_part, prompt_usuario],
                config=config,
            )

            # Validação e conversão para o modelo Pydantic
            if not response.text:
                raise ValueError("O modelo Gemini retornou uma resposta vazia.")

            analise = AnaliseArtigo.model_validate_json(response.text)
            return analise

        except Exception as e:
            ultimo_erro = e
            # Se o erro for de modelo não encontrado ou indisponibilidade, tenta o próximo modelo da lista
            continue

    # Se todos os modelos falharem
    raise RuntimeError(
        f"Não foi possível processar o artigo com os modelos Gemini disponíveis. Detalhes: {ultimo_erro}"
    )
