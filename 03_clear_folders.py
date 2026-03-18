# clear_folders.py
from pathlib import Path
import shutil


def clear_directory(directory: Path):
    if not directory.exists():
        print(f"[SKIP] 폴더 없음: {directory}")
        return

    for item in directory.iterdir():
        if item.is_file() or item.is_symlink():
            item.unlink()
            print(f"[DEL FILE] {item}")
        elif item.is_dir():
            shutil.rmtree(item)
            print(f"[DEL DIR ] {item}")


def clear_input_output_folders():
    base_dir = Path(__file__).parent
    input_dir = base_dir / "input"
    output_dir = base_dir / "output"

    clear_directory(input_dir)
    clear_directory(output_dir)

    print("\n[OK] input, output 폴더 비우기 완료")


if __name__ == "__main__":
    clear_input_output_folders()