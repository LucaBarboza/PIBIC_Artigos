import io
import re
from typing import List, Tuple
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Flowable,
)
from reportlab.pdfgen import canvas

from src.schemas import AnaliseArtigo


# Paleta visual acadêmica (alinhada ao app Streamlit)
COR_NAVY = colors.HexColor("#0F172A")
COR_AZUL_ESCURO = colors.HexColor("#1E3A8A")
COR_AZUL_SECAO = colors.HexColor("#1E40AF")
COR_AZUL_DESTAQUE = colors.HexColor("#2563EB")
COR_TEXTO = colors.HexColor("#334155")
COR_MUTED = colors.HexColor("#64748B")
COR_BORDA = colors.HexColor("#CBD5E1")
COR_BORDA_SUAVE = colors.HexColor("#E2E8F0")
COR_BORDA_AZUL = colors.HexColor("#BFDBFE")
COR_FUNDO_TLDR = colors.HexColor("#EFF6FF")
COR_FUNDO_CARD_HEAD = colors.HexColor("#F1F5F9")
COR_FUNDO_SUAVE = colors.HexColor("#F8FAFC")
COR_BRANCO = colors.white

MARGEM_LATERAL = 48
MARGEM_SUPERIOR = 54
MARGEM_INFERIOR = 54


class _AccentRule(Flowable):
    """Linha divisória de seção com barra de destaque azul à esquerda."""

    def __init__(self, width: float, accent_width: float = 38.0):
        super().__init__()
        self.width = width
        self.height = 4.0
        self.accent_width = accent_width

    def draw(self):
        c = self.canv
        c.saveState()
        # Linha base suave
        c.setStrokeColor(COR_BORDA_SUAVE)
        c.setLineWidth(0.75)
        c.line(0, 1.5, self.width, 1.5)
        # Barra de destaque azul
        c.setStrokeColor(COR_AZUL_DESTAQUE)
        c.setLineWidth(2.2)
        c.line(0, 1.5, min(self.accent_width, self.width), 1.5)
        c.restoreState()


