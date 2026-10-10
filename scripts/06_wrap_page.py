"""Step 6: wrap site/page.html into a full index.html for GitHub Pages."""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
body = (ROOT/"site/page.html").read_text()
(ROOT/"index.html").write_text('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n' + body.replace("<style>", "<style>\n[hidden]{display:none!important}", 1).replace("<div class=\"wrap\">", "</head>\n<body>\n<div class=\"wrap\">", 1) + "\n</body>\n</html>\n")
print("ok")
