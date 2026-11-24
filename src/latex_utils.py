import io
import os
import re
from typing import Dict, List, Optional, Tuple

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ---------------------------------------------------------------------------
# Registro de fontes Unicode (DejaVuSans) para suportar símbolos matemáticos
# e letras gregas no ReportLab sem quadrados pretos (tofu).
# ---------------------------------------------------------------------------

_FONTES_REGISTRADAS: Optional[Tuple[str, str, str, str]] = None


def _encontrar_dir_dejavu() -> Optional[str]:
    """Localiza o diretório contendo DejaVuSans.ttf (via matplotlib ou sistema)."""
    candidatos: List[str] = []

    try:
        import matplotlib

        candidatos.append(os.path.join(matplotlib.get_data_path(), "fonts", "ttf"))
    except Exception:
        pass

    candidatos.extend([
        "/usr/share/fonts/truetype/dejavu",
        "/usr/share/fonts/dejavu",
        "/Library/Fonts",
        os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts"),
    ])

    for pasta in candidatos:
        if pasta and os.path.isfile(os.path.join(pasta, "DejaVuSans.ttf")):
            return pasta
    return None


def registrar_fontes_unicode() -> Tuple[str, str, str, str]:
    """
    Registra a família DejaVuSans (Regular, Bold, Oblique, BoldOblique) e DejaVuSansMono
    no ReportLab. Retorna (regular, bold, italic, mono).
    Faz fallback gracioso para Helvetica/Courier caso as TTFs não estejam disponíveis.
    """
    global _FONTES_REGISTRADAS
    if _FONTES_REGISTRADAS is not None:
        return _FONTES_REGISTRADAS

    pasta = _encontrar_dir_dejavu()
    if not pasta:
        _FONTES_REGISTRADAS = ("Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Courier")
        return _FONTES_REGISTRADAS

    arquivos = {
        "DejaVuSans": "DejaVuSans.ttf",
        "DejaVuSans-Bold": "DejaVuSans-Bold.ttf",
        "DejaVuSans-Oblique": "DejaVuSans-Oblique.ttf",
        "DejaVuSans-BoldOblique": "DejaVuSans-BoldOblique.ttf",
        "DejaVuSansMono": "DejaVuSansMono.ttf",
    }

    try:
        registradas = set(pdfmetrics.getRegisteredFontNames())
        for nome, arq in arquivos.items():
            caminho = os.path.join(pasta, arq)
            if os.path.isfile(caminho) and nome not in registradas:
                pdfmetrics.registerFont(TTFont(nome, caminho))

        registradas = set(pdfmetrics.getRegisteredFontNames())
        regular = "DejaVuSans" if "DejaVuSans" in registradas else "Helvetica"
        bold = "DejaVuSans-Bold" if "DejaVuSans-Bold" in registradas else regular
        italic = "DejaVuSans-Oblique" if "DejaVuSans-Oblique" in registradas else regular
        bold_italic = "DejaVuSans-BoldOblique" if "DejaVuSans-BoldOblique" in registradas else bold
        mono = "DejaVuSansMono" if "DejaVuSansMono" in registradas else "Courier"

        if regular == "DejaVuSans":
            pdfmetrics.registerFontFamily(
                "DejaVuSans",
                normal=regular,
                bold=bold,
                italic=italic,
                boldItalic=bold_italic,
            )

        _FONTES_REGISTRADAS = (regular, bold, italic, mono)
        return _FONTES_REGISTRADAS
    except Exception:
        _FONTES_REGISTRADAS = ("Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Courier")
        return _FONTES_REGISTRADAS


# ---------------------------------------------------------------------------
# Dicionários de conversão LaTeX -> Unicode
# ---------------------------------------------------------------------------

