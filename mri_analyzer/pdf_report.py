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
from reportlab.graphics.shapes import Drawing, Rect, String, Circle
from reportlab.graphics import renderPDF
from datetime import datetime
from io import BytesIO
import plotly.io as pio
import os
import re


# ── 폰트 등록 ─────────────────────────────────────────────
def register_fonts():
    font_paths = [
        os.path.join(os.path.dirname(__file__), "fonts", "NanumGothic.ttf"),
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "./fonts/NanumGothic.ttf",
    ]
    bold_paths = [
        os.path.join(os.path.dirname(__file__), "fonts", "NanumGothicBold.ttf"),
        "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf",
        "./fonts/NanumGothicBold.ttf",
    ]
    fn = "Helvetica"
    for path in font_paths:
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(TTFont("Korean", path))
                fn = "Korean"
                break
            except Exception:
                continue
    for path in bold_paths:
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(TTFont("KoreanBold", path))
                break
            except Exception:
                continue
    return fn


# ── 컬러 팔레트 ───────────────────────────────────────────
C_BLACK       = colors.HexColor("#111111")
C_DARK        = colors.HexColor("#222222")
C_MID         = colors.HexColor("#555555")
C_GRAY        = colors.HexColor("#888888")
C_LIGHT_GRAY  = colors.HexColor("#CCCCCC")
C_BG          = colors.HexColor("#F7F7F7")
C_WHITE       = colors.white
C_GREEN_DARK  = colors.HexColor("#1A7A3C")
C_GREEN       = colors.HexColor("#2ECC71")
C_GREEN_LIGHT = colors.HexColor("#A8E6C0")
C_YELLOW      = colors.HexColor("#F5C518")
C_YELLOW_BG   = colors.HexColor("#FFF8DC")
C_RED         = colors.HexColor("#E74C3C")
C_BLUE        = colors.HexColor("#2E86C1")
C_BORDER      = colors.HexColor("#E0E0E0")
C_HEADER_BG   = colors.HexColor("#FFFFFF")
C_HEADER_LINE = colors.HexColor("#DDDDDD")


# ── 스타일 ────────────────────────────────────────────────
def get_styles(fn):
    fb = "KoreanBold" if fn == "Korean" else fn + "-Bold"
    s  = getSampleStyleSheet()

    s.add(ParagraphStyle(
        name="PatientLabel",
        fontName=fn, fontSize=7,
        textColor=C_GRAY, leading=10,
    ))
    s.add(ParagraphStyle(
        name="PatientValue",
        fontName=fb, fontSize=8.5,
        textColor=C_BLACK, leading=12,
    ))
    s.add(ParagraphStyle(
        name="SectionTitle",
        fontName=fb, fontSize=16,
        textColor=C_BLACK, leading=22,
        spaceBefore=8, spaceAfter=4,
    ))
    s.add(ParagraphStyle(
        name="SubTitle",
        fontName=fb, fontSize=12,
        textColor=C_BLACK, leading=16,
        spaceBefore=6, spaceAfter=3,
    ))
    s.add(ParagraphStyle(
        name="BodyText",
        fontName=fn, fontSize=8.5,
        textColor=C_MID, leading=14,
        spaceAfter=3,
    ))
    s.add(ParagraphStyle(
        name="SmallText",
        fontName=fn, fontSize=7,
        textColor=C_GRAY, leading=10,
    ))
    s.add(ParagraphStyle(
        name="BulletText",
        fontName=fn, fontSize=8.5,
        textColor=C_MID, leading=14,
        leftIndent=10, spaceAfter=2,
    ))
    s.add(ParagraphStyle(
        name="AIHead",
        fontName=fb, fontSize=10,
        textColor=C_BLACK, leading=15,
        spaceBefore=6, spaceAfter=3,
    ))
    s.add(ParagraphStyle(
        name="AIBody",
        fontName=fn, fontSize=8.5,
        textColor=C_MID, leading=14,
        spaceAfter=3,
    ))
    return s, fb


# ── 헬퍼 ─────────────────────────────────────────────────
def fig_to_image(fig, width=500, height=350):
    try:
        img_bytes = pio.to_image(
            fig, format="png", width=width, height=height, scale=2
        )
        return BytesIO(img_bytes)
    except Exception:
        return None


