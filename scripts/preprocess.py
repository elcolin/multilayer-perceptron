import pandas as pd
import argparse
import sys
import math
import utils as u
from datetime import datetime
from pathlib import Path

def load_dataset(path: Path) -> pd.DataFrame:
    """Lit le CSV brut (sans en-tete) et le renvoie sous forme de DataFrame."""
    df = pd.read_csv(path, header=None)
    df[1].isin(["M", "B"]).all()
    return df

def check_numeric_features(df: pd.DataFrame) -> None:
    """Verifie que les colonnes de mesures (2 a la fin) sont numeriques."""
    for col in df.columns[2:]:
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError(f"column {col} is not numeric (dtype: {df[col].dtype})")

def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Retire l'identifiant, convertit le label M/B en 1/0 et le place en premiere colonne."""
    df = df.drop(columns=0)
    df[1] = df[1].map({"M": 1, "B": 0})
    u.normalize(df)
    return df


# def shuffle(df: pd.DataFrame, seed: int) -> pd.DataFrame:
#     """Melange les lignes de facon reproductible."""
#     pass


def split(df: pd.DataFrame, train_ratio: float) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Separe le DataFrame en (train, valid) selon train_ratio."""
    if len(df) == 0:
        raise pd.errors.EmptyDataError
    if (not isinstance(df, pd.DataFrame)):
        raise TypeError
    idx = len(df) * train_ratio
    idx = math.floor(idx)
    return(df[:idx:], df[idx::])


def save(df: pd.DataFrame, path: Path) -> None:
    """Ecrit le DataFrame en CSV numerique, sans en-tete ni index."""
    if (len(df) == 0):
        raise pd.errors.EmptyDataError
    if (not isinstance(df, pd.DataFrame)):
            raise TypeError
    df.to_csv(path, index=False, header=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="...")
    parser.add_argument("--dataset", type=Path, default=Path("data/data.csv"))
    parser.add_argument("--output", type=Path, default=Path("output"))
    parser.add_argument("--train-ratio", type=float, default=0.8)
    args = parser.parse_args()
    try:
        df = load_dataset(Path.cwd() / args.dataset)
        df = clean(df)
        tf, vf = split(df, args.train_ratio)
        save(tf, Path.cwd() / args.output / f"training_data_{datetime.now().strftime("%Y%m%d-%H%M%S")}.csv")
        save(vf, Path.cwd() / args.output / f"validation_data_{datetime.now().strftime("%Y%m%d-%H%M%S")}.csv")

    except FileNotFoundError as e:
        print(f"error: file not found: {e.filename}", file=sys.stderr)
        sys.exit(1)
    except PermissionError as e:
        print(f"error: permission denied: {e.filename}", file=sys.stderr)
        sys.exit(1)
    except pd.errors.EmptyDataError as e:
        print(f"error: {args.dataset}: file is empty", file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError as e:
        print(f"error: fichier incompatible", file=sys.stderr)


if __name__ == "__main__":
    main()
