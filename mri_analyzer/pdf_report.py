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

# ── 한글 폰트 등록 ──────────────────────────────────────────
def register_fonts():
    font_paths = [
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

# ── 색상 정의 ───────────────────────────────────────────────
COLOR_HEADER     = colors.HexColor("#1B4F72")
COLOR_SUBHEADER  = colors.HexColor("#2E86C1")
COLOR_GOOD       = colors.HexColor("#1E8449")
COLOR_WARN       = colors.HexColor("#D4AC0D")
COLOR_BAD        = colors.HexColor("#C0392B")
COLOR_LIGHT_BLUE = colors.HexColor("#D6EAF8")
COLOR_LIGHT_GRAY = colors.HexColor("#F2F3F4")
COLOR_WHITE      = colors.white
COLOR_BLACK      = colors.black

# ── 스타일 정의 ─────────────────────────────────────────────
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
        name="SectionHeader",
        fontName=font_name,
        fontSize=12,
        textColor=COLOR_WHITE,
        spaceAfter=4,
        spaceBefore=8,
        alignment=TA_LEFT,
        leading=16,
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
        name="SmallKo",
        fontName=font_name,
        fontSize=7.5,
        textColor=colors.HexColor("#555555"),
        spaceAfter=2,
        leading=11,
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
  # ── 차트 → 이미지 변환 ──────────────────────────────────────
def fig_to_image(fig, width=400, height=300):
    try:
        img_bytes = pio.to_image(fig, format="png", width=width, height=height, scale=2)
        return BytesIO(img_bytes)
    except:
        return None

# ── 섹션 헤더 블록 ──────────────────────────────────────────
def section_header(title, font_name):
    data = [[Paragraph(f"  {title}", ParagraphStyle(
        name="SH",
        fontName=font_name,
        fontSize=11,
        textColor=COLOR_WHITE,
        leading=16,
    ))]]
    t = Table(data, colWidths=[170*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), COLOR_HEADER),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
    ]))
    return t

# ── 기본 정보 테이블 ────────────────────────────────────────
def build_info_table(params, lang, font_name, styles):
    if lang == "ko":
        basic = params.get("기본 정보", {})
        seq   = params.get("시퀀스 파라미터", {})
        labels = {
            "title":        "기본 정보",
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
        basic = params.get("Basic Info", params.get("기본 정보", {}))
        seq   = params.get("Sequence Params", params.get("시퀀스 파라미터", {}))
        labels = {
            "title":        "Basic Information",
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

    def cell(txt, bold=False, bg=None):
        style = ParagraphStyle(
            name="cell",
            fontName=font_name,
            fontSize=8.5,
            leading=12,
            textColor=COLOR_BLACK if bg != COLOR_LIGHT_BLUE else COLOR_HEADER,
        )
        return Paragraph(str(txt), style)

    ko_basic = params.get("기본 정보", basic)
    ko_seq   = params.get("시퀀스 파라미터", seq)

    rows = [
        [cell(labels["filename"],     bg=COLOR_LIGHT_BLUE),
         cell(ko_basic.get("파일명",     ko_basic.get("File Name",     "N/A")))],
        [cell(labels["manufacturer"],  bg=COLOR_LIGHT_BLUE),
         cell(ko_basic.get("제조사",     ko_basic.get("Manufacturer",  "N/A")))],
        [cell(labels["detected"],      bg=COLOR_LIGHT_BLUE),
         cell(ko_basic.get("감지된 제조사", ko_basic.get("Detected Manufacturer", "N/A")))],
        [cell(labels["protocol"],      bg=COLOR_LIGHT_BLUE),
         cell(ko_basic.get("프로토콜명",  ko_basic.get("Protocol Name", "N/A")))],
        [cell(labels["bodypart"],      bg=COLOR_LIGHT_BLUE),
         cell(ko_basic.get("촬영부위",   ko_basic.get("Body Part",     "N/A")))],
        [cell(labels["fieldstr"],      bg=COLOR_LIGHT_BLUE),
         cell(ko_basic.get("자장강도(T)", ko_basic.get("Field Strength(T)", "N/A")))],
        [cell(labels["coil"],          bg=COLOR_LIGHT_BLUE),
         cell(ko_basic.get("수신코일",   ko_basic.get("Receive Coil",  "N/A")))],
        [cell(labels["tr"],            bg=COLOR_LIGHT_BLUE),
         cell(ko_seq.get("TR (ms)",    "N/A"))],
        [cell(labels["te"],            bg=COLOR_LIGHT_BLUE),
         cell(ko_seq.get("TE (ms)",    "N/A"))],
        [cell(labels["ti"],            bg=COLOR_LIGHT_BLUE),
         cell(ko_seq.get("TI (ms)",    "N/A"))],
        [cell(labels["flip"],          bg=COLOR_LIGHT_BLUE),
         cell(ko_seq.get("Flip Angle (°)", "N/A"))],
        [cell(labels["etl"],           bg=COLOR_LIGHT_BLUE),
         cell(ko_seq.get("ETL",        "N/A"))],
        [cell(labels["nex"],           bg=COLOR_LIGHT_BLUE),
         cell(ko_seq.get("NEX/NSA",    "N/A"))],
    ]

    t = Table(rows, colWidths=[50*mm, 115*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (0, -1), COLOR_LIGHT_BLUE),
        ("BACKGROUND",    (1, 0), (1, -1), COLOR_WHITE),
        ("ROWBACKGROUNDS",(0, 0), (-1,-1), [COLOR_LIGHT_BLUE, COLOR_WHITE]),
        ("GRID",          (0, 0), (-1,-1), 0.3, colors.HexColor("#CCCCCC")),
        ("TOPPADDING",    (0, 0), (-1,-1), 4),
        ("BOTTOMPADDING", (0, 0), (-1,-1), 4),
        ("LEFTPADDING",   (0, 0), (-1,-1), 6),
        ("VALIGN",        (0, 0), (-1,-1), "MIDDLE"),
    ]))
    return t

