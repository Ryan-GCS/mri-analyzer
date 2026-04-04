import io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Image as RLImage,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# ── 색상 ───────────────────────────────────────────────────
C_PRIMARY = HexColor("#2C3E50")
C_ACCENT  = HexColor("#2980B9")
C_GREEN   = HexColor("#27AE60")
C_ORANGE  = HexColor("#E67E22")
C_RED     = HexColor("#E74C3C")
C_BG      = HexColor("#F8F9FA")
C_BORDER  = HexColor("#DEE2E6")
C_MID     = HexColor("#7F8C8D")
C_BLACK   = black
C_WHITE   = white


# ── 폰트 등록 ──────────────────────────────────────────────
def register_fonts():
    font_paths = [
        ("NanumGothic",      "NanumGothic.ttf"),
        ("NanumGothic-Bold", "NanumGothicBold.ttf"),
    ]
    registered = []
    for font_name, font_file in font_paths:
        for search_dir in [".", "./fonts", "/usr/share/fonts",
                           "/usr/share/fonts/truetype/nanum"]:
            full_path = os.path.join(search_dir, font_file)
            if os.path.exists(full_path):
                try:
                    pdfmetrics.registerFont(TTFont(font_name, full_path))
                    registered.append(font_name)
                    break
                except Exception:
                    pass
    if "NanumGothic" in registered:
        return "NanumGothic"
    return "Helvetica"


# ── 스타일 ─────────────────────────────────────────────────
def get_styles(fn):
    styles = getSampleStyleSheet()

    def add_style(style):
        try:
            styles.add(style)
        except KeyError:
            # 이미 있으면 기존 스타일 속성만 업데이트
            existing = styles[style.name]
            existing.fontName  = style.fontName
            existing.fontSize  = style.fontSize
            existing.leading   = style.leading
            existing.textColor = style.textColor

    add_style(ParagraphStyle(
        name      = "BodyText",
        fontName  = fn,
        fontSize  = 9,
        leading   = 14,
        textColor = C_BLACK,
    ))
    add_style(ParagraphStyle(
        name      = "SmallText",
        fontName  = fn,
        fontSize  = 8,
        leading   = 12,
        textColor = C_MID,
    ))
    add_style(ParagraphStyle(
        name      = "SectionTitle",
        fontName  = fn,
        fontSize  = 11,
        leading   = 16,
        textColor = C_BLACK,
        spaceAfter= 4,
    ))
    add_style(ParagraphStyle(
        name      = "Disclaimer",
        fontName  = fn,
        fontSize  = 7,
        leading   = 11,
        textColor = C_MID,
    ))

    fb = fn + "-Bold" if fn != "Helvetica" else "Helvetica-Bold"
    return styles, fb
# ── 헬퍼 함수 ──────────────────────────────────────────────
def build_section_title(text, fn, fb):
    return Paragraph(
        "<font color='#2C3E50'><b>" + text + "</b></font>",
        ParagraphStyle(
            name     = "ST_" + text[:10],
            fontName = fb,
            fontSize = 12,
            leading  = 18,
            textColor= C_PRIMARY,
        )
    )


def score_color(score):
    if score >= 80:
        return C_GREEN
    elif score >= 50:
        return C_ORANGE
    return C_RED


def status_color(status):
    if "최적" in status or "Optimal" in status or "정상" in status:
        return C_GREEN
    elif "높음" in status or "낮음" in status or "High" in status or "Low" in status:
        return C_ORANGE
    elif "초과" in status or "미달" in status or "Over" in status or "Under" in status:
        return C_RED
    return C_MID


def fig_to_image(fig, width_mm=170, height_mm=90):
    buf = io.BytesIO()
    fig.write_image(buf, format="png", scale=2)
    buf.seek(0)
    return RLImage(buf, width=width_mm * mm, height=height_mm * mm)


def mpl_radar_to_image(params, user_baseline, width_mm=85, height_mm=75):
    labels = []
    values = []
    seq_p  = params.get("시퀀스 파라미터", {})
    sp_p   = params.get("공간 해상도", {})
    mfr_p  = params.get("제조사 파라미터", {})
    all_p  = {**seq_p, **sp_p, **mfr_p}

    for k, v in user_baseline.items():
        val = all_p.get(k)
        if val is None:
            continue
        try:
            cur = float(val)
            mn  = float(v["min"])
            mx  = float(v["max"])
            opt = float(v["optimal"])
            if mx == mn:
                continue
            score = max(0.0, min(1.0, 1.0 - abs(cur - opt) / (mx - mn)))
            labels.append(k)
            values.append(score)
        except Exception:
            continue

    if len(labels) < 3:
        return None

    N      = len(labels)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    values += values[:1]

    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, size=6)
    ax.set_ylim(0, 1)
    ax.plot(angles, values, "o-", linewidth=1.5, color="#2980B9")
    ax.fill(angles, values, alpha=0.25, color="#2980B9")
    ax.set_facecolor("#F8F9FA")
    fig.patch.set_facecolor("#F8F9FA")
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return RLImage(buf, width=width_mm * mm, height=height_mm * mm)


