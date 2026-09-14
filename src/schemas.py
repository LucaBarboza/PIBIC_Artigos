from typing import Optional
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
            "Referência bibliográfica padrão Vancouver (adotado pelo International Committee of Medical Journal Editors - ICMJE e indexadores MEDLINE/PubMed). "
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
            "2. TÍTULO DO ARTIGO: Entre aspas duplas, com pontuação antes da aspa de fechamento (ex: \"Deep learning in edge computing,\"). "
            "3. PERIÓDICO: Título oficial abreviado do periódico ou anais em ITÁLICO (ex: *IEEE Trans. Neural Netw. Learn. Syst.*). "
            "4. DADOS: Precedidos de 'vol.', 'no.', 'pp.', mês abreviado e ano. "
            "5. DOI: Precedido de 'doi: 10.xxxx/yyyy.'. "
            "Exemplo: J. D. Smith and A. K. Miller, \"Deep learning in edge computing,\" *IEEE Trans. Comput.*, vol. 72, no. 5, pp. 1320–1334, May 2024, doi: 10.1109/TC.2024.3312345."
        ),
    )

    chicago: Optional[str] = Field(
        default=None,
        description=(
            "Referência bibliográfica no formato Chicago Manual of Style (sistema autor-data ou bibliografia final). "
            "Regras fundamentais: "
            "1. AUTORIA: Sobrenome, Nome do primeiro autor, seguido de 'e' e Nome Sobrenome dos demais. "
            "2. ANO: Ano de publicação logo após os autores (no autor-data) ou ao final. "
            "3. TÍTULO: Título do artigo entre aspas duplas com letras maiúsculas nas palavras principais (Headline style). "
            "4. PERIÓDICO: Nome da revista em ITÁLICO, volume, número preceded por 'no.', ano entre parênteses (se sistema notas) ou páginas precedidas por dois pontos. "
            "5. DOI: Precedido por link 'https://doi.org/...'. "
            "Exemplo: Smith, John D., and Adam K. Miller. 2024. \"Historical Perspectives on AI Governance.\" *Philosophy & Technology* 37, no. 2: 45–68. https://doi.org/10.1007/s13347-024-00712-x."
        ),
    )

    mla: Optional[str] = Field(
        default=None,
        description=(
            "Referência bibliográfica padrão MLA 9ª Edição (Modern Language Association). "
            "Regras fundamentais: "
            "1. AUTORIA: Sobrenome, Nome do primeiro autor, seguido de 'and' e Nome Sobrenome do segundo (se houver). "
            "2. TÍTULO DO ARTIGO: Entre aspas duplas com maiúsculas nas palavras principais. "
            "3. PERIÓDICO: Nome da publicação em ITÁLICO, seguido de vírgula. "
            "4. DETALHES: 'vol. X, no. Y, Ano, pp. AA-BB.' "
            "5. DOI/LOCALIZAÇÃO: URL do DOI ao final sem ponto final. "
            "Exemplo: Smith, John D., and Adam K. Miller. \"Linguistic Structures in Transformer Models.\" *Modern Language Review*, vol. 119, no. 1, 2024, pp. 88-105. https://doi.org/10.1353/mlr.2024.0012"
        ),
    )


class PerguntasFundamentais(BaseModel):
    """
    Avaliação analítica crítica e profunda do artigo respondendo às perguntas
    metodológicas e teóricas mais relevantes para pesquisa e iniciação científica.
    """

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
            "objetivo primário e escopo delimitado da investigação empírica, computacional ou bibliográfica."
        )
    )

    foco_teorico: str = Field(
        description=(
            "Mapeamento exaustivo do arcabouço teórico que alicerça o trabalho: teorias basilares, "
            "escolas de pensamento, conceitos-chave, modelos matemáticos/computacionais e autores seminais citados "
            "que dão sustentação ao raciocínio dos pesquisadores."
        )
    )

    novidades_do_artigo: str = Field(
        description=(
            "Diferenciais e inovações científicas trazidas pela publicação: metodologias inéditas, "
            "algoritmos propostos, novas bases de dados criadas, resultados empíricos contraintuitivos ou superação de limitações "
            "apresentadas em trabalhos anteriores no estado da arte."
        )
    )

    fundamentacao: str = Field(
        description=(
            "Avaliação crítica detalhada sobre o rigor da fundamentação: o desenho experimental, amostras, dados estatísticos, "
            "provas matemáticas ou evidências qualitativas apresentadas são robustos e suficientes para alicerçar as conclusões? "
            "Aponte se há inferências precipitadas, pontos fortes e consistência entre dados e alegações."
        )
    )

    qualidade_artigo: str = Field(
        description=(
            "Veredito crítico sobre a qualidade global do artigo (nível de maturidade acadêmica): solidez metodológica, "
            "clareza da escrita e reprodutibilidade, grau de contribuição para a comunidade científica e explicitação clara de "
            "ameaças à validade e limitações do estudo."
        )
    )


class AnaliseArtigo(BaseModel):
    """
    Estrutura mestra contendo a síntese em múltiplos níveis, metadados bibliográficos
    e o fichamento científico estruturado do artigo.
    """

    titulo_original: str = Field(
        description="Título original literal do artigo científico, exatamente como redigido no PDF."
    )

    titulo_traduzido: str = Field(
        description="Tradução técnica fidedigna do título para o Português brasileiro, utilizando a terminologia acadêmica correta da área de conhecimento."
    )

    resumo_original: str = Field(
        description="Texto integral do resumo (abstract) do artigo em seu idioma original, exatamente como redigido pelos autores."
    )

    resumo_curto: str = Field(
        description=(
            "Síntese executiva (TL;DR) de alta densidade em 2 a 3 frases no máximo, em Português. "
            "Deve responder diretamente: (1) O que foi investigado, (2) Como foi feito, e (3) Qual o resultado/conclusão principal."
        )
    )

    resumo_traduzido: str = Field(
        description="Tradução técnica, fluente e precisa do resumo (abstract) para o Português brasileiro, mantendo rigor conceitual e terminológico."
    )

    resumo_completo: str = Field(
        description=(
            "Fichamento analítico aprofundado e abrangente em Português. "
            "Deve ser organizado de forma rica e detalhada abordando: "
            "1. Contextualização e Motivação do problema; "
            "2. Metodologia e Abordagem adotada (materiais, técnicas, experimentos ou modelos); "
            "3. Principais Resultados obtidos e Métricas alcançadas; "
            "4. Discussão dos Resultados, Implicações e Conclusão dos autores."
        )
    )

    perguntas_fundamentais: PerguntasFundamentais = Field(
        description="Conjunto estruturado de respostas minuciosas às perguntas fundamentais de mérito e rigor do artigo."
    )

    referencias: ReferenciasNormatizadas = Field(
        description="Referências bibliográficas formatadas rigorosamente nas normas selecionadas pelo usuário (campos não selecionados devem retornar None)."
    )
