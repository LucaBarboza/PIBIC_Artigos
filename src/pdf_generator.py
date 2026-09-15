import io
import re
from typing import List
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether,
)
from reportlab.pdfgen import canvas

from src.schemas import AnaliseArtigo


class NumberedCanvas(canvas.Canvas):
    """
    Canvas em dois passos para calcular o total de páginas e imprimir
    'Página X de Y' dinamicamente no rodapé.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Linha fina acima do rodapé
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 38, 558, 38)

        # Texto do rodapé
        self.drawString(54, 26, "PIBIC AI • Relatório de Análise e Fichamento Científico")
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(558, 26, page_text)
        self.restoreState()


def _escapar_texto(texto: str) -> str:
    """Higieniza caracteres para evitar quebras em tags do ReportLab."""
    if not texto:
        return ""
    # Substituir quebras de linha por tags <br/>
    t = texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # Restaurar quebras de linha em tags válidas
    t = t.replace("\n\n", "<br/><br/>").replace("\n", "<br/>")
    return t


def gerar_relatorio_pdf(analise: AnaliseArtigo, nome_arquivo_original: str = "artigo.pdf") -> bytes:
    """
    Gera um relatório acadêmico completo e diagramado em formato PDF a partir da análise do artigo.
    Retorna os bytes do arquivo PDF em memória.
    """
    buffer = io.BytesIO()

    # Documento com margens de 54pt (aprox 1.9 cm)
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=50,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()

    # Estilos tipográficos customizados
    style_tag = ParagraphStyle(
        "TagTopo",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#2563EB"),
        textTransform="uppercase",
        spaceAfter=6,
    )

    style_titulo_trad = ParagraphStyle(
        "TituloTraduzido",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=17,
        leading=22,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=4,
    )

    style_titulo_orig = ParagraphStyle(
        "TituloOriginal",
        parent=styles["Italic"],
        fontName="Helvetica-Oblique",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#64748B"),
        spaceAfter=14,
    )

    style_secao = ParagraphStyle(
        "SecaoHeader",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#1E40AF"),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True,
    )

    style_subsecao = ParagraphStyle(
        "SubSecaoHeader",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#1E293B"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True,
    )

    style_corpo = ParagraphStyle(
        "CorpoTexto",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14.5,
        textColor=colors.HexColor("#334155"),
        spaceAfter=8,
    )

    style_tldr_title = ParagraphStyle(
        "TLDRTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#1E40AF"),
        spaceAfter=4,
    )

    style_tldr_text = ParagraphStyle(
        "TLDRText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#1E3A8A"),
    )

    style_pergunta_titulo = ParagraphStyle(
        "PerguntaTitulo",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=4,
    )

    style_pergunta_texto = ParagraphStyle(
        "PerguntaTexto",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor("#334155"),
    )

    style_referencia_code = ParagraphStyle(
        "RefCode",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#1E293B"),
    )

    story = []

    # ---------------- 1. CABEÇALHO & TÍTULOS ----------------
    story.append(Paragraph("RELATÓRIO DE ANÁLISE CIENTÍFICA", style_tag))
    if analise.titulo_traduzido:
        story.append(Paragraph(_escapar_texto(analise.titulo_traduzido), style_titulo_trad))
        story.append(Paragraph(f"<b>Título Original:</b> <i>{_escapar_texto(analise.titulo_original)}</i>", style_titulo_orig))
    else:
        story.append(Paragraph(_escapar_texto(analise.titulo_original), style_titulo_trad))

    meta_itens = []
    if getattr(analise, "area_conhecimento", None):
        meta_itens.append(f"<b>Área do Conhecimento:</b> {_escapar_texto(analise.area_conhecimento)}")
    if getattr(analise, "palavras_chave", None):
        tags_str = ", ".join(analise.palavras_chave)
        meta_itens.append(f"<b>Palavras-chave:</b> {_escapar_texto(tags_str)}")
    if meta_itens:
        meta_str = " &nbsp;&bull;&nbsp; ".join(meta_itens)
        story.append(Paragraph(meta_str, style_corpo))
        story.append(Spacer(1, 4))

    # Box de Destaque para o Resumo Curto (TL;DR)
    tldr_content = [
        Paragraph("⚡ SÍNTESE EXECUTIVA (RESUMO CURTO)", style_tldr_title),
        Paragraph(_escapar_texto(analise.resumo_curto), style_tldr_text),
    ]
    tldr_table = Table([[tldr_content]], colWidths=[504])
    tldr_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F0F7FF")),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#BFDBFE")),
            ("LINEBEFORE", (0, 0), (0, -1), 3.5, colors.HexColor("#2563EB")),
            ("PADDING", (0, 0), (-1, -1), 10),
        ])
    )
    story.append(tldr_table)
    story.append(Spacer(1, 14))

    # ---------------- 2. RESUMOS ----------------
    story.append(Paragraph("Resumos", style_secao))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#E2E8F0"), spaceAfter=10))

    story.append(Paragraph("Resumo", style_subsecao))
    story.append(Paragraph(_escapar_texto(analise.resumo_original), style_corpo))
    story.append(Spacer(1, 6))

    if analise.resumo_traduzido:
        story.append(Paragraph("Resumo Traduzido", style_subsecao))
        story.append(Paragraph(_escapar_texto(analise.resumo_traduzido), style_corpo))
        story.append(Spacer(1, 6))

    story.append(Paragraph("Resumo Completo", style_subsecao))
    story.append(Paragraph(_escapar_texto(analise.resumo_completo), style_corpo))
    story.append(Spacer(1, 14))

    # ---------------- 3. PERGUNTAS FUNDAMENTAIS ----------------
    story.append(Paragraph("Perguntas Fundamentais que o Artigo Respondeu", style_secao))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#E2E8F0"), spaceAfter=10))

    pf = analise.perguntas_fundamentais
    perguntas = [
        ("Novidades do artigo", pf.novidades_do_artigo),
        ("O que foi apresentado tá bem fundamentado", pf.fundamentacao),
        ("Qualidade do artigo", pf.qualidade_artigo),
        ("Assunto principal", pf.assunto_principal),
        ("Foco", pf.foco),
        ("Foco teórico", pf.foco_teorico),
    ]

    for tit_p, txt_p in perguntas:
        card_content = [
            Paragraph(tit_p, style_pergunta_titulo),
            Paragraph(_escapar_texto(txt_p), style_pergunta_texto),
        ]
        card_table = Table([[card_content]], colWidths=[504])
        card_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
                ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#E2E8F0")),
                ("PADDING", (0, 0), (-1, -1), 9),
            ])
        )
        story.append(KeepTogether([card_table, Spacer(1, 8)]))

    story.append(Spacer(1, 10))

    # ---------------- 4. REFERÊNCIA ----------------
    story.append(Paragraph("Referência", style_secao))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#E2E8F0"), spaceAfter=10))

    refs = analise.referencias
    normas_dict = {
        "ABNT": refs.abnt,
        "APA": refs.apa,
        "Vancouver": refs.vancouver,
        "IEEE": refs.ieee,
        "Chicago": refs.chicago,
        "MLA": refs.mla,
    }

    alguma_ref = False
    for nome_norma, valor in normas_dict.items():
        if valor:
            alguma_ref = True
            ref_content = [
                Paragraph(f"<b>{nome_norma}</b>", style_subsecao),
                Paragraph(_escapar_texto(valor), style_referencia_code),
            ]
            ref_table = Table([[ref_content]], colWidths=[504])
            ref_table.setStyle(
                TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
                    ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#CBD5E1")),
                    ("PADDING", (0, 0), (-1, -1), 8),
                ])
            )
            story.append(KeepTogether([ref_table, Spacer(1, 6)]))

    if not alguma_ref:
        story.append(Paragraph("<i>Nenhuma norma selecionada.</i>", style_corpo))

    # Construção do documento com o Canvas customizado
    doc.build(story, canvasmaker=NumberedCanvas)

    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data


def sanitizar_nome_arquivo(nome: str) -> str:
    """Gera um nome de arquivo seguro e limpo para o download do relatório."""
    base = re.sub(r"[^\w\-_.]", "_", nome.replace(".pdf", ""))
    return f"Relatorio_{base[:40]}.pdf"