class NumberedCanvas(canvas.Canvas):
    """
    Canvas em dois passos para:
    - Faixa decorativa superior na página 1;
    - Cabeçalho discreto a partir da página 2;
    - Rodapé com 'Página X de Y' dinâmico em todas as páginas.
    """

    def __init__(self, *args, header_title: str = "", **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []
        self._header_title = header_title

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._draw_chrome(num_pages)
            super().showPage()
        super().save()

    def _draw_chrome(self, page_count: int):
        page_w, page_h = self._pagesize
        self.saveState()

        # Página 1: faixa superior elegante
        if self._pageNumber == 1:
            self.setFillColor(COR_AZUL_ESCURO)
            self.rect(0, page_h - 8, page_w, 8, stroke=0, fill=1)
            self.setFillColor(COR_AZUL_DESTAQUE)
            self.rect(0, page_h - 8, page_w * 0.35, 8, stroke=0, fill=1)
        else:
            # Páginas 2+: cabeçalho discreto
            y_header = page_h - 34
            self.setFont("Helvetica", 7.5)
            self.setFillColor(COR_MUTED)
            titulo_curto = self._header_title
            if len(titulo_curto) > 85:
                titulo_curto = titulo_curto[:82].rstrip() + "..."
            self.drawString(MARGEM_LATERAL, y_header + 5, titulo_curto)
            self.setFont("Helvetica-Bold", 7.5)
            self.setFillColor(COR_AZUL_DESTAQUE)
            self.drawRightString(page_w - MARGEM_LATERAL, y_header + 5, "PIBIC AI")
            self.setStrokeColor(COR_BORDA_SUAVE)
            self.setLineWidth(0.5)
            self.line(MARGEM_LATERAL, y_header, page_w - MARGEM_LATERAL, y_header)

        # Rodapé em todas as páginas
        y_line = 38
        self.setStrokeColor(COR_BORDA_SUAVE)
        self.setLineWidth(0.6)
        self.line(MARGEM_LATERAL, y_line, page_w - MARGEM_LATERAL, y_line)

        self.setFont("Helvetica", 8)
        self.setFillColor(COR_MUTED)
        self.drawString(
            MARGEM_LATERAL,
            25,
            "PIBIC AI • Relatório de Análise e Fichamento Científico",
        )
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(page_w - MARGEM_LATERAL, 25, page_text)

        self.restoreState()


def _formatar_texto_inline(texto: str) -> str:
    """
    Higieniza caracteres especiais para XML do ReportLab e converte
    negrito Markdown simples (**texto**) em <b>texto</b> sem alterar o conteúdo.
    """
    if not texto:
        return ""
    t = texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # Converte **negrito** em <b>negrito</b> de forma segura (mesma linha)
    t = re.sub(r"\*\*([^*\n]+?)\*\*", r"<b>\1</b>", t)
    t = t.replace("\n", "<br/>")
    return t


def _dividir_em_blocos(texto: str, max_chars: int = 1600) -> List[str]:
    """
    Divide um texto longo em parágrafos naturais (por linhas em branco) e,
    caso algum parágrafo isolado seja extremamente extenso, divide por linhas
    ou fronteiras de frase/palavras para garantir que células de tabela sempre
    quebrem entre páginas sem cortar nada.
    """
    if not texto or not texto.strip():
        return [""]

    texto_limpo = texto.replace("\r\n", "\n").strip()
    paragrafos = [p.strip() for p in re.split(r"\n\s*\n+", texto_limpo) if p.strip()]

    blocos: List[str] = []
    for p in paragrafos:
        if len(p) <= max_chars:
            blocos.append(p)
            continue

        # Se houver quebras de linha simples (ex.: listas longas), agrupa por linhas
        partes = [ln.strip() for ln in p.split("\n") if ln.strip()] if "\n" in p else re.split(r"(?<=[.!?])\s+", p)

        atual = ""
        for parte in partes:
            # Fallback final caso uma única parte sem pontuação exceda max_chars
            if len(parte) > max_chars:
                if atual:
                    blocos.append(atual)
                    atual = ""
                palavras = parte.split(" ")
                pedaco = ""
                for w in palavras:
                    if not pedaco:
                        pedaco = w
                    elif len(pedaco) + 1 + len(w) <= max_chars:
                        pedaco = f"{pedaco} {w}"
                    else:
                        blocos.append(pedaco)
                        pedaco = w
                if pedaco:
                    blocos.append(pedaco)
                continue

            sep = "\n" if "\n" in p else " "
            if not atual:
                atual = parte
            elif len(atual) + len(sep) + len(parte) <= max_chars:
                atual = f"{atual}{sep}{parte}"
            else:
                blocos.append(atual)
                atual = parte
        if atual:
            blocos.append(atual)

    return blocos or [""]


def _criar_bloco_callout(
    titulo: str,
    texto: str,
    usable_width: float,
    style_titulo: ParagraphStyle,
    style_corpo: ParagraphStyle,
    bg_color=COR_FUNDO_TLDR,
    border_color=COR_BORDA_AZUL,
    accent_color=COR_AZUL_DESTAQUE,
) -> Table:
    """
    Cria um box de destaque (ex.: Síntese Executiva ou Abstract) multi-linha
    com splitByRow=1 para nunca cortar texto em quebras de página.
    """
    blocos = _dividir_em_blocos(texto)
    rows: List[List[Paragraph]] = []

    if titulo:
        rows.append([Paragraph(titulo, style_titulo)])

    for b in blocos:
        rows.append([Paragraph(_formatar_texto_inline(b), style_corpo)])

    tbl = Table(rows, colWidths=[usable_width], splitByRow=1)

    cmds: List[Tuple] = [
        ("BACKGROUND", (0, 0), (-1, -1), bg_color),
        ("BOX", (0, 0), (-1, -1), 0.75, border_color),
        ("LINEBEFORE", (0, 0), (0, -1), 3.2, accent_color),
        ("LEFTPADDING", (0, 0), (-1, -1), 13),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, 0), 10),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 10),
    ]

    if titulo and len(rows) > 1:
        cmds.append(("BOTTOMPADDING", (0, 0), (-1, 0), 4))
        cmds.append(("NOSPLIT", (0, 0), (-1, 1)))

    tbl.setStyle(TableStyle(cmds))
    return tbl


