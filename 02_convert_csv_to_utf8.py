from pathlib import Path
import hashlib


CANDIDATE_ENCODINGS = [
    "utf-8-sig",
    "utf-8",
    "cp949",
    "euc-kr",
]


def decode_input_bytes(raw: bytes, file_name: str) -> tuple[str, str]:
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


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def detect_line_ending(text: str) -> str:
    has_crlf = "\r\n" in text
    has_lf = "\n" in text
    has_cr = "\r" in text and not has_crlf

    if has_crlf and has_lf:
        return "CRLF/LF mixed"
    if has_crlf:
        return "CRLF"
    if has_lf:
        return "LF"
    if has_cr:
        return "CR"
    return "No line ending"


def count_lines(text: str) -> int:
    if not text:
        return 0
    return text.count("\n") + (0 if text.endswith("\n") else 1)


def format_size(num_bytes: int) -> str:
    return f"{num_bytes:,} bytes"


def find_first_difference(a: str, b: str) -> tuple[int | None, str, str]:
    min_len = min(len(a), len(b))

    for i in range(min_len):
        if a[i] != b[i]:
            start = max(0, i - 30)
            end = i + 30
            return i, repr(a[start:end]), repr(b[start:end])

    if len(a) != len(b):
        return min_len, repr(a[max(0, min_len - 30):min_len + 30]), repr(
            b[max(0, min_len - 30):min_len + 30]
        )

    return None, "", ""


def convert_one_csv(input_file: Path, output_dir: Path) -> Path:
    raw = input_file.read_bytes()
    text, _ = decode_input_bytes(raw, input_file.name)

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{input_file.stem}_utf8{input_file.suffix}"

    output_bytes = text.encode("utf-8-sig")
    output_file.write_bytes(output_bytes)

    return output_file


def verify_one_pair(input_file: Path, output_file: Path) -> dict:
    input_raw = input_file.read_bytes()
    input_text, detected_encoding = decode_input_bytes(input_raw, input_file.name)

    output_raw = output_file.read_bytes()
    output_text = output_raw.decode("utf-8-sig", errors="strict")

    input_hash = sha256_text(input_text)
    output_hash = sha256_text(output_text)

    is_same = input_text == output_text

    return {
        "file_name": input_file.name,
        "output_name": output_file.name,
        "detected_encoding": detected_encoding,
        "input_size": len(input_raw),
        "output_size": len(output_raw),
        "input_chars": len(input_text),
        "output_chars": len(output_text),
        "input_lines": count_lines(input_text),
        "output_lines": count_lines(output_text),
        "input_line_ending": detect_line_ending(input_text),
        "output_line_ending": detect_line_ending(output_text),
        "input_hash": input_hash,
        "output_hash": output_hash,
        "is_same": is_same,
        "input_text": input_text,
        "output_text": output_text,
    }


def print_verification_report(result: dict):
    print("=" * 72)
    print(f"FILE            : {result['file_name']}")
    print(f"OUTPUT          : {result['output_name']}")
    print(f"ENCODING        : {result['detected_encoding']} -> utf-8-sig")
    print("-" * 72)
    print(f"INPUT SIZE      : {format_size(result['input_size'])}")
    print(f"OUTPUT SIZE     : {format_size(result['output_size'])}")
    print(f"INPUT CHARS     : {result['input_chars']:,}")
    print(f"OUTPUT CHARS    : {result['output_chars']:,}")
    print(f"INPUT LINES     : {result['input_lines']:,}")
    print(f"OUTPUT LINES    : {result['output_lines']:,}")
    print(f"INPUT NEWLINE   : {result['input_line_ending']}")
    print(f"OUTPUT NEWLINE  : {result['output_line_ending']}")
    print("-" * 72)
    print(f"TEXT SHA256 IN  : {result['input_hash']}")
    print(f"TEXT SHA256 OUT : {result['output_hash']}")

    if result["is_same"]:
        print("-" * 72)
        print("RESULT          : VERIFIED")
        print("DETAIL          : Decoded text content is identical.")
    else:
        diff_index, input_snippet, output_snippet = find_first_difference(
            result["input_text"], result["output_text"]
        )
        print("-" * 72)
        print("RESULT          : FAILED")
        print("DETAIL          : Decoded text content is different.")
        if diff_index is not None:
            print(f"FIRST DIFF POS  : {diff_index}")
            print(f"INPUT SNIPPET   : {input_snippet}")
            print(f"OUTPUT SNIPPET  : {output_snippet}")


def process_all_csv():
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

    print(f"\n총 {len(csv_files)}개 CSV 파일을 변환하고 검증합니다.\n")

    success_count = 0
    fail_count = 0

    for input_file in csv_files:
        try:
            output_file = convert_one_csv(input_file, output_dir)
            result = verify_one_pair(input_file, output_file)
            print_verification_report(result)

            if result["is_same"]:
                success_count += 1
            else:
                fail_count += 1

            print()

        except Exception as e:
            print("=" * 72)
            print(f"FILE            : {input_file.name}")
            print("RESULT          : ERROR")
            print(f"DETAIL          : {e}")
            print()
            fail_count += 1

    print("#" * 72)
    print("FINAL SUMMARY")
    print(f"SUCCESS         : {success_count}")
    print(f"FAILED          : {fail_count}")
    print("#" * 72)


if __name__ == "__main__":
    process_all_csv()