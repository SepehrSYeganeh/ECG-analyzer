from pydantic import BaseModel


class HeartArrhythmia(BaseModel):
    name: str
    re_pattern: str
    severity: int  # 1=low .. 5=critical
    possible_diagnoses: list[str]


class DiagnosisHeartArrhythmiaReport(BaseModel):
    severity: int
    possible_diagnoses: list[str]
    counts_arrhythmia: dict[str, int]  # name: count

    def to_report_text(self) -> str:
        diagnoses = ", ".join(self.possible_diagnoses) or "None"

        arrhythmia_counts = "\n".join(
            f"  - {name}: {count}"
            for name, count in self.counts_arrhythmia.items()
        ) or "  - None"

        return (
            "Your heart arrhythmia diagnosis report is:\n"
            f"Severity: {self.severity}\n"
            f"Possible diagnoses: {diagnoses}\n"
            "Arrhythmia counts:\n"
            f"{arrhythmia_counts}"
        )
