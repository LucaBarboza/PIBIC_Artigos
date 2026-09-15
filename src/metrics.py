import io
from typing import Dict, Any, Optional
from pypdf import PdfReader


def estimar_tempo_leitura(pdf_bytes: Optional[bytes], densidade: str = "media") -> Dict[str, Any]:
    """
    Calcula de forma híbrida e transparente o tempo de leitura acadêmica economizado.

    Taxas de leitura crítica acadêmica por densidade técnica:
    - 'alta': 130 PPM (pesada em formulações matemáticas, equações, modelos estatísticos avançados, algoritmos)
    - 'media': 180 PPM (estudo empírico/experimental padrão com dados e gráficos)
    - 'baixa': 220 PPM (ensaios, revisões narrativas, ciências sociais com prosa fluida)
    """
    ppm_map = {
        "alta": 130,
        "media": 180,
        "baixa": 220,
    }
    densidade_normalizada = (densidade or "media").lower().strip()
    if densidade_normalizada not in ppm_map:
        densidade_normalizada = "media"

    ppm = ppm_map[densidade_normalizada]

    num_paginas = 0
    total_palavras = 0
    eh_escaneado = False

    if pdf_bytes:
        try:
            reader = PdfReader(io.BytesIO(pdf_bytes))
            num_paginas = len(reader.pages)
            texto_extraido = "".join([page.extract_text() or "" for page in reader.pages])
            palavras = texto_extraido.split()
            total_palavras = len(palavras)

            # Se tiver menos de 300 palavras no total mas tiver páginas, é imagem/escaneado
            if total_palavras < 300 and num_paginas > 0:
                eh_escaneado = True
                # Média acadêmica consagrada de 500 palavras por página
                total_palavras = num_paginas * 500
        except Exception:
            num_paginas = 1
            total_palavras = 4000
    else:
        num_paginas = 1
        total_palavras = 4000

    # Tempo de leitura direta pelo pesquisador
    tempo_leitura = total_palavras / ppm

    # Tempo estimado de fichamento/anotação crítica estruturada (~1.5 min por página, mínimo 10 min)
    tempo_fichamento = max(10, round(num_paginas * 1.5))

    tempo_total = max(15, round(tempo_leitura + tempo_fichamento))

    return {
        "tempo_minutos": tempo_total,
        "total_palavras": total_palavras,
        "num_paginas": num_paginas,
        "ppm": ppm,
        "densidade": densidade_normalizada,
        "eh_escaneado": eh_escaneado,
    }
