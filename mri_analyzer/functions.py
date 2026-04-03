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
            "iPAT Factor":        safe_get((0x0051, 0x100A)),
            "FOV Siemens":        safe_get((0x0051, 0x100B)),
            "Slice Orientation":  safe_get((0x0051, 0x100E)),
            "BW per Pixel Phase": safe_get((0x0019, 0x1028)),
            "Mosaic Image Count": safe_get((0x0019, 0x100A)),
            "Slice Duration":     safe_get((0x0019, 0x100B)),
            "Real Dwell Time":    safe_get((0x0051, 0x1016)),
            "GRAPPA Factor":      safe_get((0x0051, 0x1011)),
        }
        siemens_params.update(common_advanced)
        return siemens_params
    elif mfr == "PHILIPS":
        philips_params = {
            "B-Factor (Philips)": safe_get((0x2001, 0x1003)),
            "Diffusion Direction":safe_get((0x2001, 0x1004)),
            "Number of Slices":   safe_get((0x2005, 0x1011)),
            "Prepulse Delay":     safe_get((0x2001, 0x1018)),
            "Dynamic Scans":      safe_get((0x2001, 0x1081)),
            "SENSE Factor":       safe_get((0x2005, 0x100E)),
            "Water Fat Shift":    safe_get((0x2001, 0x1022)),
        }
        philips_params.update(common_advanced)
        return philips_params
    else:
        return common_advanced
        
def translate_params(params, lang):
    if lang == "ko":
        return params

    key_map = {
        # 섹션명
        "기본 정보":       "Basic Info",
        "시퀀스 파라미터": "Sequence Params",
        "공간 해상도":     "Spatial Resolution",
        "DWI 파라미터":    "DWI Params",
        "제조사 파라미터": "Manufacturer Params",
        # 기본 정보 키
        "파일명":          "File Name",
        "제조사":          "Manufacturer",
        "감지된 제조사":   "Detected Manufacturer",
        "시퀀스명":        "Sequence Name",
        "프로토콜명":      "Protocol Name",
        "촬영부위":        "Body Part",
        "자장강도(T)":     "Field Strength(T)",
        "수신코일":        "Receive Coil",
        "시리즈설명":      "Series Description",
        # 공간 해상도 키
        "획득방식(2D/3D)": "Acquisition(2D/3D)",
    }

    translated = {}
    for section_ko, section_data in params.items():
        section_en = key_map.get(section_ko, section_ko)
        if isinstance(section_data, dict):
            translated[section_en] = {
                key_map.get(k, k): v
                for k, v in section_data.items()
            }
        else:
            translated[section_en] = section_data
    return translated

def extract_dicom_params(file_bytes, filename=""):
    ds = pydicom.dcmread(BytesIO(file_bytes), force=True)

    def safe_get(tag, default="N/A"):
        try:
            val = ds[tag].value
            return str(val) if val is not None else default
        except:
            return default

    def get_fov():
        fov = safe_get((0x0018, 0x1100))
        if fov != "N/A":
            return fov
        try:
            spacing = ds[(0x0028, 0x0030)].value
            rows    = ds[(0x0028, 0x0010)].value
            if isinstance(spacing, (list, tuple)):
                ps = float(spacing[0])
            else:
                ps = float(str(spacing).split("\\")[0])
            return str(round(ps * int(rows), 1))
        except:
            pass
        fov = safe_get((0x0051, 0x100C))
        if fov != "N/A":
            return fov
        fov = safe_get((0x2005, 0x100D))
        if fov != "N/A":
            return fov
        return "N/A"

    def get_slice_thickness():
        st = safe_get((0x0018, 0x0050))
        if st != "N/A":
            return st
        st = safe_get((0x0043, 0x1039))
        if st != "N/A":
            return st
        return "N/A"

    mfr, manufacturer_raw = detect_manufacturer(ds)
    mfr_params = extract_manufacturer_params(ds, mfr)
    mfr_params_filtered = {k: v for k, v in mfr_params.items() if v != "N/A"}

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
            "Slice Thickness (mm)": get_slice_thickness(),
            "Pixel Spacing":        safe_get((0x0028, 0x0030)),
            "Matrix Row":           safe_get((0x0028, 0x0010)),
            "Matrix Col":           safe_get((0x0028, 0x0011)),
            "FOV (mm)":             get_fov(),
            "획득방식(2D/3D)":      safe_get((0x0018, 0x0023)),
        },
        "DWI 파라미터": {
            "B-value": safe_get((0x0019, 0x100C)),
        },
        "제조사 파라미터": mfr_params_filtered,
    }
    return params, ds