def score_color(score):
    if score is None:
        return C_GRAY
    if score >= 15:
        return C_GREEN_DARK
    elif score >= 5:
        return C_GREEN
    else:
        return C_YELLOW


def make_bar(value, max_val, bar_width, bar_height, color):
    ratio    = min(max(float(value) / float(max_val), 0), 1)
    fill_w   = bar_width * ratio
    d        = Drawing(bar_width, bar_height)
    bg       = Rect(0, 0, bar_width, bar_height,
                    fillColor=C_LIGHT_GRAY, strokeColor=None)
    fg       = Rect(0, 0, fill_w, bar_height,
                    fillColor=color, strokeColor=None,
                    rx=bar_height/2, ry=bar_height/2)
    label    = String(
        fill_w - 4 if fill_w > 20 else fill_w + 4,
        bar_height / 2 - 4,
        str(int(value)),
        fontSize=9, fillColor=colors.white,
        textAnchor="end" if fill_w > 20 else "start",
    )
    d.add(bg)
    d.add(fg)
    d.add(label)
    return d
def build_patient_header(info, fn, fb, logo_text="MRI Analyzer"):
    def lbl(txt):
        return Paragraph(txt, ParagraphStyle(
            name="lbl_" + txt[:4],
            fontName=fn, fontSize=7,
            textColor=C_GRAY, leading=9,
        ))
    def val(txt):
        return Paragraph(str(txt), ParagraphStyle(
            name="val_" + str(txt)[:4],
            fontName=fb, fontSize=9,
            textColor=C_BLACK, leading=12,
        ))

    patient_name = info.get("파일명", "N/A")
    protocol     = info.get("프로토콜명", "N/A")
    mfr          = info.get("제조사", "N/A")
    field        = str(info.get("자장강도(T)", "N/A")) + " T"
    coil         = info.get("수신코일", "N/A")
    scan_date    = datetime.now().strftime("%Y-%m-%d")

    info_data = [
        [lbl("PATIENT"),   lbl("MANUFACTURER"), lbl("FIELD STRENGTH"),
         lbl("PROTOCOL"),  lbl("COIL"),          lbl("SCAN DATE")],
        [val(patient_name), val(mfr),            val(field),
         val(protocol),    val(coil),            val(scan_date)],
    ]

    info_table = Table(
        info_data,
        colWidths=[38*mm, 32*mm, 28*mm, 42*mm, 28*mm, 26*mm]
    )
    info_table.setStyle(TableStyle([
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
        ("TOPPADDING",    (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ]))

    logo = Paragraph(
        "<b>" + logo_text + "</b>",
        ParagraphStyle(
            name="logo", fontName=fb, fontSize=11,
            textColor=C_BLACK, leading=14,
            alignment=TA_RIGHT,
        )
    )

    header_row = Table(
        [[info_table, logo]],
        colWidths=[170*mm, 24*mm]
    )
    header_row.setStyle(TableStyle([
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
        ("TOPPADDING",    (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))

    wrapper = Table([[header_row]], colWidths=[194*mm])
    wrapper.setStyle(TableStyle([
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("LINEBELOW",     (0, 0), (-1, -1), 0.5, C_HEADER_LINE),
        ("BACKGROUND",    (0, 0), (-1, -1), C_WHITE),
    ]))
    return wrapper


def build_score_card(score, label, description, fn, fb):
    score_int = int(round(score)) if score is not None else 0
    color     = score_color(score_int)

    score_para = Paragraph(
        "<b>" + str(score_int) + "</b>",
        ParagraphStyle(
            name="score_num", fontName=fb, fontSize=48,
            textColor=C_BLACK, leading=56,
            alignment=TA_CENTER,
        )
    )

    score_box = Table(
        [[score_para]],
        colWidths=[45*mm]
    )
    score_box.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), colors.HexColor("#EAF6FF")),
        ("TOPPADDING",    (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
        ("ROUNDEDCORNERS",(0, 0), (-1, -1), [10, 10, 10, 10]),
    ]))

    desc_para = Paragraph(description, ParagraphStyle(
        name="score_desc", fontName=fn, fontSize=8.5,
        textColor=C_MID, leading=14,
    ))

    card = Table(
        [[score_box, desc_para]],
        colWidths=[50*mm, 140*mm]
    )
    card.setStyle(TableStyle([
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING",   (0, 0), (-1, -1), 4),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 4),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return card


def build_legend(fn):
    items = [
        (C_YELLOW,     "< 5",  "Consider consulting a healthcare professional."),
        (C_GREEN,      "15",   "Within the normal range but requires monitoring."),
        (C_GREEN_DARK, "95",   "You are within the normal range."),
    ]

    cells = []
    for color, val, desc in items:
        bar_d = Drawing(60*mm, 8*mm)
        bg    = Rect(0, 0, 60*mm, 8*mm,
                     fillColor=C_LIGHT_GRAY, strokeColor=None,
                     rx=4, ry=4)
        fg    = Rect(0, 0, int(val.replace("<","").strip())/100*60*mm if val != "95" else 57*mm,
                     8*mm, fillColor=color, strokeColor=None, rx=4, ry=4)
        lbl   = String(4, 1, val, fontSize=8,
                       fillColor=colors.white, textAnchor="start")
        bar_d.add(bg)
        bar_d.add(fg)
        bar_d.add(lbl)

        desc_p = Paragraph(desc, ParagraphStyle(
            name="leg_" + val, fontName=fn, fontSize=7,
            textColor=C_MID, leading=10,
        ))
        cells.append([bar_d, desc_p])

    t = Table(cells, colWidths=[65*mm, 100*mm])
    t.setStyle(TableStyle([
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING",   (0, 0), (-1, -1), 4),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("TOPPADDING",    (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("BACKGROUND",    (0, 0), (-1, -1), C_BG),
        ("BOX",           (0, 0), (-1, -1), 0.5, C_BORDER),
    ]))
    return t
def build_param_bars(df, fn, fb, lang):
    if df is None or df.empty:
        return None

    param_col   = df.columns[0]
    current_col = df.columns[1]
    min_col     = df.columns[2]
    max_col     = df.columns[4]
    status_col  = df.columns[7]

    rows = []
    for _, row in df.iterrows():
        param   = str(row[param_col])
        current = row[current_col]
        mn      = row[min_col]
        mx      = row[max_col]
        status  = str(row[status_col])

        if "✅" in status:
            color = C_GREEN_DARK
        elif "⚠️" in status:
            color = C_YELLOW
        elif "❌" in status:
            color = C_RED
        else:
            color = C_LIGHT_GRAY

        try:
            cur_f = float(current)
            mx_f  = float(mx)
            mn_f  = float(mn)
            if mx_f <= mn_f:
                mx_f = mn_f + 1
            bar_max = mx_f * 1.1
            bar = make_bar(cur_f, bar_max, 90*mm, 7*mm, color)
        except Exception:
            bar = Paragraph("-", ParagraphStyle(
                name="nobar", fontName=fn, fontSize=8,
                textColor=C_GRAY,
            ))

        name_p = Paragraph(
            "<b>" + param + "</b>",
            ParagraphStyle(
                name="pname_" + param[:6],
                fontName=fb, fontSize=8,
                textColor=C_BLACK, leading=11,
            )
        )
        val_p = Paragraph(
            str(current),
            ParagraphStyle(
                name="pval_" + param[:6],
                fontName=fn, fontSize=8,
                textColor=C_MID, leading=11,
                alignment=TA_RIGHT,
            )
        )
        status_p = Paragraph(
            status,
            ParagraphStyle(
                name="pstat_" + param[:6],
                fontName=fn, fontSize=8,
                textColor=C_MID, leading=11,
                alignment=TA_CENTER,
            )
        )
        rows.append([name_p, bar, val_p, status_p])

    if not rows:
        return None

    if lang == "ko":
        hdr = ["파라미터", "적합도", "현재값", "상태"]
    else:
        hdr = ["Parameter", "Fitness", "Current", "Status"]

    def hdr_p(txt):
        return Paragraph(
            "<b>" + txt + "</b>",
            ParagraphStyle(
                name="hdr_" + txt[:4],
                fontName=fb, fontSize=8,
                textColor=C_WHITE, leading=11,
                alignment=TA_CENTER,
            )
        )

    all_rows = [[hdr_p(h) for h in hdr]] + rows

    t = Table(all_rows, colWidths=[52*mm, 92*mm, 24*mm, 22*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  C_BLACK),
        ("LINEBELOW",     (0, 0), (-1, 0),  1,   C_BORDER),
        ("BACKGROUND",    (0, 1), (-1, -1), C_WHITE),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [C_WHITE, C_BG]),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("GRID",          (0, 0), (-1, -1), 0.3, C_BORDER),
    ]))
    return t


def build_compare_bars(df_a, df_b, name_a, name_b, fn, fb, lang):
    if df_a is None or df_b is None:
        return None

    param_col   = df_a.columns[0]
    current_col = df_a.columns[1]
    max_col     = df_a.columns[4]
    status_col  = df_a.columns[7]

    if lang == "ko":
        hdr = ["파라미터", name_a + " 적합도", name_b + " 적합도", "차이"]
    else:
        hdr = ["Parameter", name_a + " Fitness", name_b + " Fitness", "Diff"]

    def hdr_p(txt):
        return Paragraph(
            "<b>" + txt + "</b>",
            ParagraphStyle(
                name="chdr_" + txt[:4],
                fontName=fb, fontSize=7.5,
                textColor=C_WHITE, leading=11,
                alignment=TA_CENTER,
            )
        )

    rows = [[hdr_p(h) for h in hdr]]

    for i in range(min(len(df_a), len(df_b))):
        row_a = df_a.iloc[i]
        row_b = df_b.iloc[i]

        param    = str(row_a[param_col])
        cur_a    = row_a[current_col]
        cur_b    = row_b[current_col]
        mx       = row_a[max_col]
        status_a = str(row_a[status_col])
        status_b = str(row_b[status_col])

        color_a = C_GREEN_DARK if "✅" in status_a else (
            C_YELLOW if "⚠️" in status_a else C_RED
        )
        color_b = C_GREEN_DARK if "✅" in status_b else (
            C_YELLOW if "⚠️" in status_b else C_RED
        )

        try:
            mx_f  = float(mx) * 1.1
            bar_a = make_bar(float(cur_a), mx_f, 55*mm, 6*mm, color_a)
            bar_b = make_bar(float(cur_b), mx_f, 55*mm, 6*mm, color_b)
            diff  = float(cur_b) - float(cur_a)
            if diff > 0:
                diff_txt = "🔺 +" + str(round(diff, 1))
                diff_color = C_RED
            elif diff < 0:
                diff_txt = "🔻 " + str(round(diff, 1))
                diff_color = C_BLUE
            else:
                diff_txt = "➖ 0"
                diff_color = C_GRAY
        except Exception:
            bar_a     = Paragraph("-", ParagraphStyle(name="nb1", fontName=fn, fontSize=8))
            bar_b     = Paragraph("-", ParagraphStyle(name="nb2", fontName=fn, fontSize=8))
            diff_txt  = "-"
            diff_color= C_GRAY

        name_p = Paragraph(
            "<b>" + param + "</b>",
            ParagraphStyle(
                name="cpn_" + param[:6],
                fontName=fb, fontSize=8,
                textColor=C_BLACK, leading=11,
            )
        )
        diff_p = Paragraph(
            diff_txt,
            ParagraphStyle(
                name="cdiff_" + param[:6],
                fontName=fn, fontSize=8,
                textColor=diff_color, leading=11,
                alignment=TA_CENTER,
            )
        )
        rows.append([name_p, bar_a, bar_b, diff_p])

    t = Table(rows, colWidths=[48*mm, 58*mm, 58*mm, 26*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  C_BLACK),
        ("LINEBELOW",     (0, 0), (-1, 0),  1,   C_BORDER),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [C_WHITE, C_BG]),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("GRID",          (0, 0), (-1, -1), 0.3, C_BORDER),
    ]))
    return t