LATEX_SIMBOLOS: Dict[str, str] = {
    # Letras gregas minúsculas
    "alpha": "α",
    "beta": "β",
    "gamma": "γ",
    "delta": "δ",
    "epsilon": "ε",
    "varepsilon": "ε",
    "zeta": "ζ",
    "eta": "η",
    "theta": "θ",
    "vartheta": "ϑ",
    "iota": "ι",
    "kappa": "κ",
    "lambda": "λ",
    "mu": "μ",
    "nu": "ν",
    "xi": "ξ",
    "pi": "π",
    "varpi": "ϖ",
    "rho": "ρ",
    "varrho": "ϱ",
    "sigma": "σ",
    "varsigma": "ς",
    "tau": "τ",
    "upsilon": "υ",
    "phi": "φ",
    "varphi": "φ",
    "chi": "χ",
    "psi": "ψ",
    "omega": "ω",
    # Letras gregas maiúsculas
    "Gamma": "Γ",
    "Delta": "Δ",
    "Theta": "Θ",
    "Lambda": "Λ",
    "Xi": "Ξ",
    "Pi": "Π",
    "Sigma": "Σ",
    "Upsilon": "Υ",
    "Phi": "Φ",
    "Psi": "Ψ",
    "Omega": "Ω",
    # Operadores e relações
    "pm": "±",
    "mp": "∓",
    "times": "×",
    "div": "÷",
    "cdot": "·",
    "cdots": "⋯",
    "ldots": "…",
    "dots": "…",
    "vdots": "⋮",
    "ddots": "⋱",
    "ast": "∗",
    "star": "⋆",
    "circ": "∘",
    "bullet": "•",
    "oplus": "⊕",
    "otimes": "⊗",
    "odot": "⊙",
    "leq": "≤",
    "le": "≤",
    "leqslant": "≤",
    "geq": "≥",
    "ge": "≥",
    "geqslant": "≥",
    "neq": "≠",
    "ne": "≠",
    "approx": "≈",
    "equiv": "≡",
    "sim": "∼",
    "simeq": "≃",
    "cong": "≅",
    "propto": "∝",
    "ll": "≪",
    "gg": "≫",
    "asymp": "≍",
    "doteq": "≐",
    # Conjuntos e lógica
    "in": "∈",
    "notin": "∉",
    "ni": "∋",
    "subset": "⊂",
    "subseteq": "⊆",
    "supset": "⊃",
    "supseteq": "⊇",
    "cup": "∪",
    "cap": "∩",
    "bigcup": "⋃",
    "bigcap": "⋂",
    "emptyset": "∅",
    "varnothing": "∅",
    "setminus": "∖",
    "forall": "∀",
    "exists": "∃",
    "nexists": "∄",
    "neg": "¬",
    "lnot": "¬",
    "land": "∧",
    "wedge": "∧",
    "lor": "∨",
    "vee": "∨",
    "top": "⊤",
    "bot": "⊥",
    "perp": "⊥",
    "parallel": "∥",
    "vdash": "⊢",
    "models": "⊨",
    # Setas
    "to": "→",
    "rightarrow": "→",
    "longrightarrow": "→",
    "leftarrow": "←",
    "longleftarrow": "←",
    "leftrightarrow": "↔",
    "longleftrightarrow": "↔",
    "Rightarrow": "⇒",
    "Longrightarrow": "⇒",
    "implies": "⇒",
    "Leftarrow": "⇐",
    "Longleftarrow": "⇐",
    "Leftrightarrow": "⇔",
    "Longleftrightarrow": "⇔",
    "iff": "⇔",
    "mapsto": "↦",
    "uparrow": "↑",
    "downarrow": "↓",
    "updownarrow": "↕",
    # Cálculo e símbolos especiais
    "infty": "∞",
    "partial": "∂",
    "nabla": "∇",
    "sum": "∑",
    "prod": "∏",
    "coprod": "∐",
    "int": "∫",
    "iint": "∬",
    "iiint": "∭",
    "oint": "∮",
    "prime": "′",
    "degree": "°",
    "angle": "∠",
    "triangle": "△",
    "square": "□",
    "diamond": "◇",
    "dagger": "†",
    "ddagger": "‡",
    "ell": "ℓ",
    "hbar": "ℏ",
    "Re": "ℜ",
    "Im": "ℑ",
    "aleph": "ℵ",
    "wp": "℘",
    "langle": "⟨",
    "rangle": "⟩",
    "lfloor": "⌊",
    "rfloor": "⌋",
    "lceil": "⌈",
    "rceil": "⌉",
    "mid": "|",
    "Vert": "‖",
    "vert": "|",
    "backslash": "\\",
    # Espaçamento
    "quad": " ",
    "qquad": "  ",
    "enspace": " ",
    "thinspace": " ",
    "medspace": " ",
    "thickspace": " ",
}

