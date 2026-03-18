from pathlib import Path


CANDIDATE_ENCODINGS = [
    "utf-8-sig",
    "utf-8",
    "cp949",
    "euc-kr",
]


def decode_bytes_strict(raw: bytes, file_name: str) -> tuple[str, str]:
    last_error = None

    for enc in CANDIDATE_ENCODINGS:
        try:
            text = raw.decode(enc, errors="strict")
            return text, enc
        except UnicodeDecodeError as e:
            last_error = e

    raise UnicodeError(
        f"디코딩 실패: {file_name} / 시도한 인코딩: {CANDIDATE_ENCODINGS}"
    ) from last_error


def convert_one_csv(input_file: Path, output_dir: Path) -> Path:
    raw = input_file.read_bytes()
    text, detected_encoding = decode_bytes_strict(raw, input_file.name)

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{input_file.stem}_utf8{input_file.suffix}"

    output_bytes = text.encode("utf-8-sig")
    output_file.write_bytes(output_bytes)

    print(f"[OK] {input_file.name} ({detected_encoding}) -> {output_file.name}")
    return output_file


def convert_all_csv_in_input_folder():
    base_dir = Path(__file__).parent
    input_dir = base_dir / "input"
    output_dir = base_dir / "output"

    if not input_dir.exists():
        print("input 폴더가 없습니다. 먼저 main.py를 실행하세요.")
        return

    csv_files = sorted(input_dir.glob("*.csv"))

    if not csv_files:
        print("input 폴더에 CSV 파일이 없습니다.")
        return

    print(f"총 {len(csv_files)}개 CSV 파일을 변환합니다.\n")

    success_count = 0
    fail_count = 0

    for csv_file in csv_files:
        try:
            convert_one_csv(csv_file, output_dir)
            success_count += 1
        except Exception as e:
            print(f"[FAIL] {csv_file.name} -> {e}")
            fail_count += 1

    print("\n변환 완료")
    print(f"성공: {success_count}")
    print(f"실패: {fail_count}")


if __name__ == "__main__":
    convert_all_csv_in_input_folder()