def build_section_title(txt, fn, fb):
    data = [[
        Paragraph("<b>" + txt + "</b>", ParagraphStyle(
            name="st_" + txt[:6],
            fontName=fb, fontSize=14,
            textColor=C_BLACK, leading=20,
        ))
    ]]
    t = Table(data, colWidths=[194*mm])
    t.setStyle(TableStyle([
        ("LINEBELOW",     (0, 0), (-1, -1), 1,   C_BLACK),
        ("TOPPADDING",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("BACKGROUND",    (0, 0), (-1, -1), C_WHITE),
    ]))
    return t
def build_ai_section(ai_result, fn, fb):
    story_items = []
    lines       = ai_result.split("\n")
    i           = 0

    while i < len(lines):
        line = lines[i].strip()

        if not line:
            story_items.append(Spacer(1, 2*mm))
            i += 1
            continue

        if line.startswith("|") and line.endswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            tbl = parse_ai_markdown_table(table_lines, fn, fb)
            if tbl:
                story_items.append(Spacer(1, 2*mm))
                story_items.append(tbl)
                story_items.append(Spacer(1, 2*mm))
            continue

        line_clean = line.replace("**", "").strip()

        if line_clean.startswith("## "):
            txt = line_clean[3:].strip()
            story_items.append(Paragraph(
                "<b>" + txt + "</b>",
                ParagraphStyle(
                    name="aih2_" + txt[:6],
                    fontName=fb, fontSize=10,
                    textColor=C_BLACK, leading=15,
                    spaceBefore=6, spaceAfter=3,
                )
            ))
            i += 1
            continue

        if line_clean.startswith("# "):
            txt = line_clean[2:].strip()
            story_items.append(Paragraph(
                "<b>" + txt + "</b>",
                ParagraphStyle(
                    name="aih1_" + txt[:6],
                    fontName=fb, fontSize=12,
                    textColor=C_BLACK, leading=17,
                    spaceBefore=8, spaceAfter=4,
                )
            ))
            i += 1
            continue

        if line_clean.startswith(("- ", "* ", "+ ")):
            txt = line_clean[2:].strip()
            story_items.append(Paragraph(
                "• " + txt,
                ParagraphStyle(
                    name="bull_" + txt[:6],
                    fontName=fn, fontSize=8.5,
                    textColor=C_MID, leading=13,
                    leftIndent=10, spaceAfter=2,
                )
            ))
            i += 1
            continue

        story_items.append(Paragraph(
            line_clean,
            ParagraphStyle(
                name="aibody_" + line_clean[:6],
                fontName=fn, fontSize=8.5,
                textColor=C_MID, leading=14,
                spaceAfter=2,
            )
        ))
        i += 1

    return story_items


def parse_ai_markdown_table(table_lines, fn, fb):
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

    max_cols   = max(len(r) for r in clean)
    col_w      = 190 / max_cols
    col_widths = [col_w * mm] * max_cols

    def hdr_p(txt):
        return Paragraph(
            "<b>" + str(txt) + "</b>",
            ParagraphStyle(
                name="mth_" + str(txt)[:4],
                fontName=fb, fontSize=7.5,
                textColor=C_WHITE, leading=11,
                alignment=TA_CENTER,
            )
        )

    def cell_p(txt, idx):
        return Paragraph(
            str(txt),
            ParagraphStyle(
                name="mtd_" + str(txt)[:4],
                fontName=fn, fontSize=7.5,
                textColor=C_DARK, leading=11,
                alignment=TA_LEFT if idx == 0 else TA_CENTER,
            )
        )

    rows = []
    for r_idx, row in enumerate(clean):
        while len(row) < max_cols:
            row.append("")
        if r_idx == 0:
            rows.append([hdr_p(c) for c in row])
        else:
            rows.append([cell_p(c, i) for i, c in enumerate(row)])

    t = Table(rows, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  C_BLACK),
        ("LINEBELOW",     (0, 0), (-1, 0),  1,   C_BORDER),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [C_WHITE, C_BG]),
        ("GRID",          (0, 0), (-1, -1), 0.3, C_BORDER),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t