LATEX_FUNCOES = {
    "sin", "cos", "tan", "cot", "sec", "csc",
    "arcsin", "arccos", "arctan", "sinh", "cosh", "tanh", "coth",
    "exp", "log", "ln", "lg",
    "lim", "limsup", "liminf", "sup", "inf", "max", "min",
    "arg", "argmax", "argmin", "det", "dim", "ker", "deg", "gcd",
    "hom", "Pr", "mod", "bmod", "pmod", "Var", "Cov", "diag", "rank", "tr",
}

BLACKBOARD_BOLD: Dict[str, str] = {
    "R": "ℝ",
    "N": "ℕ",
    "Z": "ℤ",
    "Q": "ℚ",
    "C": "ℂ",
    "E": "𝔼",
    "P": "ℙ",
    "H": "ℍ",
    "F": "𝔽",
    "I": "𝕀",
    "K": "𝕂",
    "1": "𝟙",
}

VULGAR_FRACTIONS: Dict[Tuple[str, str], str] = {
    ("1", "2"): "½",
    ("1", "3"): "⅓",
    ("2", "3"): "⅔",
    ("1", "4"): "¼",
    ("3", "4"): "¾",
}


# ---------------------------------------------------------------------------
# Utilitários de parsing de chaves/argumentos LaTeX
# ---------------------------------------------------------------------------

def _escapar_xml(texto: str) -> str:
    return texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _extrair_grupo(s: str, idx: int) -> Tuple[str, int]:
    """
    Extrai um argumento LaTeX a partir de `idx`:
    - Se começa com `{`, retorna o conteúdo até a `}` correspondente (com aninhamento).
    - Se começa com `\\`, retorna o comando `\\nome`.
    - Caso contrário, retorna um único caractere.
    """
    n = len(s)
    while idx < n and s[idx] == " ":
        idx += 1
    if idx >= n:
        return "", idx

    if s[idx] == "{":
        depth = 0
        start = idx + 1
        i = idx
        while i < n:
            ch = s[i]
            if ch == "\\" and i + 1 < n:
                i += 2
                continue
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return s[start:i], i + 1
            i += 1
        return s[start:], n

    if s[idx] == "\\":
        m = re.match(r"\\[A-Za-z]+|\\.", s[idx:])
        if m:
            return m.group(0), idx + len(m.group(0))

    return s[idx], idx + 1


def _substituir_comando_2args(s: str, comandos: Tuple[str, ...], fn) -> str:
    """Substitui comandos de 2 argumentos (ex.: \\frac{a}{b}, \\binom{n}{k})."""
    pattern = re.compile(r"\\(?:" + "|".join(comandos) + r")(?![A-Za-z])")
    out: List[str] = []
    pos = 0
    while True:
        m = pattern.search(s, pos)
        if not m:
            out.append(s[pos:])
            break
        out.append(s[pos:m.start()])
        arg1, next_pos = _extrair_grupo(s, m.end())
        arg2, next_pos = _extrair_grupo(s, next_pos)
        out.append(fn(arg1, arg2))
        pos = next_pos
    return "".join(out)


def _substituir_comando_1arg(s: str, comandos: Tuple[str, ...], fn) -> str:
    """Substitui comandos de 1 argumento (ex.: \\text{...}, \\mathbf{...})."""
    pattern = re.compile(r"\\(?:" + "|".join(comandos) + r")(?![A-Za-z])")
    out: List[str] = []
    pos = 0
    while True:
        m = pattern.search(s, pos)
        if not m:
            out.append(s[pos:])
            break
        out.append(s[pos:m.start()])
        arg, next_pos = _extrair_grupo(s, m.end())
        out.append(fn(arg))
        pos = next_pos
    return "".join(out)