def build_score_bar(score, fn, fb, width_mm=170):
    color = score_color(score)
    bar_w = int(width_mm * score / 100)

    bar_table = Table(
        [[""]],
        colWidths  = [bar_w * mm],
        rowHeights = [5 * mm],
    )
    bar_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
        ("LINEABOVE",  (0, 0), (-1, -1), 0, color),
    ]))

    bg_table = Table(
        [[bar_table]],
        colWidths  = [width_mm * mm],
        rowHeights = [5 * mm],
    )
    bg_table.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), C_BORDER),
        ("ALIGN",        (0, 0), (-1, -1), "LEFT"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING",   (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 0),
    ]))
    return bg_table


def build_disclaimer(fn, lang):
    if lang == "ko":
        txt = (
            "※ 본 보고서는 DICOM 파일에서 자동 추출된 파라미터를 기반으로 AI가 생성한 참고 자료입니다. "
            "임상적 판단의 근거로 사용할 수 없으며, 최종 판단은 반드시 전문 의료진이 수행해야 합니다."
        )
    else:
        txt = (
            "※ This report is a reference document generated by AI based on parameters "
            "automatically extracted from DICOM files. It cannot be used as a basis for "
            "clinical judgment. Final decisions must be made by qualified medical professionals."
        )
    return Paragraph(txt, ParagraphStyle(
        name      = "Disc",
        fontName  = fn,
        fontSize  = 7,
        leading   = 11,
        textColor = C_MID,
    ))


def build_ai_section(ai_result, fn, fb):
    items  = []
    styles = getSampleStyleSheet()
    body_style = ParagraphStyle(
        name     = "AIBody",
        fontName = fn,
        fontSize = 9,
        leading  = 14,
    )
    head_style = ParagraphStyle(
        name     = "AIHead",
        fontName = fb,
        fontSize = 10,
        leading  = 16,
        textColor= C_PRIMARY,
    )
    for line in ai_result.split("\n"):
        line = line.strip()
        if not line:
            items.append(Spacer(1, 3 * mm))
        elif line.startswith("##"):
            items.append(Paragraph(line.replace("##", "").strip(), head_style))
        elif line.startswith("#"):
            items.append(Paragraph(line.replace("#", "").strip(), head_style))
        else:
            items.append(Paragraph(line, body_style))
    return items