def build_disclaimer(fn, lang):
    if lang == "ko":
        lines = [
            "본 리포트는 보조적 참고용이며, 최종 판단은 전문 방사선사 및 영상의학과 전문의가 해야 합니다.",
            "AI 분석 결과는 Groq LLaMA 모델 기반이며, 의료적 진단을 대체하지 않습니다.",
            "파라미터 기준값 출처: ACR · ISMRM · ESUR · RSNA 가이드라인, GE/Siemens/Philips 공식 매뉴얼.",
        ]
    else:
        lines = [
            "This report is for reference only. Final decisions must be made by qualified MRI technologists and radiologists.",
            "AI analysis is powered by Groq LLaMA and does not replace medical diagnosis.",
            "References: ACR · ISMRM · ESUR · RSNA Guidelines, GE/Siemens/Philips Official Manuals.",
        ]

    paras = [[Paragraph(
        "* " + line,
        ParagraphStyle(
            name="disc_" + str(idx),
            fontName=fn, fontSize=7,
            textColor=C_GRAY, leading=11,
        )
    )] for idx, line in enumerate(lines)]

    t = Table(paras, colWidths=[194*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), C_BG),
        ("BOX",           (0, 0), (-1, -1), 0.5, C_BORDER),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("LINEABOVE",     (0, 0), (-1, 0),  2, C_BLACK),
    ]))
    return t
