from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


root = Path(__file__).resolve().parents[1]
source = root / "lambda" / "app.py"
output = root / "lambda" / "build" / "medibook-api.zip"
output.parent.mkdir(parents=True, exist_ok=True)
with ZipFile(output, "w", ZIP_DEFLATED) as archive:
    archive.write(source, "app.py")
print(f"Created {output}")

