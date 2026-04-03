import streamlit as st
from baseline import SEQUENCE_BASELINES, LABEL_EN_MAP, IMPACT_EN_MAP
from baseline_common import MANUFACTURER_PARAMS
from translations import get_text
from functions import (
    extract_dcm_from_zip,
    extract_dicom_params,
    create_comparison_table,
    create_radar_chart,
    create_gauge_charts,
    analyze_with_openai,
)

st.set_page_config(
    page_title="MRI DICOM AI Analyzer",
    page_icon="🧠",
    layout="wide"
)

mfr_keys = list(MANUFACTURER_PARAMS.keys())

if "lang" not in st.session_state:
    st.session_state.lang = "ko"

try:
    api_key = st.secrets["groq"]["api_key"]
except:
    api_key = ""

def translate_label(label, lang):
    if lang == "ko":
        return label
    return LABEL_EN_MAP.get(label, label)

def translate_impact(impact, lang):
    if lang == "ko":
        return impact
    return IMPACT_EN_MAP.get(impact, impact)

with st.sidebar:
    lang = st.radio(
        "🌐 언어 / Language",
        options=["ko", "en"],
        format_func=lambda x: "🇰🇷 한국어" if x == "ko" else "🇺🇸 English",
        horizontal=True,
        key="lang"
    )

    T = lambda key: get_text(lang, key)

    st.markdown("---")
    st.header(T("seq_select"))

    seq_options = {
        translate_label(v["label"], lang): k
        for k, v in SEQUENCE_BASELINES.items()
    }

    selected_label  = st.selectbox(T("seq_label"), list(seq_options.keys()))
    selected_seq    = seq_options[selected_label]
    baseline_params = SEQUENCE_BASELINES[selected_seq]["params"]

    st.markdown("---")
    st.header(T("baseline_setting"))
    st.caption(T("baseline_caption"))

    user_baseline = {}

    st.subheader(T("seq_params"))
    for param_name, values in baseline_params.items():
        if param_name not in mfr_keys:
            impact_label = translate_impact(values["impact"], lang)
            with st.expander(f"📌 {param_name} | {impact_label}"):
                c1, c2, c3 = st.columns(3)
                mn  = c1.number_input(T("min"),     value=float(values["min"]),     key=f"min_{selected_seq}_{param_name}")
                opt = c2.number_input(T("optimal"), value=float(values["optimal"]), key=f"opt_{selected_seq}_{param_name}")
                mx  = c3.number_input(T("max"),     value=float(values["max"]),     key=f"max_{selected_seq}_{param_name}")
                user_baseline[param_name] = {
                    "min":     mn,
                    "optimal": opt,
                    "max":     mx,
                    "unit":    values["unit"],
                    "impact":  values["impact"]
                }

    st.markdown("---")
    st.subheader(T("mfr_params"))
    st.caption(T("mfr_caption"))
    for param_name, values in baseline_params.items():
        if param_name in mfr_keys:
            impact_label = translate_impact(values["impact"], lang)
            with st.expander(f"⚙️ {param_name} | {impact_label}"):
                c1, c2, c3 = st.columns(3)
                mn  = c1.number_input(T("min"),     value=float(values["min"]),     key=f"min_{selected_seq}_{param_name}")
                opt = c2.number_input(T("optimal"), value=float(values["optimal"]), key=f"opt_{selected_seq}_{param_name}")
                mx  = c3.number_input(T("max"),     value=float(values["max"]),     key=f"max_{selected_seq}_{param_name}")
                user_baseline[param_name] = {
                    "min":     mn,
                    "optimal": opt,
                    "max":     mx,
                    "unit":    values["unit"],
                    "impact":  values["impact"]
    st.markdown("---")
    with st.expander(T("reference_header")):
        st.markdown(T("reference_body"))
                }
T = lambda key: get_text(lang, key)

st.title(T("app_title"))
st.warning(T("app_warning"))
st.markdown("---")

st.header(T("upload_header"))
st.caption(T("upload_caption"))

uploaded_file = st.file_uploader(
    T("upload_label"),
    type=None
)