def generate_pdf_report(params, user_baseline, df, radar_fig, gauge_figs,
                        ai_result, selected_seq, lang="ko"):
    fn         = register_fonts()
    styles, fb = get_styles(fn)

    buffer = BytesIO()
    doc    = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=8*mm,
        leftMargin=8*mm,
        topMargin=8*mm,
        bottomMargin=10*mm,
    )

    basic = params.get("기본 정보", {})
    story = []

    # ── 헤더 ──────────────────────────────────────────────
    story.append(build_patient_header(basic, fn, fb))
    story.append(Spacer(1, 6*mm))

    # ── 적합도 점수 계산 ──────────────────────────────────
    try:
        seq_p  = params.get("시퀀스 파라미터", {})
        sp_p   = params.get("공간 해상도", {})
        mfr_p  = params.get("제조사 파라미터", {})
        all_p  = {**seq_p, **sp_p, **mfr_p}
        scores = []
        for k, baseline in user_baseline.items():
            v = all_p.get(k)
            try:
                cur = float(v)
                mn  = float(baseline["min"])
                mx  = float(baseline["max"])
                opt = float(baseline["optimal"])
                rng = mx - mn if mx != mn else 1
                sc  = max(0, min(100, 100 - abs(cur - opt) / rng * 100))
                scores.append(sc)
            except Exception:
                pass
        avg_score = round(sum(scores) / len(scores)) if scores else 0
    except Exception:
        avg_score = 0

    # ── 점수 카드 ─────────────────────────────────────────
    if lang == "ko":
        score_title = "파라미터 적합도 점수"
        score_desc  = (
            "파라미터 적합도 점수는 현재 MRI 스캔 파라미터가 "
            "권장 기준값과 얼마나 일치하는지를 나타냅니다. "
            "점수가 높을수록 최적 범위에 가깝습니다. "
            "전문 방사선사와 함께 결과를 검토하시기 바랍니다."
        )
    else:
        score_title = "Parameter Fitness Score"
        score_desc  = (
            "The parameter fitness score represents how closely "
            "the current MRI scan parameters match the recommended "
            "reference values. A higher score indicates closer to "
            "the optimal range. Please review results with a qualified radiographer."
        )

    story.append(build_section_title(score_title, fn, fb))
    story.append(Spacer(1, 4*mm))
    story.append(build_score_card(avg_score, score_title, score_desc, fn, fb))
    story.append(Spacer(1, 4*mm))
    story.append(build_legend(fn))
    story.append(Spacer(1, 8*mm))

    # ── 파라미터 바 차트 ──────────────────────────────────
    if lang == "ko":
        bar_title = "파라미터 분석"
    else:
        bar_title = "Parameter Analysis"

    story.append(build_section_title(bar_title, fn, fb))
    story.append(Spacer(1, 4*mm))
    bar_table = build_param_bars(df, fn, fb, lang)
    if bar_table:
        story.append(bar_table)
    story.append(Spacer(1, 8*mm))

    # ── 레이더 차트 ───────────────────────────────────────
    if lang == "ko":
        radar_title = "레이더 차트"
    else:
        radar_title = "Radar Chart"

    story.append(build_section_title(radar_title, fn, fb))
    story.append(Spacer(1, 4*mm))

    if radar_fig:
        radar_img = fig_to_image(radar_fig, width=500, height=400)
        if radar_img:
            story.append(RLImage(radar_img, width=120*mm, height=96*mm))
    story.append(Spacer(1, 8*mm))

    # ── AI 분석 ───────────────────────────────────────────
    if ai_result:
        if lang == "ko":
            ai_title = "AI 분석 결과"
        else:
            ai_title = "AI Analysis Result"

        story.append(build_section_title(ai_title, fn, fb))
        story.append(Spacer(1, 4*mm))

        ai_items = build_ai_section(ai_result, fn, fb)
        ai_wrap  = Table(
            [[item] for item in ai_items],
            colWidths=[190*mm]
        )
        ai_wrap.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), C_BG),
            ("BOX",           (0, 0), (-1, -1), 0.5, C_BORDER),
            ("LEFTPADDING",   (0, 0), (-1, -1), 10),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
            ("TOPPADDING",    (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("LINEABOVE",     (0, 0), (-1, 0),  2, C_BLACK),
        ]))
        story.append(ai_wrap)
        story.append(Spacer(1, 8*mm))

    # ── 면책조항 ──────────────────────────────────────────
    story.append(build_disclaimer(fn, lang))

    doc.build(story)
    buffer.seek(0)
    return buffer


