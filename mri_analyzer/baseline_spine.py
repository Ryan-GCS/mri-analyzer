BASELINE_SPINE = {
    "T1_CSPINE": {
        "label": "🦴 C-Spine - T1 (경추 구조)",
        "params": {
            "TR (ms)":              {"min": 400,  "max": 800,   "optimal": 600,  "unit": "ms",    "impact": "T1 대조도"},
            "TE (ms)":              {"min": 10,   "max": 25,    "optimal": 15,   "unit": "ms",    "impact": "SNR"},
            "Slice Thickness (mm)": {"min": 2,    "max": 4,     "optimal": 3,    "unit": "mm",    "impact": "해상도"},
            "NEX/NSA":              {"min": 2,    "max": 4,     "optimal": 3,    "unit": "",      "impact": "SNR"},
            "Bandwidth":            {"min": 130,  "max": 200,   "optimal": 150,  "unit": "Hz/px", "impact": "SNR/왜곡"},
            "Matrix Row":           {"min": 256,  "max": 512,   "optimal": 384,  "unit": "",      "impact": "해상도"},
            "FOV (mm)":             {"min": 200,  "max": 260,   "optimal": 220,  "unit": "mm",    "impact": "커버리지"},
        }
    },
    "T2_CSPINE": {
        "label": "🦴 C-Spine - T2 (경추 디스크/척수)",
        "params": {
            "TR (ms)":              {"min": 2500, "max": 5000,  "optimal": 3500, "unit": "ms",    "impact": "T2 대조도"},
            "TE (ms)":              {"min": 80,   "max": 130,   "optimal": 110,  "unit": "ms",    "impact": "T2 대조도"},
            "ETL":                  {"min": 8,    "max": 20,    "optimal": 14,   "unit": "",      "impact": "시간/블러"},
            "Slice Thickness (mm)": {"min": 2,    "max": 4,     "optimal": 3,    "unit": "mm",    "impact": "해상도"},
            "NEX/NSA":              {"min": 2,    "max": 4,     "optimal": 3,    "unit": "",      "impact": "SNR"},
            "Bandwidth":            {"min": 130,  "max": 220,   "optimal": 180,  "unit": "Hz/px", "impact": "SNR"},
            "Matrix Row":           {"min": 256,  "max": 512,   "optimal": 384,  "unit": "",      "impact": "해상도"},
            "FOV (mm)":             {"min": 200,  "max": 260,   "optimal": 220,  "unit": "mm",    "impact": "커버리지"},
        }
    },
    "T1_TSPINE": {
        "label": "🦴 T-Spine - T1 (흉추 구조)",
        "params": {
            "TR (ms)":              {"min": 400,  "max": 800,   "optimal": 600,  "unit": "ms",    "impact": "T1 대조도"},
            "TE (ms)":              {"min": 10,   "max": 25,    "optimal": 15,   "unit": "ms",    "impact": "SNR"},
            "Slice Thickness (mm)": {"min": 3,    "max": 4,     "optimal": 3.5,  "unit": "mm",    "impact": "해상도"},
            "NEX/NSA":              {"min": 2,    "max": 4,     "optimal": 3,    "unit": "",      "impact": "SNR"},
            "Bandwidth":            {"min": 130,  "max": 200,   "optimal": 150,  "unit": "Hz/px", "impact": "SNR/왜곡"},
            "Matrix Row":           {"min": 256,  "max": 512,   "optimal": 384,  "unit": "",      "impact": "해상도"},
            "FOV (mm)":             {"min": 280,  "max": 360,   "optimal": 320,  "unit": "mm",    "impact": "커버리지"},
        }
    },
    "T2_TSPINE": {
        "label": "🦴 T-Spine - T2 (흉추 디스크)",
        "params": {
            "TR (ms)":              {"min": 2500, "max": 5000,  "optimal": 3500, "unit": "ms",    "impact": "T2 대조도"},
            "TE (ms)":              {"min": 80,   "max": 130,   "optimal": 110,  "unit": "ms",    "impact": "T2 대조도"},
            "ETL":                  {"min": 8,    "max": 20,    "optimal": 14,   "unit": "",      "impact": "시간/블러"},
            "Slice Thickness (mm)": {"min": 3,    "max": 4,     "optimal": 3.5,  "unit": "mm",    "impact": "해상도"},
            "NEX/NSA":              {"min": 2,    "max": 4,     "optimal": 3,    "unit": "",      "impact": "SNR"},
            "Bandwidth":            {"min": 130,  "max": 220,   "optimal": 180,  "unit": "Hz/px", "impact": "SNR"},
            "Matrix Row":           {"min": 256,  "max": 512,   "optimal": 384,  "unit": "",      "impact": "해상도"},
            "FOV (mm)":             {"min": 280,  "max": 360,   "optimal": 320,  "unit": "mm",    "impact": "커버리지"},
        }
    },
    "T1_LSPINE": {
        "label": "🦴 L-Spine - T1 (요추 구조)",
        "params": {
            "TR (ms)":              {"min": 400,  "max": 800,   "optimal": 600,  "unit": "ms",    "impact": "T1 대조도"},
            "TE (ms)":              {"min": 10,   "max": 25,    "optimal": 15,   "unit": "ms",    "impact": "SNR"},
            "Slice Thickness (mm)": {"min": 3,    "max": 4,     "optimal": 3.5,  "unit": "mm",    "impact": "해상도"},
            "NEX/NSA":              {"min": 2,    "max": 4,     "optimal": 3,    "unit": "",      "impact": "SNR"},
            "Bandwidth":            {"min": 130,  "max": 200,   "optimal": 150,  "unit": "Hz/px", "impact": "SNR/왜곡"},
            "Matrix Row":           {"min": 256,  "max": 512,   "optimal": 384,  "unit": "",      "impact": "해상도"},
            "FOV (mm)":             {"min": 260,  "max": 320,   "optimal": 280,  "unit": "mm",    "impact": "커버리지"},
        }
    },
    "T2_LSPINE": {
        "label": "🦴 L-Spine - T2 (요추 디스크)",
        "params": {
            "TR (ms)":              {"min": 2500, "max": 5000,  "optimal": 3500, "unit": "ms",    "impact": "T2 대조도"},
            "TE (ms)":              {"min": 80,   "max": 130,   "optimal": 110,  "unit": "ms",    "impact": "T2 대조도"},
            "ETL":                  {"min": 8,    "max": 20,    "optimal": 14,   "unit": "",      "impact": "시간/블러"},
            "Slice Thickness (mm)": {"min": 3,    "max": 4,     "optimal": 3.5,  "unit": "mm",    "impact": "해상도"},
            "NEX/NSA":              {"min": 2,    "max": 4,     "optimal": 3,    "unit": "",      "impact": "SNR"},
            "Bandwidth":            {"min": 130,  "max": 220,   "optimal": 180,  "unit": "Hz/px", "impact": "SNR"},
            "Matrix Row":           {"min": 256,  "max": 512,   "optimal": 384,  "unit": "",      "impact": "해상도"},
            "FOV (mm)":             {"min": 260,  "max": 320,   "optimal": 280,  "unit": "mm",    "impact": "커버리지"},
        }
    },
}
