import pydicom
import zipfile
import io
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from groq import Groq
from baseline import SEQUENCE_BASELINES
from baseline_common import MANUFACTURER_PARAMS


def extract_dcm_from_zip(uploaded_file):
    dcm_files = []
    with zipfile.ZipFile(io.BytesIO(uploaded_file.read()), "r") as z:
        for name in z.namelist():
            if name.lower().endswith(".dcm") or "." not in name.split("/")[-1]:
                try:
                    with z.open(name) as f:
                        data = f.read()
                        if data:
                            dcm_files.append({"name": name, "bytes": data})
                except:
                    continue
    return dcm_files


def extract_dicom_params(file_bytes, filename="unknown.dcm"):
    ds = pydicom.dcmread(io.BytesIO(file_bytes), force=True)

    def safe(tag, default="N/A"):
        try:
            val = ds[tag].value
            if isinstance(val, (list, pydicom.sequence.Sequence)):
                return str(val)
            return val
        except:
            return default

    def safe_float(tag, default=None):
        try:
            return float(ds[tag].value)
        except:
            return default

    # 제조사 감지
    mfr_raw  = str(safe(0x00080070, "")).upper()
    if "GE"      in mfr_raw: mfr = "GE"
    elif "SIEMENS" in mfr_raw: mfr = "SIEMENS"
    elif "PHILIPS" in mfr_raw: mfr = "PHILIPS"
    else: mfr = "UNKNOWN"

    tr    = safe_float(0x00180080)
    te    = safe_float(0x00180081)
    ti    = safe_float(0x00180082)
    flip  = safe_float(0x00181314)
    etl   = safe_float(0x00180091)
    nex   = safe_float(0x00180083)
    bw    = safe_float(0x00180095)
    rows  = safe_float(0x00280010)
    fov_r = safe_float(0x00181312)

    try:
        fov_val = ds[0x00181312].value
        if hasattr(fov_val, "__iter__"):
            fov = float(list(fov_val)[0])
        else:
            fov = float(fov_val)
    except:
        fov = None

    try:
        pixel_spacing = ds[0x00280030].value
        slice_thick   = safe_float(0x00500004) or safe_float(0x00180050)
    except:
        pixel_spacing = None
        slice_thick   = safe_float(0x00180050)

    # 제조사별 파라미터
    mfr_params = {}
    if mfr == "GE":
        mfr_params = {
            "SAR":              safe_float(0x00181316),
            "Gradient Mode":    str(safe(0x00189028, "N/A")),
        }
    elif mfr == "SIEMENS":
        mfr_params = {
            "SAR":              safe_float(0x00181316),
            "iPAT Factor":      safe_float(0x00189069),
            "Coil String":      str(safe(0x00511019, "N/A")),
        }
    elif mfr == "PHILIPS":
        mfr_params = {
            "SENSE Factor":     safe_float(0x00189087),
            "Water Fat Shift":  safe_float(0x00189024),
            "SAR":              safe_float(0x00181316),
        }

    params = {
        "기본 정보": {
            "파일명":       filename,
            "제조사":       str(safe(0x00080070, "N/A")),
            "감지된 제조사": mfr,
            "프로토콜명":   str(safe(0x00181030, "N/A")),
            "촬영부위":     str(safe(0x00180015, "N/A")),
            "자장강도(T)":  safe_float(0x00180087) or safe_float(0x00181030),
            "수신코일":     str(safe(0x00181250, "N/A")),
            "시리즈설명":   str(safe(0x0008103E, "N/A")),
        },
        "시퀀스 파라미터": {
            "TR (ms)":       tr,
            "TE (ms)":       te,
            "TI (ms)":       ti,
            "Flip Angle (°)": flip,
            "ETL":           etl,
            "NEX/NSA":       nex,
            "Bandwidth":     bw,
        },
        "공간 해상도": {
            "Slice Thickness (mm)": slice_thick,
            "Matrix Row":           rows,
            "FOV (mm)":             fov,
            "Pixel Spacing":        str(pixel_spacing) if pixel_spacing else "N/A",
        },
        "DWI 파라미터": {
            "b-value":              safe_float(0x00189087),
            "Diffusion Direction":  str(safe(0x00189089, "N/A")),
        },
        "제조사 파라미터": mfr_params,
    }
    return params, ds