# ════════════════════════════════════════════════════════════
# ⚖️ 두 영상 비교 PDF
# ════════════════════════════════════════════════════════════
def generate_compare_pdf_report(params_a, params_b,
                                filename_a, filename_b,
                                user_baseline, df_a, df_b,
                                radar_fig_a, radar_fig_b,
                                ai_result, selected_seq, lang="ko"):
    fn         = register_fonts()
    styles, fb = get_styles(fn)

    buffer = BytesIO()
    doc    = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=8*mm,
        leftMargin=8*mm,
        topMargin=8*mm,
        bottomMargin=10*mm,
    )

    basic_a = params_a.get("기본 정보", {})
    story   = []

    # ── 헤더 ──────────────────────────────────────────────
    story.append(build_patient_header(basic_a, fn, fb))
    story.append(Spacer(1, 6*mm))

    # ── 비교 제목 카드 ────────────────────────────────────
    if lang == "ko":
        cmp_title = "두 영상 비교 분석 리포트"
        fa_label  = "영상 A"
        fb_label  = "영상 B"
    else:
        cmp_title = "Two Image Comparison Report"
        fa_label  = "Image A"
        fb_label  = "Image B"

    title_p = Paragraph(
        "<b>" + cmp_title + "</b>",
        ParagraphStyle(
            name="cmp_title",
            fontName=fb, fontSize=18,
            textColor=C_BLACK, leading=24,
        )
    )
    fa_p = Paragraph(
        fa_label + " : " + filename_a,
        ParagraphStyle(
            name="fa_label",
            fontName=fn, fontSize=9,
            textColor=C_MID, leading=13,
        )
    )
    fb_p = Paragraph(
        fb_label + " : " + filename_b,
        ParagraphStyle(
            name="fb_label",
            fontName=fn, fontSize=9,
            textColor=C_MID, leading=13,
        )
    )

    title_box = Table(
        [[title_p], [fa_p], [fb_p]],
        colWidths=[194*mm]
    )
    title_box.setStyle(TableStyle([
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("LINEBELOW",     (0, 2), (-1, 2),  1, C_BLACK),
    ]))
    story.append(title_box)
    story.append(Spacer(1, 6*mm))

    # ── 점수 비교 카드 ────────────────────────────────────
    def calc_score(params):
        try:
            seq_p  = params.get("시퀀스 파라미터", {})
            sp_p   = params.get("공간 해상도", {})
            mfr_p  = params.get("제조사 파라미터", {})
            all_p  = {**seq_p, **sp_p, **mfr_p}
            scores = []
            for k, baseline in user_baseline.items():
                v = all_p.get(k)
                try:
                    cur = float(v)
                    mn  = float(baseline["min"])
                    mx  = float(baseline["max"])
                    opt = float(baseline["optimal"])
                    rng = mx - mn if mx != mn else 1
                    sc  = max(0, min(100, 100 - abs(cur - opt) / rng * 100))
                    scores.append(sc)
                except Exception:
                    pass
            return round(sum(scores) / len(scores)) if scores else 0
        except Exception:
            return 0

    score_a = calc_score(params_a)
    score_b = calc_score(params_b)

    if lang == "ko":
        score_title = "적합도 점수 비교"
    else:
        score_title = "Fitness Score Comparison"

    story.append(build_section_title(score_title, fn, fb))
    story.append(Spacer(1, 4*mm))

    card_a = build_score_card(
        score_a,
        fa_label,
        fa_label + " : " + filename_a,
        fn, fb
    )
    card_b = build_score_card(
        score_b,
        fb_label,
        fb_label + " : " + filename_b,
        fn, fb
    )

    score_row = Table(
        [[card_a], [card_b]],
        colWidths=[194*mm]
    )
    score_row.setStyle(TableStyle([
        ("TOPPADDING",    (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
        ("LINEBELOW",     (0, 0), (-1, 0),  0.5, C_BORDER),
    ]))
    story.append(score_row)
    story.append(Spacer(1, 4*mm))
    story.append(build_legend(fn))
    story.append(Spacer(1, 8*mm))

    # ── 파라미터 비교 바 ──────────────────────────────────
    if lang == "ko":
        cmp_bar_title = "파라미터 비교"
    else:
        cmp_bar_title = "Parameter Comparison"

    story.append(build_section_title(cmp_bar_title, fn, fb))
    story.append(Spacer(1, 4*mm))

    cmp_bar = build_compare_bars(df_a, df_b, fa_label, fb_label, fn, fb, lang)
    if cmp_bar:
        story.append(cmp_bar)
    story.append(Spacer(1, 8*mm))

    # ── 레이더 차트 비교 ──────────────────────────────────
    if lang == "ko":
        radar_title = "레이더 차트 비교"
    else:
        radar_title = "Radar Chart Comparison"

    story.append(build_section_title(radar_title, fn, fb))
    story.append(Spacer(1, 4*mm))

    radar_cells = []
    if radar_fig_a:
        img_a = fig_to_image(radar_fig_a, width=400, height=320)
        if img_a:
            radar_cells.append(RLImage(img_a, width=90*mm, height=72*mm))
        else:
            radar_cells.append(Paragraph("N/A", ParagraphStyle(name="rna", fontName=fn, fontSize=8)))
    else:
        radar_cells.append(Paragraph("N/A", ParagraphStyle(name="rna2", fontName=fn, fontSize=8)))

    if radar_fig_b:
        img_b = fig_to_image(radar_fig_b, width=400, height=320)
        if img_b:
            radar_cells.append(RLImage(img_b, width=90*mm, height=72*mm))
        else:
            radar_cells.append(Paragraph("N/A", ParagraphStyle(name="rnb", fontName=fn, fontSize=8)))
    else:
        radar_cells.append(Paragraph("N/A", ParagraphStyle(name="rnb2", fontName=fn, fontSize=8)))

    radar_label_a = Paragraph(
        "🔵 " + fa_label,
        ParagraphStyle(name="rla", fontName=fb, fontSize=9,
                       textColor=C_BLACK, alignment=TA_CENTER)
    )
    radar_label_b = Paragraph(
        "🟠 " + fb_label,
        ParagraphStyle(name="rlb", fontName=fb, fontSize=9,
                       textColor=C_BLACK, alignment=TA_CENTER)
    )

    radar_table = Table(
        [[radar_label_a,  radar_label_b],
         [radar_cells[0], radar_cells[1]]],
        colWidths=[97*mm, 97*mm]
    )
    radar_table.setStyle(TableStyle([
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING",   (0, 0), (-1, -1), 3),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 3),
        ("LINEBELOW",     (0, 0), (-1, 0),  0.5, C_BORDER),
    ]))
    story.append(radar_table)
    story.append(Spacer(1, 8*mm))

    # ── AI 비교 분석 ──────────────────────────────────────
    if ai_result:
        if lang == "ko":
            ai_title = "AI 비교 분석 결과"
        else:
            ai_title = "AI Comparison Analysis Result"

        story.append(build_section_title(ai_title, fn, fb))
        story.append(Spacer(1, 4*mm))

        ai_items = build_ai_section(ai_result, fn, fb)
        ai_wrap  = Table(
            [[item] for item in ai_items],
            colWidths=[190*mm]
        )
        ai_wrap.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), C_BG),
            ("BOX",           (0, 0), (-1, -1), 0.5, C_BORDER),
            ("LEFTPADDING",   (0, 0), (-1, -1), 10),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
            ("TOPPADDING",    (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("LINEABOVE",     (0, 0), (-1, 0),  2, C_BLACK),
        ]))
        story.append(ai_wrap)
        story.append(Spacer(1, 8*mm))

    # ── 면책조항 ──────────────────────────────────────────
    story.append(build_disclaimer(fn, lang))

    doc.build(story)
    buffer.seek(0)
    return buffer
  
