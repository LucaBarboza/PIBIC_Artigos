from typing import Optional, List
from pydantic import BaseModel, Field


class ReferenciasNormatizadas(BaseModel):
    """
    Modelagem estruturada para geração rigorosa de referências bibliográficas
    acadêmicas nas principais normas internacionais e nacionais.
    Campos opcionais: preenchidos apenas quando solicitados pelo usuário.
    """

    abnt: Optional[str] = Field(
        default=None,
        description=(
            "Referência bibliográfica completa formatada com rigor absoluto segundo a norma brasileira ABNT NBR 6023. "
            "Regras fundamentais: "
            "1. AUTORIA: SOBRENOME DO(S) AUTOR(ES) EM CAIXA ALTA, seguido(s) do prenome abreviado ou por extenso. Para mais de 3 autores, pode-se usar et al. ou listar todos. "
            "2. TÍTULO: Título do artigo em fonte regular (sem negrito); subtítulo (se houver) precedido de dois pontos também sem negrito. "
            "3. PERIÓDICO: Título da revista/periódico ou anais de evento em DESTAQUE (usar negrito em Markdown, ex: **Nome da Revista**). "
            "4. DADOS DE PUBLICAÇÃO: Cidade de publicação (se identificada), volume (v. X), número ou fascículo (n. Y), páginas inicial e final (p. AA-BB), mês abreviado (se houver) e ano de publicação. "
            "5. IDENTIFICADOR DIGITAL: DOI formatado como link ou 'DOI: 10.xxxx/yyyy'. "
            "Exemplo: SILVA, João da; SANTOS, Maria. Aplicações de inteligência artificial em saúde pública. **Revista Brasileira de Epidemiologia**, São Paulo, v. 25, n. 2, p. 110-125, maio 2023. DOI: 10.1590/1980-549720230012."
        ),
    )

    apa: Optional[str] = Field(
        default=None,
        description=(
            "Referência bibliográfica completa segundo a 7ª edição da APA (American Psychological Association). "
            "Regras fundamentais: "
            "1. AUTORIA: Sobrenome do autor seguido de vírgula e iniciais do prenome seguidas de ponto (ex: Smith, J. D., & Miller, A. K.). "
            "2. ANO: Ano de publicação entre parênteses seguido de ponto final. "
            "3. TÍTULO DO ARTIGO: Em formato de frase (Sentence case), apenas a primeira letra da primeira palavra e de nomes próprios em maiúscula, sem itálico nem aspas. "
            "4. PERIÓDICO: Nome completo do periódico em ITÁLICO com letras maiúsculas nas palavras principais (Title Case), seguido de vírgula e número do volume também em ITÁLICO, número da edição entre parênteses sem itálico, e intervalo de páginas com hífen en-dash. "
            "5. DOI: Formato de URL ativa iniciando estritamente com https://doi.org/... "
            "Exemplo: Smith, J. D., & Miller, A. K. (2024). Deep learning applications in automated document analysis. *Journal of Computer Science*, 18(4), 102–118. https://doi.org/10.1016/j.jcs.2024.102"
        ),
    )

    vancouver: Optional[str] = Field(
        default=None,
        description=(
            "Referência bibliográfica padrão Vancouver (adotado pelo ICMJE e indexadores MEDLINE/PubMed). "
            "Regras fundamentais: "
            "1. AUTORIA: Sobrenome seguido das iniciais sem pontos nem vírgulas entre eles (ex: Smith JD, Miller AK). Listar até 6 autores antes de usar 'et al.'. "
            "2. TÍTULO DO ARTIGO: Em caixa baixa (exceto primeira letra e nomes próprios), sem aspas nem itálico. "
            "3. PERIÓDICO: Título abreviado padrão da revista médica indexada na NLM sem pontos após as abreviaturas, seguido de ponto. "
            "4. DATA E LOCALIZAÇÃO: Ano de publicação seguido de ponto e vírgula, volume e edição entre parênteses seguidos de dois pontos, páginas sem a letra 'p'. "
            "5. DOI: Incluir ao final 'doi: 10.xxxx/yyyy'. "
            "Exemplo: Smith JD, Miller AK, Johnson RE. Clinical outcomes in digital pathology. N Engl J Med. 2024;390(8):720-731. doi: 10.1056/NEJMoa2309123."
        ),
    )

    ieee: Optional[str] = Field(
        default=None,
        description=(
            "Referência bibliográfica padrão IEEE (Institute of Electrical and Electronics Engineers). "
            "Regras fundamentais: "
            "1. AUTORIA: Inicial(is) do prenome com ponto, espaço e sobrenome completo (ex: J. D. Smith and A. K. Miller). "
            "2. TÍTULO DO ARTIGO: Entre aspas duplas, com pontuação antes da aspa de fechamento. "
            "3. PERIÓDICO: Título oficial abreviado do periódico ou anais em ITÁLICO (ex: *IEEE Trans. Neural Netw. Learn. Syst.*). "
            "4. DADOS: Precedidos de 'vol.', 'no.', 'pp.', mês abreviado e ano. "
            "5. DOI: Precedido de 'doi: 10.xxxx/yyyy.'. "
            "Exemplo: J. D. Smith and A. K. Miller, \"Deep learning in edge computing,\" *IEEE Trans. Comput.*, vol. 72, no. 5, pp. 1320–1334, May 2024, doi: 10.1109/TC.2024.3312345."
        ),
    )

    chicago: Optional[str] = Field(
        default=None,
        description=(
            "Referência bibliográfica no formato Chicago Manual of Style (sistema autor-data ou notas). "
            "Exemplo: Smith, John D., and Adam K. Miller. 2024. \"Historical Perspectives on AI Governance.\" *Philosophy & Technology* 37, no. 2: 45–68. https://doi.org/10.1007/s13347-024-00712-x."
        ),
    )

    mla: Optional[str] = Field(
        default=None,
        description=(
            "Referência bibliográfica padrão MLA 9ª Edição (Modern Language Association). "
            "Exemplo: Smith, John D., and Adam K. Miller. \"Linguistic Structures in Transformer Models.\" *Modern Language Review*, vol. 119, no. 1, 2024, pp. 88-105. https://doi.org/10.1353/mlr.2024.0012"
        ),
    )


