import html as H
from docx import Document

SRC = r"C:\Postgres\MARATONaide\MARATONAIDE ver 4 diagramada.docx"
OUT = r"C:\Postgres\MARATONaide\leer\maratonaide-4-0.html"

d = Document(SRC)
paras = d.paragraphs


def run_markup(p):
    out = []
    for r in p.runs:
        t = H.escape(r.text)
        if not t:
            continue
        if r.italic and r.bold:
            t = "<strong><em>" + t + "</em></strong>"
        elif r.italic:
            t = "<em>" + t + "</em>"
        elif r.bold:
            t = "<strong>" + t + "</strong>"
        out.append(t)
    return "".join(out)


def is_dialogue(p):
    t = p.text.lstrip()
    return t.startswith("—")


blocks = []  # list of (kind, payload)
chapter_idx = 0  # 0 = prólogo ...
chapter_anchor = {}
fin_emitted = [False]  # ensure single FIN

# Body starts at first Heading 1 (PRÓLOGO); cover/legal pages stay out of the reader.
first_h1 = next(i for i, p in enumerate(paras) if p.style.name == "Heading 1")

# collect body
body = paras[first_h1:]
for p in body:
    txt = p.text.strip()
    if not txt:
        continue
    if p.style.name == "Heading 1":
        anchor = "cap-00" if chapter_idx == 0 else "cap-%02d" % chapter_idx
        chapter_anchor[txt] = anchor
        blocks.append(("h1", txt, anchor))
        chapter_idx += 1
    else:
        blocks.append(("p", p, None))

NAV_ITEM_TEMPLATE = """            <li><a href="../index.html">Inicio</a></li>
            <li><a href="maratonaide-4-0.html" class="active">Leer 4.0</a></li>
            <li><a href="../index.html#estructura">Estructura</a></li>
            <li><a href="../index.html#acerca">Acerca</a></li>"""

CSS = """.reader-container { max-width:800px; margin:0 auto; padding:2rem; line-height:1.8; font-family:var(--font-serif); }.reader-header { text-align:center; margin-bottom:3rem; padding-bottom:2rem; border-bottom:1px solid var(--border); }.reader-header h1 { font-size:2.5rem; color:var(--gold); margin-bottom:0.5rem; }.reader-header .subtitle { color:var(--text-secondary); font-style:italic; }.reader-header .meta { margin-top:1rem; font-size:0.9rem; color:var(--text-muted); }.chapter { margin-bottom:3rem; padding-bottom:2rem; border-bottom:1px solid var(--border); }.chapter h2 { font-size:1.8rem; color:var(--gold); margin-bottom:1.5rem; text-align:center; }.chapter h3 { font-size:1.3rem; color:var(--text-primary); margin:2rem 0 1rem; }.timestamp { display:inline-block; background:rgba(212,168,75,0.1); color:var(--gold); padding:0.25rem 0.75rem; border-radius:4px; font-size:0.85rem; margin-bottom:1rem; font-family:var(--font-sans); }.dialogue { margin:1rem 0; padding-left:1rem; border-left:2px solid var(--gold); } .dialogue p { margin:0 0 0.4rem; } .dialogue p:last-child { margin-bottom:0; }.poem { margin:1.5rem 0; padding:1rem 1.5rem; border-left:2px solid var(--gold); font-style:italic; color:var(--text-secondary); }.chapter-end { text-align:center; font-size:0.85rem; color:var(--text-muted); font-family:var(--font-sans); margin:2rem 0; font-style:italic; }.navigation { position:fixed; bottom:2rem; right:2rem; display:flex; gap:0.5rem; z-index:100; flex-direction:column; align-items:flex-end; }.nav-btn { background:var(--bg-card); border:1px solid var(--border); color:var(--text-primary); padding:0.75rem 1rem; border-radius:var(--radius); cursor:pointer; transition:var(--transition); font-size:0.9rem; }.nav-btn:hover { border-color:var(--gold); background:rgba(212,168,75,0.1); }.back-link { display:inline-block; margin-bottom:2rem; color:var(--gold); text-decoration:none; font-family:var(--font-sans); font-size:0.9rem; }.back-link:hover { text-decoration:underline; }.stats { background:var(--bg-card); border:1px solid var(--border); border-radius:var(--radius); padding:1.5rem; margin:2rem 0; display:grid; grid-template-columns:repeat(auto-fit, minmax(150px,1fr)); gap:1rem; text-align:center; }.stat-item { padding:0.5rem; }.stat-value { font-size:1.5rem; color:var(--gold); font-weight:bold; }.stat-label { font-size:0.8rem; color:var(--text-muted); margin-top:0.25rem; }.chapter-divider { border:none; border-top:1px solid var(--border); margin:2rem 0; }"""

