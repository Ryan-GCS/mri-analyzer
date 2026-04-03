BASELINE_PELVIS = {
    "T1_PELVIS": {
        "label": "🦴 Pelvis - T1 (골반 구조)",
        "params": {
            "TR (ms)":              {"min": 400,  "max": 700,   "optimal": 550,  "unit": "ms",    "impact": "T1 대조도"},
            "TE (ms)":              {"min": 10,   "max": 20,    "optimal": 15,   "unit": "ms",    "impact": "SNR"},
            "Slice Thickness (mm)": {"min": 3,    "max": 5,     "optimal": 4,    "unit": "mm",    "impact": "해상도"},
            "NEX/NSA":              {"min": 2,    "max": 4,     "optimal": 2,    "unit": "",      "impact": "SNR"},
            "Bandwidth":            {"min": 130,  "max": 250,   "optimal": 180,  "unit": "Hz/px", "impact": "SNR/왜곡"},
            "Matrix Row":           {"min": 256,  "max": 512,   "optimal": 384,  "unit": "",      "impact": "해상도"},
            "FOV (mm)":             {"min": 280,  "max": 380,   "optimal": 320,  "unit": "mm",    "impact": "커버리지"},
        }
    },
    "T2_PELVIS": {
        "label": "🦴 Pelvis - T2 (전립선/자궁)",
        "params": {
            "TR (ms)":              {"min": 3000, "max": 6000,  "optimal": 4500, "unit": "ms",    "impact": "T2 대조도"},
            "TE (ms)":              {"min": 80,   "max": 130,   "optimal": 100,  "unit": "ms",    "impact": "T2 대조도"},
            "ETL":                  {"min": 8,    "max": 20,    "optimal": 14,   "unit": "",      "impact": "시간/블러"},
            "Slice Thickness (mm)": {"min": 3,    "max": 5,     "optimal": 3.5,  "unit": "mm",    "impact": "해상도"},
            "NEX/NSA":              {"min": 2,    "max": 4,     "optimal": 3,    "unit": "",      "impact": "SNR"},
            "Bandwidth":            {"min": 130,  "max": 220,   "optimal": 180,  "unit": "Hz/px", "impact": "SNR"},
            "Matrix Row":           {"min": 256,  "max": 512,   "optimal": 384,  "unit": "",      "impact": "해상도"},
            "FOV (mm)":             {"min": 180,  "max": 260,   "optimal": 220,  "unit": "mm",    "impact": "커버리지"},
        }
    },
    "DWI_PELVIS": {
        "label": "🦴 Pelvis - DWI (전립선암 감별)",
        "params": {
            "TR (ms)":              {"min": 3000, "max": 6000,  "optimal": 5000, "unit": "ms",    "impact": "SNR"},
            "TE (ms)":              {"min": 60,   "max": 90,    "optimal": 70,   "unit": "ms",    "impact": "SNR"},
            "B-value":              {"min": 0,    "max": 1400,  "optimal": 1000, "unit": "s/mm2", "impact": "확산 대조도"},
            "Slice Thickness (mm)": {"min": 3,    "max": 5,     "optimal": 4,    "unit": "mm",    "impact": "SNR/해상도"},
            "NEX/NSA":              {"min": 4,    "max": 8,     "optimal": 6,    "unit": "",      "impact": "SNR/시간"},
            "Matrix Row":           {"min": 128,  "max": 192,   "optimal": 160,  "unit": "",      "impact": "해상도/왜곡"},
            "FOV (mm)":             {"min": 180,  "max": 260,   "optimal": 220,  "unit": "mm",    "impact": "커버리지"},
        }
    },
}
