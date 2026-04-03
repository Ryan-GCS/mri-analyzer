import pydicom
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO
import zipfile
import os
import tempfile
import json
from groq import Groq


def extract_dcm_from_zip(uploaded_zip):
    dcm_files = []
    tmp = tempfile.mkdtemp()
    with zipfile.ZipFile(uploaded_zip, "r") as zf:
        zf.extractall(tmp)
    for root, dirs, files in os.walk(tmp):
        for fname in files:
            fpath = os.path.join(root, fname)
            try:
                ds = pydicom.dcmread(fpath, force=True)
                if hasattr(ds, "Modality") or hasattr(ds, "pixel_array"):
                    with open(fpath, "rb") as f:
                        dcm_files.append({"name": fname, "bytes": f.read()})
            except:
                pass
    return dcm_files


def detect_manufacturer(ds):
    def safe_get(tag, default=""):
        try:
            val = ds[tag].value
            return str(val).upper() if val is not None else default
        except:
            return default

    manufacturer = safe_get((0x0008, 0x0070))
    if "GE" in manufacturer:
        return "GE", manufacturer
    elif "SIEMENS" in manufacturer:
        return "SIEMENS", manufacturer
    elif "PHILIPS" in manufacturer:
        return "PHILIPS", manufacturer
    else:
        return "UNKNOWN", manufacturer


def extract_manufacturer_params(ds, mfr):
    def safe_get(tag, default="N/A"):
        try:
            val = ds[tag].value
            return str(val) if val is not None else default
        except:
            return default

    common_advanced = {
        "Parallel Imaging Factor": safe_get((0x0018, 0x9069)),
        "Partial Fourier":         safe_get((0x0018, 0x9081)),
        "Diffusion Gradient Dir":  safe_get((0x0018, 0x9089)),
        "Fat Saturation":          safe_get((0x0018, 0x9012)),
        "Inversion Recovery":      safe_get((0x0018, 0x9009)),
        "Spoiling":                safe_get((0x0018, 0x9016)),
        "Receive Coil Name":       safe_get((0x0018, 0x1250)),
        "Transmit Coil Name":      safe_get((0x0018, 0x1251)),
        "SAR":                     safe_get((0x0018, 0x1316)),
        "Cardiac RR Interval":     safe_get((0x0018, 0x0088)),
    }

    if mfr == "GE":
        ge_params = {
            "Pulse Sequence Name":    safe_get((0x0019, 0x109C)),
            "Internal Pulse Seq":     safe_get((0x0019, 0x109E)),
            "Slice Thickness (GE)":   safe_get((0x0043, 0x1039)),
            "Noise Reduction Factor": safe_get((0x0043, 0x102F)),
            "Acquisition Type":       safe_get((0x0019, 0x10A4)),
            "ARC/ASSET Factor":       safe_get((0x0043, 0x1028)),
            "Auto Prescan":           safe_get((0x0019, 0x10F2)),
        }
        ge_params.update(common_advanced)
        return ge_params

    elif mfr == "SIEMENS":
        siemens_params = {
            "iPAT Factor":            safe_get((0x0051, 0x100A)),
            "FOV Siemens":            safe_get((0x0051, 0x100B)),
            "Slice Orientation":      safe_get((0x0051, 0x100E)),
            "BW per Pixel Phase":     safe_get((0x0019, 0x1028)),
            "Mosaic Image Count":     safe_get((0x0019, 0x100A)),
            "Slice Duration":         safe_get((0x0019, 0x100B)),
            "Real Dwell Time":        safe_get((0x0051, 0x1016)),
            "GRAPPA Factor":          safe_get((0x0051, 0x1011)),
        }
        siemens_params.update(common_advanced)
        return siemens_params

    elif mfr == "PHILIPS":
        philips_params = {
            "B-Factor (Philips)":     safe_get((0x2001, 0x1003)),
            "Diffusion Direction":    safe_get((0x2001, 0x1004)),
            "Number of Slices":       safe_get((0x2005, 0x1011)),
            "Prepulse Delay":         safe_get((0x2001, 0x1018)),
            "Dynamic Scans":          safe_get((0x2001, 0x1081)),
            "SENSE Factor":           safe_get((0x2005, 0x100E)),
            "Water Fat Shift":        safe_get((0x2001, 0x1022)),
        }
        philips_params.update(common_advanced)
        return philips_params

    else:
        return common_advanced


