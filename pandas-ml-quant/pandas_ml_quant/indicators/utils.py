import numpy as np
import pandas as pd
from numba import guvectorize, float32, int32, float64, int64


@guvectorize([(float32[:], int32, float32[:]),
              (float64[:], int64, float64[:])], '(n),()->(n)')
def wilders_smoothing(arr: np.ndarray, period: int, res: np.ndarray):
    assert period > 0
    alpha = (period - 1) / period
    beta = 1 / period

    res[0:period] = np.nan
    res[period - 1] = arr[0:period].mean()
    for i in range(period, len(arr)):
        res[i] = alpha * res[i-1] + arr[i] * beta


def with_column_suffix(suffix, po, ref_po=None):
    if ref_po is None:
        ref_po = po

    if isinstance(po, pd.Series):
        if isinstance(po.name, tuple):
            return po.rename((suffix, *ref_po.name))
        else:
            return po.rename(f'{ref_po.name}_{suffix}')
    else:
        if isinstance(po.index, pd.MultiIndex):
            po.columns = pd.MultiIndex.from_tuples([(suffix, *col) for col in ref_po.columns.to_list()])
            return po
        else:
            po.columns = ref_po.columns
            return po.add_suffix(f'_{suffix}')
