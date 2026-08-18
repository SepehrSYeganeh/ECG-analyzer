import pandas as pd
import numpy as np
import wfdb
import ast
from pathlib import Path


def load_raw_data(df: pd.DataFrame, sampling_rate: int, path: Path) -> np.ndarray:
    if sampling_rate == 100:
        data = [wfdb.rdsamp(path / f) for f in df.filename_lr]
    else:
        data = [wfdb.rdsamp(path / f) for f in df.filename_hr]
    data = np.array([signal for signal, meta in data])
    return data


def aggregate_diagnostic(y_dic: dict) -> list[list[str]]:
    tmp = []
    for key in y_dic.keys():
        if key in agg_df.index:
            tmp.append(agg_df.loc[key].diagnostic_class)
    return list(set(tmp))


if __name__ == '__main__':
    data_path = Path(__file__).resolve().parents[1] / "data" / "ptb-xl"

    # load and convert annotation data
    Y = pd.read_csv(data_path / 'ptbxl_database.csv', index_col='ecg_id')
    Y.scp_codes = Y.scp_codes.apply(lambda x: ast.literal_eval(x))

    # Load scp_statements.csv for diagnostic aggregation
    agg_df = pd.read_csv(data_path / 'scp_statements.csv', index_col=0)
    agg_df = agg_df[agg_df.diagnostic == 1]

    # Apply diagnostic superclass
    Y['diagnostic_superclass'] = Y.scp_codes.apply(aggregate_diagnostic)

    # save
    Y.to_parquet(data_path.parent / "metadata.parquet")
    print("saved metadata")

    # save raw signal data
    np.save(data_path.parent / "12lead-ecg-100.npy", load_raw_data(Y, 100, data_path))
    print("saved 12lead-ecg-100")
    np.save(data_path.parent / "12lead-ecg-500.npy", load_raw_data(Y, 500, data_path))
    print("saved 12lead-ecg-500")
