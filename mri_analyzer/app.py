import streamlit as st
from baseline import SEQUENCE_BASELINES
from baseline_common import MANUFACTURER_PARAMS
from functions import (
    extract_dcm_from_zip,
    extract_dicom_params,
    create_comparison_table,
    create_radar_chart,
    create_gauge_charts,
    analyze_with_openai,
)

st.set_page_config(page_title="MRI DICOM AI 분석기", page_icon="🧠", layout="wide")
st.title("🧠 MRI DICOM AI 파라미터 분석기")
st.markdown("---")

mfr_keys = list(MANUFACTURER_PARAMS.keys())

with st.sidebar:
    st.header("⚙️ 설정")
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        help="https://console.groq.com 에서 무료 발급"
    )
    st.caption("🆓 Groq API는 완전 무료입니다")
    st.markdown("---")

    st.header("🎯 시퀀스 선택")
    seq_options = {v["label"]: k for k, v in SEQUENCE_BASELINES.items()}
    selected_label = st.selectbox("분석할 시퀀스", list(seq_options.keys()))
    selected_seq = seq_options[selected_label]
    baseline_params = SEQUENCE_BASELINES[selected_seq]["params"]
    st.markdown("---")

    st.header("📊 기준값 설정")
    st.caption("최소 / 최적 / 최대값 수정 가능")

    user_baseline = {}

    # 시퀀스 기본 파라미터
    st.subheader("🔬 시퀀스 파라미터")
    for param_name, values in baseline_params.items():
        if param_name not in mfr_keys:
            with st.expander(f"📌 {param_name} | {values['impact']}"):
                c1, c2, c3 = st.columns(3)
                mn  = c1.number_input("최소", value=float(values["min"]),     key=f"min_{param_name}")
                opt = c2.number_input("최적", value=float(values["optimal"]), key=f"opt_{param_name}")
                mx  = c3.number_input("최대", value=float(values["max"]),     key=f"max_{param_name}")
                user_baseline[param_name] = {
                    "min":     mn,
                    "optimal": opt,
                    "max":     mx,
                    "unit":    values["unit"],
                    "impact":  values["impact"]
                }

    st.markdown("---")

    # 제조사 파라미터
    st.subheader("🏭 제조사 파라미터")
    st.caption("GE / Siemens / Philips 공통")
    for param_name, values in baseline_params.items():
        if param_name in mfr_keys:
            with st.expander(f"⚙️ {param_name} | {values['impact']}"):
                c1, c2, c3 = st.columns(3)
                mn  = c1.number_input("최소", value=float(values["min"]),     key=f"min_{param_name}")
                opt = c2.number_input("최적", value=float(values["optimal"]), key=f"opt_{param_name}")
                mx  = c3.number_input("최대", value=float(values["max"]),     key=f"max_{param_name}")
                user_baseline[param_name] = {
                    "min":     mn,
                    "optimal": opt,
                    "max":     mx,
                    "unit":    values["unit"],
                    "impact":  values["impact"]
                }

if not api_key:
    st.warning("⚠️ 왼쪽 사이드바에 Groq API Key를 입력해주세요")
    st.markdown("""
    ### Groq API Key 발급 방법
    1. [https://console.groq.com](https://console.groq.com) 접속
    2. 구글 계정으로 가입
    3. API Keys 메뉴에서 Create API Key 클릭
    4. 발급된 키 복사 후 위 입력창에 붙여넣기
    """)

st.header("📁 DICOM 파일 업로드")
st.caption("✅ .dcm 파일 또는 .zip 압축파일 모두 지원")

uploaded_file = st.file_uploader(
    "DICOM 파일을 드래그하거나 클릭하여 업로드",
    type=None
)

