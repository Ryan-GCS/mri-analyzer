BASELINE_CARDIAC = {
    "CINE_CARDIAC": {
        "label": "❤️ Cardiac - Cine (심장 기능)",
        "params": {
            "TR (ms)":              {"min": 3,    "max": 8,     "optimal": 5,    "unit": "ms",    "impact": "시간 해상도"},
            "TE (ms)":              {"min": 1,    "max": 3,     "optimal": 2,    "unit": "ms",    "impact": "SNR"},
            "Flip Angle (°)":       {"min": 45,   "max": 75,    "optimal": 60,   "unit": "deg",   "impact": "혈액 대조도"},
            "Slice Thickness (mm)": {"min": 6,    "max": 10,    "optimal": 8,    "unit": "mm",    "impact": "해상도/SNR"},
            "NEX/NSA":              {"min": 1,    "max": 2,     "optimal": 1,    "unit": "",      "impact": "SNR/시간"},
            "Matrix Row":           {"min": 192,  "max": 256,   "optimal": 224,  "unit": "",      "impact": "해상도"},
            "FOV (mm)":             {"min": 300,  "max": 400,   "optimal": 360,  "unit": "mm",    "impact": "커버리지"},
        }
    },
    "T2_CARDIAC": {
        "label": "❤️ Cardiac - T2 (심근 부종)",
        "params": {
            "TR (ms)":              {"min": 1500, "max": 3000,  "optimal": 2000, "unit": "ms",    "impact": "T2 대조도"},
            "TE (ms)":              {"min": 50,   "max": 80,    "optimal": 60,   "unit": "ms",    "impact": "T2 대조도"},
            "ETL":                  {"min": 16,   "max": 32,    "optimal": 24,   "unit": "",      "impact": "시간/블러"},
            "Slice Thickness (mm)": {"min": 6,    "max": 10,    "optimal": 8,    "unit": "mm",    "impact": "해상도/SNR"},
            "NEX/NSA":              {"min": 2,    "max": 4,     "optimal": 2,    "unit": "",      "impact": "SNR/시간"},
            "Matrix Row":           {"min": 192,  "max": 256,   "optimal": 224,  "unit": "",      "impact": "해상도"},
            "FOV (mm)":             {"min": 300,  "max": 400,   "optimal": 360,  "unit": "mm",    "impact": "커버리지"},
        }
    },
    "LGE_CARDIAC": {
        "label": "❤️ Cardiac - LGE (심근 섬유화)",
        "params": {
            "TR (ms)":              {"min": 4,    "max": 8,     "optimal": 6,    "unit": "ms",    "impact": "T1 대조도"},
            "TE (ms)":              {"min": 1,    "max": 3,     "optimal": 2,    "unit": "ms",    "impact": "SNR"},
            "TI (ms)":              {"min": 200,  "max": 350,   "optimal": 280,  "unit": "ms",    "impact": "심근 억제"},
            "Flip Angle (°)":       {"min": 20,   "max": 30,    "optimal": 25,   "unit": "deg",   "impact": "T1 대조도"},
            "Slice Thickness (mm)": {"min": 6,    "max": 10,    "optimal": 8,    "unit": "mm",    "impact": "해상도/SNR"},
            "NEX/NSA":              {"min": 1,    "max": 2,     "optimal": 1,    "unit": "",      "impact": "SNR/시간"},
            "Matrix Row":           {"min": 192,  "max": 256,   "optimal": 224,  "unit": "",      "impact": "해상도"},
            "FOV (mm)":             {"min": 300,  "max": 400,   "optimal": 360,  "unit": "mm",    "impact": "커버리지"},
        }
    },
    "MRA_CARDIAC": {
        "label": "❤️ Cardiac - MRA (관상동맥)",
        "params": {
            "TR (ms)":              {"min": 3,    "max": 6,     "optimal": 4,    "unit": "ms",    "impact": "혈류 대조도"},
            "TE (ms)":              {"min": 1,    "max": 3,     "optimal": 2,    "unit": "ms",    "impact": "SNR"},
            "Flip Angle (°)":       {"min": 20,   "max": 30,    "optimal": 25,   "unit": "deg",   "impact": "혈류 포화"},
            "Slice Thickness (mm)": {"min": 0.5,  "max": 1.5,   "optimal": 1.0,  "unit": "mm",    "impact": "해상도"},
            "NEX/NSA":              {"min": 1,    "max": 2,     "optimal": 1,    "unit": "",      "impact": "SNR/시간"},
            "Matrix Row":           {"min": 256,  "max": 512,   "optimal": 384,  "unit": "",      "impact": "혈관 해상도"},
            "FOV (mm)":             {"min": 280,  "max": 380,   "optimal": 320,  "unit": "mm",    "impact": "커버리지"},
        }
    },
}