def _criar_card_pergunta(
    indice: int,
    titulo: str,
    texto: str,
    usable_width: float,
    style_titulo: ParagraphStyle,
    style_corpo: ParagraphStyle,
) -> Table:
    """
    Cria um card estruturado para cada Pergunta Fundamental com cabeçalho
    destacado, borda lateral azul e quebra segura entre páginas (splitByRow=1).
    """
    header_html = (
        f'<font color="#2563EB"><b>{indice:02d}</b></font>'
        f'&nbsp;&nbsp;<font color="#CBD5E1">|</font>&nbsp;&nbsp;'
        f'{_formatar_texto_inline(titulo)}'
    )
    blocos = _dividir_em_blocos(texto)

    rows: List[List[Paragraph]] = [[Paragraph(header_html, style_titulo)]]
    for b in blocos:
        rows.append([Paragraph(_formatar_texto_inline(b), style_corpo)])

    tbl = Table(rows, colWidths=[usable_width], splitByRow=1)

    cmds: List[Tuple] = [
        # Cabeçalho do card
        ("BACKGROUND", (0, 0), (-1, 0), COR_FUNDO_CARD_HEAD),
        ("TOPPADDING", (0, 0), (-1, 0), 7),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 7),
        ("LINEBELOW", (0, 0), (-1, 0), 0.6, COR_BORDA_SUAVE),
        # Corpo do card
        ("BACKGROUND", (0, 1), (-1, -1), COR_BRANCO),
        ("TOPPADDING", (0, 1), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 4),
        ("TOPPADDING", (0, 1), (-1, 1), 8),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 9),
        # Bordas e padding lateral
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("BOX", (0, 0), (-1, -1), 0.65, COR_BORDA),
        ("LINEBEFORE", (0, 0), (0, -1), 3.0, COR_AZUL_DESTAQUE),
    ]

    # Garante que o título do card nunca fique órfão no fim da página
    if len(rows) > 1:
        cmds.append(("NOSPLIT", (0, 0), (-1, 1)))

    tbl.setStyle(TableStyle(cmds))
    return tbl


def _adicionar_cabecalho_secao(
    story: list,
    titulo: str,
    usable_width: float,
    style_secao: ParagraphStyle,
):
    """Adiciona título de seção + linha divisória com keepWithNext para evitar órfãos."""
    p = Paragraph(titulo, style_secao)
    story.append(p)
    rule = _AccentRule(usable_width)
    rule.keepWithNext = True
    story.append(rule)
    story.append(Spacer(1, 10))


