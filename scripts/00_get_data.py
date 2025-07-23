#!/usr/bin/env python
"""
CLI to fetch open datasets for Skip-Sensei.

Usage:
    poetry run python scripts/00_get_data.py fma
    poetry run python scripts/00_get_data.py mssd
"""
import subprocess, pathlib, sys, typer

app = typer.Typer()
DATA_DIR = pathlib.Path("data/raw").resolve()
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ── FMA (audio) ─────────────────────────────────────────
FMA_URL = "https://os.unil.cloud.switch.ch/fma/fma_small.zip"

@app.command()
def fma():
    "Download the FMA-small dataset (≈8 GB)."
    out = DATA_DIR / "fma_small.zip"
    typer.echo(f"→ Downloading FMA-small to {out} …")
    subprocess.run(["curl", "-L", FMA_URL, "-o", str(out)], check=True)
    typer.echo("✓ Done. Unzip with `unzip` or 7-Zip into data/raw/fma_small/")

# ── MSSD (skip logs) ────────────────────────────────────
MSSD_S3 = (
    "s3://mssd-public/spotify/milli_streaming_sessions/MSSD_sample.tar.gz"
)  # 1 % sample

@app.command()
def mssd():
    """
    Download the Spotify Music-Streaming-Sessions 1 % sample.
    Requires AWS CLI but **no** credentials (`--no-sign-request`).
    """
    out = DATA_DIR / "MSSD_sample.tar.gz"
    typer.echo(f"→ Downloading MSSD sample to {out} …")
    subprocess.run(
        ["aws", "s3", "cp", "--no-sign-request", MSSD_S3, str(out)],
        check=True,
    )
    typer.echo("✓ Done. Extract with `tar -xzf` then move JSON to data/raw/mssd/")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        typer.echo(app.get_help(ctx=None))
    else:
        app()
