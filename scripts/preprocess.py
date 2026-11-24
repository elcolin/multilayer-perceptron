import pandas as pd
import argparse
import sys
import math
import utils as u

def load_dataset(path: str) -> pd.DataFrame:
    """Lit le CSV brut (sans en-tete) et le renvoie sous forme de DataFrame."""
    df = pd.read_csv(path, header=None)
    return df


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


def save(df: pd.DataFrame, path: str) -> None:
    """Ecrit le DataFrame en CSV numerique, sans en-tete ni index."""
    if (len(df) == 0):
        raise pd.errors.EmptyDataError
    if (not isinstance(df, pd.DataFrame)):
            raise TypeError
    df.to_csv(path, index=False, header=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="...")
    parser.add_argument("dataset") 
    parser.add_argument("output")
    args = parser.parse_args()
    try:
        df = load_dataset(args.dataset)
        df = clean(df)
        save(df, args.output)
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