def extract_dicom_params(file_bytes, filename=""):
    ds = pydicom.dcmread(BytesIO(file_bytes), force=True)

    def safe_get(tag, default="N/A"):
        try:
            val = ds[tag].value
            return str(val) if val is not None else default
        except:
            return default

    mfr, manufacturer_raw = detect_manufacturer(ds)
    mfr_params = extract_manufacturer_params(ds, mfr)
    mfr_params_filtered = {
        k: v for k, v in mfr_params.items() if v != "N/A"
    }

    params = {
        "기본 정보": {
            "파일명":        filename,
            "제조사":        manufacturer_raw,
            "감지된 제조사": mfr,
            "시퀀스명":      safe_get((0x0018, 0x0024)),
            "프로토콜명":    safe_get((0x0018, 0x1030)),
            "촬영부위":      safe_get((0x0018, 0x0015)),
            "자장강도(T)":   safe_get((0x0018, 0x0087)),
            "수신코일":      safe_get((0x0018, 0x1250)),
            "시리즈설명":    safe_get((0x0008, 0x103E)),
        },
        "시퀀스 파라미터": {
            "TR (ms)":        safe_get((0x0018, 0x0080)),
            "TE (ms)":        safe_get((0x0018, 0x0081)),
            "TI (ms)":        safe_get((0x0018, 0x0082)),
            "Flip Angle (°)": safe_get((0x0018, 0x1314)),
            "ETL":            safe_get((0x0018, 0x0091)),
            "NEX/NSA":        safe_get((0x0018, 0x0083)),
            "Bandwidth":      safe_get((0x0018, 0x0095)),
        },
        "공간 해상도": {
            "Slice Thickness (mm)": safe_get((0x0050, 0x0018)),
            "Pixel Spacing":        safe_get((0x0028, 0x0030)),
            "Matrix Row":           safe_get((0x0028, 0x0010)),
            "Matrix Col":           safe_get((0x0028, 0x0011)),
            "FOV (mm)":             safe_get((0x0018, 0x1100)),
            "획득방식(2D/3D)":      safe_get((0x0018, 0x0023)),
        },
        "DWI 파라미터": {
            "B-value": safe_get((0x0019, 0x100C)),
        },
        "제조사 파라미터": mfr_params_filtered,
    }

    return params, ds
def create_comparison_table(params, user_baseline):
    all_params = {}
    for section in params.values():
        if isinstance(section, dict):
            all_params.update(section)

    rows = []
    for param_name, baseline in user_baseline.items():
        current_val = all_params.get(param_name, "N/A")
        try:
            cur = float(current_val)
            mn  = baseline["min"]
            opt = baseline["optimal"]
            mx  = baseline["max"]
            if cur < mn:
                status = "🚨 경고 (낮음)"
            elif cur > mx:
                status = "🚨 경고 (높음)"
            elif abs(cur - opt) <= (mx - mn) * 0.1:
                status = "✅ 최적"
            else:
                status = "⚠️ 주의"
        except:
            status = "❓ 확인불가"
            mn = opt = mx = "-"
            cur = current_val

        rows.append({
            "파라미터": param_name,
            "현재값":   current_val,
            "최소":     mn,
            "최적":     opt,
            "최대":     mx,
            "단위":     baseline["unit"],
            "영향":     baseline["impact"],
            "상태":     status,
        })
    return pd.DataFrame(rows)


