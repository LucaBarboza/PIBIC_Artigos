from typing import Optional, List
from pydantic import BaseModel, Field


# --- ETAPA 1: Identificação Bibliográfica e Metadados ---
class IdentificacaoEMetadados(BaseModel):
    """
    Sub-schema focado na extração de dados bibliográficos,
    autoria, títulos, área e palavras-chave.
    """
    titulo_original: str = Field(
        description="Título original literal do artigo científico, exatamente como redigido no PDF."
    )
    titulo_traduzido: Optional[str] = Field(
        default=None,
        description=(
            "Tradução técnica fidedigna do título para o Português brasileiro culto. "
            "REGRA OBRIGATÓRIA: Se o título original do artigo JÁ estiver em Português, "
            "defina este campo estritamente como null (None)."
        ),
    )
    resumo_original: str = Field(
        description="Texto integral do resumo (abstract) original do artigo em seu idioma de origem, sem omissões."
    )
    area_conhecimento: str = Field(
        description="Grande área e subárea do conhecimento científico a que o artigo pertence (ex.: 'Ciência da Computação / Inteligência Artificial', 'Medicina / Radiologia', 'Engenharia Mecânica / Termodinâmica')."
    )
    palavras_chave: List[str] = Field(
        description="Lista com 3 a 5 palavras-chave conceituais em Português que melhor caracterizam o estudo."
    )
    densidade_tecnica: str = Field(
        default="media",
        description=(
            "Densidade conceitual e esforço técnico de leitura exigido pelo artigo: "
            "'baixa' (revisão narrativa, ensaios conceituais, ciências sociais/humanas com prosa fluida), "
            "'media' (estudo empírico/experimental padrão com gráficos e dados) ou "
            "'alta' (pesada em formulações matemáticas, equações, modelos estatísticos avançados, física teórica ou algoritmos complexos)."
        ),
    )



# --- ETAPA 2: Sínteses em Múltiplos Níveis ---
class SintesesDoArtigo(BaseModel):
    """
    Sub-schema focado exclusivamente em sínteses e fichamento analítico expandido.
    """
    resumo_curto: str = Field(
        description=(
            "Síntese executiva densa (TL;DR) em 2 a 3 frases no máximo, em Português. "
            "Deve sintetizar com precisão: (1) O problema investigado, (2) O método/experimento chave empregado, e (3) O principal achado ou conclusão alcançada."
        )
    )
    resumo_traduzido: Optional[str] = Field(
        default=None,
        description=(
            "Tradução técnica, fluente e rigorosa do resumo (abstract) para o Português brasileiro formal, "
            "preservando termos técnicos e jargões da área acadêmica do estudo. "
            "REGRA OBRIGATÓRIA: Se o resumo original do artigo JÁ estiver em Português, "
            "defina este campo estritamente como null (None)."
        )
    )
    resumo_completo: str = Field(
        description=(
            "Fichamento analítico aprofundado, denso e minucioso em Português (mínimo de 4 a 6 parágrafos estruturados). "
            "DEVE contemplar detalhadamente: "
            "1. CONTEXTUALIZAÇÃO E MOTIVAÇÃO: O cenário do problema científico, justificativa e a relevância da pesquisa. "
            "2. PROCEDIMENTOS METODOLÓGICOS: Desenho do estudo, ferramentas, algoritmos, bases de dados, amostragem ou técnicas experimentais utilizadas passo a passo. "
            "3. RESULTADOS E DESCOBERTAS: Métricas quantitativas ou qualitativas exatas obtidas, comparações com o estado da arte e validações. "
            "4. DISCUSSÃO E CONCLUSÕES: Implicações teóricas/práticas, significado dos achados para a área e direcionamentos futuros apontados pelos autores. "
            "NÃO resuma em poucas linhas. Seja exaustivo e analítico."
        )
    )


# --- ETAPA 3: Avaliação Crítica e Perguntas Fundamentais ---
class PerguntasFundamentais(BaseModel):
    """
    Avaliação analítica crítica e profunda do artigo respondendo às perguntas
    metodológicas e teóricas essenciais. Cada resposta DEVE ser densa e fundamentada.
    """

    novidades_do_artigo: str = Field(
        description=(
            "Diferenciais e inovações científicas trazidas pela publicação (mínimo 2 parágrafos detalhados). "
            "Disseque: Quais foram as contribuições inéditas? Novos algoritmos, novas formulações matemáticas, dados primários inéditos, "
            "métodos de avaliação inovadores ou superação de limitações de trabalhos anteriores? "
            "O que diferencia este trabalho do restante da literatura existente?"
        )
    )

    fundamentacao: str = Field(
        description=(
            "Avaliação crítica detalhada sobre o rigor da fundamentação (mínimo 2 parágrafos analíticos). "
            "Responda: O que foi apresentado está bem fundamentado? "
            "Examine minuciosamente a consistência dos experimentos, tamanho amostral, tratamentos estatísticos, testes de hipótese, "
            "provas teóricas e se os dados empíricos de fato sustentam logicamente as alegações dos autores, ou se há extrapolações indevidas."
        )
    )

    qualidade_artigo: str = Field(
        description=(
            "Veredito crítico sobre a qualidade global do artigo (mínimo 2 parágrafos analíticos). "
            "Analise: Rigor acadêmico, clareza redacional, reprodutibilidade metodológica, relevância científica para a comunidade "
            "e transparência na apresentação das limitações e ameaças à validade do estudo."
        )
    )

    assunto_principal: str = Field(
        description=(
            "Identificação técnica detalhada do grande tema e subárea do artigo. "
            "Explique qual a problemática central enfrentada, o contexto científico em que o estudo está inserido "
            "e qual lacuna de conhecimento da literatura os autores buscam preencher."
        )
    )

    foco: str = Field(
        description=(
            "Declaração cristalina do foco específico do trabalho: hipótese de pesquisa formulada, "
            "objetivo primário delimitado e escopo exato da investigação empírica ou teórica."
        )
    )

    foco_teorico: str = Field(
        description=(
            "Mapeamento exaustivo do arcabouço teórico que alicerça o trabalho: teorias basilares, "
            "escolas de pensamento, conceitos-chave, modelos matemáticos/computacionais e autores seminais citados "
            "que dão sustentação ao raciocínio dos pesquisadores."
        )
    )


# --- OBJETO CONSOLIDADO FINAL ---
class AnaliseArtigo(BaseModel):
    """
    Estrutura mestra consolidada contendo todos os dados combinados das etapas.
    """
    titulo_original: str
    titulo_traduzido: Optional[str] = None
    resumo_original: str
    resumo_curto: str
    resumo_traduzido: Optional[str] = None
    resumo_completo: str
    perguntas_fundamentais: PerguntasFundamentais
    area_conhecimento: str
    palavras_chave: List[str]
    densidade_tecnica: str = "media"
