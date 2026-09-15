from typing import List, Dict
from google import genai
from google.genai import types

from src.gemini_analyzer import obter_api_key

SYSTEM_INSTRUCTION_CHAT = """
Você é um assistente acadêmico de alta precisão especializado no artigo científico em PDF em anexo.
Sua missão é responder às dúvidas do pesquisador EXCLUSIVAMENTE com base nas informações deste documento.

DIRETRIZES DE STRICT GROUNDING (ZERO ALUCINAÇÃO):
1. BASEIE-SE EXCLUSIVAMENTE NO PDF:
   - Toda e qualquer afirmação, número, dado experimental, tabela ou citação DEVE ser extraída diretamente do texto, figuras ou tabelas do artigo fornecido.
   - NUNCA use conhecimentos externos, suposições ou dados que não estejam expressos no documento.

2. TRATAMENTO DE INFORMAÇÕES AUSENTES:
   - Se o usuário fizer uma pergunta cuja resposta NÃO esteja presente no artigo, responda de forma categórica e honesta:
     "Esta informação não consta no artigo analisado."
   - Não tente adivinhar nem extrapolar.

3. CITAÇÃO DE EVIDÊNCIAS:
   - Sempre que responder, aponte a seção, metodologia, tabela ou número de página onde a informação se encontra (ex.: "Segundo a Tabela 2...", "Conforme a Seção 4 (Discussão)...").

4. LINGUAGEM E ESTILO:
   - Responda em Português brasileiro culto, com clareza científica, objetividade e foco acadêmico.
"""


def responder_pergunta_artigo(
    pdf_bytes: bytes,
    pergunta: str,
    historico_chat: List[Dict[str, str]],
    nome_arquivo: str = "artigo.pdf",
    modelo_preferido: str = "gemini-3.5-flash-lite",
) -> str:
    """
    Executa o RAG Efêmero com Long Context Direto: envia o PDF em memória junto com
    o histórico da conversa e a pergunta do usuário para uma resposta estritamente fundamentada.
    """
    api_key = obter_api_key()
    client = genai.Client(api_key=api_key)

    # Objeto binário do PDF em memória
    pdf_part = types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf")

    # Montagem dos conteúdos (Contexto longo: PDF + histórico + pergunta)
    contents = [pdf_part]

    # Inclusão do histórico de mensagens anteriores da sessão
    for msg in historico_chat[-6:]:  # Mantém as últimas mensagens para contexto ágil
        role = "user" if msg["role"] == "user" else "model"
        contents.append(f"[{role.upper()}]: {msg['content']}")

    # Pergunta atual com contextualização
    prompt_atual = (
        f"Artigo em análise: '{nome_arquivo}'.\n"
        f"Pergunta do pesquisador: {pergunta}\n\n"
        "Lembre-se: responda APENAS com base no que está comprovado no PDF e cite a seção/tabela/página da evidência."
    )
    contents.append(prompt_atual)

    config = types.GenerateContentConfig(
        temperature=0.2,  # Baixa temperatura para fidelidade estrita ao documento
        system_instruction=SYSTEM_INSTRUCTION_CHAT,
    )

    modelos = [modelo_preferido, "gemini-2.5-flash"]
    ultimo_erro = None

    for modelo in modelos:
        try:
            response = client.models.generate_content(
                model=modelo,
                contents=contents,
                config=config,
            )
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            ultimo_erro = e
            continue

    raise RuntimeError(f"Erro ao consultar o artigo no chat: {ultimo_erro}")
