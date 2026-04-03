# 모든 바디파트에 공통으로 추가될 제조사 파라미터
MANUFACTURER_PARAMS = {
    # 공통
    "Parallel Imaging Factor": {"min": 1,   "max": 4,   "optimal": 2,   "unit": "",      "impact": "SNR/시간"},
    "SAR":                     {"min": 0,   "max": 3.2, "optimal": 1.5, "unit": "W/kg",  "impact": "환자 안전"},
    # GE
    "ARC/ASSET Factor":        {"min": 1,   "max": 4,   "optimal": 2,   "unit": "",      "impact": "SNR/시간(GE)"},
    "Noise Reduction Factor":  {"min": 0,   "max": 5,   "optimal": 2,   "unit": "",      "impact": "SNR(GE)"},
    # Siemens
    "iPAT Factor":             {"min": 1,   "max": 4,   "optimal": 2,   "unit": "",      "impact": "SNR/시간(Siemens)"},
    "GRAPPA Factor":           {"min": 1,   "max": 4,   "optimal": 2,   "unit": "",      "impact": "SNR/시간(Siemens)"},
    "BW per Pixel Phase":      {"min": 10,  "max": 50,  "optimal": 20,  "unit": "Hz/px", "impact": "왜곡(Siemens)"},
    # Philips
    "SENSE Factor":            {"min": 1,   "max": 4,   "optimal": 2,   "unit": "",      "impact": "SNR/시간(Philips)"},
    "Water Fat Shift":         {"min": 0.3, "max": 1.0, "optimal": 0.5, "unit": "px",    "impact": "화학적이동(Philips)"},
    "Prepulse Delay":          {"min": 100, "max": 500, "optimal": 300, "unit": "ms",    "impact": "조직억제(Philips)"},
}