def translate_params(params, lang):
    if lang == "ko":
        return params

    section_map = {
        "기본 정보":       "Basic Info",
        "시퀀스 파라미터": "Sequence Params",
        "공간 해상도":     "Spatial Resolution",
        "DWI 
def create_comparison_table(params, user_baseline, lang):
    seq_params   = params.get("시퀀스 파라미터", {})
    space_params = params.get("공간 해상도", {})
    mfr_params   = params.get("제조사 파라미터", {})

    all_params = {}
    all_params.update(seq_params)
    all_params.update(space_params)
    all_params.update(mfr_params)

    if lang == "ko":
        col_param   = "파라미터"
        col_current = "현재값"
        col_min     = "최소값"
        col_optimal = "최적값"
        col_max     = "최대값"
        col_unit    = "단위"
        col_impact  = "영향"
        col_status  = "상태"
        col_eval    = "평가"
        status_opt  = "✅ 최적"
        status_warn = "⚠️ 경고"
        status_caut = "🔵 주의"
        status_na   = "➖ N/A"
    else:
        col_param   = "Parameter"
        col_current = "Current"
        col_min     = "Min"
        col_optimal = "Optimal"
        col_max     = "Max"
        col_unit    = "Unit"
        col_impact  = "Impact"
        col_status  = "Status"
        col_eval    = "Evaluation"
        status_opt  = "✅ Optimal"
        status_warn = "⚠️ Warning"
        status_caut = "🔵 Caution"
        status_na   = "➖ N/A"

    rows = []
    for param_name, baseline in user_baseline.items():
        current = all_params.get(param_name)
        mn      = baseline.get("min")
        opt     = baseline.get("optimal")
        mx      = baseline.get("max")
        unit    = baseline.get("unit", "")
        impact  = baseline.get("impact", "")

        if current is None or current == "N/A":
            status = status_na
            eval_txt = "-"
        else:
            try:
                cur_f = float(current)
                if mn <= cur_f <= mx:
                    if abs(cur_f - opt) / (mx - mn + 1e-9) < 0.15:
                        status = status_opt
                        eval_txt = "최적 범위" if lang == "ko" else "Optimal range"
                    else:
                        status = status_caut
                        eval_txt = "허용 범위" if lang == "ko" else "Acceptable range"
                else:
                    status = status_warn
                    if cur_f < mn:
                        eval_txt = "기준 미달" if lang == "ko" else "Below minimum"
                    else:
                        eval_txt = "기준 초과" if lang == "ko" else "Above maximum"
            except:
                status   = status_na
                eval_txt = "-"

        rows.append({
            col_param:   param_name,
            col_current: current if current is not None else "N/A",
            col_min:     mn,
            col_optimal: opt,
            col_max:     mx,
            col_unit:    unit,
            col_impact:  impact,
            col_status:  status,
            col_eval:    eval_txt,
        })

    return pd.DataFrame(rows)


def create_radar_chart(params, user_baseline, lang):
    seq_params   = params.get("시퀀스 파라미터", {})
    space_params = params.get("공간 해상도", {})
    mfr_params   = params.get("제조사 파라미터", {})

    all_params = {}
    all_params.update(seq_params)
    all_params.update(space_params)
    all_params.update(mfr_params)

    scores = []
    labels = []

    for param_name, baseline in user_baseline.items():
        current = all_params.get(param_name)
        mn      = baseline.get("min")
        mx      = baseline.get("max")
        opt     = baseline.get("optimal")

        try:
            cur_f = float(current)
            rng   = mx - mn if mx != mn else 1
            score = max(0, min(100, 100 - abs(cur_f - opt) / rng * 100))
        except:
            score = 0

        scores.append(score)
        labels.append(param_name)

    if not scores:
        return None

    labels_closed = labels + [labels[0]]
    scores_closed = scores + [scores[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r     = scores_closed,
        theta = labels_closed,
        fill  = "toself",
        name  = "Score",
        line  = dict(color="#2E6DA4", width=2),
        fillcolor="rgba(46,109,164,0.2)",
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        showlegend=False,
        margin=dict(l=40, r=40, t=40, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor ="rgba(0,0,0,0)",
    )
    return fig


def create_gauge_charts(params, user_baseline):
    seq_params   = params.get("시퀀스 파라미터", {})
    space_params = params.get("공간 해상도", {})
    mfr_params   = params.get("제조사 파라미터", {})

    all_params = {}
    all_params.update(seq_params)
    all_params.update(space_params)
    all_params.update(mfr_params)

    gauges = []
    for param_name, baseline in user_baseline.items():
        current = all_params.get(param_name)
        mn      = baseline.get("min")
        mx      = baseline.get("max")
        opt     = baseline.get("optimal")
        unit    = baseline.get("unit", "")

        try:
            cur_f = float(current)
        except:
            continue

        rng   = mx - mn if mx != mn else 1
        score = max(0, min(100, 100 - abs(cur_f - opt) / rng * 100))

        if score >= 80:
            color = "#2E7D32"
        elif score >= 50:
            color = "#F57F17"
        else:
            color = "#C62828"

        fig = go.Figure(go.Indicator(
            mode  = "gauge+number",
            value = cur_f,
            title = {"text": f"{param_name}<br><sub>{unit}</sub>", "font": {"size": 12}},
            gauge = {
                "axis":  {"range": [mn, mx]},
                "bar":   {"color": color},
                "steps": [
                    {"range": [mn, opt],  "color": "#E3F2FD"},
                    {"range": [opt, mx],  "color": "#BBDEFB"},
                ],
                "threshold": {
                    "line":  {"color": "#1B3A5C", "width": 3},
                    "thickness": 0.75,
                    "value": opt,
                },
            },
        ))
        fig.update_layout(
            height=200,
            margin=dict(l=20, r=20, t=50, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
        )
        gauges.append((param_name, fig))

    return gauges if gauges else None
def analyze_with_openai(params, api_key, user_baseline,
                        selected_seq, lang, custom_prompt=None):
    client = Groq(api_key=api_key)

    if custom_prompt:
        prompt = custom_prompt
    else:
        seq_params   = params.get("시퀀스 파라미터", {})
        space_params = params.get("공간 해상도", {})
        mfr_params   = params.get("제조사 파라미터", {})
        basic_params = params.get("기본 정보", {})

        mfr      = basic_params.get("감지된 제조사", "UNKNOWN")
        protocol = basic_params.get("프로토콜명", "N/A")

        all_params = {}
        all_params.update(seq_params)
        all_params.update(space_params)
        all_params.update(mfr_params)

        param_lines = []
        for k, v in all_params.items():
            baseline = user_baseline.get(k, {})
            mn  = baseline.get("min",     "N/A")
            opt = baseline.get("optimal", "N/A")
            mx  = baseline.get("max",     "N/A")
            unit= baseline.get("unit",    "")
            param_lines.append(
                f"  - {k}: 현재={v}{unit} | 기준(최소={mn}, 최적={opt}, 최대={mx})"
            )

        param_text = "\n".join(param_lines)

        if lang == "ko":
            prompt = f"""
당신은 MRI 전문 방사선사 AI 어시스턴트입니다.
아래 MRI DICOM 파라미터를 분석하고 전문적인 의견을 제시해주세요.

[스캔 정보]
- 시퀀스  : {selected_seq}
- 제조사  : {mfr}
- 프로토콜: {protocol}

[파라미터 현재값 vs 기준값]
{param_text}

다음 항목으로 분석해주세요:

## 1. 시퀀스 식별 및 목적
- 촬영 목적과 임상적 의미

## 2. 파라미터 분석표
| 파라미터 | 현재값 | 최소 | 최적 | 최대 | 상태 | 평가 |
|---------|--------|------|------|------|------|------|
(각 파라미터를 표로 정리)

## 3. 제조사 특정 파라미터 분석
- {mfr} 장비 특성 고려

## 4. 문제 및 위험 항목
- 기준 범위를 벗어난 파라미터
- 임상적 영향

## 5. 최적화 추천
- 파라미터별 조정 방향
- 우선순위 순으로 정리

## 6. 종합 평가
- 전반적인 프로토콜 품질 점수 (100점 만점)
- 핵심 개선사항 요약
"""
        else:
            prompt = f"""
You are an expert MRI radiographer AI assistant.
Analyze the following MRI DICOM parameters and provide professional recommendations.

[Scan Information]
- Sequence : {selected_seq}
- Manufacturer: {mfr}
- Protocol: {protocol}

[Parameters: Current vs Reference]
{param_text}

Please analyze the following:

## 1. Sequence Identification & Purpose
- Clinical purpose and significance

## 2. Parameter Analysis Table
| Parameter | Current | Min | Optimal | Max | Status | Evaluation |
|-----------|---------|-----|---------|-----|--------|------------|
(summarize each parameter in table)

## 3. Manufacturer-Specific Analysis
- Considering {mfr} equipment characteristics

## 4. Issues & Risk Items
- Parameters outside reference range
- Clinical impact

## 5. Optimization Recommendations
- Adjustment direction per parameter
- Listed by priority

## 6. Overall Assessment
- Overall protocol quality score (out of 100)
- Summary of key improvements
"""

    if lang == "ko":
        system_msg = (
            "당신은 MRI 전문 방사선사 AI입니다. "
            "한국어로 전문적이고 명확하게 답변하세요. "
            "파라미터 분석표는 반드시 마크다운 테이블 형식으로 작성하세요."
        )
    else:
        system_msg = (
            "You are an expert MRI radiographer AI. "
            "Answer professionally and clearly in English. "
            "Always write parameter analysis tables in markdown table format."
        )

    response = client.chat.completions.create(
        model    = "llama3-70b-8192",
        messages = [
            {"role": "system",  "content": system_msg},
            {"role": "user",    "content": prompt},
        ],
        temperature = 0.3,
        max_tokens  = 4096,
    )

    return response.choices[0].message.content
