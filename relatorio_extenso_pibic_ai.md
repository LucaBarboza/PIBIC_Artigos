# Relatório Científico Extenso: PIBIC AI - Analisador de Artigos Científicos

## 1. Introdução

O volume de publicações científicas tem crescido exponencialmente nas últimas décadas, tornando o processo de revisão bibliográfica uma tarefa hercúlea para estudantes, pesquisadores e acadêmicos. Diante do desafio de filtrar, ler e fichar dezenas ou até centenas de artigos para embasar projetos de pesquisa — como Iniciação Científica (PIBIC), Trabalhos de Conclusão de Curso (TCC), Dissertações de Mestrado e Teses de Doutorado —, surge a necessidade imperativa de ferramentas computacionais avançadas que auxiliem a cognição humana. É nesse contexto de sobrecarga informacional que o **PIBIC AI - Analisador de Artigos Científicos** é introduzido.

O PIBIC AI é uma aplicação interativa desenvolvida com tecnologias web modernas, projetada primariamente para operar como um assistente de pesquisa incansável. Ao invés de substituir a leitura analítica do ser humano, o sistema atua como um acelerador cognitivo, fornecendo em segundos um panorama dissecado do documento científico. Essa triagem avançada permite que o pesquisador julgue imediatamente a pertinência de um artigo para o seu escopo de estudo, poupando preciosas horas que seriam gastas na leitura de trabalhos tangenciais ou metodologicamente frágeis.

A fundamentação tecnológica deste projeto baseia-se nos recentes avanços em Inteligência Artificial Generativa Multimodal (LLMs - *Large Language Models*). Com o advento de modelos capazes de ingerir diretamente arquivos em formato PDF — interpretando não apenas o texto cru, mas o layout visual, hierarquias de cabeçalhos e fluxos de leitura —, tornou-se viável automatizar a extração estruturada de informações. O PIBIC AI explora essa capacidade em sua plenitude, consumindo publicações densas e extraindo, de maneira estruturada, o cerne metodológico, teórico e empírico do trabalho em questão.

Ao automatizar o laborioso processo de fichamento, a ferramenta promove uma democratização e aceleração da ciência, auxiliando jovens pesquisadores que, frequentemente, enfrentam dificuldades iniciais para decifrar jargões metodológicos complexos, identificar lacunas literárias ou compreender estruturas estatísticas intrincadas.

## 2. Objetivos do Projeto

### Objetivo Geral
O objetivo fundamental deste sistema é fornecer uma interface de extração de inteligência documental que converta artigos científicos brutos em formato PDF em fichamentos analíticos hiperestruturados, reduzindo drasticamente o tempo de triagem bibliográfica do usuário. 

### Objetivos Específicos
* **Automação do Fichamento:** Processar documentos acadêmicos e gerar resumos em múltiplos níveis de profundidade (desde o rápido *TL;DR* até um fichamento completo abrangendo de quatro a seis parágrafos detalhados).
* **Avaliação Metodológica Crítica:** Utilizar os LLMs não apenas para sumarizar, mas para avaliar criticamente a solidez dos argumentos empíricos e a confiabilidade estatística apresentada no artigo.
* **Extração Garantida via Esquemas Tipados:** Forçar o modelo de IA a devolver respostas que sigam rigorosamente uma estrutura de dados de máquina (*Structured Outputs*), permitindo que a interface gráfica apresente métricas e *badges* sem falhas de formatação.
* **Supressão de Alucinação (*Zero Hallucination*):** Implementar um módulo interativo (Chat) estritamente fundamentado, no qual a IA está terminantemente proibida de inventar dados, baseando-se única e exclusivamente no documento anexado e referenciando páginas ou seções do mesmo.
* **Geração de Artefatos:** Possibilitar a exportação do fichamento consolidado na forma de um relatório PDF diagramado e legível offline.

## 3. Metodologia e Abordagem Arquitetural

A engenharia do sistema baseia-se em uma arquitetura orientada a fluxos modulares. Dado que artigos científicos frequentemente contêm milhares de palavras e dezenas de páginas, requisitar a um LLM que faça absolutamente tudo (fichamento, metadados e análise crítica) em uma única instrução (prompt único) quase sempre resulta em perda de qualidade temporal — o fenômeno conhecido como *Lost in the Middle*, onde o modelo dilui sua atenção e entrega resumos excessivamente supérfluos, rasos e genéricos.

Para mitigar essa limitação, a metodologia de desenvolvimento adota um **Pipeline Particionado em Três Etapas Independentes**. Em vez de uma grande chamada à API, o sistema faz três requisições sequenciais altamente especializadas para o mesmo PDF. Cada requisição utiliza uma Persona (System Instruction) distinta e um Prompt ultra-focado, garantindo que o modelo concentre todo o seu poder computacional de atenção naquele exato escopo.

A integração foi desenvolvida utilizando a linguagem Python e o pacote `google-genai`. Como retaguarda visual, o framework Streamlit gerencia os estados de sessão da web e orquestra a submissão assíncrona, atualizando a barra de progresso do usuário conforme as etapas são concluídas. O uso de `pydantic` assegura que, a cada etapa do pipeline, os JSONs gerados pela API sejam perfeitamente transmutados em objetos nativos Python fortemente tipados e validados, mitigando qualquer inconsistência de chaves faltantes ou tipos incorretos.

