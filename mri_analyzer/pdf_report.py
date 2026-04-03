from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Image as RLImage
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from datetime import datetime
from io import BytesIO
import plotly.io as pio
import os


def register_fonts():
    font_paths = [
        os.path.join(os.path.dirname(__file__), "fonts", "NanumGothic.ttf"),
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "./fonts/NanumGothic.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(TTFont("Korean", path))
                pdfmetrics.registerFont(TTFont("Korean-Bold", path))
                return "Korean"
            except:
                continue
    return "Helvetica"


COLOR_HEADER     = colors.HexColor("#1B4F72")
COLOR_SUBHEADER  = colors.HexColor("#2E86C1")
COLOR_GOOD       = colors.HexColor("#1E8449")
COLOR_WARN       = colors.HexColor("#D4AC0D")
COLOR_BAD        = colors.HexColor("#C0392B")
COLOR_LIGHT_BLUE = colors.HexColor("#D6EAF8")
COLOR_LIGHT_GRAY = colors.HexColor("#F2F3F4")
COLOR_WHITE      = colors.white
COLOR_BLACK      = colors.black


def get_styles(font_name):
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="ReportTitle",
        fontName=font_name,
        fontSize=20,
        textColor=COLOR_HEADER,
        spaceAfter=4,
        alignment=TA_LEFT,
        leading=24,
    ))
    styles.add(ParagraphStyle(
        name="ReportSubTitle",
        fontName=font_name,
        fontSize=11,
        textColor=COLOR_SUBHEADER,
        spaceAfter=2,
        alignment=TA_LEFT,
    ))
    styles.add(ParagraphStyle(
        name="NormalKo",
        fontName=font_name,
        fontSize=9,
        textColor=COLOR_BLACK,
        spaceAfter=2,
        leading=13,
    ))
    styles.add(ParagraphStyle(
        name="Disclaimer",
        fontName=font_name,
        fontSize=7,
        textColor=colors.HexColor("#777777"),
        spaceAfter=2,
        leading=10,
        alignment=TA_LEFT,
    ))
    styles.add(ParagraphStyle(
        name="DateRight",
        fontName=font_name,
        fontSize=9,
        textColor=colors.HexColor("#555555"),
        alignment=TA_RIGHT,
    ))
    return styles


def fig_to_image(fig, width=400, height=300):
    try:
        img_bytes = pio.to_image(
            fig, format="png", width=width, height=height, scale=2
        )
        return BytesIO(img_bytes)
    except:
        return None


def section_header(title, font_name):
    data = [[Paragraph(
        f"  {title}",
        ParagraphStyle(
            name="SH",
            fontName=font_name,
            fontSize=11,
            textColor=COLOR_WHITE,
            leading=16,
        )
    )]]
    t = Table(data, colWidths=[170 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), COLOR_HEADER),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
    ]))
    return t