def create_comparison_table(params, user_baseline, lang="ko"):
    from translations import get_text
    T = lambda key: get_text(lang, key)

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
                status = T("status_low")
            elif cur > mx:
                status = T("status_high")
            elif abs(cur - opt) <= (mx - mn) * 0.1:
                status = T("status_optimal")
            else:
                status = T("status_caution")
        except:
            status = T("status_unknown")
            mn = opt = mx = "-"
            cur = current_val

        rows.append({
            T("col_param"):   param_name,
            T("col_current"): current_val,
            T("col_min"):     mn,
            T("col_optimal"): opt,
            T("col_max"):     mx,
            T("col_unit"):    baseline["unit"],
            T("col_impact"):  baseline["impact"],
            T("col_status"):  status,
        })
    return pd.DataFrame(rows)


def create_radar_chart(params, user_baseline, lang="ko"):
    from translations import get_text
    T = lambda key: get_text(lang, key)

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
        name=T("radar_current"),
        line_color="royalblue"
    ))
    fig.add_trace(go.Scatterpolar(
        r=optimal_vals + [optimal_vals[0]],
        theta=labels + [labels[0]],
        fill="toself",
        name=T("radar_optimal"),
        line_color="tomato",
        opacity=0.5
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        title=T("radar_title"),
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


def analyze_with_openai(params, api_key, user_baseline, selected_seq, lang="ko"):
    from translations import get_text
    client = Groq(api_key=api_key)

    mfr         = params["기본 정보"]["감지된 제조사"]
    mfr_params  = params.get("제조사 파라미터", {})
    prompt_lang = get_text(lang, "prompt_lang")

    prompt = f"""You are an expert MRI parameter analysis AI. {prompt_lang}

Selected Sequence: {selected_seq}
Detected Manufacturer: {mfr}

Extracted DICOM Parameters:
{json.dumps(params, ensure_ascii=False, indent=2)}

User Baseline (Min/Optimal/Max):
{json.dumps(user_baseline, ensure_ascii=False, indent=2)}

Manufacturer Specific Parameters:
{json.dumps(mfr_params, ensure_ascii=False, indent=2)}

Please analyze the following:

1. Sequence Identification & Purpose
   - Detected manufacturer and device characteristics
   - Clinical purpose of the sequence

2. Parameter Analysis Table
   | Parameter | Current | Min | Optimal | Max | Status | Evaluation |
   Status: Optimal / Caution / Warning

3. Manufacturer Specific Parameter Analysis
   - GE: ARC/ASSET/Noise analysis
   - Siemens: iPAT/GRAPPA analysis
   - Philips: SENSE/Water Fat Shift analysis

4. Issues & Risk Items
   - Parameters outside baseline range
   - Manufacturer specific parameter anomalies

5. Optimization Recommendations
   - Adjustment direction per parameter
   - Include tradeoff explanation

6. Priority Action Items
   - Priority 1: Immediate correction needed
   - Priority 2: Improvement recommended
   - Priority 3: Optional optimization

7. Overall Image Quality Score
   - SNR:        X/10
   - Resolution: X/10
   - Contrast:   X/10
   - Overall:    X/10
   - One-line summary
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4096
    )
    return response.choices[0].message.content