if uploaded_file:
    if uploaded_file.name.endswith(".zip"):
        with st.spinner("📦 ZIP 압축 해제 중..."):
            dcm_files = extract_dcm_from_zip(uploaded_file)
            if not dcm_files:
                st.error("❌ ZIP 안에서 DICOM 파일을 찾지 못했습니다")
                st.stop()
            st.success(f"✅ DICOM 파일 {len(dcm_files)}개 발견!")
            file_names = [f["name"] for f in dcm_files]
            selected_name = st.selectbox("분석할 파일 선택", file_names)
            chosen = next(f for f in dcm_files if f["name"] == selected_name)
            file_bytes = chosen["bytes"]
            filename = chosen["name"]
    else:
        file_bytes = uploaded_file.read()
        filename = uploaded_file.name

    with st.spinner("📂 DICOM 파일 읽는 중..."):
        try:
            params, ds = extract_dicom_params(file_bytes, filename)
        except Exception as e:
            st.error(f"❌ DICOM 오류: {e}")
            st.stop()

    # 제조사 감지 배너
    mfr = params["기본 정보"]["감지된 제조사"]
    if mfr == "GE":
        st.info("🔵 GE 장비 감지됨 - GE 전용 파라미터 추출 완료")
    elif mfr == "SIEMENS":
        st.info("🔴 Siemens 장비 감지됨 - iPAT 등 전용 파라미터 추출 완료")
    elif mfr == "PHILIPS":
        st.info("🟡 Philips 장비 감지됨 - SENSE 등 전용 파라미터 추출 완료")
    else:
        st.warning("⚠️ 제조사를 감지하지 못했습니다 - 공통 파라미터만 표시")

    # 파라미터 탭
    st.header("📊 추출된 파라미터")

    if mfr == "GE":
        t1, t2, t3, t4, t5 = st.tabs([
            "기본정보", "시퀀스파라미터", "공간해상도", "DWI", "GE전용"
        ])
        with t1: st.json(params["기본 정보"])
        with t2: st.json(params["시퀀스 파라미터"])
        with t3: st.json(params["공간 해상도"])
        with t4: st.json(params["DWI 파라미터"])
        with t5: st.json(params["제조사 파라미터"])

    elif mfr == "SIEMENS":
        t1, t2, t3, t4, t5 = st.tabs([
            "기본정보", "시퀀스파라미터", "공간해상도", "DWI", "Siemens전용"
        ])
        with t1: st.json(params["기본 정보"])
        with t2: st.json(params["시퀀스 파라미터"])
        with t3: st.json(params["공간 해상도"])
        with t4: st.json(params["DWI 파라미터"])
        with t5: st.json(params["제조사 파라미터"])

    elif mfr == "PHILIPS":
        t1, t2, t3, t4, t5 = st.tabs([
            "기본정보", "시퀀스파라미터", "공간해상도", "DWI", "Philips전용"
        ])
        with t1: st.json(params["기본 정보"])
        with t2: st.json(params["시퀀스 파라미터"])
        with t3: st.json(params["공간 해상도"])
        with t4: st.json(params["DWI 파라미터"])
        with t5: st.json(params["제조사 파라미터"])

    else:
        t1, t2, t3, t4 = st.tabs([
            "기본정보", "시퀀스파라미터", "공간해상도", "DWI"
        ])
        with t1: st.json(params["기본 정보"])
        with t2: st.json(params["시퀀스 파라미터"])
        with t3: st.json(params["공간 해상도"])
        with t4: st.json(params["DWI 파라미터"])

    # 비교표
    st.header("📋 기준값 비교표")
    df = create_comparison_table(params, user_baseline)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # 레이더 차트
    st.header("📡 파라미터 레이더 차트")
    radar = create_radar_chart(params, user_baseline)
    if radar:
        st.plotly_chart(radar, use_container_width=True)
    else:
        st.info("차트를 그릴 수 있는 수치 파라미터가 없습니다")

    # 게이지 차트
    st.header("🎯 파라미터별 게이지")
    gauges = create_gauge_charts(params, user_baseline)
    if gauges:
        cols = st.columns(3)
        for i, (name, fig) in enumerate(gauges):
            with cols[i % 3]:
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("게이지를 그릴 수 있는 수치 파라미터가 없습니다")

    # AI 분석
    st.header("🤖 AI 분석 결과")
    if not api_key:
        st.warning("⚠️ API Key를 입력해야 AI 분석이 가능합니다")
    else:
        if st.button("🔍 AI 분석 시작", type="primary"):
            with st.spinner("AI 분석 중... (10~20초 소요)"):
                try:
                    result = analyze_with_openai(
                        params, api_key, user_baseline, selected_seq
                    )
                    st.markdown(result)
                    st.download_button(
                        label="📥 분석 결과 다운로드",
                        data=result,
                        file_name="mri_analysis_result.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"❌ AI 분석 오류: {e}")
