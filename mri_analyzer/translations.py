TRANSLATIONS = {
    "ko": {
        "app_title":        "🧠 MRI DICOM AI 파라미터 분석기",
        "app_warning":      "이 서비스는 MRI 파라미터 분석 보조 도구입니다. AI 분석 결과는 참고용이며, 최종 판단은 전문 의료진이 해야 합니다. 환자 개인정보가 포함된 DICOM 파일 업로드는 금지됩니다.",
        "seq_select":       "📋 시퀀스 선택",
        "seq_label":        "시퀀스",
        "baseline_setting": "⚙️ 기준값 설정",
        "baseline_caption": "파라미터별 최소/최적/최대값을 설정하세요",
        "seq_params":       "📌 시퀀스 파라미터",
        "mfr_params":       "🏭 제조사 파라미터",
        "mfr_caption":      "제조사별 특수 파라미터",
        "min":              "최소",
        "optimal":          "최적",
        "max":              "최대",
        "upload_header":    "📁 DICOM 파일 업로드",
        "upload_caption":   ".dcm 파일 또는 .zip 압축파일을 지원합니다",
        "upload_label":     "DICOM 파일을 업로드하세요",
        "zip_spinner":      "ZIP 파일 처리 중...",
        "zip_error":        "ZIP 파일에서 DICOM 파일을 찾을 수 없습니다",
        "zip_success":      "{}개의 DICOM 파일을 찾았습니다",
        "zip_select":       "분석할 DICOM 파일 선택",
        "dcm_spinner":      "DICOM 파일 분석 중...",
        "dcm_error":        "DICOM 파일 읽기 오류: {}",
        "mfr_ge":           "🟡 GE 장비가 감지되었습니다",
        "mfr_siemens":      "🔵 Siemens 장비가 감지되었습니다",
        "mfr_philips":      "🟣 Philips 장비가 감지되었습니다",
        "mfr_unknown":      "⚪ 제조사를 감지할 수 없습니다",
        "params_header":    "📊 추출된 파라미터",
        "tab_basic":        "기본 정보",
        "tab_seq":          "시퀀스 파라미터",
        "tab_spatial":      "공간 해상도",
        "tab_dwi":          "DWI",
        "tab_ge":           "GE Specific",
        "tab_siemens":      "Siemens Specific",
        "tab_philips":      "Philips Specific",
        "compare_header":   "📋 파라미터 비교",
        "radar_header":     "🕸️ 레이더 차트",
        "radar_empty":      "레이더 차트를 생성할 수 없습니다",
        "gauge_header":     "🎯 파라미터 적합도",
        "gauge_empty":      "게이지 차트를 생성할 수 없습니다",
        "ai_header":        "🤖 AI 분석",
        "ai_no_key":        "API 키가 없습니다",
        "ai_button":        "🤖 AI 분석 시작",
        "ai_spinner":       "AI 분석 중...",
        "ai_error":         "AI 분석 오류: {}",
        "download_button":  "📄 분석 결과 텍스트 다운로드",
        "pdf_download":     "📄 PDF 리포트 다운로드",
        "prompt_lang":      "반드시 한국어로 답변해주세요.",
        "reference_header": "📚 파라미터 기준값 출처",
        "radar_title": "파라미터 적합도 레이더 차트",
        "reference_body":   """
본 앱의 MRI 시퀀스별 파라미터 기준값은 아래 국제 가이드라인 및 문헌을 바탕으로 설정되었습니다.

📖 **주요 참고 문헌 및 기관**
- ACR (American College of Radiology) MRI 프로토콜 가이드라인
- ISMRM (International Society for Magnetic Resonance in Medicine) 권고안
- ESUR (European Society of Urogenital Radiology) 가이드라인
- RSNA (Radiological Society of North America) 교육 자료
- 각 MRI 제조사 (GE, Siemens, Philips) 공식 프로토콜 매뉴얼
- 국내외 대학병원 임상 프로토콜 (서울대, 연세대, 아산병원 등)
- 다수의 peer-reviewed 논문 (Radiology, JMRI, MRM 등)

⚠️ **주의사항**
- 기준값은 일반적인 임상 권고 범위이며, 장비 사양·환자 상태·임상 목적에 따라 조정이 필요합니다.
- 본 도구는 **보조적 참고용**이며, 최종 프로토콜 결정은 반드시 **전문 방사선사 및 영상의학과 전문의**가 해야 합니다.
- AI 분석 결과는 Groq LLaMA 모델 기반이며, 의료적 진단을 대체하지 않습니다.
""",
    },

    "en": {
        "app_title":        "🧠 MRI DICOM AI Parameter Analyzer",
        "app_warning":      "This service is an MRI parameter analysis assistant tool. AI analysis results are for reference only. Final decisions must be made by a qualified physician. Uploading DICOM files containing patient personal information is prohibited.",
        "seq_select":       "📋 Sequence Selection",
        "seq_label":        "Sequence",
        "baseline_setting": "⚙️ Baseline Settings",
        "baseline_caption": "Set min/optimal/max values for each parameter",
        "seq_params":       "📌 Sequence Parameters",
        "mfr_params":       "🏭 Manufacturer Parameters",
        "mfr_caption":      "Manufacturer-specific parameters",
        "min":              "Min",
        "optimal":          "Optimal",
        "max":              "Max",
        "upload_header":    "📁 DICOM File Upload",
        "upload_caption":   "Supports .dcm files or .zip archives",
        "upload_label":     "Upload DICOM file",
        "zip_spinner":      "Processing ZIP file...",
        "zip_error":        "No DICOM files found in ZIP",
        "zip_success":      "Found {} DICOM files",
        "zip_select":       "Select DICOM file to analyze",
        "dcm_spinner":      "Analyzing DICOM file...",
        "dcm_error":        "DICOM read error: {}",
        "mfr_ge":           "🟡 GE scanner detected",
        "mfr_siemens":      "🔵 Siemens scanner detected",
        "mfr_philips":      "🟣 Philips scanner detected",
        "mfr_unknown":      "⚪ Manufacturer not detected",
        "params_header":    "📊 Extracted Parameters",
        "tab_basic":        "Basic Info",
        "tab_seq":          "Sequence Params",
        "tab_spatial":      "Spatial Resolution",
        "tab_dwi":          "DWI",
        "tab_ge":           "GE Specific",
        "tab_siemens":      "Siemens Specific",
        "tab_philips":      "Philips Specific",
        "compare_header":   "📋 Parameter Comparison",
        "radar_header":     "🕸️ Radar Chart",
        "radar_empty":      "Unable to generate radar chart",
        "gauge_header":     "🎯 Parameter Fitness",
        "gauge_empty":      "Unable to generate gauge charts",
        "ai_header":        "🤖 AI Analysis",
        "ai_no_key":        "No API key found",
        "ai_button":        "🤖 Start AI Analysis",
        "ai_spinner":       "AI analyzing...",
        "ai_error":         "AI analysis error: {}",
        "download_button":  "📄 Download Text Result",
        "pdf_download":     "📄 Download PDF Report",
        "prompt_lang":      "Please respond in English.",
        "reference_header": "📚 Parameter Reference Sources",
        "radar_title": "Parameter Fitness Radar Chart",
        "reference_body":   """
The MRI sequence parameter baselines in this app are based on the following international guidelines and literature.

📖 **Key References & Organizations**
- ACR (American College of Radiology) MRI Protocol Guidelines
- ISMRM (International Society for Magnetic Resonance in Medicine) Recommendations
- ESUR (European Society of Urogenital Radiology) Guidelines
- RSNA (Radiological Society of North America) Educational Materials
- Official Protocol Manuals from MRI Manufacturers (GE, Siemens, Philips)
- Clinical Protocols from Major Academic Medical Centers
- Peer-reviewed Journals (Radiology, JMRI, MRM, etc.)

⚠️ **Disclaimer**
- Baseline values represent general clinical recommendations and may need adjustment based on equipment specifications, patient condition, and clinical purpose.
- This tool is for **reference purposes only**. Final protocol decisions must be made by **qualified MRI technologists and radiologists**.
- AI analysis is powered by Groq LLaMA model and does not replace medical diagnosis.
""",
    },
}

def get_text(lang, key):
    return TRANSLATIONS.get(lang, TRANSLATIONS["ko"]).get(key, key)
