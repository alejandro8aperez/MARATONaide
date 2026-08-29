import markdown
import codecs

with codecs.open('MARATONaide-10.0.md', mode='r', encoding='utf-8') as f:
    text = f.read()

html_content = markdown.markdown(text)

full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>MARATONaide</title>
</head>
<body>
{html_content}
</body>
</html>
"""

with codecs.open('MARATONaide-10.0.html', mode='w', encoding='utf-8') as f:
    f.write(full_html)