def _substituir_sqrt(s: str) -> str:
    """Converte \\sqrt[n]{x} e \\sqrt{x}."""
    pattern = re.compile(r"\\sqrt(?![A-Za-z])")
    out: List[str] = []
    pos = 0
    while True:
        m = pattern.search(s, pos)
        if not m:
            out.append(s[pos:])
            break
        out.append(s[pos:m.start()])
        i = m.end()
        while i < len(s) and s[i] == " ":
            i += 1
        indice = ""
        if i < len(s) and s[i] == "[":
            fim_colchete = s.find("]", i + 1)
            if fim_colchete != -1:
                indice = s[i + 1:fim_colchete].strip()
                i = fim_colchete + 1
        radicando, next_pos = _extrair_grupo(s, i)
        rad_conv = _converter_latex_interno(radicando)
        prefixo = f"\x01SUP\x02{_converter_latex_interno(indice)}\x01/SUP\x02" if indice else ""
        rad_limpo = re.sub(r"\x01/?[A-Z]+\x02", "", rad_conv)
        if len(rad_limpo) <= 1:
            out.append(f"{prefixo}√{rad_conv}")
        else:
            out.append(f"{prefixo}√({rad_conv})")
        pos = next_pos
    return "".join(out)


def _converter_latex_interno(expr: str) -> str:
    """
    Converte uma expressão LaTeX em texto Unicode com marcadores internos de tag
    (\\x01TAG\\x02...\\x01/TAG\\x02) que só viram XML no final, evitando conflito
    com escape de `<`, `>` e `&`.
    """
    if not expr:
        return ""

    s = expr.strip()

    # Remover delimitadores de tamanho e modificadores de exibição
    s = re.sub(
        r"\\(?:left|right|bigl|bigr|big|Bigl|Bigr|Big|biggl|biggr|bigg|Biggl|Biggr|Bigg|"
        r"displaystyle|textstyle|scriptstyle|scriptscriptstyle|limits|nolimits)(?![A-Za-z])",
        "",
        s,
    )

    # Remover ambientes simples (ex.: \begin{aligned}...\end{aligned})
    s = re.sub(r"\\begin\{[^}]+\}", "", s)
    s = re.sub(r"\\end\{[^}]+\}", "", s)
    s = s.replace("\\\\", "; ")

    # Frações: \frac, \dfrac, \tfrac, \cfrac
    def _fmt_frac(a: str, b: str) -> str:
        ca = _converter_latex_interno(a).strip()
        cb = _converter_latex_interno(b).strip()
        a_plain = re.sub(r"\x01/?[A-Z]+\x02", "", ca)
        b_plain = re.sub(r"\x01/?[A-Z]+\x02", "", cb)
        if (a_plain, b_plain) in VULGAR_FRACTIONS:
            return VULGAR_FRACTIONS[(a_plain, b_plain)]
        precisa_par_a = any(op in a_plain for op in ("+", "-", " ", "="))
        precisa_par_b = any(op in b_plain for op in ("+", "-", " ", "=", "/"))
        fa = f"({ca})" if precisa_par_a else ca
        fb = f"({cb})" if precisa_par_b else cb
        return f"{fa}/{fb}"

    s = _substituir_comando_2args(s, ("frac", "dfrac", "tfrac", "cfrac"), _fmt_frac)
    s = _substituir_comando_2args(
        s,
        ("binom", "dbinom", "tbinom"),
        lambda a, b: f"C({_converter_latex_interno(a)}, {_converter_latex_interno(b)})",
    )

    # Raízes
    s = _substituir_sqrt(s)

    # Comandos de estilo / texto com 1 argumento
    s = _substituir_comando_1arg(
        s,
        ("text", "textrm", "mathrm", "operatorname", "mbox", "hbox", "mathsf", "texttt", "rm"),
        lambda a: _converter_latex_interno(a),
    )
    s = _substituir_comando_1arg(
        s,
        ("mathbf", "textbf", "boldsymbol", "bm", "bf"),
        lambda a: f"\x01B\x02{_converter_latex_interno(a)}\x01/B\x02",
    )
    s = _substituir_comando_1arg(
        s,
        ("mathit", "textit", "emph", "mathcal", "mathscr", "mathfrak"),
        lambda a: f"\x01I\x02{_converter_latex_interno(a)}\x01/I\x02",
    )
    s = _substituir_comando_1arg(
        s,
        ("mathbb",),
        lambda a: "".join(BLACKBOARD_BOLD.get(ch, ch) for ch in a.strip()),
    )
    s = _substituir_comando_1arg(
        s,
        ("overline", "bar"),
        lambda a: f"{_converter_latex_interno(a)}\u0304" if len(a.strip()) == 1 else f"média({_converter_latex_interno(a)})",
    )
    s = _substituir_comando_1arg(
        s,
        ("hat", "widehat"),
        lambda a: f"{_converter_latex_interno(a)}\u0302" if len(a.strip()) == 1 else f"{_converter_latex_interno(a)}^",
    )
    s = _substituir_comando_1arg(
        s,
        ("tilde", "widetilde"),
        lambda a: f"{_converter_latex_interno(a)}\u0303" if len(a.strip()) == 1 else f"~{_converter_latex_interno(a)}",
    )
    s = _substituir_comando_1arg(
        s,
        ("vec",),
        lambda a: f"\x01B\x02{_converter_latex_interno(a)}\x01/B\x02",
    )
    s = _substituir_comando_1arg(
        s,
        ("dot",),
        lambda a: f"{_converter_latex_interno(a)}\u0307" if len(a.strip()) == 1 else _converter_latex_interno(a),
    )

    # Símbolos escapados com barra invertida: \%, \_, \&, \#, \$, \{, \}, \|, \, \; \: \! \ 
    s = re.sub(r"\\([%&_#$\{\}])", r"\1", s)
    s = s.replace("\\|", "‖")
    s = re.sub(r"\\[,;: ]", " ", s)
    s = s.replace("\\!", "")

    # Substituir comandos \nome (símbolos e funções conhecidas)
    def _sub_cmd(match: re.Match) -> str:
        cmd = match.group(1)
        if cmd in LATEX_SIMBOLOS:
            return LATEX_SIMBOLOS[cmd]
        if cmd in LATEX_FUNCOES:
            return cmd
        # Comando desconhecido: remove a barra para não poluir o texto
        return cmd

    s = re.sub(r"\\([A-Za-z]+)", _sub_cmd, s)

    # Sobrescritos (^) e subscritos (_)
    out: List[str] = []
    i = 0
    n = len(s)
    while i < n:
        ch = s[i]
        if ch in ("^", "_"):
            tag = "SUP" if ch == "^" else "SUB"
            arg, next_i = _extrair_grupo(s, i + 1)
            if arg:
                conv = _converter_latex_interno(arg)
                # Sinal de menos tipográfico em expoentes (ex.: 10^-3 -> 10⁻³)
                conv = conv.replace("-", "−")
                out.append(f"\x01{tag}\x02{conv}\x01/{tag}\x02")
                i = next_i
                continue
        out.append(ch)
        i += 1
    s = "".join(out)

    # Remover chaves de agrupamento residuais
    s = s.replace("{", "").replace("}", "")

    # Normalizar espaços extras
    s = re.sub(r"[ \t]{2,}", " ", s).strip()
    return s


