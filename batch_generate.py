import argparse
import csv
import subprocess
import sys
import time
from pathlib import Path


def wait_for_file(file_path: Path, timeout: float = 30.0, poll_interval: float = 0.25) -> None:
    """Wait until file_path exists and has non-zero size."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if file_path.exists() and file_path.stat().st_size > 0:
            return
        time.sleep(poll_interval)
    raise TimeoutError(f"Timed out waiting for output file to be created: {file_path}")


def run_batch(
    csv_path: Path,
    generator_script: Path,
    output_dir: Path,
    timeout: float = 30.0,
) -> None:
    if not csv_path.is_file():
        raise FileNotFoundError(f"CSV input file not found: {csv_path}")
    if not generator_script.is_file():
        raise FileNotFoundError(f"Generator script not found: {generator_script}")

    output_dir.mkdir(parents=True, exist_ok=True)

    with csv_path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)

        for line_num, raw_row in enumerate(reader, start=1):
            # Skip completely blank lines
            if not raw_row or all(cell.strip() == "" for cell in raw_row):
                continue

            # Skip comment lines starting with '#' (after optional leading whitespace)
            if raw_row[0].lstrip().startswith("#"):
                continue

            words = [cell.strip() for cell in raw_row]
            if len(words) != 4:
                raise ValueError(
                    f"Line {line_num} has {len(words)} values (expected 4): {raw_row}"
                )

            output_file = output_dir / f"{'-'.join(words)}.stl"

            # Remove any stale file from an earlier run before generating
            if output_file.exists():
                output_file.unlink()

            cmd = [
                sys.executable,
                str(generator_script),
                *words,
                "-o",
                str(output_file),
            ]

            print(f"[Line {line_num}] Generating {output_file.name} ...")
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                print(result.stdout, end="")
                print(result.stderr, file=sys.stderr, end="")
                raise RuntimeError(
                    f"Generator script failed on line {line_num} (exit code {result.returncode})"
                )

            wait_for_file(output_file, timeout=timeout)
            print(f"[Line {line_num}] Verified {output_file}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Batch-generate STL files sequentially from a 4-column CSV."
    )
    parser.add_argument("csv_file", type=Path, help="Path to comma-separated input file")
    parser.add_argument(
        "-s",
        "--script",
        type=Path,
        default=Path("make_plate.py"),
        help="Path to the STL generator script (default: make_plate.py)",
    )
    parser.add_argument(
        "-d",
        "--output-dir",
        type=Path,
        default=Path("output_stls"),
        help="Directory to write generated STL files (default: output_stls)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Seconds to wait for each output STL file to appear (default: 30)",
    )
    args = parser.parse_args()

    try:
        run_batch(
            csv_path=args.csv_file,
            generator_script=args.script,
            output_dir=args.output_dir,
            timeout=args.timeout,
        )
    except Exception as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    print("\nAll rows completed successfully.")


if __name__ == "__main__":
    main()