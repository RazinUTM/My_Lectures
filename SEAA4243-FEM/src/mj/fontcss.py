"""The local font CSS with FONTSDIR resolved to src/fonts/node_modules (run npm ci in src/fonts once)."""
import pathlib

HERE = pathlib.Path(__file__).resolve().parent


def font_css():
    nm = (HERE.parent / "fonts" / "node_modules").resolve()
    if not nm.exists():
        raise SystemExit("fonts missing: run  (cd src/fonts && npm ci)  first")
    return (HERE / "fonts_local.css").read_text().replace("FONTSDIR", "file://" + str(nm))
