from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, HRFlowable, Image as RLImage
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from datetime import datetime
from io import BytesIO
import plotly.io as pio
import os
import re


def register_fonts():
    font_paths = [
        os.path.join(os.path.dirname(__file__), "fonts", "NanumGothic.ttf"),
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "./fonts/NanumGothic.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(TTFont("Korean", path))
                return "Korean"
            except Exception:
                continue
    return "Helvetica"


C_NAVY         = colors.HexColor("#1B3A5C")
C_BLUE         = colors.HexColor("#2E6DA4")
C_BLUE_MID     = colors.HexColor("#5B9BD5")
C_PASTEL_BLUE  = colors.HexColor("#BDD7EE")
C_LIGHT_BLUE   = colors.HexColor("#DEEAF1")
C_LIGHTEST     = colors.HexColor("#F0F6FB")
C_WHITE        = colors.white
C_TEXT_DARK    = colors.HexColor("#1A2B3C")
C_TEXT_GRAY    = colors.HexColor("#7A9BB5")
C_BORDER       = colors.HexColor("#C5D8E8")
C_GOOD_BG      = colors.HexColor("#E8F5E9")
C_GOOD_TEXT    = colors.HexColor("#2E7D32")
C_WARN_BG      = colors.HexColor("#FFF8E1")
C_WARN_TEXT    = colors.HexColor("#F57F17")
C_BAD_BG       = colors.HexColor("#FFEBEE")
C_BAD_TEXT     = colors.HexColor("#C62828")
C_CAUTION_BG   = colors.HexColor("#E3F2FD")
C_CAUTION_TEXT = colors.HexColor("#1565C0")


def get_styles(fn):
    s = getSampleStyleSheet()
    s.add(ParagraphStyle(
        name="NormalKo",
        fontName=fn, fontSize=8.5,
        textColor=C_TEXT_DARK,
        leading=13, spaceAfter=2,
    ))
    s.add(ParagraphStyle(
        name="Disclaimer",
        fontName=fn, fontSize=7,
        textColor=C_TEXT_GRAY,
        leading=10, spaceAfter=2,
    ))
    s.add(ParagraphStyle(
        name="AIBody",
        fontName=fn, fontSize=8.5,
        textColor=C_TEXT_DARK,
        leading=14, spaceAfter=3,
    ))
    s.add(ParagraphStyle(
        name="AIHead",
        fontName=fn, fontSize=10,
        textColor=C_NAVY,
        leading=15, spaceAfter=3,
        spaceBefore=6,
    ))
    return s


def fig_to_image(fig, width=500, height=350):
    try:
        img_bytes = pio.to_image(
            fig, format="png", width=width, height=height, scale=2
        )
        return BytesIO(img_bytes)
    except Exception:
        return None


def section_title(txt, fn):
    data = [[
        Paragraph(
            "<b>" + txt + "</b>",
            ParagraphStyle(
                name="st", fontName=fn, fontSize=12,
                textColor=C_NAVY, leading=16,
            )
        )
    ]]
    t = Table(data, colWidths=[184 * mm])
    t.setStyle(TableStyle([
        ("LINEBELOW",     (0, 0), (-1, -1), 2,   C_BLUE),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 2),
        ("BACKGROUND",    (0, 0), (-1, -1), C_LIGHTEST),
    ]))
    return t
