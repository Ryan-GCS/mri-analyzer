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
