from pathlib import Path
from ecg_analyzer.io import load_ecg_file

test_path = Path.cwd()


def test_sr100():
    t_path = test_path / "00001_lr"
    rec = load_ecg_file(t_path, "00001")
    return rec


def test_sr500():
    t_path = test_path / "04048_hr"
    rec = load_ecg_file(t_path, "04048")
    return rec
