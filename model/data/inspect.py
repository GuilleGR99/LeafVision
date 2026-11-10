
from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean

from PIL import Image, ImageDraw, ImageOps


SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
THUMBNAIL_SIZE = (180, 180)
SAMPLE_COLUMNS = 4


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect a plant leaf image dataset."
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        required=True,
        help="Dataset root directory. Each class must have its own subdirectory.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("reports"),
        help="Directory where inspection reports will be saved.",
    )
    parser.add_argument(
        "--samples-per-class",
        type=int,
        default=4,
        help="Number of sample images per class in the contact sheet.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed used to select sample images.",
    )
    return parser.parse_args()


def calculate_sha256(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def inspect_image(path: Path) -> dict:
    """Validate an image and return its basic metadata."""
    with Image.open(path) as image:
        image.verify()

    with Image.open(path) as image:
        width, height = image.size

        return {
            "width": width,
            "height": height,
            "format": image.format,
            "mode": image.mode,
            "aspect_ratio": round(width / height, 4),
        }


def collect_dataset(data_dir: Path) -> dict:
    classes = sorted(
        path for path in data_dir.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    )

    if not classes:
        raise ValueError(f"No class directories found in: {data_dir}")

    records = []
    corrupt_images = []
    unsupported_files = []
    hashes = defaultdict(list)

    for class_dir in classes:
        for path in sorted(class_dir.rglob("*")):
            if not path.is_file() or path.name.startswith("."):
                continue

            if path.suffix.lower() not in SUPPORTED_FORMATS:
                unsupported_files.append(str(path.relative_to(data_dir)))
                continue

            relative_path = str(path.relative_to(data_dir))

            try:
                metadata = inspect_image(path)
                image_hash = calculate_sha256(path)

                record = {
                    "path": relative_path,
                    "class": class_dir.name,
                    "size_bytes": path.stat().st_size,
                    "sha256": image_hash,
                    **metadata,
                }

                records.append(record)
                hashes[image_hash].append(relative_path)

            except Exception as error:
                corrupt_images.append({
                    "path": relative_path,
                    "error": str(error),
                })

    duplicates = [
        paths for paths in hashes.values()
        if len(paths) > 1
    ]

    return {
        "classes": [path.name for path in classes],
        "records": records,
        "corrupt_images": corrupt_images,
        "unsupported_files": unsupported_files,
        "duplicates": duplicates,
    }


def build_report(dataset: dict, data_dir: Path) -> dict:
    records = dataset["records"]

    class_counts = Counter(record["class"] for record in records)
    dimensions = Counter(
        (record["width"], record["height"]) for record in records
    )
    formats = Counter(record["format"] for record in records)
    modes = Counter(record["mode"] for record in records)

    counts = list(class_counts.values())

    report = {
        "dataset": str(data_dir.resolve()),
        "summary": {
            "num_classes": len(dataset["classes"]),
            "num_images": len(records),
            "num_corrupt_images": len(dataset["corrupt_images"]),
            "num_unsupported_files": len(dataset["unsupported_files"]),
            "num_duplicate_groups": len(dataset["duplicates"]),
            "num_images_in_duplicate_groups": sum(
                len(group) for group in dataset["duplicates"]
            ),
            "total_size_mb": round(
                sum(record["size_bytes"] for record in records) / (1024**2),
                2,
            ),
        },
        "class_distribution": {
            class_name: class_counts.get(class_name, 0)
            for class_name in dataset["classes"]
        },
        "class_statistics": {
            "minimum": min(counts, default=0),
            "maximum": max(counts, default=0),
            "mean": round(mean(counts), 2) if counts else 0,
            "imbalance_ratio": round(max(counts) / min(counts), 2)
            if counts and min(counts) > 0 else None,
        },
        "image_formats": dict(formats.most_common()),
        "image_modes": dict(modes.most_common()),
        "dimensions": [
            {
                "width": width,
                "height": height,
                "count": count,
            }
            for (width, height), count in dimensions.most_common()
        ],
        "corrupt_images": dataset["corrupt_images"],
        "unsupported_files": dataset["unsupported_files"],
        "exact_duplicates": dataset["duplicates"],
        "images": records,
    }

    return report


def create_contact_sheet(
    dataset: dict,
    output_path: Path,
    samples_per_class: int,
    seed: int,
) -> None:
    rng = random.Random(seed)
    records_by_class = defaultdict(list)

    for record in dataset["records"]:
        records_by_class[record["class"]].append(record)

    selected = []

    for class_name in dataset["classes"]:
        samples = records_by_class[class_name]
        selected.extend(
            rng.sample(samples, min(samples_per_class, len(samples)))
        )

    cell_width = THUMBNAIL_SIZE[0]
    cell_height = THUMBNAIL_SIZE[1] + 35
    rows = (len(selected) + SAMPLE_COLUMNS - 1) // SAMPLE_COLUMNS

    sheet = Image.new(
        "RGB",
        (SAMPLE_COLUMNS * cell_width, rows * cell_height),
        "white",
    )
    draw = ImageDraw.Draw(sheet)

    for index, record in enumerate(selected):
        path = Path(dataset["root"]) / record["path"]
        x = (index % SAMPLE_COLUMNS) * cell_width
        y = (index // SAMPLE_COLUMNS) * cell_height

        with Image.open(path) as image:
            thumbnail = ImageOps.contain(
                image.convert("RGB"),
                THUMBNAIL_SIZE,
            )

        image_x = x + (cell_width - thumbnail.width) // 2
        image_y = y + (THUMBNAIL_SIZE[1] - thumbnail.height) // 2

        sheet.paste(thumbnail, (image_x, image_y))
        draw.text(
            (x + 4, y + THUMBNAIL_SIZE[1] + 5),
            record["class"][:28],
            fill="black",
        )

    sheet.save(output_path, quality=90)


def main() -> None:
    args = parse_args()
    data_dir = args.data_dir.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()

    if not data_dir.is_dir():
        raise NotADirectoryError(f"Dataset directory not found: {data_dir}")

    if args.samples_per_class < 1:
        raise ValueError("--samples-per-class must be at least 1")

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Inspecting dataset: {data_dir}")
    dataset = collect_dataset(data_dir)
    dataset["root"] = str(data_dir)

    report = build_report(dataset, data_dir)

    report_path = output_dir / "inspection_report.json"
    report_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    contact_sheet_path = output_dir / "sample_images.jpg"
    create_contact_sheet(
        dataset,
        contact_sheet_path,
        args.samples_per_class,
        args.seed,
    )

    summary = report["summary"]

    print("\nInspection completed.")
    print(f"Classes: {summary['num_classes']}")
    print(f"Valid images: {summary['num_images']}")
    print(f"Corrupt images: {summary['num_corrupt_images']}")
    print(f"Unsupported files: {summary['num_unsupported_files']}")
    print(f"Duplicate groups: {summary['num_duplicate_groups']}")
    print(f"Class imbalance ratio: "
          f"{report['class_statistics']['imbalance_ratio']}")
    print(f"\nReport: {report_path}")
    print(f"Samples: {contact_sheet_path}")


if __name__ == "__main__":
    main()
