"""Download the local costume image collection; resumable, standard library only."""
import argparse
import concurrent.futures
import json
from pathlib import Path
import time
import urllib.request

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://ai-costume-gallery.pages.dev/"
FIELDS = ("サムネ", "画像", "原寸")


def image_header(data, path):
    if path.endswith(".png"):
        return data.startswith(b"\x89PNG\r\n\x1a\n") and b"IEND" in data[-32:]
    return len(data) > 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP" and int.from_bytes(data[4:8], "little") + 8 == len(data)


def download(path):
    target = ROOT / path
    if target.exists() and image_header(target.read_bytes(), path):
        return "cached", path, target.stat().st_size
    target.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(5):
        try:
            request = urllib.request.Request(BASE + path, headers={"User-Agent": "Mozilla/5.0", "Referer": BASE})
            with urllib.request.urlopen(request, timeout=75) as response:
                content = response.read()
                expected = response.headers.get("Content-Length")
            if expected and len(content) != int(expected):
                raise ValueError("incomplete response")
            if not image_header(content, path):
                raise ValueError("invalid image header or incomplete image")
            temporary = target.with_suffix(target.suffix + ".part")
            temporary.write_bytes(content)
            temporary.replace(target)
            return "downloaded", path, len(content)
        except Exception as error:
            if attempt == 4:
                return "failed", path, str(error)
            time.sleep(min(2 ** attempt, 12))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=48)
    parser.add_argument("--limit", type=int, default=0, help="Download only the first N files for diagnosis")
    args = parser.parse_args()
    data = json.loads((ROOT / "data/costume.json").read_text("utf-8"))
    paths = list(dict.fromkeys(row[field] for row in data for field in FIELDS))
    if args.limit:
        paths = paths[:args.limit]
    counts = {"cached": 0, "downloaded": 0, "failed": 0}
    failures = []
    size = 0
    start = time.monotonic()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        jobs = [pool.submit(download, path) for path in paths]
        for completed, job in enumerate(concurrent.futures.as_completed(jobs), 1):
            status, path, result = job.result()
            counts[status] += 1
            if status == "failed":
                failures.append({"path": path, "error": result})
                print(f"FAILED {path}: {result}", flush=True)
            else:
                size += result
            if completed % 100 == 0 or completed == len(paths):
                print(f"{completed}/{len(paths)} {counts} {size / 1048576:.1f} MiB {time.monotonic()-start:.0f}s", flush=True)
    report = {"total": len(paths), **counts, "bytes": size, "failures": failures}
    (ROOT / "data/download-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", "utf-8")
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
