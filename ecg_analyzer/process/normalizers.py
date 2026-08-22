from ecg_analyzer.models import ECGLeads


def z_score_normalization(leads: ECGLeads) -> ECGLeads:
    x = leads.to_numpy()
    mean = x.mean(axis=1, keepdims=True)
    std = x.std(axis=1, keepdims=True)
    return ECGLeads.from_numpy((x - mean) / std)
