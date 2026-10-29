"""Validate record parity, translations and every downloaded image container.

Use --decode with Pillow to additionally decode every pixel of every image.
The normal check only requires the Python standard library.
"""
import argparse
from collections import Counter
import concurrent.futures
import csv
import json
from pathlib import Path

from download import image_header
from i18n import CATEGORIES

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--decode", action="store_true")
    args = parser.parse_args()
    if args.decode:
        from PIL import Image
    original = json.loads((ROOT / "data/costume.json").read_text("utf-8"))
    chinese = json.loads((ROOT / "data/costume-zh.json").read_text("utf-8"))
    meta = json.loads((ROOT / "data/meta.json").read_text("utf-8"))
    translated_meta = json.loads((ROOT / "data/meta-zh.json").read_text("utf-8"))
    errors, paths = [], []
    if len(original) != 1407 or len(chinese) != len(original):
        errors.append("Record counts do not match the 1407-record source snapshot")
    if len({item["id"] for item in chinese}) != len(chinese):
        errors.append("Duplicate Chinese IDs")
    if Counter(item["カテゴリ"] for item in original) != meta["counts"]:
        errors.append("Original category counts differ from meta.json")
    if Counter(item["分类"] for item in chinese) != translated_meta["数量"]:
        errors.append("Chinese category counts differ from meta-zh.json")
    if translated_meta["总数"] != len(chinese) or meta["total"] != len(original):
        errors.append("Metadata totals do not match records")
    for source, target in zip(original, chinese):
        if target["id"] != source["id"] or target["分类"] != CATEGORIES[source["カテゴリ"]]:
            errors.append(f"Record identity/category mismatch: {source['id']}")
        for original_field, translated_field in [("サムネ", "缩略图"), ("画像", "预览图"), ("原寸", "原图")]:
            path = target[translated_field]
            if path != source[original_field] or not (ROOT / path).resolve().is_relative_to(ROOT):
                errors.append(f"Invalid asset path: {path}")
                continue
            paths.append(path)
        if not target["服装名称"] or not target["中文描述"] or any("a" <= char.lower() <= "z" for char in target["中文描述"]):
            errors.append(f"Missing/untranslated Chinese description: {target['id']}")
        if target["英文关键词"] != source["キーワード"] or target["id"].lower() not in target["检索"]:
            errors.append(f"Source keywords/search missing: {target['id']}")
    if len(set(paths)) != 4221:
        errors.append(f"Expected 4221 unique assets, got {len(set(paths))}")
    with (ROOT / "data/translations.csv").open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len([row for row in rows if row["类型"] in {item["id"] for item in chinese}]) != len(chinese):
        errors.append("Translation concordance missing records")

    def verify_image(path):
        file = ROOT / path
        if not file.is_file():
            return path, "missing", 0
        content = file.read_bytes()
        if not image_header(content, path):
            return path, "invalid or incomplete image container", len(content)
        if args.decode:
            try:
                with Image.open(file) as image:
                    image.load()
                    if min(image.size) <= 0:
                        return path, "zero image dimensions", len(content)
            except Exception as error:
                return path, str(error), len(content)
        return path, None, len(content)

    size = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for path, error, length in pool.map(verify_image, paths):
            size += length
            if error:
                errors.append(f"{path}: {error}")
    report = {"records": len(chinese), "categories": dict(Counter(item["分类"] for item in chinese)),
              "expected_images": len(paths), "bytes": size, "decoded": args.decode,
              "error_count": len(errors), "errors": errors}
    (ROOT / "data/verification-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", "utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "errors"}, ensure_ascii=False, indent=2))
    for error in errors[:30]:
        print(error)
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
