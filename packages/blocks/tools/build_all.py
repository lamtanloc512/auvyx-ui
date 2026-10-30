"""Regenerate every block and format the HTML with Prettier.

  python3 packages/blocks/tools/build_all.py
"""
import pathlib, runpy, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
for mod in ["auth", "sidebar", "calendar", "dashboard"]:
    runpy.run_path(str(HERE / f"{mod}.py"), run_name="__main__")

files = sorted(str(p) for p in (HERE.parent).glob("*.html"))
subprocess.run(["node", str(ROOT / "packages/docs/tools/format-html.mjs"), "--files", *files], check=True)
print(f"formatted {len(files)} blocks")
