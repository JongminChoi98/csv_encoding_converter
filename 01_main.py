from pathlib import Path


def create_required_folders():
    base_dir = Path(__file__).parent
    input_dir = base_dir / "input"
    output_dir = base_dir / "output"

    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"[OK] input 폴더: {input_dir}")
    print(f"[OK] output 폴더: {output_dir}")


if __name__ == "__main__":
    create_required_folders()