def gerar_relatorio_pdf(analise: AnaliseArtigo, nome_arquivo_original: str = "artigo.pdf") -> bytes:
    """
    Gera um relatório acadêmico completo e diagramado em formato PDF a partir da análise do artigo.
    Retorna os bytes do arquivo PDF em memória.
    """
    buffer = io.BytesIO()
    page_w, page_h = A4
    usable_width = page_w - (2 * MARGEM_LATERAL)

    # Frame com padding 0 para alinhamento milimétrico entre textos, cards, linhas e rodapé
    frame = Frame(
        MARGEM_LATERAL,
        MARGEM_INFERIOR,
        usable_width,
        page_h - MARGEM_SUPERIOR - MARGEM_INFERIOR,
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
        id="main_frame",
    )

    doc = BaseDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=MARGEM_LATERAL,
        rightMargin=MARGEM_LATERAL,
        topMargin=MARGEM_SUPERIOR,
        bottomMargin=MARGEM_INFERIOR,
        title=analise.titulo_traduzido or analise.titulo_original,
        author="PIBIC AI",
    )
    doc.addPageTemplates([PageTemplate(id="default", frames=[frame])])

    styles = getSampleStyleSheet()

    # ---------------- ESTILOS TIPOGRÁFICOS ----------------
    style_tag = ParagraphStyle(
        "TagTopo",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=COR_AZUL_DESTAQUE,
        spaceAfter=6,
        splitLongWords=1,
    )

    style_titulo_trad = ParagraphStyle(
        "TituloTraduzido",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=17,
        leading=22,
        textColor=COR_NAVY,
        spaceAfter=5,
        splitLongWords=1,
    )

    style_titulo_orig = ParagraphStyle(
        "TituloOriginal",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=COR_MUTED,
        spaceAfter=10,
        splitLongWords=1,
    )

    style_meta = ParagraphStyle(
        "MetaTexto",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.8,
        leading=13,
        textColor=COR_TEXTO,
        alignment=TA_LEFT,
        splitLongWords=1,
    )

    style_secao = ParagraphStyle(
        "SecaoHeader",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12.5,
        leading=16,
        textColor=COR_AZUL_ESCURO,
        spaceBefore=12,
        spaceAfter=4,
        keepWithNext=True,
        splitLongWords=1,
    )

    style_subsecao = ParagraphStyle(
        "SubSecaoHeader",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        textColor=COR_NAVY,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True,
        splitLongWords=1,
    )

    style_corpo = ParagraphStyle(
        "CorpoTexto",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14.5,
        textColor=COR_TEXTO,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
        allowWidows=0,
        allowOrphans=0,
        splitLongWords=1,
    )

    style_tldr_title = ParagraphStyle(
        "TLDRTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=COR_AZUL_SECAO,
        splitLongWords=1,
    )

    style_tldr_text = ParagraphStyle(
        "TLDRText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14.2,
        textColor=COR_AZUL_ESCURO,
        alignment=TA_JUSTIFY,
        allowWidows=0,
        allowOrphans=0,
        splitLongWords=1,
    )

    style_abstract_text = ParagraphStyle(
        "AbstractText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.2,
        leading=14,
        textColor=COR_TEXTO,
        alignment=TA_JUSTIFY,
        allowWidows=0,
        allowOrphans=0,
        splitLongWords=1,
    )

    style_pergunta_titulo = ParagraphStyle(
        "PerguntaTitulo",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.8,
        leading=13,
        textColor=COR_NAVY,
        splitLongWords=1,
    )

    style_pergunta_texto = ParagraphStyle(
        "PerguntaTexto",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.3,
        leading=14,
        textColor=COR_TEXTO,
        alignment=TA_JUSTIFY,
        allowWidows=0,
        allowOrphans=0,
        splitLongWords=1,
    )

    story = []

    # ---------------- 1. CABEÇALHO & TÍTULOS ----------------
    story.append(Paragraph("RELATÓRIO DE ANÁLISE CIENTÍFICA", style_tag))

    if analise.titulo_traduzido:
        story.append(Paragraph(_formatar_texto_inline(analise.titulo_traduzido), style_titulo_trad))
        story.append(
            Paragraph(
                f"<b>Título Original:</b> <i>{_formatar_texto_inline(analise.titulo_original)}</i>",
                style_titulo_orig,
            )
        )
    else:
        story.append(Paragraph(_formatar_texto_inline(analise.titulo_original), style_titulo_trad))
        story.append(Spacer(1, 6))

    # Painel de Metadados (Área do Conhecimento e Palavras-chave)
    meta_rows = []
    if getattr(analise, "area_conhecimento", None):
        meta_rows.append(
            [
                Paragraph(
                    f'<font color="#1E40AF"><b>Área do Conhecimento:</b></font> '
                    f'{_formatar_texto_inline(analise.area_conhecimento)}',
                    style_meta,
                )
            ]
        )
    if getattr(analise, "palavras_chave", None):
        tags_fmt = " &nbsp;&bull;&nbsp; ".join(
            f'<font color="#1E3A8A">#{_formatar_texto_inline(tag)}</font>'
            for tag in analise.palavras_chave
        )
        meta_rows.append(
            [
                Paragraph(
                    f'<font color="#1E40AF"><b>Palavras-chave:</b></font> {tags_fmt}',
                    style_meta,
                )
            ]
        )

    if meta_rows:
        meta_table = Table(meta_rows, colWidths=[usable_width], splitByRow=1)
        meta_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), COR_FUNDO_SUAVE),
                ("BOX", (0, 0), (-1, -1), 0.65, COR_BORDA_SUAVE),
                ("LINEBEFORE", (0, 0), (0, -1), 2.5, COR_BORDA),
                ("LEFTPADDING", (0, 0), (-1, -1), 11),
                ("RIGHTPADDING", (0, 0), (-1, -1), 11),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, 0), 7),
                ("BOTTOMPADDING", (0, -1), (-1, -1), 7),
            ])
        )
        story.append(meta_table)
        story.append(Spacer(1, 10))

    # Box de Destaque para o Resumo Curto (TL;DR)
    tldr_table = _criar_bloco_callout(
        titulo="SÍNTESE EXECUTIVA (RESUMO CURTO)",
        texto=analise.resumo_curto,
        usable_width=usable_width,
        style_titulo=style_tldr_title,
        style_corpo=style_tldr_text,
        bg_color=COR_FUNDO_TLDR,
        border_color=COR_BORDA_AZUL,
        accent_color=COR_AZUL_DESTAQUE,
    )
    story.append(tldr_table)
    story.append(Spacer(1, 12))

    # ---------------- 2. RESUMOS ----------------
    _adicionar_cabecalho_secao(story, "Resumos", usable_width, style_secao)

    story.append(Paragraph("Resumo", style_subsecao))
    abstract_box = _criar_bloco_callout(
        titulo="",
        texto=analise.resumo_original,
        usable_width=usable_width,
        style_titulo=style_tldr_title,
        style_corpo=style_abstract_text,
        bg_color=COR_FUNDO_SUAVE,
        border_color=COR_BORDA_SUAVE,
        accent_color=COR_BORDA,
    )
    story.append(abstract_box)
    story.append(Spacer(1, 6))

    if analise.resumo_traduzido:
        story.append(Paragraph("Resumo Traduzido", style_subsecao))
        for bloco in _dividir_em_blocos(analise.resumo_traduzido):
            story.append(Paragraph(_formatar_texto_inline(bloco), style_corpo))
        story.append(Spacer(1, 4))

    story.append(Paragraph("Resumo Completo", style_subsecao))
    for bloco in _dividir_em_blocos(analise.resumo_completo):
        story.append(Paragraph(_formatar_texto_inline(bloco), style_corpo))
    story.append(Spacer(1, 10))

    # ---------------- 3. PERGUNTAS FUNDAMENTAIS ----------------
    _adicionar_cabecalho_secao(
        story,
        "Perguntas Fundamentais que o Artigo Respondeu",
        usable_width,
        style_secao,
    )

    pf = analise.perguntas_fundamentais
    perguntas = [
        ("Novidades do artigo", pf.novidades_do_artigo),
        ("O que foi apresentado tá bem fundamentado", pf.fundamentacao),
        ("Qualidade do artigo", pf.qualidade_artigo),
        ("Assunto principal", pf.assunto_principal),
        ("Foco", pf.foco),
        ("Foco teórico", pf.foco_teorico),
    ]

    for idx, (tit_p, txt_p) in enumerate(perguntas, start=1):
        card_table = _criar_card_pergunta(
            indice=idx,
            titulo=tit_p,
            texto=txt_p,
            usable_width=usable_width,
            style_titulo=style_pergunta_titulo,
            style_corpo=style_pergunta_texto,
        )
        story.append(card_table)
        story.append(Spacer(1, 9))

    # Construção do documento com o Canvas customizado
    header_title = analise.titulo_traduzido or analise.titulo_original
    doc.build(
        story,
        canvasmaker=lambda *args, **kwargs: NumberedCanvas(
            *args, header_title=header_title, **kwargs
        ),
    )

    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data


def sanitizar_nome_arquivo(nome: str) -> str:
    """Gera um nome de arquivo seguro e limpo para o download do relatório."""
    base = re.sub(r"[^\w\-_.]", "_", nome.replace(".pdf", ""))
    return f"Relatorio_{base[:40]}.pdf"
