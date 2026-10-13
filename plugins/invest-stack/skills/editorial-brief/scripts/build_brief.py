#!/usr/bin/env python3
"""Render a weekly brief from content.json into one self-contained HTML page.

Usage: python3 build_brief.py content.json out.html

The page has no external images. Every figure is an inline SVG drawn from the
numbers in content.json, so the brief carries no third-party photos.
"""
import html
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CSS = (HERE.parent / "assets" / "brief.css").read_text(encoding="utf-8")

THAI_MONTHS = ["", "ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."]


def e(s):
    return html.escape(str(s if s is not None else ""), quote=True)


def thai_date(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    return f"{d} {THAI_MONTHS[m]} {y}"


def pct(x, digits=2):
    if x is None:
        return "–"
    return f"{'+' if x > 0 else ''}{x:.{digits}f}%"


def usd(x, digits=2):
    if x is None:
        return "–"
    sign = "-" if x < 0 else ""
    return f"{sign}${abs(x):,.{digits}f}"


def tone(x):
    if x is None:
        return ""
    return "pos" if x > 0 else "neg" if x < 0 else ""


def inline(text):
    """Escape, then allow **bold** and [label](https://url)."""
    import re
    t = e(text)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\[(.+?)\]\((https?://[^\s)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', t)
    t = re.sub(r"\[\^(\d+)\]", r'<sup class="fn"><a href="#src-\1">\1</a></sup>', t)
    return t


def paras(items):
    return "".join(f"<p>{inline(p)}</p>" for p in items)


# ---------- figures ----------

def line_figure(fig):
    """Indexed lines (e.g. portfolio vs S&P 500 rebased to 100)."""
    series = fig["series"]
    labels = fig["labels"]
    W, H, L, R, T, B = 680, 260, 46, 70, 16, 30
    vals = [v for s in series for v in s["values"] if v is not None]
    lo, hi = min(vals), max(vals)
    pad = (hi - lo) * 0.15 or 1
    lo, hi = lo - pad, hi + pad
    n = len(labels)
    X = lambda i: L + (W - L - R) * i / max(n - 1, 1)
    Y = lambda v: T + (H - T - B) * (1 - (v - lo) / (hi - lo))
    out = []
    for k in range(5):
        v = lo + (hi - lo) * k / 4
        out.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" class="grid"/>'
                   f'<text x="{L-8}" y="{Y(v)+4:.1f}" text-anchor="end">{v:.{fig.get("digits",1)}f}</text>')
    step = max(1, math.ceil(n / 7))
    for i, lab in enumerate(labels):
        if i % step == 0 or i == n - 1:
            out.append(f'<text x="{X(i):.1f}" y="{H-8}" text-anchor="middle">{e(lab)}</text>')
    for idx, s in enumerate(series):
        pts = [(X(i), Y(v)) for i, v in enumerate(s["values"]) if v is not None]
        d = "".join(f"{'M' if j == 0 else 'L'}{x:.1f},{y:.1f}" for j, (x, y) in enumerate(pts))
        cl = "s-main" if idx == 0 else f"s-alt s-alt{idx}"
        if idx == 0:
            out.append(f'<path d="{d}L{pts[-1][0]:.1f},{H-B}L{pts[0][0]:.1f},{H-B}Z" class="area"/>')
        out.append(f'<path d="{d}" class="{cl}"/>')
        lx, ly = pts[-1]
        out.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="4" class="dot {cl}"/>'
                   f'<text x="{lx+8:.1f}" y="{ly+4:.1f}" class="endlab {cl}">{e(s["name"])}</text>')
    return f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{e(fig.get("alt",""))}">{"".join(out)}</svg>'


def bars_figure(fig):
    """Horizontal diverging bars, e.g. each holding's contribution in USD or %."""
    items = fig["items"]
    W, rowh, L, R = 680, 30, 110, 90
    H = rowh * len(items) + 20
    m = max(abs(i["value"]) for i in items) or 1
    zero = L + (W - L - R) / 2
    half = (W - L - R) / 2
    out = [f'<line x1="{zero:.1f}" x2="{zero:.1f}" y1="4" y2="{H-6}" class="axis"/>']
    for k, it in enumerate(items):
        y = 10 + k * rowh
        w = half * abs(it["value"]) / m
        x = zero if it["value"] >= 0 else zero - w
        cls = "barpos" if it["value"] >= 0 else "barneg"
        fmt = it.get("display") or (f'{"+" if it["value"]>0 else ""}{it["value"]:.2f}{fig.get("unit","")}')
        out.append(f'<text x="{L-10}" y="{y+15}" text-anchor="end" class="tick-strong">{e(it["label"])}</text>'
                   f'<rect x="{x:.1f}" y="{y+3}" width="{max(w,1.5):.1f}" height="{rowh-12}" rx="2" class="{cls}"/>'
                   f'<text x="{(zero+w+8) if it["value"]>=0 else (zero-w-8):.1f}" y="{y+15}" text-anchor="{"start" if it["value"]>=0 else "end"}">{e(fmt)}</text>')
    return f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{e(fig.get("alt",""))}">{"".join(out)}</svg>'


def alloc_figure(fig):
    """Stacked bar of current weights with target ticks below."""
    items = fig["items"]
    W, H, L, R = 680, 120, 10, 10
    out = []
    x = L
    total = sum(i["weight"] for i in items) or 1
    for k, it in enumerate(items):
        w = (W - L - R) * it["weight"] / total
        out.append(f'<rect x="{x:.1f}" y="20" width="{max(w-2,1):.1f}" height="34" class="seg seg{k%6}"/>')
        if w > 46:
            out.append(f'<text x="{x+6:.1f}" y="42" class="seglab">{e(it["label"])} {it["weight"]:.0f}%</text>')
        x += w
    cum = 0
    for it in items:
        if it.get("target") is None:
            continue
        cum += it["target"]
        tx = L + (W - L - R) * cum / 100
        out.append(f'<line x1="{tx:.1f}" x2="{tx:.1f}" y1="60" y2="74" class="axis"/>')
    out.append(f'<text x="{L}" y="94">แถบ = สัดส่วนจริง · ขีดด้านล่าง = รอยต่อตามเป้าหมาย</text>')
    return f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{e(fig.get("alt",""))}">{"".join(out)}</svg>'


def pulse_art(seed_values, label):
    """Generated cover art: one column per trading-day return, height and tone from the data."""
    W, H = 680, 210
    n = len(seed_values)
    out = []
    colw = W / max(n, 1)
    for i, v in enumerate(seed_values):
        h = min(H * 0.9, 18 + abs(v) * 42)
        y = H / 2 - h / 2
        cls = "artpos" if v >= 0 else "artneg"
        for j in range(5):
            jitter = (j - 2) * colw * 0.13
            hh = h * (1 - abs(j - 2) * 0.17)
            out.append(f'<rect x="{i*colw+colw*0.38+jitter:.1f}" y="{H/2-hh/2:.1f}" width="{colw*0.06:.1f}" height="{hh:.1f}" class="{cls}" opacity="{1-abs(j-2)*0.25:.2f}"/>')
    out.append(f'<line x1="0" x2="{W}" y1="{H/2}" y2="{H/2}" class="axis"/>')
    return f'<svg viewBox="0 0 {W} {H}" class="art" role="img" aria-label="{e(label)}">{"".join(out)}</svg>'


FIGURES = {"line": line_figure, "bars": bars_figure, "alloc": alloc_figure}


def figure(fig):
    if not fig:
        return ""
    svg = FIGURES[fig["kind"]](fig)
    src = f'<span class="figsrc">ที่มา: {inline(fig["source"])}</span>' if fig.get("source") else ""
    return f'<figure class="fig"><div class="figbox">{svg}</div><figcaption>{inline(fig.get("caption",""))} {src}</figcaption></figure>'


# ---------- page ----------

def render(c):
    p = c["portfolio"]
    stats = "".join(
        f'<div class="stat"><span class="k">{e(s["label"])}</span><span class="v {tone(s.get("tone"))}">{e(s["value"])}</span>'
        f'<span class="n">{e(s.get("note",""))}</span></div>' for s in p["stats"])

    holdings_rows = "".join(
        f'<tr><td><b>{e(h["ticker"])}</b><span class="hn">{e(h.get("name",""))}</span></td>'
        f'<td class="num">{usd(h.get("price"))}</td><td class="num {tone(h.get("week_pct"))}">{pct(h.get("week_pct"))}</td>'
        f'<td class="num {tone(h.get("total_pct"))}">{pct(h.get("total_pct"))}</td><td class="num">{h.get("weight",0):.1f}%</td>'
        f'<td class="why">{inline(h.get("why",""))}</td></tr>' for h in p["holdings"])

    stories = []
    for i, s in enumerate(c["stories"]):
        tags = "".join(f'<span class="tag">{e(t)}</span>' for t in s.get("tickers", []))
        impact = ""
        if s.get("impact"):
            impact = (f'<aside class="impact"><h4>กระทบพอร์ตเรายังไง</h4>{paras(s["impact"])}'
                      f'<p class="exposure">ส่วนของพอร์ตที่โดน: <b>{e(s.get("exposure","–"))}</b></p></aside>')
        stories.append(
            f'<article class="story" id="story-{i+1}"><div class="kicker">{e(s.get("kicker",""))} {tags}</div>'
            f'<h3>{e(s["headline"])}</h3><p class="dek">{e(s.get("dek",""))}</p>'
            f'<div class="body">{paras(s["body"])}</div>{figure(s.get("figure"))}{impact}</article>')

    debate = ""
    if c.get("debate"):
        d = c["debate"]
        debate = (f'<section class="debate"><div class="sec-head"><span class="eyebrow">สองฝั่งของเรื่องเดียวกัน</span><h2>{e(d["question"])}</h2></div>'
                  f'<div class="sides"><div class="side bull"><h4>ฝั่งที่มองบวก</h4>{paras(d["bull"])}</div>'
                  f'<div class="side bear"><h4>ฝั่งที่มองลบ</h4>{paras(d["bear"])}</div></div>'
                  f'<p class="verdict"><b>Claude ชั่งแล้ว:</b> {inline(d["verdict"])}</p></section>')

    conf_th = {"high": "มั่นใจสูง", "mid": "มั่นใจปานกลาง", "low": "ยังไม่แน่ใจ"}
    action_items = []
    for a in c.get("actions", []):
        conf = a.get("confidence", "mid")
        trigger = f'<p class="trigger">เปลี่ยนใจถ้า: {inline(a["trigger"])}</p>' if a.get("trigger") else ""
        action_items.append(
            f'<li class="action"><span class="conf c-{e(conf)}">{conf_th.get(conf, "")}</span>'
            f'<div><b>{inline(a["what"])}</b><p>{inline(a["why"])}</p>{trigger}</div></li>')
    actions = "".join(action_items)

    watch = "".join(f'<li><span class="when">{e(w["when"])}</span><span>{inline(w["what"])}</span></li>' for w in c.get("watchlist", []))

    sources = "".join(
        f'<li id="src-{i+1}"><span class="sn">{i+1}</span><a href="{e(s["url"])}" target="_blank" rel="noopener">{e(s["title"])}</a>'
        f'<span class="sp">{e(s.get("publisher",""))}{" · " + e(s["date"]) if s.get("date") else ""}</span></li>'
        for i, s in enumerate(c.get("sources", [])))

    lead = c["lead"]
    cover = pulse_art(c.get("cover_series", [0.2, -0.4, 0.8, 0.1, -0.2]), "ภาพประกอบสร้างจากผลตอบแทนรายวันของพอร์ตสัปดาห์นี้")

    return f"""<title>{e(c['masthead'])} {e(c['edition_label'])}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+Thai:wght@500;700;800&family=Anuphan:wght@400;500;600&family=JetBrains+Mono:wght@400;600&display=swap">
<style>{CSS}</style>
<div class="page">
<header class="mast">
  <div class="mast-row"><span class="brand">{e(c['masthead'])}</span><span class="ed">{e(c['edition_label'])} · {thai_date(c['week_start'])} – {thai_date(c['week_end'])}</span></div>
  <div class="mast-sub">{e(c.get('tagline','จดหมายข่าวพอร์ตหุ้นสหรัฐฯ ส่วนตัว'))}</div>
</header>

<section class="lead">
  <div class="lead-text">
    <span class="eyebrow">{e(lead.get('kicker','เรื่องหลักของสัปดาห์'))}</span>
    <h1>{e(lead['headline'])}</h1>
    <p class="standfirst">{e(lead['dek'])}</p>
    <p class="byline">เขียนโดย Claude สำหรับ {e(c.get('reader','Ped'))} · อ่านราว {e(c.get('read_minutes',6))} นาที · ข้อมูลราคา ณ {e(c.get('prices_as_of',''))}</p>
  </div>
  <figure class="cover">{cover}<figcaption>ภาพประกอบ: แต่ละแท่งคือผลตอบแทนรายวันของพอร์ตในสัปดาห์นี้ (สร้างจากข้อมูล)</figcaption></figure>
  <div class="lead-body">{paras(lead['body'])}</div>
</section>

<section class="numbers">
  <div class="sec-head"><span class="eyebrow">พอร์ตสัปดาห์นี้</span><h2>{e(p['headline'])}</h2></div>
  <div class="stats">{stats}</div>
  {figure(p.get('figure'))}
  <div class="tablebox"><table class="holdings"><thead><tr><th>หุ้น</th><th>ราคา</th><th>สัปดาห์นี้</th><th>ตั้งแต่ซื้อ</th><th>สัดส่วน</th><th>ทำไมขยับ</th></tr></thead><tbody>{holdings_rows}</tbody></table></div>
  {figure(p.get('alloc_figure'))}
</section>

<section class="stories"><div class="sec-head"><span class="eyebrow">ข่าวที่เกี่ยวกับของที่เราถือ</span><h2>{e(c.get('stories_title','เกิดอะไรขึ้นบ้าง'))}</h2></div>{''.join(stories)}</section>

{debate}

<section class="actions"><div class="sec-head"><span class="eyebrow">ถ้าเป็นผม</span><h2>{e(c.get('actions_title','สิ่งที่น่าทำในสัปดาห์หน้า'))}</h2></div>
<ol class="action-list">{actions}</ol>
<p class="disclaimer">{e(c.get('disclaimer','ทั้งหมดนี้เป็นความเห็นประกอบการตัดสินใจจาก Claude ซึ่งไม่ใช่ที่ปรึกษาการลงทุนที่มีใบอนุญาต ตัวเลขในอดีตไม่ได้บอกผลในอนาคต'))}</p>
</section>

<section class="watch"><div class="sec-head"><span class="eyebrow">ปฏิทิน</span><h2>จับตาสัปดาห์หน้า</h2></div><ul class="watch-list">{watch}</ul></section>

<footer class="sources"><h2>แหล่งข้อมูล</h2><ol>{sources}</ol>
<p class="colophon">ภาพและกราฟทั้งหมดในฉบับนี้สร้างจากข้อมูลพอร์ตและราคาตลาด ไม่ได้คัดลอกรูปจากสำนักข่าว อ่านภาพข่าวต้นฉบับได้จากลิงก์ด้านบน</p></footer>
</div>
"""


def main():
    src, out = sys.argv[1], sys.argv[2]
    c = json.loads(Path(src).read_text(encoding="utf-8"))
    Path(out).write_text(render(c), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
