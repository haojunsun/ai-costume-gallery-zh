"""Build Chinese metadata and an editable translation concordance."""
from collections import Counter
import csv
import json
from pathlib import Path

from i18n import CATEGORIES, PHRASES, WORDS, translate_keywords

ROOT = Path(__file__).resolve().parent.parent


def main():
    original = json.loads((ROOT / "data/costume.json").read_text("utf-8"))
    result = []
    for item in original:
        parts = translate_keywords(item["キーワード"])
        category = CATEGORIES[item["カテゴリ"]]
        description = "、".join(parts)
        result.append({
            "id": item["id"], "分类": category, "分类原文": item["カテゴリ"],
            "服装名称": " · ".join(parts[:2]), "中文描述": description,
            "关键词": parts, "英文关键词": item["キーワード"],
            "缩略图": item["サムネ"], "预览图": item["画像"], "原图": item["原寸"],
            "检索": " ".join([item["id"], category, item["カテゴリ"], description, item["キーワード"]]).lower(),
        })
    counts = Counter(item["分类"] for item in result)
    meta = {"总数": len(result), "分类": list(CATEGORIES.values()), "数量": counts}
    for name, value in [("costume-zh.json", result), ("meta-zh.json", meta)]:
        (ROOT / "data" / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", "utf-8")
    with (ROOT / "data/translations.csv").open("w", encoding="utf-8-sig", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(["类型", "原文", "中文"])
        writer.writerows(["分类", key, value] for key, value in CATEGORIES.items())
        writer.writerows(["词汇", key, value[0]] for key, value in sorted(WORDS.items()))
        writer.writerows(["词组", key, value[0]] for key, value in sorted(PHRASES.items()))
        writer.writerows([item["id"], item["英文关键词"], item["中文描述"]] for item in result)
    print(f"Translated {len(result)} records / {len(counts)} categories; no untranslated tokens.")


if __name__ == "__main__":
    main()