# ── 파라미터 비교 테이블 ────────────────────────────────────
def build_comparison_table(df, font_name, lang):
    if df is None or df.empty:
        return None

    def hdr(txt):
        return Paragraph(f"<b>{txt}</b>", ParagraphStyle(
            name="th", fontName=font_name, fontSize=8,
            textColor=COLOR_WHITE, leading=11,
        ))

    def cell(txt, color=COLOR_BLACK):
        return Paragraph(str(txt), ParagraphStyle(
            name="td", fontName=font_name, fontSize=8,
            textColor=color, leading=11,
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

        rows.append([cell(str(v), sc if i == len(df.columns)-1 else COLOR_BLACK)
                     for i, v in enumerate(row)])

    col_w = 170 / len(df.columns)
    t = Table(rows, colWidths=[col_w*mm]*len(df.columns))
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), COLOR_HEADER),
        ("ROWBACKGROUNDS",(0, 1), (-1,-1), [COLOR_WHITE, COLOR_LIGHT_GRAY]),
        ("GRID",          (0, 0), (-1,-1), 0.3, colors.HexColor("#CCCCCC")),
        ("TOPPADDING",    (0, 0), (-1,-1), 3),
        ("BOTTOMPADDING", (0, 0), (-1,-1), 3),
        ("LEFTPADDING",   (0, 0), (-1,-1), 4),
        ("VALIGN",        (0, 0), (-1,-1), "MIDDLE"),
    ]))
    return t
          ("VALIGN",  (0,0), (-1,-1), "BOTTOM"),
        ("LEFTPADDING",  (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
    ]))
    story.append(header_table)
    story.append(Paragraph(subtitle_txt, styles["ReportSubTitle"]))
    story.append(HRFlowable(width="100%", thickness=2,
                            color=COLOR_HEADER, spaceAfter=6))

    # ── 1. 기본 정보 ─────────────────────────────────────────
    if lang == "ko":
        story.append(section_header("1. 기본 정보", font_name))
    else:
        story.append(section_header("1. Basic Information", font_name))
    story.append(Spacer(1, 3*mm))
    story.append(build_info_table(params, lang, font_name, styles))
    story.append(Spacer(1, 5*mm))

    # ── 2. 파라미터 비교 + 레이더 차트 ──────────────────────
    if lang == "ko":
        story.append(section_header("2. 파라미터 비교 분석", font_name))
    else:
        story.append(section_header("2. Parameter Comparison", font_name))
    story.append(Spacer(1, 3*mm))

    # 비교표 + 레이더 차트 좌우 배치
    comp_table = build_comparison_table(df, font_name, lang)
    radar_img  = fig_to_image(radar_fig, width=400, height=350) if radar_fig else None

    if comp_table and radar_img:
        radar_rl = RLImage(radar_img, width=75*mm, height=65*mm)
        side_data = [[comp_table, radar_rl]]
        side_table = Table(side_data, colWidths=[100*mm, 75*mm])
        side_table.setStyle(TableStyle([
            ("VALIGN",       (0,0), (-1,-1), "TOP"),
            ("LEFTPADDING",  (0,0), (-1,-1), 0),
            ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ]))
        story.append(side_table)
    elif comp_table:
        story.append(comp_table)
    story.append(Spacer(1, 5*mm))

    # ── 3. 게이지 차트 ───────────────────────────────────────
    if gauge_figs:
        if lang == "ko":
            story.append(section_header("3. 파라미터 적합도", font_name))
        else:
            story.append(section_header("3. Parameter Fitness", font_name))
        story.append(Spacer(1, 3*mm))

        gauge_images = []
        for name, fig in gauge_figs[:6]:  # 최대 6개
            img = fig_to_image(fig, width=250, height=180)
            if img:
                gauge_images.append(RLImage(img, width=52*mm, height=38*mm))

        if gauge_images:
            # 3열로 배치
            rows = []
            for i in range(0, len(gauge_images), 3):
                row = gauge_images[i:i+3]
                while len(row) < 3:
                    row.append("")
                rows.append(row)

            gauge_table = Table(rows, colWidths=[56*mm, 56*mm, 56*mm])
            gauge_table.setStyle(TableStyle([
                ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
                ("ALIGN",        (0,0), (-1,-1), "CENTER"),
                ("LEFTPADDING",  (0,0), (-1,-1), 1),
                ("RIGHTPADDING", (0,0), (-1,-1), 1),
            ]))
            story.append(gauge_table)
        story.append(Spacer(1, 5*mm))

    # ── 4. AI 분석 결과 ──────────────────────────────────────
    if ai_result:
        if lang == "ko":
            story.append(section_header("4. AI 분석 결과", font_name))
        else:
            story.append(section_header("4. AI Analysis Result", font_name))
        story.append(Spacer(1, 3*mm))

        for line in ai_result.split("\n"):
            line = line.strip()
            if not line:
                story.append(Spacer(1, 2*mm))
                continue
            # 마크다운 ## 제거
            line = line.replace("##", "").replace("**", "").strip()
            story.append(Paragraph(line, styles["NormalKo"]))

        story.append(Spacer(1, 5*mm))

    # ── 5. 출처 & 면책조항 ───────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=0.5,
                            color=colors.HexColor("#AAAAAA"), spaceAfter=4))
    if lang == "ko":
        disclaimer_lines = [
            "📚 파라미터 기준값 출처 : ACR · ISMRM · ESUR · RSNA 가이드라인, "
            "GE/Siemens/Philips 공식 매뉴얼, 국내외 대학병원 임상 프로토콜, "
            "Radiology · JMRI · MRM 등 peer-reviewed 논문",
            "⚠️ 본 리포트는 보조적 참고용이며, 최종 판단은 전문 방사선사 및 영상의학과 전문의가 해야 합니다.",
            "⚠️ AI 분석 결과는 Groq LLaMA 모델 기반이며, 의료적 진단을 대체하지 않습니다.",
        ]
    else:
        disclaimer_lines = [
            "📚 References : ACR · ISMRM · ESUR · RSNA Guidelines, "
            "GE/Siemens/Philips Official Manuals, Academic Medical Center Protocols, "
            "Peer-reviewed Journals (Radiology, JMRI, MRM)",
            "⚠️ This report is for reference only. Final decisions must be made by "
            "qualified MRI technologists and radiologists.",
            "⚠️ AI analysis is powered by Groq LLaMA and does not replace medical diagnosis.",
        ]

    for line in disclaimer_lines:
        story.append(Paragraph(line, styles["Disclaimer"]))

    # ── PDF 빌드 ─────────────────────────────────────────────
    doc.build(story)
    buffer.seek(0)
    return buffer


