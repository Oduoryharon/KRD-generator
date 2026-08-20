import shutil
from pathlib import Path

from generator.config import OUTPUT_DIR
from generator.utils import create_directory


# Export raw dataset

def export_raw_data():

    print("=" * 30)
    print("EXPORTING RAW DATASETS")
    print("=" * 30)

    # Source directory

    raw_directory = Path(OUTPUT_DIR) / "raw"

    # Final export directory

    export_directory = Path(OUTPUT_DIR) / "final_export"

    create_directory(export_directory)

    # Check raw directory

    if not raw_directory.exists():

        raise FileNotFoundError(
            f"Raw directory not found: {raw_directory}"
        )

    # Get all csv and xlsx files

    files = list(raw_directory.glob("*.csv"))

    files += list(
        raw_directory.glob("*.xlsx")
    )

    if not files:

        raise ValueError(
            "No raw files found to export."
        )

    # Copy files

    exported_files = []

    for file in files:

        destination = (
            export_directory / file.name
        )

        shutil.copy2(
            file,
            destination
        )

        exported_files.append(
            file.name
        )

        print(
            f"Exported: {file.name}"
        )

    # Summary.
    print("\n" + "=" * 60)

    print(
        f"Successfully exported "
        f"{len(exported_files)} files."
    )

    print(
        f"\nExport location:\n"
        f"{export_directory.resolve()}"
    )

    print("=" * 60)

    return exported_files


# Main

if __name__ == "__main__":

    export_raw_data()