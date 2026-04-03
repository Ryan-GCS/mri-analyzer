BASELINE_ABDOMEN = {
    "T1_ABDOMEN": {
        "label": "🫁 Abdomen - T1 (복부 구조)",
        "params": {
            "TR (ms)":              {"min": 150,  "max": 300,   "optimal": 200,  "unit": "ms",    "impact": "T1 대조도"},
            "TE (ms)":              {"min": 1,    "max": 5,     "optimal": 2,    "unit": "ms",    "impact": "SNR"},
            "Flip Angle (°)":       {"min": 10,   "max": 20,    "optimal": 15,   "unit": "deg",   "impact": "T1 대조도"},
            "Slice Thickness (mm)": {"min": 3,    "max": 6,     "optimal": 5,    "unit": "mm",    "impact": "해상도/SNR"},
            "NEX/NSA":              {"min": 1,    "max": 2,     "optimal": 1,    "unit": "",      "impact": "SNR/시간"},
            "Bandwidth":            {"min": 400,  "max": 800,   "optimal": 600,  "unit": "Hz/px", "impact": "호흡 아티팩트"},
            "Matrix Row":           {"min": 192,  "max": 384,   "optimal": 256,  "unit": "",      "impact": "해상도"},
            "FOV (mm)":             {"min": 320,  "max": 420,   "optimal": 380,  "unit": "mm",    "impact": "커버리지"},
        }
    },
    "T2_ABDOMEN": {
        "label": "🫁 Abdomen - T2 (간/담도/췌장)",
        "params": {
            "TR (ms)":              {"min": 1000, "max": 3000,  "optimal": 2000, "unit": "ms",    "impact": "T2 대조도"},
            "TE (ms)":              {"min": 80,   "max": 120,   "optimal": 100,  "unit": "ms",    "impact": "T2 대조도"},
            "ETL":                  {"min": 16,   "max": 32,    "optimal": 24,   "unit": "",      "impact": "시간/블러"},
            "Slice Thickness (mm)": {"min": 4,    "max": 7,     "optimal": 5,    "unit": "mm",    "impact": "해상도/SNR"},
            "NEX/NSA":              {"min": 1,    "max": 4,     "optimal": 2,    "unit": "",      "impact": "SNR/시간"},
            "Bandwidth":            {"min": 300,  "max": 600,   "optimal": 400,  "unit": "Hz/px", "impact": "SNR"},
            "Matrix Row":           {"min": 192,  "max": 384,   "optimal": 256,  "unit": "",      "impact": "해상도"},
            "FOV (mm)":             {"min": 320,  "max": 420,   "optimal": 380,  "unit": "mm",    "impact": "커버리지"},
        }
    },
    "DWI_ABDOMEN": {
        "label": "🫁 Abdomen - DWI (종양 감별)",
        "params": {
            "TR (ms)":              {"min": 3000, "max": 6000,  "optimal": 5000, "unit": "ms",    "impact": "SNR"},
            "TE (ms)":              {"min": 50,   "max": 80,    "optimal": 60,   "unit": "ms",    "impact": "SNR"},
            "B-value":              {"min": 0,    "max": 800,   "optimal": 800,  "unit": "s/mm2", "impact": "확산 대조도"},
            "Slice Thickness (mm)": {"min": 4,    "max": 7,     "optimal": 5,    "unit": "mm",    "impact": "SNR/해상도"},
            "NEX/NSA":              {"min": 2,    "max": 6,     "optimal": 4,    "unit": "",      "impact": "SNR/시간"},
            "Matrix Row":           {"min": 128,  "max": 192,   "optimal": 160,  "unit": "",      "impact": "해상도/왜곡"},
            "FOV (mm)":             {"min": 320,  "max": 420,   "optimal": 380,  "unit": "mm",    "impact": "커버리지"},
        }
    },
    "MRCP": {
        "label": "🫁 Abdomen - MRCP (담도/췌관)",
        "params": {
            "TR (ms)":              {"min": 4000, "max": 8000,  "optimal": 6000, "unit": "ms",    "impact": "T2 대조도"},
            "TE (ms)":              {"min": 500,  "max": 1000,  "optimal": 700,  "unit": "ms",    "impact": "담즙 대조도"},
            "ETL":                  {"min": 40,   "max": 100,   "optimal": 60,   "unit": "",      "impact": "시간/블러"},
            "Slice Thickness (mm)": {"min": 30,   "max": 60,    "optimal": 40,   "unit": "mm",    "impact": "투영 두께"},
            "NEX/NSA":              {"min": 1,    "max": 2,     "optimal": 1,    "unit": "",      "impact": "SNR/시간"},
            "Matrix Row":           {"min": 256,  "max": 512,   "optimal": 384,  "unit": "",      "impact": "해상도"},
            "FOV (mm)":             {"min": 300,  "max": 400,   "optimal": 350,  "unit": "mm",    "impact": "커버리지"},
        }
    },
}
