import os, json, pathlib, datetime

BASE = "https://galanisaistandards-christos.github.io/pwem-mirror/"
ROOT = pathlib.Path(".").resolve()
CHRON = ROOT / "memory" / "chron"
CATALOG = ROOT / "memory" / "catalog.json"

def abs_url(rel_path: pathlib.Path) -> str:
    rel = str(rel_path).replace("\\", "/").lstrip("./")
    return BASE + rel

def find_json_files():
    items = []
    if not CHRON.exists():
        return items
    for year_dir in sorted(CHRON.iterdir()):
        if not year_dir.is_dir() or not year_dir.name.isdigit():
            continue
        for month_dir in sorted(year_dir.iterdir()):
            if not month_dir.is_dir():
                continue
            for f in sorted(month_dir.glob("*.json")):
                items.append(f.relative_to(ROOT))
    return items

def ensure_parent(path: pathlib.Path):
    path.parent.mkdir(parents=True, exist_ok=True)

def write_root_index(years):
    out = ROOT / "index.html"
    ensure_parent(out)
    lines = [
        "<!DOCTYPE html><html><head><meta charset='utf-8'><title>PWEM · Index</title></head><body>",
        "<h1>PWEM · Years</h1>",
        "<p>Κάθε σύνδεσμος είναι <em>απόλυτος</em>.</p>",
    ]
    for y in years:
        url = abs_url(pathlib.Path("memory/chron") / y / "index.html")
        lines.append(f"<p><a href='{url}'>{url}</a></p>")
    lines.append("</body></html>")
    out.write_text("\n".join(lines), encoding="utf-8")

def write_year_index(year, months):
    out = ROOT / "memory" / "chron" / year / "index.html"
    ensure_parent(out)
    lines = [
        "<!DOCTYPE html><html><head><meta charset='utf-8'>",
        f"<title>PWEM · {year}</title></head><body>",
        f"<h1>PWEM · {year}</h1>",
        "<p>Μήνες:</p>",
    ]
    for m in months:
        url = abs_url(pathlib.Path("memory/chron") / year / m / "index.html")
        lines.append(f"<p><a href='{url}'>{url}</a></p>")
    lines.append("</body></html>")
    out.write_text("\n".join(lines), encoding="utf-8")

def write_month_index(year, month, files):
    out = ROOT / "memory" / "chron" / year / month / "index.html"
    ensure_parent(out)
    lines = [
        "<!DOCTYPE html><html><head><meta charset='utf-8'>",
        f"<title>PWEM · {year}/{month}</title></head><body>",
        f"<h1>PWEM · {year}/{month}</h1>",
        "<p>Κάθε link είναι <em>απόλυτο</em> προς το JSON.</p>",
    ]
    for f in files:
        url = abs_url(f)
        lines.append(f"<p><a href='{url}'>{url}</a></p>")
    lines.append("</body></html>")
    out.write_text("\n".join(lines), encoding="utf-8")

def build_indexes_and_catalog():
    json_files = find_json_files()
    # catalog
    items = []
    for p in json_files:
        parts = p.parts  # memory/chron/YYYY/MM/file.json
        year, month, name = parts[2], parts[3], parts[4]
        full = ROOT / p
        size = full.stat().st_size if full.exists() else None
        items.append({
            "year": int(year),
            "month": month,
            "name": name,
            "url": abs_url(p),
            "rel_path": str(p).replace("\\", "/"),
            "size_bytes": size,
        })
    items.sort(key=lambda x: (x["year"], x["month"], x["name"]))
    CATALOG.parent.mkdir(parents=True, exist_ok=True)
    CATALOG.write_text(json.dumps({
        "version": "1.0",
        "generated_at": datetime.datetime.utcnow().isoformat()+"Z",
        "items": items
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    # root index (years)
    years = sorted({str(it["year"]) for it in items})
    write_root_index(years)

    # year & month indexes
    by_year_month = {}
    for it in items:
        by_year_month.setdefault(str(it["year"]), {}).setdefault(it["month"], []).append(
            pathlib.Path(it["rel_path"])
        )
    for y, months in by_year_month.items():
        write_year_index(y, sorted(months.keys()))
        for m, files in months.items():
            write_month_index(y, m, files)

if __name__ == "__main__":
    build_indexes_and_catalog()
    print("PWEM indexes & catalog generated.")