def build_header(params, selected_seq, lang, fn, now):
    ko_basic = params.get("기본 정보", {})

    if lang == "ko":
        title_sub    = "파라미터 분석 리포트"
        lbl_seq      = "시퀀스"
        lbl_mfr      = "제조사"
        lbl_field    = "자장강도"
        lbl_protocol = "프로토콜"
        lbl_date     = "분석일시"
        lbl_coil     = "수신코일"
    else:
        title_sub    = "Parameter Analysis Report"
        lbl_seq      = "SEQUENCE"
        lbl_mfr      = "MANUFACTURER"
        lbl_field    = "FIELD"
        lbl_protocol = "PROTOCOL"
        lbl_date     = "DATE"
        lbl_coil     = "COIL"

    mfr      = ko_basic.get("제조사", "N/A")
    field    = ko_basic.get("자장강도(T)", "N/A")
    protocol = ko_basic.get("프로토콜명", "N/A")
    coil     = ko_basic.get("수신코일", "N/A")

    def lbl(txt):
        return Paragraph(txt, ParagraphStyle(
            name="hl", fontName=fn, fontSize=7,
            textColor=C_PASTEL_BLUE, leading=10,
        ))

    def val(txt):
        return Paragraph(str(txt), ParagraphStyle(
            name="hv", fontName=fn, fontSize=9,
            textColor=C_WHITE, leading=13,
        ))

    info_row = [
        [lbl(lbl_seq),      lbl(lbl_mfr), lbl(lbl_field),
         lbl(lbl_protocol), lbl(lbl_coil), lbl(lbl_date)],
        [val(selected_seq), val(mfr),      val(str(field) + " T"),
         val(protocol),     val(coil),     val(now)],
    ]

    info_table = Table(
        info_row,
        colWidths=[32*mm, 35*mm, 24*mm, 38*mm, 26*mm, 29*mm]
    )
    info_table.setStyle(TableStyle([
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 4),
        ("TOPPADDING",    (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ]))

    header_data = [
        [Paragraph(
            "<b>MRI DICOM</b>  " + title_sub,
            ParagraphStyle(
                name="ht", fontName=fn, fontSize=20,
                textColor=C_WHITE, leading=26,
            )
        )],
        [info_table],
    ]

    header_table = Table(header_data, colWidths=[184 * mm])
    header_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), C_NAVY),
        ("TOPPADDING",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
        ("LINEBELOW",     (0, 0), (-1, 0),  1, C_BLUE_MID),
    ]))
    return header_table


