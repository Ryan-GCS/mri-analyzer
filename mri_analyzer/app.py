import streamlit as st
from datetime import datetime
from baseline import SEQUENCE_BASELINES, LABEL_EN_MAP, IMPACT_EN_MAP
from baseline_common import MANUFACTURER_PARAMS
from translations import get_text
from functions import (
    extract_dcm_from_zip,
    extract_dicom_params,
    translate_params,
    create_comparison_table,
    create_radar_chart,
    create_gauge_charts,
    analyze_with_openai,
)
from pdf_report import generate_pdf_report, generate_compare_pdf_report

st.set_page_config(
    page_title="MRI DICOM AI Analyzer",
    page_icon="🧠",
    layout="wide"
)

mfr_keys = list(MANUFACTURER_PARAMS.keys())

if "lang" not in st.session_state:
    st.session_state.lang = "ko"
if "mode" not in st.session_state:
    st.session_state.mode = "single"


def translate_label(label, lang):
    if lang == "ko":
        return label
    return LABEL_EN_MAP.get(label, label)


def translate_impact(impact, lang):
    if lang == "ko":
        return impact
    return IMPACT_EN_MAP.get(impact, impact)


def get_section_key(ko_key, lang):
    section_map = {
        "기본 정보":       {"ko": "기본 정보",       "en": "Basic Info"},
        "시퀀스 파라미터": {"ko": "시퀀스 파라미터", "en": "Sequence Params"},
        "공간 해상도":     {"ko": "공간 해상도",     "en": "Spatial Resolution"},
        "DWI 파라미터":    {"ko": "DWI 파라미터",    "en": "DWI Params"},
        "제조사 파라미터": {"ko": "제조사 파라미터", "en": "Manufacturer Params"},
    }
    return section_map.get(ko_key, {}).get(lang, ko_key)


# ── 사이드바 ───────────────────────────────────────────────
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

    # ── API Key 입력 ───────────────────────────────────────
    st.header("🔑 API Key")
    user_api_key = st.text_input(
        "Groq API Key" if lang == "en" else "Groq API Key 입력",
        type="password",
        placeholder="gsk_...",
        help="https://console.groq.com 에서 무료 발급" if lang == "ko"
             else "Get your free key at https://console.groq.com",
        key="user_api_key"
    )
    if lang == "ko":
        st.caption("🔗 [무료 API Key 발급받기](https://console.groq.com)")
        st.caption("⚠️ 키는 저장되지 않으며 세션 종료시 사라집니다.")
    else:
        st.caption("🔗 [Get Free API Key](https://console.groq.com)")
        st.caption("⚠️ Key is not stored and disappears when session ends.")

    # api_key 우선순위: 사용자 입력 > secrets
    try:
        secret_key = st.secrets["groq"]["api_key"]
    except Exception:
        secret_key = ""
    api_key = user_api_key if user_api_key else secret_key

    st.markdown("---")

    st.header("🔀 분석 모드" if lang == "ko" else "🔀 Analysis Mode")
    mode = st.radio(
        "모드 선택" if lang == "ko" else "Select Mode",
        options=["single", "compare"],
        format_func=lambda x: (
            "🔬 단일 영상 분석" if x == "single" else "⚖️ 두 영상 비교"
        ) if lang == "ko" else (
            "🔬 Single Analysis" if x == "single" else "⚖️ Compare Two"
        ),
        key="mode"
    )

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
            with st.expander("📌 " + param_name + " | " + impact_label):
                c1, c2, c3 = st.columns(3)
                mn  = c1.number_input(T("min"),     value=float(values["min"]),     key="min_"  + selected_seq + "_" + param_name)
                opt = c2.number_input(T("optimal"), value=float(values["optimal"]), key="opt_"  + selected_seq + "_" + param_name)
                mx  = c3.number_input(T("max"),     value=float(values["max"]),     key="max_"  + selected_seq + "_" + param_name)
                user_baseline[param_name] = {
                    "min":     mn,
                    "optimal": opt,
                    "max":     mx,
                    "unit":    values["unit"],
                    "impact":  values["impact"],
                }

    st.markdown("---")
    st.subheader(T("mfr_params"))
    st.caption(T("mfr_caption"))
    for param_name, values in baseline_params.items():
        if param_name in mfr_keys:
            impact_label = translate_impact(values["impact"], lang)
            with st.expander("⚙️ " + param_name + " | " + impact_label):
                c1, c2, c3 = st.columns(3)
                mn  = c1.number_input(T("min"),     value=float(values["min"]),     key="min_"  + selected_seq + "_" + param_name)
                opt = c2.number_input(T("optimal"), value=float(values["optimal"]), key="opt_"  + selected_seq + "_" + param_name)
                mx  = c3.number_input(T("max"),     value=float(values["max"]),     key="max_"  + selected_seq + "_" + param_name)
                user_baseline[param_name] = {
                    "min":     mn,
                    "optimal": opt,
                    "max":     mx,
                    "unit":    values["unit"],
                    "impact":  values["impact"],
                }