def build_info_table(params, lang, font_name):
    ko_basic = params.get("기본 정보", {})
    ko_seq   = params.get("시퀀스 파라미터", {})

    if lang == "ko":
        labels = {
            "filename":     "파일명",
            "manufacturer": "제조사",
            "detected":     "감지된 제조사",
            "protocol":     "프로토콜명",
            "bodypart":     "촬영부위",
            "fieldstr":     "자장강도(T)",
            "coil":         "수신코일",
            "series":       "시리즈설명",
            "tr":           "TR (ms)",
            "te":           "TE (ms)",
            "ti":           "TI (ms)",
            "flip":         "Flip Angle (°)",
            "etl":          "ETL",
            "nex":          "NEX/NSA",
        }
    else:
        labels = {
            "filename":     "File Name",
            "manufacturer": "Manufacturer",
            "detected":     "Detected Manufacturer",
            "protocol":     "Protocol Name",
            "bodypart":     "Body Part",
            "fieldstr":     "Field Strength(T)",
            "coil":         "Receive Coil",
            "series":       "Series Description",
            "tr":           "TR (ms)",
            "te":           "TE (ms)",
            "ti":           "TI (ms)",
            "flip":         "Flip Angle (°)",
            "etl":          "ETL",
            "nex":          "NEX/NSA",
        }

    def cell_label(txt):
        return Paragraph(str(txt), ParagraphStyle(
            name="cl", fontName=font_name, fontSize=8.5,
            leading=12, textColor=COLOR_HEADER,
        ))

    def cell_value(txt):
        return Paragraph(str(txt), ParagraphStyle(
            name="cv", fontName=font_name, fontSize=8.5,
            leading=12, textColor=COLOR_BLACK,
        ))

    rows = [
        [cell_label(labels["filename"]),
         cell_value(ko_basic.get("파일명", "N/A"))],
        [cell_label(labels["manufacturer"]),
         cell_value(ko_basic.get("제조사", "N/A"))],
        [cell_label(labels["detected"]),
         cell_value(ko_basic.get("감지된 제조사", "N/A"))],
        [cell_label(labels["protocol"]),
         cell_value(ko_basic.get("프로토콜명", "N/A"))],
        [cell_label(labels["bodypart"]),
         cell_value(ko_basic.get("촬영부위", "N/A"))],
        [cell_label(labels["fieldstr"]),
         cell_value(ko_basic.get("자장강도(T)", "N/A"))],
        [cell_label(labels["coil"]),
         cell_value(ko_basic.get("수신코일", "N/A"))],
        [cell_label(labels["tr"]),
         cell_value(ko_seq.get("TR (ms)", "N/A"))],
        [cell_label(labels["te"]),
         cell_value(ko_seq.get("TE (ms)", "N/A"))],
        [cell_label(labels["ti"]),
         cell_value(ko_seq.get("TI (ms)", "N/A"))],
        [cell_label(labels["flip"]),
         cell_value(ko_seq.get("Flip Angle (°)", "N/A"))],
        [cell_label(labels["etl"]),
         cell_value(ko_seq.get("ETL", "N/A"))],
        [cell_label(labels["nex"]),
         cell_value(ko_seq.get("NEX/NSA", "N/A"))],
    ]

    t = Table(rows, colWidths=[55 * mm, 115 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (0, -1), COLOR_LIGHT_BLUE),
        ("BACKGROUND",     (1, 0), (1, -1), COLOR_WHITE),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [COLOR_LIGHT_BLUE, COLOR_WHITE]),
        ("GRID",           (0, 0), (-1, -1), 0.3, colors.HexColor("#CCCCCC")),
        ("TOPPADDING",     (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",  (0, 0), (-1, -1), 4),
        ("LEFTPADDING",    (0, 0), (-1, -1), 6),
        ("VALIGN",         (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t


def build_comparison_table(df, font_name):
    if df is None or df.empty:
        return None

    col_count = len(df.columns)
    if col_count == 8:
        col_widths = [22, 18, 16, 18, 16, 14, 20, 46]
    else:
        col_w = 170 / col_count
        col_widths = [col_w] * col_count

    def hdr(txt):
        return Paragraph(f"<b>{txt}</b>", ParagraphStyle(
            name="th", fontName=font_name, fontSize=8,
            textColor=COLOR_WHITE, leading=11,
            alignment=TA_CENTER,
        ))

    def cell_center(txt, color=COLOR_BLACK):
        return Paragraph(str(txt), ParagraphStyle(
            name="td_c", fontName=font_name, fontSize=8,
            textColor=color, leading=11,
            alignment=TA_CENTER,
        ))

    def cell_left(txt, color=COLOR_BLACK):
        return Paragraph(str(txt), ParagraphStyle(
            name="td_l", fontName=font_name, fontSize=8,
            textColor=color, leading=11,
            alignment=TA_LEFT,
        ))

    headers = [hdr(c) for c in df.columns]
    rows    = [headers]

    for _, row in df.iterrows():
        status = str(row.get("상태", row.get("Status", "")))
        if "✅" in status:
            sc = COLOR_GOOD
        elif "⚠️" in status:
            sc = COLOR_WARN
        elif "❌" in status:
            sc = COLOR_BAD
        else:
            sc = COLOR_BLACK

        row_cells = []
        for i, v in enumerate(row):
            txt = str(v)
            if i == len(df.columns) - 1:
                row_cells.append(cell_left(txt, sc))
            elif i in [1, 2, 3, 4]:
                row_cells.append(cell_center(txt))
            else:
                row_cells.append(cell_left(txt))
        rows.append(row_cells)

    t = Table(rows, colWidths=[w * mm for w in col_widths])

    style_cmds = [
        ("BACKGROUND",    (0, 0), (-1, 0),  COLOR_HEADER),
        ("LINEBELOW",     (0, 0), (-1, 0),  1.5, COLOR_SUBHEADER),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("GRID",          (0, 0), (-1, -1), 0.3, colors.HexColor("#BDC3C7")),
    ]

    for idx, (_, row) in enumerate(df.iterrows()):
        status = str(row.get("상태", row.get("Status", "")))
        if "✅" in status:
            bg = colors.HexColor("#EAFAF1")
        elif "⚠️" in status:
            bg = colors.HexColor("#FEFDE7")
        elif "❌" in status:
            bg = colors.HexColor("#FDEDEC")
        else:
            bg = COLOR_WHITE if idx % 2 == 0 else COLOR_LIGHT_GRAY
        style_cmds.append(("BACKGROUND", (0, idx + 1), (-1, idx + 1), bg))

    t.setStyle(TableStyle(style_cmds))
    return t
def generate_pdf_report(params, user_baseline, df, radar_fig, gauge_figs,
                        ai_result, selected_seq, lang="ko"):
    font_name = register_fonts()
    styles    = get_styles(font_name)
    buffer    = BytesIO()
    now       = datetime.now().strftime("%Y-%m-%d %H:%M")

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
    )

    story = []

    if lang == "ko":
        title_txt    = "MRI DICOM 파라미터 분석 리포트"
        subtitle_txt = f"시퀀스 : {selected_seq}"
        date_txt     = f"분석일시 : {now}"
        sec1 = "1. 기본 정보"
        sec2 = "2. 파라미터 비교 분석"
        sec3 = "3. 파라미터 적합도"
        sec4 = "4. AI 분석 결과"
        disclaimer_lines = [
            "📚 파라미터 기준값 출처 : ACR · ISMRM · ESUR · RSNA 가이드라인, "
            "GE/Siemens/Philips 공식 매뉴얼, 국내외 대학병원 임상 프로토콜, "
            "Radiology · JMRI · MRM 등 peer-reviewed 논문",
            "⚠️ 본 리포트는 보조적 참고용이며, 최종 판단은 전문 방사선사 및 영상의학과 전문의가 해야 합니다.",
            "⚠️ AI 분석 결과는 Groq LLaMA 모델 기반이며, 의료적 진단을 대체하지 않습니다.",
        ]
    else:
        title_txt    = "MRI DICOM Parameter Analysis Report"
        subtitle_txt = f"Sequence : {selected_seq}"
        date_txt     = f"Date : {now}"
        sec1 = "1. Basic Information"
        sec2 = "2. Parameter Comparison"
        sec3 = "3. Parameter Fitness"
        sec4 = "4. AI Analysis Result"
        disclaimer_lines = [
            "📚 References : ACR · ISMRM · ESUR · RSNA Guidelines, "
            "GE/Siemens/Philips Official Manuals, Academic Medical Center Protocols, "
            "Peer-reviewed Journals (Radiology, JMRI, MRM)",
            "⚠️ This report is for reference only. Final decisions must be made by "
            "qualified MRI technologists and radiologists.",
            "⚠️ AI analysis is powered by Groq LLaMA and does not replace medical diagnosis.",
        ]

    # ── 헤더 ──────────────────────────────────────────────────
    header_data = [[
        Paragraph(title_txt, styles["ReportTitle"]),
        Paragraph(date_txt,  styles["DateRight"]),
    ]]
    header_table = Table(header_data, colWidths=[130 * mm, 40 * mm])
    header_table.setStyle(TableStyle([
        ("VALIGN",       (0, 0), (-1, -1), "BOTTOM"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(header_table)
    story.append(Paragraph(subtitle_txt, styles["ReportSubTitle"]))
    story.append(HRFlowable(
        width="100%", thickness=2,
        color=COLOR_HEADER, spaceAfter=6
    ))

    # ── 1. 기본 정보 ──────────────────────────────────────────
    story.append(section_header(sec1, font_name))
    story.append(Spacer(1, 3 * mm))
    story.append(build_info_table(params, lang, font_name))
    story.append(Spacer(1, 5 * mm))

    # ── 2. 파라미터 비교 + 레이더 차트 ───────────────────────
    story.append(section_header(sec2, font_name))
    story.append(Spacer(1, 3 * mm))

    comp_table = build_comparison_table(df, font_name)
    radar_img  = fig_to_image(radar_fig, width=400, height=350) if radar_fig else None

    if comp_table and radar_img:
        radar_rl   = RLImage(radar_img, width=75 * mm, height=65 * mm)
        side_data  = [[comp_table, radar_rl]]
        side_table = Table(side_data, colWidths=[95 * mm, 75 * mm])
        side_table.setStyle(TableStyle([
            ("VALIGN",       (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING",  (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ]))
        story.append(side_table)
    elif comp_table:
        story.append(comp_table)

    story.append(Spacer(1, 5 * mm))

    # ── 3. 게이지 차트 ────────────────────────────────────────
    if gauge_figs:
        story.append(section_header(sec3, font_name))
        story.append(Spacer(1, 3 * mm))

        gauge_images = []
        for name, fig in gauge_figs[:6]:
            img = fig_to_image(fig, width=250, height=180)
            if img:
                gauge_images.append(RLImage(img, width=52 * mm, height=38 * mm))

        if gauge_images:
            rows = []
            for i in range(0, len(gauge_images), 3):
                row = gauge_images[i:i+3]
                while len(row) < 3:
                    row.append("")
                rows.append(row)

            gauge_table = Table(rows, colWidths=[56 * mm, 56 * mm, 56 * mm])
            gauge_table.setStyle(TableStyle([
                ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN",        (0, 0), (-1, -1), "CENTER"),
                ("LEFTPADDING",  (0, 0), (-1, -1), 1),
                ("RIGHTPADDING", (0, 0), (-1, -1), 1),
            ]))
            story.append(gauge_table)

        story.append(Spacer(1, 5 * mm))

    # ── 4. AI 분석 결과 ───────────────────────────────────────
    if ai_result:
        story.append(section_header(sec4, font_name))
        story.append(Spacer(1, 3 * mm))

        for line in ai_result.split("\n"):
            line = line.strip()
            if not line:
                story.append(Spacer(1, 2 * mm))
                continue
            line = line.replace("##", "").replace("**", "").strip()
            story.append(Paragraph(line, styles["NormalKo"]))

        story.append(Spacer(1, 5 * mm))

    # ── 5. 면책조항 ───────────────────────────────────────────
    story.append(HRFlowable(
        width="100%", thickness=0.5,
        color=colors.HexColor("#AAAAAA"), spaceAfter=4
    ))
    for line in disclaimer_lines:
        story.append(Paragraph(line, styles["Disclaimer"]))

    # ── PDF 빌드 ──────────────────────────────────────────────
    doc.build(story)
    buffer.seek(0)
    return buffer