O pipeline lida ainda com estratégias robustas contra falhas transitórias de infraestrutura, implementando *graceful degradation* (fallback). Caso o modelo primário `gemini-3.5-flash-lite` apresente anomalias de rede, cota ou *timeout*, a lógica transita transparentemente para o modelo estável `gemini-3.1-flash-lite`, assegurando continuidade no serviço.

## 4. Métodos: O Pipeline de Três Etapas

A seguir, a dissecação metodológica de cada uma das três etapas do pipeline, apresentando a mecânica do processo, a justificativa e as instruções literais transmitidas à Inteligência Artificial.

### Etapa 1: Identificação Bibliográfica e Metadados
Nesta etapa, o motor foca estritamente nos aspectos "catalográficos" do artigo. O modelo varre o documento buscando títulos, rodapés de periódicos, o abstract original, a subárea e tenta estimar, pela densidade de equações ou prosa fluida, a "densidade técnica" da leitura.

**System Instruction (Persona):**
> "Você é um catalogador acadêmico sênior com máxima precisão em metadados bibliográficos, identificação de autoria, periódicos e áreas do conhecimento científico."

**Prompt Exato (Instrução):**
```text
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
```

### Etapa 2: Sínteses em Múltiplos Níveis e Fichamento Analítico Denso
Na segunda fase, a carga cognitiva foca na densidade do texto. É aqui que o sistema proíbe respostas curtas. A intenção não é prover uma leitura preguiçosa, mas construir um documento robusto que sirva como fichamento definitivo do aluno. 

**System Instruction (Persona):**
> "Você é um orientador de pesquisa acadêmica renomado. Sua escrita é rica, técnica, densa, estruturada e exaustiva. Você não poupa detalhes metodológicos e resultados."

**Prompt Exato (Instrução):**
```text
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
```

### Etapa 3: Avaliação Crítica e Perguntas Fundamentais Aprofundadas
A etapa final eleva o grau de criticidade. Transforma-se a IA de uma mera resumidora para uma juíza das evidências (*reviewer*). Ela é encarregada de desmembrar inovações, julgar a fundamentação, apontar as lacunas exploradas (o gap na literatura) e extrair o modelo teórico.

**System Instruction (Persona):**
> "Você é um avaliador de artigos de revistas de alto impacto (Nature, IEEE, Science, Scielo). Sua análise é crítica, criteriosa, altamente analítica e sem superficialidade."

**Prompt Exato (Instrução):**
```text
Você é um parecerista científico de periódico internacional Qualis A1 avaliando com rigor o artigo '{nome_arquivo}'.

ATENÇÃO: Cada uma das 6 perguntas fundamentais DEVE ser respondida de forma substancial e aprofundada, com múltiplos parágrafos, citando argumentos, dados e procedimentos concretos extraídos do texto do artigo. Respostas curtas de 1 ou 2 linhas serão REJEITADAS.

PERGUNTAS A RESPONDER:
1. 'novidades_do_artigo': Quais as inovações concretas, dados inéditos, novos algoritmos ou diferenciais que este trabalho traz em relação ao estado da arte? (Mínimo 2 parágrafos densos).
2. 'fundamentacao': O que foi apresentado tá bem fundamentado? Avalie com rigor crítico se as evidências empíricas, dados estatísticos, amostras ou deduções teóricas realmente sustentam as conclusões ou se há lacunas e extrapolações. (Mínimo 2 parágrafos analíticos).
3. 'qualidade_artigo': Qual o veredito sobre a qualidade acadêmica global? Avalie clareza, rigor metodológico, reprodutibilidade, relevância e explicitação de limitações. (Mínimo 2 parágrafos).
4. 'assunto_principal': Identifique o grande tema e a lacuna da literatura enfrentada pelos pesquisadores.
5. 'foco': Explique com clareza a hipótese central, pergunta norteadora e objetivo específico do estudo.
6. 'foco_teorico': Mapeie as teorias fundamentais, autores seminais, escolas de pensamento e modelos conceituais que sustentam o artigo.
```

### Módulo de Chat: RAG com Zero Alucinação (Strict Grounding)
Embora os relatórios estáticos resolvam grande parte da necessidade do usuário, perguntas específicas (ex: *"Qual o p-valor exato da Tabela 2?"*) necessitam de um canal conversacional. O Módulo de Chat implementa uma abordagem efêmera onde o documento em memória, somado ao histórico recente do chat e à pergunta do usuário formam um "contexto longo" na camada de entrada do Gemini.

**System Instruction do Módulo de Chat:**
```text
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
```

## 5. Schemas Pydantic (Structured Outputs)

A robustez da plataforma reside em sua camada de validação e modelagem de dados. Ao invés de o Gemini responder com textos livres não-estruturados, a API recebe *JSON schemas* garantindo que cada campo desejado será populado. 

Abaixo, a definição exata das classes Pydantic utilizadas para moldar a saída de cada etapa:

```python
from typing import Optional, List
from pydantic import BaseModel, Field

# --- ETAPA 1: Identificação Bibliográfica e Metadados ---
class IdentificacaoEMetadados(BaseModel):
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
```

## 6. Considerações Finais

Através do emprego coeso de bibliotecas como `streamlit`, `pydantic` e o SDK moderno `google-genai`, a plataforma transcende o caráter de "brinquedo experimental" de IA para consolidar-se como um utilitário verdadeiramente acadêmico e rigoroso. Ao segmentar os prompts, proibir o viés de concisão excessiva, tipificar os schemas e estipular regras de *zero hallucination*, o PIBIC AI honra as exigências severas do ambiente universitário e providencia um instrumental de valor inestimável para a pesquisa científica moderna.
