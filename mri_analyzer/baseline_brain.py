BASELINE_BRAIN = {
    "T1_BRAIN": {
        "label": "🧠 Brain - T1 (뇌 구조)",
        "params": {
            "TR (ms)":              {"min": 400,  "max": 700,   "optimal": 550,  "unit": "ms",    "impact": "T1 대조도"},
            "TE (ms)":              {"min": 10,   "max": 20,    "optimal": 15,   "unit": "ms",    "impact": "SNR"},
            "Flip Angle (°)":       {"min": 70,   "max": 90,    "optimal": 80,   "unit": "deg",   "impact": "T1 대조도"},
            "Slice Thickness (mm)": {"min": 3,    "max": 5,     "optimal": 4,    "unit": "mm",    "impact": "해상도/SNR"},
            "NEX/NSA":              {"min": 1,    "max": 4,     "optimal": 2,    "unit": "",      "impact": "SNR/시간"},
            "Bandwidth":            {"min": 130,  "max": 200,   "optimal": 150,  "unit": "Hz/px", "impact": "SNR/왜곡"},
            "Matrix Row":           {"min": 256,  "max": 512,   "optimal": 384,  "unit": "",      "impact": "해상도"},
            "FOV (mm)":             {"min": 200,  "max": 240,   "optimal": 220,  "unit": "mm",    "impact": "커버리지"},
        }
    },
    "T2_BRAIN": {
        "label": "🧠 Brain - T2 (부종/병변)",
        "params": {
            "TR (ms)":              {"min": 3000, "max": 6000,  "optimal": 4500, "unit": "ms",    "impact": "T2 대조도"},
            "TE (ms)":              {"min": 80,   "max": 120,   "optimal": 100,  "unit": "ms",    "impact": "T2 대조도"},
            "ETL":                  {"min": 8,    "max": 20,    "optimal": 12,   "unit": "",      "impact": "시간/블러"},
            "Slice Thickness (mm)": {"min": 3,    "max": 5,     "optimal": 4,    "unit": "mm",    "impact": "해상도/SNR"},
            "NEX/NSA":              {"min": 1,    "max": 3,     "optimal": 2,    "unit": "",      "impact": "SNR/시간"},
            "Bandwidth":            {"min": 130,  "max": 250,   "optimal": 180,  "unit": "Hz/px", "impact": "SNR"},
            "Matrix Row":           {"min": 256,  "max": 512,   "optimal": 384,  "unit": "",      "impact": "해상도"},
            "FOV (mm)":             {"min": 200,  "max": 240,   "optimal": 220,  "unit": "mm",    "impact": "커버리지"},
        }
    },
    "FLAIR_BRAIN": {
        "label": "🧠 Brain - FLAIR (백질 병변)",
        "params": {
            "TR (ms)":              {"min": 8000, "max": 11000, "optimal": 9000, "unit": "ms",    "impact": "CSF 억제"},
            "TE (ms)":              {"min": 90,   "max": 130,   "optimal": 110,  "unit": "ms",    "impact": "T2 대조도"},
            "TI (ms)":              {"min": 2200, "max": 2500,  "optimal": 2350, "unit": "ms",    "impact": "CSF 억제"},
            "ETL":                  {"min": 8,    "max": 16,    "optimal": 12,   "unit": "",      "impact": "시간/블러"},
            "Slice Thickness (mm)": {"min": 3,    "max": 5,     "optimal": 4,    "unit": "mm",    "impact": "해상도"},
            "NEX/NSA":              {"min": 1,    "max": 2,     "optimal": 1,    "unit": "",      "impact": "SNR/시간"},
            "Bandwidth":            {"min": 130,  "max": 200,   "optimal": 160,  "unit": "Hz/px", "impact": "SNR"},
            "Matrix Row":           {"min": 256,  "max": 384,   "optimal": 320,  "unit": "",      "impact": "해상도"},
        }
    },
    "DWI_BRAIN": {
        "label": "🧠 Brain - DWI (급성 뇌경색)",
        "params": {
            "TR (ms)":              {"min": 4000, "max": 8000,  "optimal": 6000, "unit": "ms",    "impact": "SNR"},
            "TE (ms)":              {"min": 60,   "max": 100,   "optimal": 80,   "unit": "ms",    "impact": "SNR"},
            "B-value":              {"min": 0,    "max": 1000,  "optimal": 1000, "unit": "s/mm2", "impact": "확산 대조도"},
            "Slice Thickness (mm)": {"min": 4,    "max": 6,     "optimal": 5,    "unit": "mm",    "impact": "SNR/해상도"},
            "NEX/NSA":              {"min": 1,    "max": 4,     "optimal": 2,    "unit": "",      "impact": "SNR/시간"},
            "Matrix Row":           {"min": 128,  "max": 256,   "optimal": 192,  "unit": "",      "impact": "해상도/왜곡"},
            "FOV (mm)":             {"min": 220,  "max": 260,   "optimal": 240,  "unit": "mm",    "impact": "커버리지"},
        }
    },
    "GRE_BRAIN": {
        "label": "🧠 Brain - GRE/SWI (출혈/철분)",
        "params": {
            "TR (ms)":              {"min": 500,  "max": 800,   "optimal": 650,  "unit": "ms",    "impact": "T2* 대조도"},
            "TE (ms)":              {"min": 15,   "max": 25,    "optimal": 20,   "unit": "ms",    "impact": "T2* 대조도"},
            "Flip Angle (°)":       {"min": 15,   "max": 30,    "optimal": 20,   "unit": "deg",   "impact": "T1/T2* 대조도"},
            "Slice Thickness (mm)": {"min": 3,    "max": 5,     "optimal": 4,    "unit": "mm",    "impact": "해상도"},
            "NEX/NSA":              {"min": 1,    "max": 2,     "optimal": 1,    "unit": "",      "impact": "SNR/시간"},
            "Bandwidth":            {"min": 150,  "max": 300,   "optimal": 200,  "unit": "Hz/px", "impact": "왜곡 감소"},
            "Matrix Row":           {"min": 256,  "max": 512,   "optimal": 384,  "unit": "",      "impact": "해상도"},
        }
    },
    "MRA_BRAIN": {
        "label": "🧠 Brain - MRA (뇌혈관)",
        "params": {
            "TR (ms)":              {"min": 20,   "max": 35,    "optimal": 25,   "unit": "ms",    "impact": "혈류 대조도"},
            "TE (ms)":              {"min": 3,    "max": 7,     "optimal": 5,    "unit": "ms",    "impact": "SNR"},
            "Flip Angle (°)":       {"min": 15,   "max": 25,    "optimal": 20,   "unit": "deg",   "impact": "혈류 포화"},
            "Slice Thickness (mm)": {"min": 0.5,  "max": 1.5,   "optimal": 1.0,  "unit": "mm",    "impact": "해상도"},
            "NEX/NSA":              {"min": 1,    "max": 2,     "optimal": 1,    "unit": "",      "impact": "SNR/시간"},
            "Matrix Row":           {"min": 384,  "max": 512,   "optimal": 512,  "unit": "",      "impact": "혈관 해상도"},
            "FOV (mm)":             {"min": 160,  "max": 220,   "optimal": 200,  "unit": "mm",    "impact": "커버리지"},
        }
    },
}