# ── 공통 함수 ──────────────────────────────────────────────
def load_dicom(uploaded_file, label=""):
    if uploaded_file is None:
        return None, None, None

    if uploaded_file.name.endswith(".zip"):
        with st.spinner(T("zip_spinner")):
            dcm_files = extract_dcm_from_zip(uploaded_file)
            if not dcm_files:
                st.error(T("zip_error"))
                return None, None, None
            st.success(T("zip_success").format(len(dcm_files)))
            file_names    = [f["name"] for f in dcm_files]
            selected_name = st.selectbox(
                T("zip_select"),
                file_names,
                key="zip_select_" + label
            )
            chosen     = next(f for f in dcm_files if f["name"] == selected_name)
            file_bytes = chosen["bytes"]
            filename   = chosen["name"]
    else:
        file_bytes = uploaded_file.read()
        filename   = uploaded_file.name

    with st.spinner(T("dcm_spinner")):
        try:
            params, ds = extract_dicom_params(file_bytes, filename)
            return params, ds, filename
        except Exception as e:
            st.error(T("dcm_error").format(e))
            return None, None, None


def show_mfr_info(params):
    mfr = params["기본 정보"]["감지된 제조사"]
    if mfr == "GE":
        st.info(T("mfr_ge"))
    elif mfr == "SIEMENS":
        st.info(T("mfr_siemens"))
    elif mfr == "PHILIPS":
        st.info(T("mfr_philips"))
    else:
        st.warning(T("mfr_unknown"))
    return mfr


def show_params_tabs(params, mfr, lang, prefix=""):
    params_display = translate_params(params, lang)
    if mfr in ["GE", "SIEMENS", "PHILIPS"]:
        tab_mfr = {
            "GE":      T("tab_ge"),
            "SIEMENS": T("tab_siemens"),
            "PHILIPS": T("tab_philips"),
        }[mfr]
        t1, t2, t3, t4, t5 = st.tabs([
            T("tab_basic"), T("tab_seq"),
            T("tab_spatial"), T("tab_dwi"), tab_mfr
        ])
        with t1: st.json(params_display[get_section_key("기본 정보",       lang)])
        with t2: st.json(params_display[get_section_key("시퀀스 파라미터", lang)])
        with t3: st.json(params_display[get_section_key("공간 해상도",     lang)])
        with t4: st.json(params_display[get_section_key("DWI 파라미터",    lang)])
        with t5: st.json(params_display[get_section_key("제조사 파라미터", lang)])
    else:
        t1, t2, t3, t4 = st.tabs([
            T("tab_basic"), T("tab_seq"),
            T("tab_spatial"), T("tab_dwi")
        ])
        with t1: st.json(params_display[get_section_key("기본 정보",       lang)])
        with t2: st.json(params_display[get_section_key("시퀀스 파라미터", lang)])
        with t3: st.json(params_display[get_section_key("공간 해상도",     lang)])
        with t4: st.json(params_display[get_section_key("DWI 파라미터",    lang)])
T = lambda key: get_text(lang, key)

st.title(T("app_title"))
st.warning(T("app_warning"))

# ── API Key 안내 배너 ──────────────────────────────────────
if not api_key:
    if lang == "ko":
        st.error("⚠️ 좌측 사이드바에서 Groq API Key를 입력해주세요! [무료 발급](https://console.groq.com)")
    else:
        st.error("⚠️ Please enter your Groq API Key in the left sidebar! [Get Free Key](https://console.groq.com)")
else:
    if lang == "ko":
        st.success("✅ API Key가 입력되었습니다. AI 분석을 사용할 수 있습니다.")
    else:
        st.success("✅ API Key entered. AI analysis is available.")

