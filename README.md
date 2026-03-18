# CSV Encoding Converter

A lightweight Python utility for converting CSV files to **UTF-8 with BOM (`utf-8-sig`)**.

It is useful when some CSV files display Korean text correctly while others appear garbled because of mixed encodings such as `cp949`, `euc-kr`, or `utf-8`.

## Files

- `01_main.py`  
  Creates the `input` and `output` folders.

- `02_convert_csv_to_utf8.py`  
  Converts all CSV files in `input` to UTF-8 with BOM and verifies that the decoded text content is unchanged.

- `03_clear_folders.py`  
  Clears all files inside `input` and `output` while keeping the folders.

## Execution Order

Run the scripts in the following order:

1. **`01_main.py`**  
   Create the `input` and `output` folders.

2. Put your source CSV files into the **`input`** folder.

3. **`02_convert_csv_to_utf8.py`**  
   Convert and verify all CSV files.

4. **`03_clear_folders.py`** *(optional)*  
   Clear the `input` and `output` folders when needed.

## Project Structure

```text
csv_encoding_converter/
├── 01_main.py
├── 02_convert_csv_to_utf8.py
├── 03_clear_folders.py
├── input/
└── output/
