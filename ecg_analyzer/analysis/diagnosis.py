import re
from ecg_analyzer.models import HeartArrhythmia, DiagnosisHeartArrhythmiaReport

vt_run = HeartArrhythmia(
    name="Ventricular run",
    re_pattern=r"V{3,}",
    severity=5,
    possible_diagnoses=[
        "Nonsustained ventricular tachycardia (NSVT) if <30s",
        "Sustained VT if prolonged / continuous (needs timing)",
        "Ventricular ectopy storm / frequent PVCs in salvos"
    ],
)

pvc_couplet = HeartArrhythmia(
    name="PVC couplet",
    re_pattern=r"(?<!V)VV(?!V)",  # exactly 2 V, not part of longer run
    severity=4,
    possible_diagnoses=[
        "Ventricular couplets (paired PVCs)",
        "Increased risk marker for higher-grade ventricular ectopy"
    ]
)

ventricular_bigeminy = HeartArrhythmia(
    name="Ventricular bigeminy",
    re_pattern=r"(?:NV){3,}N?",
    severity=3,
    possible_diagnoses=[
        "Ventricular bigeminy",
        "Frequent premature ventricular contractions (PVCs)"
    ]
)

ventricular_trigeminy = HeartArrhythmia(
    name="Ventricular trigeminy",
    re_pattern=r"(?:NNV){3,}N{0,2}",
    severity=3,
    possible_diagnoses=[
        "Ventricular trigeminy",
        "Frequent PVCs in trigeminal pattern"
    ]
)

fusion_near_v = HeartArrhythmia(
    name="Fusion near ventricular activity",
    re_pattern=r"(?:FV+|V+F|VFV)",
    severity=3,
    possible_diagnoses=[
        "Fusion beats with ventricular ectopy",
        "Possible accelerated idioventricular rhythm (AIVR) context",
        "Unstable ventricular ectopy / competing rhythms"
    ]
)

supraventricular_run = HeartArrhythmia(
    name="Supraventricular run",
    re_pattern=r"S{3,}",
    severity=2,
    possible_diagnoses=[
        "Nonsustained SVT / atrial tachycardia run",
        "Frequent PACs in salvos",
        "Possible AF/SVT-like burst (needs RR irregularity)"
    ]
)

atrial_bigeminy = HeartArrhythmia(
    name="Atrial / supraventricular bigeminy",
    re_pattern=r"(?:NS){3,}N?",
    severity=2,
    possible_diagnoses=[
        "Atrial bigeminy (PAC bigeminy)",
        "Frequent premature atrial contractions"
    ]
)

arrhythmia_list = [
    vt_run,
    pvc_couplet,
    ventricular_bigeminy,
    ventricular_trigeminy,
    fusion_near_v,
    supraventricular_run,
    atrial_bigeminy
]


def diagnose_heart_arrhythmia(symbols: list[str]):
    seq = "".join(symbols)
    severity: int = 0
    possible_diagnoses: list[str] = []
    counts_arrhythmia: dict[str, int] = dict()
    for arrhythmia in arrhythmia_list:
        count = len(re.findall(arrhythmia.re_pattern, seq))
        if count > 0:
            severity += count * arrhythmia.severity
            possible_diagnoses += arrhythmia.possible_diagnoses
            counts_arrhythmia[arrhythmia.name] = count

    return DiagnosisHeartArrhythmiaReport(
        severity=severity,
        possible_diagnoses=possible_diagnoses,
        counts_arrhythmia=counts_arrhythmia
    )