def build_info_cards(params, lang, fn):
    ko_seq   = params.get("시퀀스 파라미터", {})
    ko_space = params.get("공간 해상도", {})

    items = [
        ("TR",         ko_seq.get("TR (ms)", "N/A"),                   "ms"),
        ("TE",         ko_seq.get("TE (ms)", "N/A"),                   "ms"),
        ("TI",         ko_seq.get("TI (ms)", "N/A"),                   "ms"),
        ("Flip Angle", ko_seq.get("Flip Angle (°)", "N/A"),            "deg"),
        ("ETL",        ko_seq.get("ETL", "N/A"),                       ""),
        ("NEX / NSA",  ko_seq.get("NEX/NSA", "N/A"),                   ""),
        ("Slice",      ko_space.get("Slice Thickness (mm)", "N/A"),    "mm"),
        ("FOV",        ko_space.get("FOV (mm)", "N/A"),                "mm"),
    ]

    def card(label, value, unit):
        inner = Table([
            [Paragraph(label, ParagraphStyle(
                name="cl", fontName=fn, fontSize=7,
                textColor=C_TEXT_GRAY, leading=10,
            ))],
            [Paragraph("<b>" + str(value) + "</b>", ParagraphStyle(
                name="cv", fontName=fn, fontSize=15,
                textColor=C_NAVY, leading=20,
            ))],
            [Paragraph(unit, ParagraphStyle(
                name="cu", fontName=fn, fontSize=7,
                textColor=C_TEXT_GRAY, leading=10,
            ))],
        ], colWidths=[41 * mm])
        inner.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), C_WHITE),
            ("BOX",           (0, 0), (-1, -1), 0.5, C_BORDER),
            ("TOPPADDING",    (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING",   (0, 0), (-1, -1), 8),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
            ("LINEABOVE",     (0, 0), (-1, 0),  3, C_BLUE),
        ]))
        return inner

    cards = [card(l, v, u) for l, v, u in items]
    row1  = cards[:4]
    row2  = cards[4:]
    while len(row2) < 4:
        row2.append("")

    card_table = Table([row1, row2], colWidths=[44*mm, 44*mm, 44*mm, 44*mm])
    card_table.setStyle(TableStyle([
        ("LEFTPADDING",   (0, 0), (-1, -1), 2),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 2),
        ("TOPPADDING",    (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ]))
    return card_table
def build_comparison_table(df, fn, lang):
    if df is None or df.empty:
        return None

    col_count = len(df.columns)
    if col_count == 8:
        col_widths = [28, 18, 14, 16, 14, 12, 22, 26]
    elif col_count == 7:
        col_widths = [30, 20, 16, 18, 16, 14, 36]
    else:
        w = 150 / col_count
        col_widths = [w] * col_count

    def hdr(txt):
        return Paragraph("<b>" + str(txt) + "</b>", ParagraphStyle(
            name="th", fontName=fn, fontSize=8,
            textColor=C_WHITE, leading=11,
            alignment=TA_CENTER,
        ))

    def cell_c(txt, fc=C_TEXT_DARK):
        return Paragraph(str(txt), ParagraphStyle(
            name="tdc", fontName=fn, fontSize=8,
            textColor=fc, leading=11,
            alignment=TA_CENTER,
        ))

    def cell_l(txt, fc=C_TEXT_DARK):
        return Paragraph(str(txt), ParagraphStyle(
            name="tdl", fontName=fn, fontSize=8,
            textColor=fc, leading=11,
            alignment=TA_LEFT,
        ))

    headers = [hdr(c) for c in df.columns]
    rows    = [headers]

    for _, row in df.iterrows():
        status = str(row.get("상태", row.get("Status", "")))
        if "✅" in status:
            sc = C_GOOD_TEXT
        elif "⚠️" in status:
            sc = C_WARN_TEXT
        elif "❌" in status:
            sc = C_BAD_TEXT
        else:
            sc = C_CAUTION_TEXT

        row_cells = []
        for i, v in enumerate(row):
            txt = str(v)
            if i == len(df.columns) - 1:
                row_cells.append(cell_l(txt, sc))
            elif i in [1, 2, 3, 4]:
                row_cells.append(cell_c(txt))
            else:
                row_cells.append(cell_l(txt))
        rows.append(row_cells)

    t = Table(rows, colWidths=[w * mm for w in col_widths])

    style_cmds = [
        ("BACKGROUND",    (0, 0), (-1, 0),  C_NAVY),
        ("LINEBELOW",     (0, 0), (-1, 0),  2,   C_BLUE),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("GRID",          (0, 0), (-1, -1), 0.3, C_BORDER),
    ]

    for idx, (_, row) in enumerate(df.iterrows()):
        status = str(row.get("상태", row.get("Status", "")))
        if "✅" in status:
            bg = C_GOOD_BG
        elif "⚠️" in status:
            bg = C_WARN_BG
        elif "❌" in status:
            bg = C_BAD_BG
        else:
            bg = C_CAUTION_BG if idx % 2 == 0 else C_LIGHTEST
        style_cmds.append(("BACKGROUND", (0, idx + 1), (-1, idx + 1), bg))

    t.setStyle(TableStyle(style_cmds))
    return t


def parse_ai_markdown_table(table_lines, fn):
    clean = []
    for line in table_lines:
        line = line.strip()
        if re.match(r"^\|[\s\-\|:]+\|$", line):
            continue
        if line.startswith("|") and line.endswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            clean.append(cells)

    if not clean:
        return None

    max_cols  = max(len(r) for r in clean)
    col_w     = 178 / max_cols
    col_widths = [col_w * mm] * max_cols

    def hdr(txt):
        return Paragraph("<b>" + str(txt) + "</b>", ParagraphStyle(
            name="mth", fontName=fn, fontSize=7.5,
            textColor=C_WHITE, leading=11,
            alignment=TA_CENTER,
        ))

    def cell(txt, idx):
        return Paragraph(str(txt), ParagraphStyle(
            name="mtd", fontName=fn, fontSize=7.5,
            textColor=C_TEXT_DARK, leading=11,
            alignment=TA_LEFT if idx == 0 else TA_CENTER,
        ))

    rows = []
    for r_idx, row in enumerate(clean):
        while len(row) < max_cols:
            row.append("")
        if r_idx == 0:
            rows.append([hdr(c) for c in row])
        else:
            rows.append([cell(c, i) for i, c in enumerate(row)])

    t = Table(rows, colWidths=col_widths)

    style_cmds = [
        ("BACKGROUND",    (0, 0), (-1, 0),  C_BLUE),
        ("LINEBELOW",     (0, 0), (-1, 0),  1.5, C_PASTEL_BLUE),
        ("GRID",          (0, 0), (-1, -1), 0.3, C_BORDER),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 4),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 4),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]
    for i in range(1, len(rows)):
        bg = C_LIGHT_BLUE if i % 2 == 0 else C_LIGHTEST
        style_cmds.append(("BACKGROUND", (0, i), (-1, i), bg))

    t.setStyle(TableStyle(style_cmds))
    return t


