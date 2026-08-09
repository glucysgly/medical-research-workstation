"""Run the synthetic qPCR QC without modifying the raw fixture."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent / "scripts"))

from qpcr_qc import review_csv


if __name__ == "__main__":
    print(review_csv(ROOT / "data" / "raw" / "synthetic_qpcr.csv"))