with st.expander(T("reference_header")):
    st.markdown(T("reference_body"))
st.markdown("---")


# ════════════════════════════════════════════════════════════
# 🔬 단일 영상 분석 모드
# ════════════════════════════════════════════════════════════
if mode == "single":
    st.header(T("upload_header"))
    st.caption(T("upload_caption"))

    uploaded_file = st.file_uploader(T("upload_label"), type=None, key="single_upload")

    if uploaded_file:
        params, ds, filename = load_dicom(uploaded_file, "A")
        if params:
            mfr = show_mfr_info(params)

            st.header(T("params_header"))
            show_params_tabs(params, mfr, lang, prefix="single")

            st.header(T("compare_header"))
            df = create_comparison_table(params, user_baseline, lang)
            st.dataframe(df, use_container_width=True, hide_index=True)

            st.header(T("radar_header"))
            st.caption(
                "파라미터 적합도 레이더 차트" if lang == "ko"
                else "Parameter Fitness Radar Chart"
            )
            radar = create_radar_chart(params, user_baseline, lang)
            if radar:
                st.plotly_chart(radar, use_container_width=True, key="radar_single")
            else:
                st.info(T("radar_empty"))

            st.header(T("gauge_header"))
            gauges = create_gauge_charts(params, user_baseline)
            if gauges:
                cols = st.columns(3)
                for i, (name, fig) in enumerate(gauges):
                    with cols[i % 3]:
                        st.plotly_chart(
                            fig,
                            use_container_width=True,
                            key="gauge_single_" + str(i) + "_" + name
                        )
            else:
                st.info(T("gauge_empty"))

            st.header(T("ai_header"))
            if not api_key:
                if lang == "ko":
                    st.error("⚠️ 사이드바에서 Groq API Key를 먼저 입력해주세요!")
                else:
                    st.error("⚠️ Please enter your Groq API Key in the sidebar first!")
            else:
                if st.button(T("ai_button"), type="primary"):
                    with st.spinner(T("ai_spinner")):
                        try:
                            result = analyze_with_openai(
                                params, api_key, user_baseline, selected_seq, lang
                            )
                            st.markdown(result)
                            st.download_button(
                                label     = T("download_button"),
                                data      = result,
                                file_name = "mri_analysis_result.txt",
                                mime      = "text/plain",
                                key       = "dl_txt_single"
                            )
                            pdf_buffer = generate_pdf_report(
                                params        = params,
                                user_baseline = user_baseline,
                                df            = df,
                                radar_fig     = radar,
                                gauge_figs    = gauges if gauges else [],
                                ai_result     = result,
                                selected_seq  = selected_seq,
                                lang          = lang,
                            )
                            st.download_button(
                                label     = T("pdf_download"),
                                data      = pdf_buffer,
                                file_name = "MRI_Report_" + datetime.now().strftime("%Y%m%d_%H%M") + ".pdf",
                                mime      = "application/pdf",
                                key       = "dl_pdf_single"
                            )
                        except Exception as e:
                            st.error(T("ai_error").format(e))