# --- ETAPA 1: Identificação e Referências ---
class IdentificacaoEReferencias(BaseModel):
    """
    Sub-schema focado exclusivamente na extração cirúrgica de dados bibliográficos,
    autoria, títulos e referências normatizadas.
    """
    titulo_original: str = Field(
        description="Título original literal do artigo científico, exatamente como redigido no PDF."
    )
    titulo_traduzido: str = Field(
        description="Tradução técnica fidedigna do título para o Português brasileiro culto."
    )
    resumo_original: str = Field(
        description="Texto integral do resumo (abstract) original do artigo em seu idioma de origem, sem omissões."
    )
    referencias: ReferenciasNormatizadas = Field(
        description="Referências bibliográficas formatadas rigorosamente nas normas selecionadas pelo usuário (campos não selecionados devem retornar None)."
    )
    area_conhecimento: str = Field(
        description="Grande área e subárea do conhecimento científico a que o artigo pertence (ex.: 'Ciência da Computação / Inteligência Artificial', 'Medicina / Radiologia', 'Engenharia Mecânica / Termodinâmica')."
    )
    palavras_chave: List[str] = Field(
        description="Lista com 3 a 5 palavras-chave conceituais em Português que melhor caracterizam o estudo."
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
    resumo_traduzido: str = Field(
        description=(
            "Tradução técnica, fluente e rigorosa do resumo (abstract) para o Português brasileiro formal, "
            "preservando termos técnicos e jargões da área acadêmica do estudo."
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
    titulo_traduzido: str
    resumo_original: str
    resumo_curto: str
    resumo_traduzido: str
    resumo_completo: str
    perguntas_fundamentais: PerguntasFundamentais
    referencias: ReferenciasNormatizadas
    area_conhecimento: str
    palavras_chave: List[str]