# ── 단일 영상 PDF ───────────────────────────────────────────
def generate_pdf_report(params, user_baseline, df,
                        radar_fig, gauge_figs,
                        ai_result, selected_seq, lang="ko"):

    buffer = io.BytesIO()
    fn     = register_fonts()
    styles, fb = get_styles(fn)

    doc = SimpleDocTemplate(
        buffer,
        pagesize     = A4,
        leftMargin   = 15 * mm,
        rightMargin  = 15 * mm,
        topMargin    = 15 * mm,
        bottomMargin = 15 * mm,
    )

    story = []

    # ── 헤더 ──────────────────────────────────────────────
    if lang == "ko":
        title_txt    = "MRI DICOM 파라미터 분석 보고서"
        subtitle_txt = "시퀀스 : " + selected_seq
        date_txt     = "생성일 : " + __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M")
    else:
        title_txt    = "MRI DICOM Parameter Analysis Report"
        subtitle_txt = "Sequence : " + selected_seq
        date_txt     = "Generated : " + __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M")

    header_table = Table(
        [[
            Paragraph(
                "<font color='white'><b>" + title_txt + "</b></font>",
                ParagraphStyle(name="HT", fontName=fb, fontSize=16,
                               leading=22, textColor=C_WHITE)
            ),
            Paragraph(
                "<font color='white'>" + subtitle_txt + "<br/>" + date_txt + "</font>",
                ParagraphStyle(name="HS", fontName=fn, fontSize=9,
                               leading=14, textColor=C_WHITE, alignment=2)
            ),
        ]],
        colWidths=[120 * mm, 70 * mm],
    )
    header_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), C_PRIMARY),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 6 * mm))

    # ── 기본 정보 ──────────────────────────────────────────
    basic = params.get("기본 정보", {})
    if lang == "ko":
        info_title = "기본 정보"
        info_data_raw = {
            "환자 ID":    basic.get("환자 ID", "-"),
            "검사일":     basic.get("검사일", "-"),
            "제조사":     basic.get("감지된 제조사", "-"),
            "모델명":     basic.get("모델명", "-"),
            "자장강도":   basic.get("자장강도", "-"),
        }
    else:
        info_title = "Basic Information"
        info_data_raw = {
            "Patient ID":     basic.get("환자 ID", "-"),
            "Study Date":     basic.get("검사일", "-"),
            "Manufacturer":   basic.get("감지된 제조사", "-"),
            "Model":          basic.get("모델명", "-"),
            "Field Strength": basic.get("자장강도", "-"),
        }

    story.append(build_section_title(info_title, fn, fb))
    story.append(Spacer(1, 2 * mm))

    info_rows = []
    for k, v in info_data_raw.items():
        info_rows.append([
            Paragraph("<b>" + k + "</b>",
                      ParagraphStyle(name="IK" + k[:4], fontName=fb,
                                     fontSize=8, leading=12)),
            Paragraph(str(v),
                      ParagraphStyle(name="IV" + k[:4], fontName=fn,
                                     fontSize=8, leading=12)),
        ])

    info_table = Table(info_rows, colWidths=[50 * mm, 140 * mm])
    info_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (0, -1), C_BG),
        ("GRID",          (0, 0), (-1, -1), 0.3, C_BORDER),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 5 * mm))

    # ── 파라미터 비교표 ────────────────────────────────────
    if lang == "ko":
        table_title = "파라미터 비교표"
    else:
        table_title = "Parameter Comparison Table"

    story.append(build_section_title(table_title, fn, fb))
    story.append(Spacer(1, 2 * mm))

    if df is not None and len(df) > 0:
        col_names = list(df.columns)
        header_row = [
            Paragraph("<b>" + c + "</b>",
                      ParagraphStyle(name="TH" + str(i), fontName=fb,
                                     fontSize=8, leading=12, textColor=C_WHITE))
            for i, c in enumerate(col_names)
        ]
        table_data = [header_row]
        for _, row in df.iterrows():
            row_data = []
            for i, val in enumerate(row):
                txt = str(val)
                if i == len(col_names) - 2:
                    col = status_color(txt)
                    p = Paragraph(
                        "<font color='" + col.hexval() + "'><b>" + txt + "</b></font>",
                        ParagraphStyle(name="TD" + str(i), fontName=fn,
                                       fontSize=8, leading=12)
                    )
                else:
                    p = Paragraph(txt,
                                  ParagraphStyle(name="TD" + str(i), fontName=fn,
                                                 fontSize=8, leading=12))
                row_data.append(p)
            table_data.append(row_data)

        n_cols   = len(col_names)
        col_w    = 190 * mm / n_cols
        col_widths = [col_w] * n_cols

        param_table = Table(table_data, colWidths=col_widths, repeatRows=1)
        param_table.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, 0),  C_PRIMARY),
            ("BACKGROUND",    (0, 1), (-1, -1), C_WHITE),
            ("ROWBACKGROUNDS",(0, 1), (-1, -1), [C_WHITE, C_BG]),
            ("GRID",          (0, 0), (-1, -1), 0.3, C_BORDER),
            ("TOPPADDING",    (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING",   (0, 0), (-1, -1), 4),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 4),
            ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ]))
        story.append(param_table)
    story.append(Spacer(1, 5 * mm))

    # ── 레이더 차트 ────────────────────────────────────────
    if lang == "ko":
        radar_title = "파라미터 적합도 레이더 차트"
    else:
        radar_title = "Parameter Fitness Radar Chart"

    story.append(build_section_title(radar_title, fn, fb))
    story.append(Spacer(1, 2 * mm))

    radar_img = mpl_radar_to_image(params, user_baseline)
    if radar_img:
        story.append(radar_img)
    story.append(Spacer(1, 5 * mm))

    # ── AI 분석 결과 ───────────────────────────────────────
    if lang == "ko":
        ai_title = "AI 분석 결과"
    else:
        ai_title = "AI Analysis Result"

    story.append(build_section_title(ai_title, fn, fb))
    story.append(Spacer(1, 2 * mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=C_BORDER))
    story.append(Spacer(1, 2 * mm))

    for item in build_ai_section(ai_result, fn, fb):
        story.append(item)

    story.append(Spacer(1, 5 * mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=C_BORDER))
    story.append(Spacer(1, 2 * mm))
    story.append(build_disclaimer(fn, lang))

    doc.build(story)
    buffer.seek(0)
    return buffer