# ════════════════════════════════════════════════════════════
# ⚖️ 두 영상 비교 모드
# ════════════════════════════════════════════════════════════
elif mode == "compare":
    if lang == "ko":
        st.header("⚖️ 두 영상 비교 분석")
        label_a  = "📁 영상 A 업로드"
        label_b  = "📁 영상 B 업로드"
        name_a   = "영상 A"
        name_b   = "영상 B"
        diff_hdr = "📊 파라미터 비교표"
        diff_cap = "차이값 : 양수(+) = B가 높음 / 음수(-) = B가 낮음"
        radar_hdr= "🕸️ 레이더 차트 비교"
        gauge_hdr= "🎯 게이지 차트 비교"
        ai_hdr   = "🤖 AI 비교 분석"
        ai_btn   = "🤖 AI 비교 분석 시작"
    else:
        st.header("⚖️ Compare Two MRI Images")
        label_a  = "📁 Upload Image A"
        label_b  = "📁 Upload Image B"
        name_a   = "Image A"
        name_b   = "Image B"
        diff_hdr = "📊 Parameter Comparison Table"
        diff_cap = "Diff : positive(+) = B higher / negative(-) = B lower"
        radar_hdr= "🕸️ Radar Chart Comparison"
        gauge_hdr= "🎯 Gauge Chart Comparison"
        ai_hdr   = "🤖 AI Comparison Analysis"
        ai_btn   = "🤖 Start AI Comparison"

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader(name_a)
        upload_a = st.file_uploader(label_a, type=None, key="compare_a")

    with col_b:
        st.subheader(name_b)
        upload_b = st.file_uploader(label_b, type=None, key="compare_b")

    if upload_a and upload_b:
        with col_a:
            params_a, ds_a, filename_a = load_dicom(upload_a, "A")
        with col_b:
            params_b, ds_b, filename_b = load_dicom(upload_b, "B")

        if params_a and params_b:

            # ── 제조사 정보 ──────────────────────────────────
            with col_a:
                mfr_a = show_mfr_info(params_a)
            with col_b:
                mfr_b = show_mfr_info(params_b)

            # ── 파라미터 탭 ──────────────────────────────────
            st.markdown("---")
            if lang == "ko":
                st.subheader("📋 파라미터 상세")
            else:
                st.subheader("📋 Parameter Details")

            tab_a, tab_b = st.tabs([
                "🔬 " + name_a + " : " + filename_a,
                "🔬 " + name_b + " : " + filename_b,
            ])
            with tab_a:
                show_params_tabs(params_a, mfr_a, lang, prefix="cmp_a")
            with tab_b:
                show_params_tabs(params_b, mfr_b, lang, prefix="cmp_b")

            # ── 파라미터 비교표 ──────────────────────────────
            st.markdown("---")
            st.subheader(diff_hdr)
            st.caption(diff_cap)

            import pandas as pd
            df_a = create_comparison_table(params_a, user_baseline, lang)
            df_b = create_comparison_table(params_b, user_baseline, lang)

            if df_a is not None and df_b is not None:
                param_col = df_a.columns[0]
                val_col   = df_a.columns[1]

                def calc_diff(a, b):
                    try:
                        diff = float(b) - float(a)
                        if diff > 0:
                            return "🔺 +" + str(round(diff, 2))
                        elif diff < 0:
                            return "🔻 " + str(round(diff, 2))
                        else:
                            return "➖ 0"
                    except Exception:
                        return "-"

                df_merge = pd.DataFrame()
                df_merge[param_col]        = df_a[param_col]
                df_merge[name_a + " 값"]   = df_a[val_col]
                df_merge[name_b + " 값"]   = df_b[val_col]
                df_merge["차이 / Diff"]    = [
                    calc_diff(a, b)
                    for a, b in zip(df_a[val_col], df_b[val_col])
                ]
                df_merge[name_a + " 상태"] = df_a[df_a.columns[-2]]
                df_merge[name_b + " 상태"] = df_b[df_b.columns[-2]]

                st.dataframe(df_merge, use_container_width=True, hide_index=True)

            # ── 레이더 차트 비교 ─────────────────────────────
            st.markdown("---")
            st.subheader(radar_hdr)

            radar_a = create_radar_chart(params_a, user_baseline, lang)
            radar_b = create_radar_chart(params_b, user_baseline, lang)

            rc1, rc2 = st.columns(2)
            with rc1:
                st.caption("🔵 " + name_a)
                if radar_a:
                    st.plotly_chart(
                        radar_a,
                        use_container_width=True,
                        key="radar_compare_a"
                    )
                else:
                    st.info(T("radar_empty"))
            with rc2:
                st.caption("🟠 " + name_b)
                if radar_b:
                    st.plotly_chart(
                        radar_b,
                        use_container_width=True,
                        key="radar_compare_b"
                    )
                else:
                    st.info(T("radar_empty"))

            # ── 게이지 차트 비교 ─────────────────────────────
            st.markdown("---")
            st.subheader(gauge_hdr)

            gauges_a = create_gauge_charts(params_a, user_baseline)
            gauges_b = create_gauge_charts(params_b, user_baseline)

            if gauges_a and gauges_b:
                for i in range(min(len(gauges_a), len(gauges_b))):
                    name_ga, fig_ga = gauges_a[i]
                    name_gb, fig_gb = gauges_b[i]
                    g1, g2 = st.columns(2)
                    with g1:
                        st.plotly_chart(
                            fig_ga,
                            use_container_width=True,
                            key="gauge_a_" + str(i) + "_" + name_ga
                        )
                    with g2:
                        st.plotly_chart(
                            fig_gb,
                            use_container_width=True,
                            key="gauge_b_" + str(i) + "_" + name_gb
                        )
            else:
                if lang == "ko":
                    st.info("게이지 차트를 생성할 수 없습니다.")
                else:
                    st.info("Cannot generate gauge charts.")

            # ── AI 비교 분석 ─────────────────────────────────
            st.markdown("---")
            st.subheader(ai_hdr)

            if not api_key:
                if lang == "ko":
                    st.error("⚠️ 사이드바에서 Groq API Key를 먼저 입력해주세요!")
                else:
                    st.error("⚠️ Please enter your Groq API Key in the sidebar first!")
            else:
                if st.button(ai_btn, type="primary"):
                    with st.spinner(T("ai_spinner")):
                        try:
                            if lang == "ko":
                                compare_prompt = (
                                    "다음은 두 MRI 영상의 파라미터입니다. 두 영상을 비교 분석해주세요.\n\n"
                                    "[영상 A : " + filename_a + "]\n"
                                    "시퀀스: " + selected_seq + "\n"
                                    "파라미터: " + str(params_a.get("시퀀스 파라미터", {})) + "\n"
                                    "공간해상도: " + str(params_a.get("공간 해상도", {})) + "\n\n"
                                    "[영상 B : " + filename_b + "]\n"
                                    "시퀀스: " + selected_seq + "\n"
                                    "파라미터: " + str(params_b.get("시퀀스 파라미터", {})) + "\n"
                                    "공간해상도: " + str(params_b.get("공간 해상도", {})) + "\n\n"
                                    "다음 항목으로 비교 분석해주세요:\n"
                                    "## 1. 주요 파라미터 차이점\n"
                                    "## 2. 영상 품질 관점에서의 차이\n"
                                    "## 3. 어떤 영상이 더 적합한지 (이유 포함)\n"
                                    "## 4. 개선 권고사항\n"
                                )
                            else:
                                compare_prompt = (
                                    "Compare the following two MRI image parameters:\n\n"
                                    "[Image A : " + filename_a + "]\n"
                                    "Sequence: " + selected_seq + "\n"
                                    "Parameters: " + str(params_a.get("시퀀스 파라미터", {})) + "\n"
                                    "Spatial: " + str(params_a.get("공간 해상도", {})) + "\n\n"
                                    "[Image B : " + filename_b + "]\n"
                                    "Sequence: " + selected_seq + "\n"
                                    "Parameters: " + str(params_b.get("시퀀스 파라미터", {})) + "\n"
                                    "Spatial: " + str(params_b.get("공간 해상도", {})) + "\n\n"
                                    "Please analyze:\n"
                                    "## 1. Key parameter differences\n"
                                    "## 2. Image quality differences\n"
                                    "## 3. Which image is more suitable (with reasons)\n"
                                    "## 4. Recommendations for improvement\n"
                                )

                            result = analyze_with_openai(
                                params_a, api_key,
                                user_baseline, selected_seq, lang,
                                custom_prompt=compare_prompt
                            )

                            # ① AI 결과 출력
                            st.markdown(result)

                            # ② 텍스트 다운로드
                            st.download_button(
                                label     = T("download_button"),
                                data      = result,
                                file_name = "mri_compare_result.txt",
                                mime      = "text/plain",
                                key       = "dl_txt_compare"
                            )

                            # ③ PDF 다운로드
                            cmp_pdf = generate_compare_pdf_report(
                                params_a      = params_a,
                                params_b      = params_b,
                                filename_a    = filename_a,
                                filename_b    = filename_b,
                                user_baseline = user_baseline,
                                df_a          = df_a,
                                df_b          = df_b,
                                radar_fig_a   = radar_a,
                                radar_fig_b   = radar_b,
                                ai_result     = result,
                                selected_seq  = selected_seq,
                                lang          = lang,
                            )
                            st.download_button(
                                label     = T("pdf_download"),
                                data      = cmp_pdf,
                                file_name = "MRI_Compare_Report_" + datetime.now().strftime("%Y%m%d_%H%M") + ".pdf",
                                mime      = "application/pdf",
                                key       = "dl_pdf_compare"
                            )

                        except Exception as e:
                            st.error(T("ai_error").format(e))