def latex_inline_para_xml(expr: str) -> str:
    """Converte uma expressão LaTeX inline para XML válido de Paragraph do ReportLab."""
    interno = _converter_latex_interno(expr)
    escapado = _escapar_xml(interno)
    # Restaura os marcadores internos como tags XML válidas do ReportLab
    escapado = (
        escapado.replace("\x01B\x02", "<b>")
        .replace("\x01/B\x02", "</b>")
        .replace("\x01I\x02", "<i>")
        .replace("\x01/I\x02", "</i>")
        .replace("\x01SUP\x02", "<sup>")
        .replace("\x01/SUP\x02", "</sup>")
        .replace("\x01SUB\x02", "<sub>")
        .replace("\x01/SUB\x02", "</sub>")
    )
    return escapado


# ---------------------------------------------------------------------------
# Renderização de equações em bloco ($$...$$ e \[...\]) via matplotlib.mathtext
# ---------------------------------------------------------------------------

def _preparar_latex_para_matplotlib(expr: str) -> str:
    """Normaliza comandos LaTeX comuns para o parser mathtext do matplotlib."""
    s = expr.strip()
    # matplotlib.mathtext usa \mathrm em vez de \text / \mbox
    s = re.sub(r"\\(?:text|textrm|mbox|operatorname)\{", r"\\mathrm{", s)
    s = re.sub(r"\\textbf\{", r"\\mathbf{", s)
    s = re.sub(r"\\textit\{", r"\\mathit{", s)
    s = re.sub(r"\\(?:displaystyle|textstyle|limits|nolimits)(?![A-Za-z])", "", s)
    s = s.replace("\\implies", "\\Rightarrow").replace("\\iff", "\\Leftrightarrow")
    s = s.replace("\\leqslant", "\\leq").replace("\\geqslant", "\\geq")
    s = s.replace("\\varepsilon", "\\epsilon").replace("\\varphi", "\\phi")
    return s


