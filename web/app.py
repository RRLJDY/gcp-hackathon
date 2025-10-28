from flask import Flask, send_from_directory, abort, render_template_string
from pathlib import Path

app = Flask(__name__)

GENERATED_DIR = Path(__file__).resolve().parent.parent / "generated_images"


def _get_latest_image_path() -> Path:
    if not GENERATED_DIR.exists():
        return None
    images = sorted(
        [p for p in GENERATED_DIR.iterdir() if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return images[0] if images else None


@app.get("/")
def index():
    latest = _get_latest_image_path()
    if latest is None:
        return "No images generated yet.", 200
    return render_template_string(
        """
        <!doctype html>
        <html>
        <head>
          <meta charset="utf-8" />
          <meta name="viewport" content="width=device-width, initial-scale=1" />
          <title>Latest Generated Image</title>
          <style>
            body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; margin: 24px; }
            img { max-width: 100%; height: auto; border-radius: 12px; box-shadow: 0 6px 24px rgba(0,0,0,0.15); }
            .wrap { max-width: 960px; margin: 0 auto; }
          </style>
        </head>
        <body>
          <div class="wrap">
            <h1>Latest Generated Image</h1>
            <p>Auto-refresh to see new results.</p>
            <img src="/image/latest" alt="Generated image" />
          </div>
          <script>setInterval(() => location.reload(), 15000)</script>
        </body>
        </html>
        """
    )


@app.get("/image/latest")
def get_latest():
    latest = _get_latest_image_path()
    if latest is None:
        abort(404)
    return send_from_directory(latest.parent, latest.name)


@app.get("/image/<path:filename>")
def get_image(filename: str):
    path = GENERATED_DIR / filename
    if not path.exists():
        abort(404)
    return send_from_directory(path.parent, path.name)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)


