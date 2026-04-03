from baseline_brain    import BASELINE_BRAIN
from baseline_spine    import BASELINE_SPINE
from baseline_knee     import BASELINE_KNEE
from baseline_shoulder import BASELINE_SHOULDER
from baseline_abdomen  import BASELINE_ABDOMEN
from baseline_pelvis   import BASELINE_PELVIS
from baseline_cardiac  import BASELINE_CARDIAC
from baseline_breast   import BASELINE_BREAST
from baseline_hip      import BASELINE_HIP
from baseline_ankle    import BASELINE_ANKLE
from baseline_wrist    import BASELINE_WRIST
from baseline_common   import MANUFACTURER_PARAMS

SEQUENCE_BASELINES = {}
SEQUENCE_BASELINES.update(BASELINE_BRAIN)
SEQUENCE_BASELINES.update(BASELINE_SPINE)
SEQUENCE_BASELINES.update(BASELINE_KNEE)
SEQUENCE_BASELINES.update(BASELINE_SHOULDER)
SEQUENCE_BASELINES.update(BASELINE_ABDOMEN)
SEQUENCE_BASELINES.update(BASELINE_PELVIS)
SEQUENCE_BASELINES.update(BASELINE_CARDIAC)
SEQUENCE_BASELINES.update(BASELINE_BREAST)
SEQUENCE_BASELINES.update(BASELINE_HIP)
SEQUENCE_BASELINES.update(BASELINE_ANKLE)
SEQUENCE_BASELINES.update(BASELINE_WRIST)

for seq_key in SEQUENCE_BASELINES:
    SEQUENCE_BASELINES[seq_key]["params"].update(MANUFACTURER_PARAMS)

LABEL_EN_MAP = {
    # Brain
    "🧠 Brain - T1 (뇌 구조)":              "🧠 Brain - T1 (Brain Structure)",
    "🧠 Brain - T2 (부종/병변)":             "🧠 Brain - T2 (Edema/Lesion)",
    "🧠 Brain - FLAIR (백질 병변)":          "🧠 Brain - FLAIR (White Matter)",
    "🧠 Brain - DWI (급성 뇌경색)":          "🧠 Brain - DWI (Acute Infarction)",
    "🧠 Brain - GRE/SWI (출혈/철분)":        "🧠 Brain - GRE/SWI (Hemorrhage/Iron)",
    "🧠 Brain - MRA (뇌혈관)":               "🧠 Brain - MRA (Brain Vessels)",
    # Spine
    "🦴 C-Spine - T1 (경추 구조)":           "🦴 C-Spine - T1 (Structure)",
    "🦴 C-Spine - T2 (경추 디스크/척수)":    "🦴 C-Spine - T2 (Disc/Cord)",
    "🦴 T-Spine - T1 (흉추 구조)":           "🦴 T-Spine - T1 (Structure)",
    "🦴 T-Spine - T2 (흉추 디스크)":         "🦴 T-Spine - T2 (Disc/Lesion)",
    "🦴 L-Spine - T1 (요추 구조)":           "🦴 L-Spine - T1 (Structure)",
    "🦴 L-Spine - T2 (요추 디스크)":         "🦴 L-Spine - T2 (Disc/Lesion)",
    # Knee
    "🦵 Knee - T1 (무릎 구조)":              "🦵 Knee - T1 (Structure)",
    "🦵 Knee - T2 (연골/인대)":              "🦵 Knee - T2 (Cartilage/Ligament)",
    "🦵 Knee - PD (반월판/연골)":            "🦵 Knee - PD (Meniscus/Cartilage)",
    "🦵 Knee - GRE (연골 정밀)":             "🦵 Knee - GRE (Cartilage Detail)",
    # Shoulder
    "💪 Shoulder - T1 (어깨 구조)":          "💪 Shoulder - T1 (Structure)",
    "💪 Shoulder - T2 (회전근개/점액낭)":    "💪 Shoulder - T2 (Rotator Cuff/Bursa)",
    "💪 Shoulder - PD (회전근개 정밀)":      "💪 Shoulder - PD (Rotator Cuff Detail)",
    # Abdomen
    "🫁 Abdomen - T1 (복부 구조)":           "🫁 Abdomen - T1 (Structure)",
    "🫁 Abdomen - T2 (간/담도/췌장)":        "🫁 Abdomen - T2 (Liver/Bile/Pancreas)",
    "🫁 Abdomen - DWI (종양 감별)":          "🫁 Abdomen - DWI (Tumor Detection)",
    "🫁 Abdomen - MRCP (담도/췌관)":         "🫁 Abdomen - MRCP (Bile/Pancreatic Duct)",
    # Pelvis
    "🦴 Pelvis - T1 (골반 구조)":            "🦴 Pelvis - T1 (Structure)",
    "🦴 Pelvis - T2 (전립선/자궁)":          "🦴 Pelvis - T2 (Prostate/Uterus)",
    "🦴 Pelvis - DWI (전립선암 감별)":       "🦴 Pelvis - DWI (Prostate Cancer)",
    # Cardiac
    "❤️ Cardiac - Cine (심장 기능)":         "❤️ Cardiac - Cine (Cardiac Function)",
    "❤️ Cardiac - T2 (심근 부종)":           "❤️ Cardiac - T2 (Myocardial Edema)",
    "❤️ Cardiac - LGE (심근 섬유화)":        "❤️ Cardiac - LGE (Myocardial Fibrosis)",
    "❤️ Cardiac - MRA (관상동맥)":           "❤️ Cardiac - MRA (Coronary Artery)",
    # Breast
    "🎀 Breast - T1 (유방 구조)":            "🎀 Breast - T1 (Structure)",
    "🎀 Breast - T2 (낭종/부종)":            "🎀 Breast - T2 (Cyst/Edema)",
    "🎀 Breast - DCE (조영증강/종양)":       "🎀 Breast - DCE (Enhancement/Tumor)",
    "🎀 Breast - DWI (악성 감별)":           "🎀 Breast - DWI (Malignancy)",
    # Hip
    "🦴 Hip - T1 (고관절 구조)":             "🦴 Hip - T1 (Structure)",
    "🦴 Hip - T2 (연골/활액막)":             "🦴 Hip - T2 (Cartilage/Synovium)",
    "🦴 Hip - PD (관절와순)":                "🦴 Hip - PD (Labrum)",
    # Ankle
    "🦶 Ankle - T1 (발목 구조)":             "🦶 Ankle - T1 (Structure)",
    "🦶 Ankle - T2 (인대/힘줄)":             "🦶 Ankle - T2 (Ligament/Tendon)",
    "🦶 Ankle - PD (연골/인대 정밀)":        "🦶 Ankle - PD (Cartilage/Ligament)",
    # Wrist
    "🤚 Wrist - T1 (손목 구조)":             "🤚 Wrist - T1 (Structure)",
    "🤚 Wrist - T2 (인대/삼각섬유연골)":     "🤚 Wrist - T2 (Ligament/TFCC)",
    "🤚 Wrist - PD (연골/인대 정밀)":        "🤚 Wrist - PD (Cartilage/Ligament)",
}