if uploaded_file:
    if uploaded_file.name.endswith(".zip"):
        with st.spinner(T("zip_spinner")):
            dcm_files = extract_dcm_from_zip(uploaded_file)
            if not dcm_files:
                st.error(T("zip_error"))
                st.stop()
            st.success(T("zip_success").format(len(dcm_files)))
            file_names    = [f["name"] for f in dcm_files]
            selected_name = st.selectbox(T("zip_select"), file_names)
            chosen        = next(f for f in dcm_files if f["name"] == selected_name)
            file_bytes    = chosen["bytes"]
            filename      = chosen["name"]
    else:
        file_bytes = uploaded_file.read()
        filename   = uploaded_file.name

    with st.spinner(T("dcm_spinner")):
        try:
            params, ds = extract_dicom_params(file_bytes, filename)
        except Exception as e:
            st.error(T("dcm_error").format(e))
            st.stop()

    mfr = params["기본 정보"]["감지된 제조사"]
    if mfr == "GE":
        st.info(T("mfr_ge"))
    elif mfr == "SIEMENS":
        st.info(T("mfr_siemens"))
    elif mfr == "PHILIPS":
        st.info(T("mfr_philips"))
    else:
        st.warning(T("mfr_unknown"))

    st.header(T("params_header"))

    if mfr == "GE":
        t1, t2, t3, t4, t5 = st.tabs([
            T("tab_basic"), T("tab_seq"), T("tab_spatial"), T("tab_dwi"), T("tab_ge")
        ])
        with t1: st.json(params["기본 정보"])
        with t2: st.json(params["시퀀스 파라미터"])
        with t3: st.json(params["공간 해상도"])
        with t4: st.json(params["DWI 파라미터"])
        with t5: st.json(params["제조사 파라미터"])

    elif mfr == "SIEMENS":
        t1, t2, t3, t4, t5 = st.tabs([
            T("tab_basic"), T("tab_seq"), T("tab_spatial"), T("tab_dwi"), T("tab_siemens")
        ])
        with t1: st.json(params["기본 정보"])
        with t2: st.json(params["시퀀스 파라미터"])
        with t3: st.json(params["공간 해상도"])
        with t4: st.json(params["DWI 파라미터"])
        with t5: st.json(params["제조사 파라미터"])

    elif mfr == "PHILIPS":
        t1, t2, t3, t4, t5 = st.tabs([
            T("tab_basic"), T("tab_seq"), T("tab_spatial"), T("tab_dwi"), T("tab_philips")
        ])
        with t1: st.json(params["기본 정보"])
        with t2: st.json(params["시퀀스 파라미터"])
        with t3: st.json(params["공간 해상도"])
        with t4: st.json(params["DWI 파라미터"])
        with t5: st.json(params["제조사 파라미터"])

    else:
        t1, t2, t3, t4 = st.tabs([
            T("tab_basic"), T("tab_seq"), T("tab_spatial"), T("tab_dwi")
        ])
        with t1: st.json(params["기본 정보"])
        with t2: st.json(params["시퀀스 파라미터"])
        with t3: st.json(params["공간 해상도"])
        with t4: st.json(params["DWI 파라미터"])

    st.header(T("compare_header"))
    df = create_comparison_table(params, user_baseline, lang)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.header(T("radar_header"))
    radar = create_radar_chart(params, user_baseline, lang)
    if radar:
        st.plotly_chart(radar, use_container_width=True)
    else:
        st.info(T("radar_empty"))

    st.header(T("gauge_header"))
    gauges = create_gauge_charts(params, user_baseline)
    if gauges:
        cols = st.columns(3)
        for i, (name, fig) in enumerate(gauges):
            with cols[i % 3]:
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(T("gauge_empty"))

    st.header(T("ai_header"))
    if not api_key:
        st.error(T("ai_no_key"))
    else:
        if st.button(T("ai_button"), type="primary"):
            with st.spinner(T("ai_spinner")):
                try:
                    result = analyze_with_openai(
                        params, api_key, user_baseline, selected_seq, lang
                    )
                    st.markdown(result)
                    st.download_button(
                        label=T("download_button"),
                        data=result,
                        file_name="mri_analysis_result.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(T("ai_error").format(e))