def build_gauge_grid(gauge_figs, fn):
    if not gauge_figs:
        return None

    gauge_images = []
    for name, fig in gauge_figs[:6]:
        img = fig_to_image(fig, width=280, height=200)
        if img:
            gauge_images.append(RLImage(img, width=54 * mm, height=38 * mm))

    if not gauge_images:
        return None

    rows = []
    for i in range(0, len(gauge_images), 3):
        row = gauge_images[i:i+3]
        while len(row) < 3:
            row.append("")
        rows.append(row)

    t = Table(rows, colWidths=[58 * mm, 58 * mm, 58 * mm])
    t.setStyle(TableStyle([
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING",   (0, 0), (-1, -1), 2),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 2),
        ("TOPPADDING",    (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return t
def build_ai_section(ai_result, fn, styles):
    story_items = []
    lines       = ai_result.split("\n")
    i           = 0

    while i < len(lines):
        line = lines[i].strip()

        if not line:
            story_items.append(Spacer(1, 2 * mm))
            i += 1
            continue

        if line.startswith("|") and line.endswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            tbl = parse_ai_markdown_table(table_lines, fn)
            if tbl:
                story_items.append(Spacer(1, 2 * mm))
                story_items.append(tbl)
                story_items.append(Spacer(1, 2 * mm))
            continue

        line_clean = line.replace("**", "").strip()

        if line_clean.startswith("## "):
            txt = line_clean[3:].strip()
            story_items.append(Paragraph(
                "<b>" + txt + "</b>",
                styles["AIHead"]
            ))
            i += 1
            continue

        if line_clean.startswith("# "):
            txt = line_clean[2:].strip()
            story_items.append(Paragraph(
                "<b>" + txt + "</b>",
                ParagraphStyle(
                    name="aih1", fontName=fn, fontSize=11,
                    textColor=C_NAVY, leading=16,
                    spaceBefore=8, spaceAfter=3,
                )
            ))
            i += 1
            continue

        if line_clean.startswith(("- ", "* ", "+ ")):
            txt = line_clean[2:].strip()
            story_items.append(Paragraph(
                "• " + txt,
                ParagraphStyle(
                    name="bull", fontName=fn, fontSize=8.5,
                    textColor=C_TEXT_DARK, leading=13,
                    leftIndent=8, spaceAfter=2,
                )
            ))
            i += 1
            continue

        story_items.append(Paragraph(line_clean, styles["AIBody"]))
        i += 1

    return story_items


def generate_pdf_report(params, user_baseline, df, radar_fig, gauge_figs,
                        ai_result, selected_seq, lang="ko"):
    fn     = register_fonts()
    styles = get_styles(fn)
    buffer = BytesIO()
    now    = datetime.now().strftime("%Y-%m-%d %H:%M")

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=12 * mm,
        leftMargin=12 * mm,
        topMargin=10 * mm,
        bottomMargin=12 * mm,
    )

    story = []

    if lang == "ko":
        sec1 = "📊  기본 파라미터"
        sec2 = "📋  파라미터 비교 분석"
        sec3 = "🎯  파라미터 적합도 & 레이더 차트"
        sec4 = "🤖  AI 분석 결과"
        disclaimer_lines = [
            "📚  파라미터 기준값 출처 : ACR · ISMRM · ESUR · RSNA 가이드라인, "
            "GE/Siemens/Philips 공식 매뉴얼, 국내외 대학병원 임상 프로토콜, "
            "Radiology · JMRI · MRM 등 peer-reviewed 논문",
            "⚠️  본 리포트는 보조적 참고용이며, 최종 판단은 전문 방사선사 및 영상의학과 전문의가 해야 합니다.",
            "⚠️  AI 분석 결과는 Groq LLaMA 모델 기반이며, 의료적 진단을 대체하지 않습니다.",
        ]
    else:
        sec1 = "📊  Basic Parameters"
        sec2 = "📋  Parameter Comparison"
        sec3 = "🎯  Parameter Fitness & Radar Chart"
        sec4 = "🤖  AI Analysis Result"
        disclaimer_lines = [
            "📚  References : ACR · ISMRM · ESUR · RSNA Guidelines, "
            "GE/Siemens/Philips Official Manuals, Academic Medical Center Protocols, "
            "Peer-reviewed Journals (Radiology, JMRI, MRM)",
            "⚠️  This report is for reference only. Final decisions must be made by "
            "qualified MRI technologists and radiologists.",
            "⚠️  AI analysis is powered by Groq LLaMA and does not replace medical diagnosis.",
        ]

    # ── 헤더 ──────────────────────────────────────────────────
    story.append(build_header(params, selected_seq, lang, fn, now))
    story.append(Spacer(1, 5 * mm))

    # ── 1. 기본 파라미터 카드 ─────────────────────────────────
    story.append(section_title(sec1, fn))
    story.append(Spacer(1, 3 * mm))
    story.append(build_info_cards(params, lang, fn))
    story.append(Spacer(1, 6 * mm))

    # ── 2. 파라미터 비교 테이블 ───────────────────────────────
    story.append(section_title(sec2, fn))
    story.append(Spacer(1, 3 * mm))
    comp = build_comparison_table(df, fn, lang)
    if comp:
        story.append(comp)
    story.append(Spacer(1, 6 * mm))

    # ── 3. 게이지 + 레이더 ────────────────────────────────────
    gauge_grid = build_gauge_grid(gauge_figs, fn)
    radar_img  = fig_to_image(radar_fig, width=450, height=380) if radar_fig else None

    story.append(section_title(sec3, fn))
    story.append(Spacer(1, 3 * mm))

    if gauge_grid and radar_img:
        radar_rl   = RLImage(radar_img, width=82 * mm, height=70 * mm)
        side_data  = [[gauge_grid, radar_rl]]
        side_table = Table(side_data, colWidths=[100 * mm, 82 * mm])
        side_table.setStyle(TableStyle([
            ("VALIGN",        (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING",   (0, 0), (-1, -1), 0),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
            ("TOPPADDING",    (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
        story.append(side_table)
    elif gauge_grid:
        story.append(gauge_grid)
    elif radar_img:
        story.append(RLImage(radar_img, width=100 * mm, height=85 * mm))

    story.append(Spacer(1, 6 * mm))

    # ── 4. AI 분석 결과 ───────────────────────────────────────
    if ai_result:
        story.append(section_title(sec4, fn))
        story.append(Spacer(1, 3 * mm))

        ai_items = build_ai_section(ai_result, fn, styles)

        ai_inner = Table(
            [[item] for item in ai_items],
            colWidths=[178 * mm]
        )
        ai_inner.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), C_LIGHTEST),
            ("BOX",           (0, 0), (-1, -1), 0.8, C_BORDER),
            ("LEFTPADDING",   (0, 0), (-1, -1), 10),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
            ("TOPPADDING",    (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("LINEABOVE",     (0, 0), (-1, 0),  3, C_BLUE),
        ]))
        story.append(ai_inner)
        story.append(Spacer(1, 6 * mm))

    # ── 5. 면책조항 ───────────────────────────────────────────
    story.append(HRFlowable(
        width="100%", thickness=0.5,
        color=C_BORDER, spaceAfter=4
    ))

    disclaimer_data = [
        [Paragraph(line, styles["Disclaimer"])]
        for line in disclaimer_lines
    ]
    disclaimer_table = Table(disclaimer_data, colWidths=[184 * mm])
    disclaimer_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), C_LIGHTEST),
        ("BOX",           (0, 0), (-1, -1), 0.5, C_BORDER),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("TOPPADDING",    (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LINEABOVE",     (0, 0), (-1, 0),  2, C_PASTEL_BLUE),
    ]))
    story.append(disclaimer_table)

    # ── PDF 빌드 ──────────────────────────────────────────────
    doc.build(story)
    buffer.seek(0)
    return buffer
