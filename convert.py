import pypandoc
import os

try:
    print("Downloading pandoc...")
    pypandoc.download_pandoc()
    print("Pandoc downloaded successfully.")
except Exception as e:
    print(f"Pandoc download failed: {e}")

try:
    input_file = "MARATONaide-10.0.md"
    output_file = "MARATONaide-10.0.docx"
    print(f"Converting {input_file} to {output_file}...")
    pypandoc.convert_file(input_file, 'docx', outputfile=output_file)
    print("Conversion completed successfully!")
except Exception as e:
    print(f"Conversion failed: {e}")
