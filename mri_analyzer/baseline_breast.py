BASELINE_BREAST = {
    "T1_BREAST": {
        "label": "🎀 Breast - T1 (유방 구조)",
        "params": {
            "TR (ms)":              {"min": 400,  "max": 700,   "optimal": 550,  "unit": "ms",    "impact": "T1 대조도"},
            "TE (ms)":              {"min": 10,   "max": 20,    "optimal": 15,   "unit": "ms",    "impact": "SNR"},
            "Flip Angle (°)":       {"min": 10,   "max": 20,    "optimal": 15,   "unit": "deg",   "impact": "T1 대조도"},
            "Slice Thickness (mm)": {"min": 1,    "max": 3,     "optimal": 2,    "unit": "mm",    "impact": "해상도"},
            "NEX/NSA":              {"min": 1,    "max": 2,     "optimal": 1,    "unit": "",      "impact": "SNR/시간"},
            "Bandwidth":            {"min": 400,  "max": 800,   "optimal": 600,  "unit": "Hz/px", "impact": "SNR/왜곡"},
            "Matrix Row":           {"min": 256,  "max": 512,   "optimal": 384,  "unit": "",      "impact": "해상도"},
            "FOV (mm)":             {"min": 280,  "max": 380,   "optimal": 320,  "unit": "mm",    "impact": "커버리지"},
        }
    },
    "T2_BREAST": {
        "label": "🎀 Breast - T2 (낭종/부종)",
        "params": {
            "TR (ms)":              {"min": 3000, "max": 6000,  "optimal": 4500, "unit": "ms",    "impact": "T2 대조도"},
            "TE (ms)":              {"min": 80,   "max": 120,   "optimal": 100,  "unit": "ms",    "impact": "T2 대조도"},
            "ETL":                  {"min": 8,    "max": 20,    "optimal": 14,   "unit": "",      "impact": "시간/블러"},
            "Slice Thickness (mm)": {"min": 2,    "max": 4,     "optimal": 3,    "unit": "mm",    "impact": "해상도"},
            "NEX/NSA":              {"min": 1,    "max": 3,     "optimal": 2,    "unit": "",      "impact": "SNR/시간"},
            "Bandwidth":            {"min": 200,  "max": 500,   "optimal": 350,  "unit": "Hz/px", "impact": "SNR"},
            "Matrix Row":           {"min": 256,  "max": 512,   "optimal": 384,  "unit": "",      "impact": "해상도"},
            "FOV (mm)":             {"min": 280,  "max": 380,   "optimal": 320,  "unit": "mm",    "impact": "커버리지"},
        }
    },
    "DCE_BREAST": {
        "label": "🎀 Breast - DCE (조영증강/종양)",
        "params": {
            "TR (ms)":              {"min": 4,    "max": 8,     "optimal": 5,    "unit": "ms",    "impact": "시간 해상도"},
            "TE (ms)":              {"min": 1,    "max": 3,     "optimal": 2,    "unit": "ms",    "impact": "SNR"},
            "Flip Angle (°)":       {"min": 10,   "max": 20,    "optimal": 15,   "unit": "deg",   "impact": "T1 대조도"},
            "Slice Thickness (mm)": {"min": 1,    "max": 3,     "optimal": 2,    "unit": "mm",    "impact": "해상도"},
            "NEX/NSA":              {"min": 1,    "max": 1,     "optimal": 1,    "unit": "",      "impact": "시간 해상도"},
            "Matrix Row":           {"min": 256,  "max": 512,   "optimal": 384,  "unit": "",      "impact": "해상도"},
            "FOV (mm)":             {"min": 280,  "max": 380,   "optimal": 320,  "unit": "mm",    "impact": "커버리지"},
        }
    },
    "DWI_BREAST": {
        "label": "🎀 Breast - DWI (악성 감별)",
        "params": {
            "TR (ms)":              {"min": 4000, "max": 8000,  "optimal": 6000, "unit": "ms",    "impact": "SNR"},
            "TE (ms)":              {"min": 60,   "max": 90,    "optimal": 70,   "unit": "ms",    "impact": "SNR"},
            "B-value":              {"min": 0,    "max": 1000,  "optimal": 800,  "unit": "s/mm2", "impact": "확산 대조도"},
            "Slice Thickness (mm)": {"min": 3,    "max": 5,     "optimal": 4,    "unit": "mm",    "impact": "SNR/해상도"},
            "NEX/NSA":              {"min": 4,    "max": 8,     "optimal": 6,    "unit": "",      "impact": "SNR/시간"},
            "Matrix Row":           {"min": 128,  "max": 192,   "optimal": 160,  "unit": "",      "impact": "해상도/왜곡"},
            "FOV (mm)":             {"min": 280,  "max": 380,   "optimal": 320,  "unit": "mm",    "impact": "커버리지"},
        }
    },
}