out = []
out.append("<!DOCTYPE html>")
out.append('<html lang="es">')
out.append("<head>")
out.append('    <meta charset="UTF-8">')
out.append('    <meta name="viewport" content="width=device-width, initial-scale=1.0">')
out.append("    <title>MARATONAIDE ver 4.0 — Novela filosófica</title>")
out.append('    <meta name="description" content="MARATONAIDE ver 4.0 — Edición diagramada. Novela completa.">')
out.append('    <link rel="stylesheet" href="../css/style.css">')
out.append("    <style>" + CSS + "</style>")
out.append("</head>")
out.append("<body>")
out.append('    <nav class="navbar">')
out.append('        <div class="navbar-inner">')
out.append('            <a href="../index.html" class="logo">')
out.append('                <div class="logo-icon">M</div>')
out.append('                <span class="logo-text">maraton<span>aide</span></span>')
out.append("            </a>")
out.append('            <button class="menu-toggle">☰</button>')
out.append("            <ul class=\"nav-links\">")
out.append(NAV_ITEM_TEMPLATE)
out.append("            </ul>")
out.append("        </div>")
out.append("    </nav>")
out.append('    <main class="reader-container">')
out.append('        <a href="../index.html" class="back-link">← Volver al inicio</a>')
out.append('        <div class="reader-header">')
out.append("            <h1>MARATONAIDE</h1>")
out.append('            <div class="subtitle">La ayuda que convierte una maratón en un viaje por la mente, el cuerpo y el espíritu.</div>')
out.append('            <div class="meta">Alejandro Ochoa Pérez · Medellín, Colombia · Versión 4.0 — Edición diagramada</div>')
out.append("        </div>")
out.append('        <div class="stats">')
out.append('            <div class="stat-item"><div class="stat-value">42.195</div><div class="stat-label">Metros</div></div>')
out.append('            <div class="stat-item"><div class="stat-value">21</div><div class="stat-label">Capítulos</div></div>')
out.append('            <div class="stat-item"><div class="stat-value">7</div><div class="stat-label">Tarjetas</div></div>')
out.append('            <div class="stat-item"><div class="stat-value">2038</div><div class="stat-label">Dorsal</div></div>')
out.append("        </div>")
out.append('        <hr class="chapter-divider">')

chap_num = 0
for kind, payload, anchor in blocks:
    if kind == "h1":
        # open chapter div
        if chap_num > 0:
            out.append("        </div>")
            out.append('        <hr class="chapter-divider">')
        out.append('        <div class="chapter" id="' + anchor + '">')
        out.append("            <h2>" + H.escape(payload) + "</h2>")
        chap_num += 1
    else:
        p = payload
        if (p.text.strip() == "**FIN**" or p.text.strip() == "FIN") and not fin_emitted[0]:
            fin_emitted[0] = True
            out.append('            <p class="chapter-end">FIN</p>')
        elif is_dialogue(p):
            out.append('            <div class="dialogue"><p>' + run_markup(p) + "</p></div>")
        else:
            out.append("            <p>" + run_markup(p) + "</p>")

if chap_num > 0 and not None:  # close last chapter
    out.append("        </div>")

out.append("    </main>")
out.append('    <div class="navigation">')
out.append('        <button class="nav-btn" onclick="window.scrollTo({top:0,behavior:\'smooth\'})">↑ Inicio</button>')
out.append("    </div>")
out.append("</body>")
out.append("</html>")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("OK", OUT)
print("capitulos:", chap_num)