def create_radar_chart(params, user_baseline):
    all_params = {}
    for section in params.values():
        if isinstance(section, dict):
            all_params.update(section)

    current_vals = []
    optimal_vals = []
    labels = []

    for param_name, baseline in user_baseline.items():
        raw = all_params.get(param_name, "N/A")
        try:
            cur = float(raw)
            mn  = baseline["min"]
            mx  = baseline["max"]
            opt = baseline["optimal"]
            if mx != mn:
                cur_norm = max(0, min(100, (cur - mn) / (mx - mn) * 100))
                opt_norm = (opt - mn) / (mx - mn) * 100
                current_vals.append(round(cur_norm, 1))
                optimal_vals.append(round(opt_norm, 1))
                labels.append(param_name)
        except:
            pass

    if not labels:
        return None

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=current_vals + [current_vals[0]],
        theta=labels + [labels[0]],
        fill="toself",
        name="현재값",
        line_color="royalblue"
    ))
    fig.add_trace(go.Scatterpolar(
        r=optimal_vals + [optimal_vals[0]],
        theta=labels + [labels[0]],
        fill="toself",
        name="최적값",
        line_color="tomato",
        opacity=0.5
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        title="현재값 vs 최적값 비교",
        showlegend=True,
        height=500
    )
    return fig


def create_gauge_charts(params, user_baseline):
    all_params = {}
    for section in params.values():
        if isinstance(section, dict):
            all_params.update(section)

    charts = []
    for param_name, baseline in user_baseline.items():
        raw = all_params.get(param_name, "N/A")
        try:
            cur = float(raw)
            mn  = baseline["min"]
            mx  = baseline["max"]
            opt = baseline["optimal"]

            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=cur,
                delta={"reference": opt, "valueformat": ".1f"},
                title={"text": f"{param_name}<br><sub>{baseline['impact']}</sub>"},
                gauge={
                    "axis": {"range": [mn * 0.8, mx * 1.2]},
                    "bar":  {"color": "royalblue"},
                    "steps": [
                        {"range": [mn * 0.8, mn], "color": "lightcoral"},
                        {"range": [mn, mx],        "color": "lightgreen"},
                        {"range": [mx, mx * 1.2],  "color": "lightcoral"},
                    ],
                    "threshold": {
                        "line":      {"color": "red", "width": 4},
                        "thickness": 0.75,
                        "value":     opt
                    }
                }
            ))
            fig.update_layout(
                height=250,
                margin=dict(t=60, b=20, l=20, r=20)
            )
            charts.append((param_name, fig))
        except:
            pass
    return charts


def analyze_with_openai(params, api_key, user_baseline, selected_seq):
    client = Groq(api_key=api_key)

    mfr = params["기본 정보"]["감지된 제조사"]
    mfr_params = params.get("제조사 파라미터", {})

    prompt = f"""
당신은 MRI 촬영 파라미터 전문 분석 AI입니다. 반드시 한국어로 답변해주세요.

선택된 시퀀스: {selected_seq}
감지된 제조사: {mfr}

추출된 DICOM 파라미터:
{json.dumps(params, ensure_ascii=False, indent=2)}

사용자 기준값 (최소/최적/최대):
{json.dumps(user_baseline, ensure_ascii=False, indent=2)}

감지된 제조사 전용 파라미터:
{json.dumps(mfr_params, ensure_ascii=False, indent=2)}

아래 항목을 분석해주세요:

1. 📊 시퀀스 판별 및 목적
   - 감지된 제조사 및 장비 특성 설명
   - 해당 시퀀스의 임상적 목적

2. 📋 파라미터 분석표
   | 파라미터 | 현재값 | 최소 | 최적 | 최대 | 상태 | 평가 |
   상태: ✅최적 / ⚠️주의 / 🚨경고

3. 🏭 제조사 전용 파라미터 분석
   - 감지된 파라미터만 분석
   - GE면 ARC/ASSET/Noise 분석
   - Siemens면 iPAT/GRAPPA 분석
   - Philips면 SENSE/Water Fat Shift 분석
   - 감지 안되면 "제조사 전용 파라미터 없음" 표시

4. ⚠️ 문제점 및 위험 항목
   - 기준값 벗어난 파라미터
   - 제조사 전용 파라미터 이상 여부

5. 💡 최적화 권고사항
   - 파라미터별 조정 방향
   - 트레이드오프 설명 포함

6. 🎯 우선순위 액션 아이템
   - 1순위: 즉시 수정 필요
   - 2순위: 개선 권장
   - 3순위: 선택적 최적화

7. 📈 전체 영상 품질 점수
   - SNR:    X/10
   - 해상도: X/10
   - 대조도: X/10
   - 전체:   X/10
   - 종합 평가 한줄 요약
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4096
    )
    return response.choices[0].message.content