# ── 비교 영상 PDF ───────────────────────────────────────────
def generate_compare_pdf_report(params_a, params_b,
                                filename_a, filename_b,
                                user_baseline,
                                df_a, df_b,
                                radar_fig_a, radar_fig_b,
                                ai_result,
                                selected_seq, lang="ko"):

    buffer = io.BytesIO()
    fn     = register_fonts()
    styles, fb = get_styles(fn)

    doc = SimpleDocTemplate(
        buffer,
        pagesize     = A4,
        leftMargin   = 15 * mm,
        rightMargin  = 15 * mm,
        topMargin    = 15 * mm,
        bottomMargin = 15 * mm,
    )

    story = []

    # ── 헤더 ──────────────────────────────────────────────
    if lang == "ko":
        title_txt    = "MRI DICOM 비교 분석 보고서"
        subtitle_txt = "시퀀스 : " + selected_seq
        date_txt     = "생성일 : " + __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M")
        img_a_label  = "영상 A"
        img_b_label  = "영상 B"
    else:
        title_txt    = "MRI DICOM Comparison Report"
        subtitle_txt = "Sequence : " + selected_seq
        date_txt     = "Generated : " + __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M")
        img_a_label  = "Image A"
        img_b_label  = "Image B"

    header_table = Table(
        [[
            Paragraph(
                "<font color='white'><b>" + title_txt + "</b></font>",
                ParagraphStyle(name="CHT", fontName=fb, fontSize=16,
                               leading=22, textColor=C_WHITE)
            ),
            Paragraph(
                "<font color='white'>" + subtitle_txt + "<br/>" + date_txt + "</font>",
                ParagraphStyle(name="CHS", fontName=fn, fontSize=9,
                               leading=14, textColor=C_WHITE, alignment=2)
            ),
        ]],
        colWidths=[120 * mm, 70 * mm],
    )
    header_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), C_PRIMARY),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 6 * mm))

    # ── 파일명 표시 ────────────────────────────────────────
    file_table = Table(
        [[
            Paragraph(
                "<b>" + img_a_label + "</b><br/>" + filename_a,
                ParagraphStyle(name="FA", fontName=fn, fontSize=9,
                               leading=14, textColor=C_WHITE)
            ),
            Paragraph(
                "<b>" + img_b_label + "</b><br/>" + filename_b,
                ParagraphStyle(name="FB", fontName=fn, fontSize=9,
                               leading=14, textColor=C_WHITE)
            ),
        ]],
        colWidths=[95 * mm, 95 * mm],
    )
    file_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (0, 0), C_ACCENT),
        ("BACKGROUND",    (1, 0), (1, 0), C_ORANGE),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(file_table)
    story.append(Spacer(1, 5 * mm))

    # ── 파라미터 비교표 ────────────────────────────────────
    if lang == "ko":
        table_title = "파라미터 비교표"
        col_a_label = "영상 A 값"
        col_b_label = "영상 B 값"
        diff_label  = "차이"
        param_label = "파라미터"
    else:
        table_title = "Parameter Comparison Table"
        col_a_label = "Image A"
        col_b_label = "Image B"
        diff_label  = "Diff"
        param_label = "Parameter"

    story.append(build_section_title(table_title, fn, fb))
    story.append(Spacer(1, 2 * mm))

    if df_a is not None and df_b is not None and len(df_a) > 0:
        val_col = df_a.columns[1]

        header_row = [
            Paragraph("<b>" + param_label + "</b>",
                      ParagraphStyle(name="CTH0", fontName=fb, fontSize=8,
                                     leading=12, textColor=C_WHITE)),
            Paragraph("<b>" + col_a_label + "</b>",
                      ParagraphStyle(name="CTH1", fontName=fb, fontSize=8,
                                     leading=12, textColor=C_WHITE)),
            Paragraph("<b>" + col_b_label + "</b>",
                      ParagraphStyle(name="CTH2", fontName=fb, fontSize=8,
                                     leading=12, textColor=C_WHITE)),
            Paragraph("<b>" + diff_label + "</b>",
                      ParagraphStyle(name="CTH3", fontName=fb, fontSize=8,
                                     leading=12, textColor=C_WHITE)),
        ]

        cmp_data = [header_row]

        for i in range(min(len(df_a), len(df_b))):
            row_a   = df_a.iloc[i]
            row_b   = df_b.iloc[i]
            p_name  = str(row_a.iloc[0])
            val_a   = str(row_a.iloc[1])
            val_b   = str(row_b.iloc[1])

            try:
                diff_val = float(row_b.iloc[1]) - float(row_a.iloc[1])
                if diff_val > 0:
                    diff_txt = "▲ +" + str(round(diff_val, 2))
                    diff_col = C_ORANGE
                elif diff_val < 0:
                    diff_txt = "▼ " + str(round(diff_val, 2))
                    diff_col = C_ACCENT
                else:
                    diff_txt = "= 0"
                    diff_col = C_MID
            except Exception:
                diff_txt = "-"
                diff_col = C_MID

            cmp_data.append([
                Paragraph(p_name,
                          ParagraphStyle(name="CP0" + str(i), fontName=fn,
                                         fontSize=8, leading=12)),
                Paragraph(val_a,
                          ParagraphStyle(name="CP1" + str(i), fontName=fn,
                                         fontSize=8, leading=12)),
                Paragraph(val_b,
                          ParagraphStyle(name="CP2" + str(i), fontName=fn,
                                         fontSize=8, leading=12)),
                Paragraph(
                    "<font color='" + diff_col.hexval() + "'><b>" + diff_txt + "</b></font>",
                    ParagraphStyle(name="CP3" + str(i), fontName=fn,
                                   fontSize=8, leading=12)
                ),
            ])

        cmp_table = Table(
            cmp_data,
            colWidths   = [60 * mm, 40 * mm, 40 * mm, 40 * mm],
            repeatRows  = 1,
        )
        cmp_table.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, 0),  C_PRIMARY),
            ("ROWBACKGROUNDS",(0, 1), (-1, -1), [C_WHITE, C_BG]),
            ("GRID",          (0, 0), (-1, -1), 0.3, C_BORDER),
            ("TOPPADDING",    (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING",   (0, 0), (-1, -1), 4),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 4),
            ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ]))
        story.append(cmp_table)

    story.append(Spacer(1, 5 * mm))

    # ── 레이더 차트 비교 ───────────────────────────────────
    if lang == "ko":
        radar_title = "레이더 차트 비교"
    else:
        radar_title = "Radar Chart Comparison"

    story.append(build_section_title(radar_title, fn, fb))
    story.append(Spacer(1, 2 * mm))

    radar_img_a = mpl_radar_to_image(params_a, user_baseline,
                                     width_mm=85, height_mm=75)
    radar_img_b = mpl_radar_to_image(params_b, user_baseline,
                                     width_mm=85, height_mm=75)

    if radar_img_a and radar_img_b:
        radar_row = Table(
            [[
                Paragraph(
                    "<b>" + img_a_label + "</b>",
                    ParagraphStyle(name="RA", fontName=fb, fontSize=9,
                                   leading=14, textColor=C_ACCENT)
                ),
                Paragraph(
                    "<b>" + img_b_label + "</b>",
                    ParagraphStyle(name="RB", fontName=fb, fontSize=9,
                                   leading=14, textColor=C_ORANGE)
                ),
            ]],
            colWidths=[95 * mm, 95 * mm],
        )
        story.append(radar_row)
        story.append(Spacer(1, 1 * mm))

        radar_img_table = Table(
            [[radar_img_a, radar_img_b]],
            colWidths=[95 * mm, 95 * mm],
        )
        radar_img_table.setStyle(TableStyle([
            ("ALIGN",  (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        story.append(radar_img_table)

    story.append(Spacer(1, 5 * mm))
    # ── AI 비교 분석 결과 ──────────────────────────────────
    if lang == "ko":
        ai_title = "AI 비교 분석 결과"
    else:
        ai_title = "AI Comparison Analysis Result"

    story.append(build_section_title(ai_title, fn, fb))
    story.append(Spacer(1, 2 * mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=C_BORDER))
    story.append(Spacer(1, 2 * mm))

    for item in build_ai_section(ai_result, fn, fb):
        story.append(item)

    story.append(Spacer(1, 5 * mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=C_BORDER))
    story.append(Spacer(1, 2 * mm))
    story.append(build_disclaimer(fn, lang))

    doc.build(story)
    buffer.seek(0)
    return buffer
