from pathlib import Path
import numpy as np
from scipy.interpolate import interp1d
import torch
import torch.nn as nn

HB_CLASSIFIER_PATH = Path(__file__).parent / 'hb_classifier_model.pth'


class HBClassifierNet(nn.Module):

    def __init__(self):
        super().__init__()

        self.conv = nn.Sequential(
            nn.Conv1d(1, 32, kernel_size=7, padding=3),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.MaxPool1d(2),

            nn.Conv1d(32, 64, kernel_size=5, padding=2),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.MaxPool1d(2),

            nn.Conv1d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.AdaptiveAvgPool1d(1)
        )

        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(0.3),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 5)
        )

    def forward(self, x):
        x = self.conv(x)
        return self.fc(x)


hb_classifier_model = HBClassifierNet()
hb_classifier_model.load_state_dict(torch.load(HB_CLASSIFIER_PATH, map_location=torch.device('cpu')))
hb_classifier_model.eval()


def beat_classifier(beat: np.ndarray) -> str:
    x = torch.tensor(beat, dtype=torch.float32).unsqueeze(0).unsqueeze(0)
    with torch.no_grad():
        pred = hb_classifier_model(x).argmax(1).item()
    return hb_int2char(pred)


def resample_beat(beat: np.ndarray) -> np.ndarray:
    if beat.shape == (186,):
        return beat

    x = np.asarray(beat, dtype=float)
    N = len(x)
    target_len = 186
    t_old = np.linspace(0, 1, N)
    t_new = np.linspace(0, 1, target_len)
    return interp1d(t_old, x, kind="cubic")(t_new)


def hb_int2char(hb_int: int) -> str:
    mapping = {
        0: 'N',  # Non-ectopic beats
        1: 'S',  # Supraventricular ectopic beats
        2: 'V',  # Ventricular ectopic beats
        3: 'F',  # Fusion Beats
        4: 'Q'  # Unknown Beats
    }
    return mapping.get(hb_int, 'Q')


def ecg2beats(ecg: np.ndarray, r_peaks: list[int]) -> list[np.ndarray]:
    beats = []
    li = 0
    for i in range(len(r_peaks) - 1):
        ri = int((r_peaks[i] + r_peaks[i + 1]) / 2)
        beats.append(ecg[li:ri])
        li = ri
    beats.append(ecg[li:])
    return beats


def classify_beat_symbols(
        ecg: list[float],
        r_peaks: list[int]
) -> list[str]:
    """
    Takes lead II ecg and classifies beat types.

    :param ecg:     Filtered lead II ecg
    :param r_peaks: R peaks indices
    :return:        List of beat symbols
    """
    beats = ecg2beats(np.array(ecg), r_peaks)
    beats = [resample_beat(beat) for beat in beats]
    symbols = [beat_classifier(beat) for beat in beats]
    return symbols
