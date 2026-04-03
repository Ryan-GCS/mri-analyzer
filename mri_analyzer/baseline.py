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

# 모든 시퀀스에 제조사 파라미터 자동 추가
for seq_key in SEQUENCE_BASELINES:
    SEQUENCE_BASELINES[seq_key]["params"].update(MANUFACTURER_PARAMS)

# ↓ 영어 label 매핑 추가
LABEL_EN_MAP = {
    # Brain
    "🧠 Brain - T1 (뇌 구조)":           "🧠 Brain - T1 (Brain Structure)",
    "🧠 Brain - T2 (부종/병변)":          "🧠 Brain - T2 (Edema/Lesion)",
    "🧠 Brain - FLAIR (백질 병변)":       "🧠 Brain - FLAIR (White Matter)",
    "🧠 Brain - DWI (급성 뇌경색)":       "🧠 Brain - DWI (Acute Infarction)",
    "🧠 Brain - GRE/SWI (출혈/철분)":     "🧠 Brain - GRE/SWI (Hemorrhage/Iron)",
    "🧠 Brain - MRA (뇌혈관)":            "🧠 Brain - MRA (Brain Vessels)",
    # Spine
    "🔧 C-Spine - T1 (경추 구조)":        "🔧 C-Spine - T1 (Structure)",
    "🔧 C-Spine - T2 (경추 디스크/병변)": "🔧 C-Spine - T2 (Disc/Lesion)",
    "🔧 C-Spine - STIR (경추 부종)":      "🔧 C-Spine - STIR (Edema)",
    "🦴 L-Spine - T1 (요추 구조)":        "🦴 L-Spine - T1 (Structure)",
    "🦴 L-Spine - T2 (요추 디스크/병변)": "🦴 L-Spine - T2 (Disc/Lesion)",
    "🦴 L-Spine - STIR (요추 부종)":      "🦴 L-Spine - STIR (Edema)",
    # Knee
    "🦵 Knee - T1 (연골/뼈)":             "🦵 Knee - T1 (Cartilage/Bone)",
    "🦵 Knee - T2 (반월판/인대)":         "🦵 Knee - T2 (Meniscus/Ligament)",
    "🦵 Knee - PD (연골/반월판)":         "🦵 Knee - PD (Cartilage/Meniscus)",
    "🦵 Knee - STIR (부종/염증)":         "🦵 Knee - STIR (Edema/Inflammation)",
    # Shoulder
    "🫀 Shoulder - T1 (회전근개)":        "🫀 Shoulder - T1 (Rotator Cuff)",
    "🫀 Shoulder - T2 (힘줄/점액낭)":     "🫀 Shoulder - T2 (Tendon/Bursa)",
    "🫀 Shoulder - PD (회전근개)":        "🫀 Shoulder - PD (Rotator Cuff)",
    # Abdomen
    "🫁 Abdomen - T1 (간/췌장)":          "🫁 Abdomen - T1 (Liver/Pancreas)",
    "🫁 Abdomen - T2 (담도/췌관)":        "🫁 Abdomen - T2 (Bile Duct)",
    "🫁 Abdomen - DWI (종양 감별)":       "🫁 Abdomen - DWI (Tumor Detection)",
    # Pelvis
    "🦴 Pelvis - T1 (골반 구조)":         "🦴 Pelvis - T1 (Structure)",
    "🦴 Pelvis - T2 (골반 장기)":         "🦴 Pelvis - T2 (Pelvic Organs)",
    "🦴 Pelvis - DWI (종양 감별)":        "🦴 Pelvis - DWI (Tumor Detection)",
    # Cardiac
    "🫀 Cardiac - Cine (심장 기능)":      "🫀 Cardiac - Cine (Cardiac Function)",
    "🫀 Cardiac - T2 (심근 부종)":        "🫀 Cardiac - T2 (Myocardial Edema)",
    "🫀 Cardiac - LGE (심근 섬유화)":     "🫀 Cardiac - LGE (Myocardial Fibrosis)",
    # Breast
    "🎀 Breast - T1 (유방 구조)":         "🎀 Breast - T1 (Structure)",
    "🎀 Breast - T2 (유방 병변)":         "🎀 Breast - T2 (Lesion)",
    "🎀 Breast - DWI (종양 감별)":        "🎀 Breast - DWI (Tumor Detection)",
    # Hip
    "🦴 Hip - T1 (고관절 구조)":          "🦴 Hip - T1 (Structure)",
    "🦴 Hip - T2 (고관절 병변)":          "🦴 Hip - T2 (Lesion)",
    "🦴 Hip - PD (관절와순)":             "🦴 Hip - PD (Labrum)",
    # Ankle
    "🦶 Ankle - T1 (발목 구조)":          "🦶 Ankle - T1 (Structure)",
    "🦶 Ankle - T2 (인대/힘줄)":          "🦶 Ankle - T2 (Ligament/Tendon)",
    "🦶 Ankle - PD (연골/인대 정밀)":     "🦶 Ankle - PD (Cartilage/Ligament)",
    # Wrist
    "✋ Wrist - T1 (손목 구조)":           "✋ Wrist - T1 (Structure)",
    "✋ Wrist - T2 (인대/삼각섬유연골)":   "✋ Wrist - T2 (Ligament/TFCC)",
    "✋ Wrist - PD (연골/인대 정밀)":      "✋ Wrist - PD (Cartilage/Ligament)",
}
