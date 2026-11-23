import preprocess
import pandas as pd
from    pandas.testing import assert_frame_equal
import pytest
from pathlib import Path

@pytest.fixture
def raw_df(raw_csv: str) -> pd.DataFrame:
    return preprocess.load_dataset(raw_csv)

@pytest.fixture
def raw_csv(tmp_path: Path):
    f = tmp_path / "data.csv"
    f.write_text(
        "842302,M,17.99,10.38\n"
        "842517,B,20.57,17.77\n"
        "843009,M,19.69,21.25\n"
    )
    return str(f)

@pytest.fixture
def clean_df():
    return pd.DataFrame({
            1: [1, 0, 1],
            2: [17.99, 20.57, 19.69],
            3: [10.38, 17.77, 21.25]
            })

# ---------- load_dataset ----------
def test_load_dataset_shape(raw_csv: str):            # nombre de lignes et de colonnes attendu
    df = preprocess.load_dataset(raw_csv)
    assert (df.shape) == (3, 4)

def test_load_dataset_missing_file(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        t = tmp_path / "t"
        preprocess.load_dataset(str(t))

def test_load_dataset_empty_file(tmp_path: Path):
    with pytest.raises(pd.errors.EmptyDataError):
        e = tmp_path / "e"
        e.write_text("")
        preprocess.load_dataset(str(e))

def test_load_dataset_permission_error(tmp_path: Path):
    with pytest.raises(PermissionError):
        p = tmp_path / "p"
        p.write_text("You're not supposed to see this")
        p.chmod(0o000)
        preprocess.load_dataset(str(p))

# ---------- clean ----------

def test_diagnosis_mapping(raw_df: pd.DataFrame, clean_df: pd.DataFrame):        # la 1re ligne est une donnée, pas un en-tête
    df = preprocess.clean(raw_df)
    assert not (df.equals(raw_df))
    
    assert_frame_equal(df, clean_df)

# ---------- save ----------
def normalize(df):
    df = df.reset_index(drop=True)     # lignes → 0..n-1
    df.columns = range(df.shape[1])    # colonnes → 0..m-1
    return df

def test_save_clean_dataset(tmp_path: Path, clean_df: pd.DataFrame):
    s = tmp_path / "s"
    s.write_text("")
    preprocess.save(clean_df, path=str(s))
    cf = pd.read_csv(str(s), header=None)
    cf.columns = cf.columns.astype(int)
    clean_df = normalize(clean_df)
    assert_frame_equal(clean_df, cf, check_names=False)

def test_save_empty_file_name(clean_df: pd.DataFrame):
    with pytest.raises(FileNotFoundError):
        preprocess.save(clean_df, "")

def test_save_no_perm_file(tmp_path: Path, clean_df: pd.DataFrame):
    with pytest.raises(PermissionError):
        p = tmp_path / "p"
        p.write_text("You're not supposed to see this")
        p.chmod(0o000)
        preprocess.save(clean_df, str(p))

# ---------- split ----------
# def test_split_no_data