def renderizar_equacao_png(
    latex_expr: str,
    max_width_pt: float,
    fontsize: float = 11.5,
    dpi: int = 240,
    cor_texto: str = "#0F172A",
) -> Optional[Tuple[bytes, float, float]]:
    """
    Renderiza uma equação LaTeX em bloco para PNG transparente usando matplotlib.mathtext.
    Retorna (png_bytes, largura_pt, altura_pt) ajustados a `max_width_pt`, ou None em caso
    de falha (para fallback automático em texto Unicode).
    """
    try:
        from matplotlib.backends.backend_agg import FigureCanvasAgg
        from matplotlib.figure import Figure
    except Exception:
        return None

    expr_prep = _preparar_latex_para_matplotlib(latex_expr)
    # Se contiver ambientes complexos não suportados pelo mathtext, vai direto ao fallback
    if "\\begin{" in expr_prep or "\\\\" in expr_prep:
        return None

    try:
        fig = Figure(figsize=(0.1, 0.1), dpi=dpi)
        canvas = FigureCanvasAgg(fig)
        fig.patch.set_alpha(0.0)
        text_obj = fig.text(
            0.0,
            0.0,
            f"${expr_prep}$",
            fontsize=fontsize,
            color=cor_texto,
            ha="left",
            va="bottom",
            usetex=False,
        )
        canvas.draw()
        renderer = canvas.get_renderer()
        bbox = text_obj.get_window_extent(renderer=renderer)
        if bbox.width <= 1 or bbox.height <= 1:
            return None

        pad_px = 8.0
        w_in = (bbox.width + 2 * pad_px) / dpi
        h_in = (bbox.height + 2 * pad_px) / dpi
        fig.set_size_inches(w_in, h_in)
        text_obj.set_position((pad_px / (bbox.width + 2 * pad_px), pad_px / (bbox.height + 2 * pad_px)))
        canvas.draw()

        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=dpi, transparent=True)
        png_bytes = buf.getvalue()
        buf.close()

        # Converte dimensões de polegadas para pontos PDF (1 in = 72 pt)
        w_pt = w_in * 72.0
        h_pt = h_in * 72.0

        # Limita à largura útil do container/página preservando proporção
        if w_pt > max_width_pt:
            escala = max_width_pt / w_pt
            w_pt *= escala
            h_pt *= escala

        return png_bytes, float(w_pt), float(h_pt)
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Separação de blocos (texto vs display math) e formatação inline completa
# ---------------------------------------------------------------------------

_DISPLAY_MATH_RE = re.compile(
    r"(?<!\\)\$\$(.+?)(?<!\\)\$\$|\\\[(.+?)\\\]",
    re.DOTALL,
)

# Inline math: $...$ (não $$) ou \(...\)
_INLINE_MATH_RE = re.compile(
    r"(?<!\\)\$(?!\$)(?=\S)([^$\n]+?)(?<=\S)(?<!\\)\$|\\\((.+?)\\\)",
)

# Comandos LaTeX comuns soltos fora de $...$
_STRAY_LATEX_CMD_RE = re.compile(
    r"\\(" + "|".join(sorted(LATEX_SIMBOLOS.keys(), key=len, reverse=True)) + r")(?![A-Za-z])"
)


