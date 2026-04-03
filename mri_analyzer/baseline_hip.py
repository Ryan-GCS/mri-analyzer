BASELINE_HIP = {
    "T1_HIP": {
        "label": "🦴 Hip - T1 (고관절 구조)",
        "params": {
            "TR (ms)":              {"min": 400,  "max": 700,   "optimal": 550,  "unit": "ms",    "impact": "T1 대조도"},
            "TE (ms)":              {"min": 10,   "max": 20,    "optimal": 15,   "unit": "ms",    "impact": "SNR"},
            "Slice Thickness (mm)": {"min": 3,    "max": 5,     "optimal": 4,    "unit": "mm",    "impact": "해상도"},
            "NEX/NSA":              {"min": 2,    "max": 4,     "optimal": 2,    "unit": "",      "impact": "SNR"},
            "Bandwidth":            {"min": 130,  "max": 200,   "optimal": 150,  "unit": "Hz/px", "impact": "SNR/왜곡"},
            "Matrix Row":           {"min": 256,  "max": 512,   "optimal": 384,  "unit": "",      "impact": "해상도"},
            "FOV (mm)":             {"min": 280,  "max": 380,   "optimal": 320,  "unit": "mm",    "impact": "커버리지"},
        }
    },
    "T2_HIP": {
        "label": "🦴 Hip - T2 (연골/활액막)",
        "params": {
            "TR (ms)":              {"min": 3000, "max": 5000,  "optimal": 4000, "unit": "ms",    "impact": "T2 대조도"},
            "TE (ms)":              {"min": 80,   "max": 120,   "optimal": 100,  "unit": "ms",    "impact": "T2 대조도"},
            "ETL":                  {"min": 8,    "max": 16,    "optimal": 12,   "unit": "",      "impact": "시간/블러"},
            "Slice Thickness (mm)": {"min": 3,    "max": 5,     "optimal": 4,    "unit": "mm",    "impact": "해상도"},
            "NEX/NSA":              {"min": 2,    "max": 4,     "optimal": 2,    "unit": "",      "impact": "SNR"},
            "Bandwidth":            {"min": 130,  "max": 220,   "optimal": 180,  "unit": "Hz/px", "impact": "SNR"},
            "Matrix Row":           {"min": 256,  "max": 512,   "optimal": 384,  "unit": "",      "impact": "해상도"},
            "FOV (mm)":             {"min": 280,  "max": 380,   "optimal": 320,  "unit": "mm",    "impact": "커버리지"},
        }
    },
    "PD_HIP": {
        "label": "🦴 Hip - PD (관절와순)",
        "params": {
            "TR (ms)":              {"min": 2000, "max": 4000,  "optimal": 3000, "unit": "ms",    "impact": "PD 대조도"},
            "TE (ms)":              {"min": 20,   "max": 40,    "optimal": 30,   "unit": "ms",    "impact": "PD 대조도"},
            "ETL":                  {"min": 4,    "max": 12,    "optimal": 8,    "unit": "",      "impact": "시간/블러"},
            "Slice Thickness (mm)": {"min": 2,    "max": 4,     "optimal": 3,    "unit": "mm",    "impact": "해상도"},
            "NEX/NSA":              {"min": 2,    "max": 4,     "optimal": 2,    "unit": "",      "impact": "SNR"},
            "Bandwidth":            {"min": 130,  "max": 200,   "optimal": 160,  "unit": "Hz/px", "impact": "SNR"},
            "Matrix Row":           {"min": 256,  "max": 512,   "optimal": 384,  "unit": "",      "impact": "해상도"},
            "FOV (mm)":             {"min": 280,  "max": 380,   "optimal": 320,  "unit": "mm",    "impact": "커버리지"},
        }
    },
}