IMPACT_EN_MAP = {
    "CSF 억제":           "CSF Suppression",
    "PD 대조도":          "PD Contrast",
    "SNR":                "SNR",
    "SNR(GE)":            "SNR(GE)",
    "SNR/시간":           "SNR/Time",
    "SNR/시간(GE)":       "SNR/Time(GE)",
    "SNR/시간(Philips)":  "SNR/Time(Philips)",
    "SNR/시간(Siemens)":  "SNR/Time(Siemens)",
    "SNR/왜곡":           "SNR/Distortion",
    "SNR/해상도":         "SNR/Resolution",
    "T1 대조도":          "T1 Contrast",
    "T1/T2* 대조도":      "T1/T2* Contrast",
    "T2 대조도":          "T2 Contrast",
    "T2* 대조도":         "T2* Contrast",
    "담즙 대조도":        "Bile Contrast",
    "시간 해상도":        "Temporal Resolution",
    "시간/블러":          "Time/Blur",
    "심근 억제":          "Myocardial Suppression",
    "연골 대조도":        "Cartilage Contrast",
    "왜곡 감소":          "Distortion Reduction",
    "왜곡(Siemens)":      "Distortion(Siemens)",
    "조직억제(Philips)":  "Tissue Suppression(Philips)",
    "커버리지":           "Coverage",
    "투영 두께":          "Projection Thickness",
    "해상도":             "Resolution",
    "해상도/SNR":         "Resolution/SNR",
    "해상도/왜곡":        "Resolution/Distortion",
    "혈관 해상도":        "Vascular Resolution",
    "혈류 대조도":        "Flow Contrast",
    "혈류 포화":          "Flow Saturation",
    "혈액 대조도":        "Blood Contrast",
    "호흡 아티팩트":      "Respiratory Artifact",
    "화학적이동(Philips)":"Chemical Shift(Philips)",
    "확산 대조도":        "Diffusion Contrast",
    "환자 안전":          "Patient Safety",
}