def _parece_moeda(texto: str, start: int, conteudo: str) -> bool:
    """Evita confundir valores monetários (ex.: R$ 100 e R$ 200) com math inline."""
    if start > 0 and texto[start - 1] in ("R", "r", "S", "s"):
        # Ex.: "R$ 100 ... R$ 200" -> conteúdo começa com espaço ou dígito seguido de texto
        if re.match(r"^\s*\d", conteudo):
            return True
    # Se começa com dígitos e tem palavras comuns de prosa sem operadores/comandos LaTeX
    if re.match(r"^\d[\d.,]*\s+[A-Za-zÀ-ÿ]{3,}", conteudo) and "\\" not in conteudo and "^" not in conteudo and "_" not in conteudo:
        return True
    return False


def separar_segmentos_display(texto: str) -> List[Tuple[str, str]]:
    """
    Separa um bloco de texto em segmentos ordenados:
      - ("text", trecho_de_texto)
      - ("display_math", expressao_latex)
    """
    if not texto:
        return []

    segmentos: List[Tuple[str, str]] = []
    pos = 0
    for m in _DISPLAY_MATH_RE.finditer(texto):
        antes = texto[pos:m.start()].strip()
        if antes:
            segmentos.append(("text", antes))
        expr = (m.group(1) if m.group(1) is not None else m.group(2)).strip()
        if expr:
            segmentos.append(("display_math", expr))
        pos = m.end()

    depois = texto[pos:].strip()
    if depois:
        segmentos.append(("text", depois))

    return segmentos or [("text", texto)]


def formatar_texto_para_pdf(texto: str, font_mono: str = "DejaVuSansMono") -> str:
    """
    Converte texto científico contendo Markdown leve e LaTeX inline ($...$, \\(...\\),
    e comandos soltos) em XML seguro e limpo para ReportLab Paragraph.
    """
    if not texto:
        return ""

    # 1. Captura expressões matemáticas inline e substitui por placeholders seguros
    math_placeholders: List[str] = []

    def _capturar_math(m: re.Match) -> str:
        if m.group(1) is not None:
            conteudo = m.group(1)
            if _parece_moeda(texto, m.start(), conteudo):
                return m.group(0)
        else:
            conteudo = m.group(2)
        idx = len(math_placeholders)
        math_placeholders.append(latex_inline_para_xml(conteudo))
        return f"\x00MATH{idx}\x00"

    t = _INLINE_MATH_RE.sub(_capturar_math, texto)

    # 2. Captura trechos de código inline `...` antes do escape
    code_placeholders: List[str] = []

    def _capturar_code(m: re.Match) -> str:
        idx = len(code_placeholders)
        code_xml = f'<font name="{font_mono}" size="8.4">{_escapar_xml(m.group(1))}</font>'
        code_placeholders.append(code_xml)
        return f"\x00CODE{idx}\x00"

    t = re.sub(r"`([^`\n]+?)`", _capturar_code, t)

    # 3. Limpa comandos LaTeX soltos fora de $...$ (ex.: \alpha, \leq, \%, \textbf{...})
    t = _substituir_comando_1arg(t, ("textbf", "mathbf"), lambda a: f"**{a}**")
    t = _substituir_comando_1arg(t, ("textit", "emph", "mathit"), lambda a: f"*{a}*")
    t = _STRAY_LATEX_CMD_RE.sub(lambda m: LATEX_SIMBOLOS[m.group(1)], t)
    t = re.sub(r"\\([%&_#$])", r"\1", t)

    # 4. Escapa XML do texto normal
    t = _escapar_xml(t)

    # 5. Converte Markdown leve: **negrito**, *itálico* e bullets no início da linha
    t = re.sub(r"\*\*([^*\n]+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<!\*)\*(?!\s)([^*\n]+?)(?<!\s)\*(?!\*)", r"<i>\1</i>", t)
    t = re.sub(r"(?m)^[ \t]*[-*]\s+", "• ", t)
    t = t.replace("\n", "<br/>")

    # 6. Restaura placeholders de código e matemática
    for idx, code_xml in enumerate(code_placeholders):
        t = t.replace(f"\x00CODE{idx}\x00", code_xml)
    for idx, math_xml in enumerate(math_placeholders):
        t = t.replace(f"\x00MATH{idx}\x00", math_xml)

    return t
