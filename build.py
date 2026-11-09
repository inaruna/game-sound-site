#!/usr/bin/env python3
"""ゲーム音のどうぐ箱 — 静的サイトビルダー

使い方:  python3 build.py
  config.json   … サイト名・URL・運営者情報・itchのURL
  links.json    … アフィリエイトリンク（空の枠は表示されません）
  content/articles/*.md … 記事
  tools/*.html  … 無料ツール
出力先: docs/  （GitHub Pages が main ブランチの /docs を公開します）
"""
import html
import json
import re
import shutil
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
DIST = ROOT / "docs"
CFG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
_RAW = json.loads((ROOT / "links.json").read_text(encoding="utf-8"))
RAKUTEN_ID = str(_RAW.get("RAKUTEN_ID", "")).strip()
RAKUTEN_ITEMS = _RAW.get("RAKUTEN_ITEMS", {}) or {}
LINKS = {k: v.strip() for k, v in _RAW.items()
         if not k.startswith("_") and isinstance(v, str) and k != "RAKUTEN_ID"}
HAS_AMAZON = any(v for k, v in LINKS.items() if k.startswith("AMAZON"))
HAS_RAKUTEN = bool(RAKUTEN_ID)
HAS_UNITY = any(v for k, v in LINKS.items() if k.startswith("UNITY"))
SITE = CFG["site_name"]
BASE = CFG["site_url"].rstrip("/")
from urllib.parse import urlparse
SITE_ROOT = (urlparse(BASE).path.rstrip("/") + "/") or "/"
esc = html.escape

CSS = """
:root{--bg:#f7f7f5;--card:#fff;--text:#1d1d1f;--muted:#5f6368;--line:#e3e3df;--accent:#2f6fde;--accent-soft:#e8f0fd;--code:#f0f0ec}
@media (prefers-color-scheme:dark){:root{--bg:#141416;--card:#1e1e22;--text:#ececef;--muted:#a0a0a8;--line:#2f2f35;--accent:#7aa7ff;--accent-soft:#22304a;--code:#26262b}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font-family:"Hiragino Sans","Noto Sans JP","Yu Gothic UI",system-ui,sans-serif;line-height:1.85;font-size:16px}
a{color:var(--accent)}
.top{border-bottom:1px solid var(--line);background:var(--card)}
.top .in{max-width:760px;margin:0 auto;padding:12px 16px;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
.logo{font-weight:700;text-decoration:none;color:var(--text)}
.top nav a{font-size:14px;margin-left:14px;color:var(--muted);text-decoration:none}
main{max-width:760px;margin:0 auto;padding:24px 16px 56px}
.pr{font-size:14px;color:var(--text);background:var(--code);border-left:4px solid var(--accent);padding:6px 10px;margin:0 0 16px}
h1{font-size:clamp(22px,4.4vw,30px);line-height:1.45;margin:8px 0 16px}
h2{font-size:21px;line-height:1.5;margin:44px 0 14px;padding-bottom:6px;border-bottom:2px solid var(--line)}
h3{font-size:18px;margin:30px 0 10px}
p{margin:0 0 16px}
ul,ol{padding-left:1.4em;margin:0 0 16px}
li{margin:4px 0}
table{width:100%;border-collapse:collapse;margin:8px 0 20px;font-size:15px;display:block;overflow-x:auto}
th,td{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}
th{background:var(--code)}
pre{background:var(--code);border-radius:10px;padding:14px;overflow-x:auto;font-size:13.5px;line-height:1.6}
code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
p code,li code,td code{background:var(--code);padding:1px 5px;border-radius:5px;font-size:.9em}
.box{display:block;text-decoration:none;color:inherit;border:1px solid var(--line);background:var(--card);border-radius:14px;padding:16px 18px;margin:24px 0}
.box:hover{border-color:var(--accent)}
.box .tag{display:block;font-size:13px;color:var(--text);font-weight:600}
.box strong{display:block;font-size:17px;margin:2px 0 4px}
.box span{display:block;font-size:14px;color:var(--muted)}
.box .go{display:block;margin-top:8px;font-size:14px;color:var(--accent);font-weight:600}
.own,.toolbox{border-color:var(--accent);background:var(--accent-soft)}
.btns{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.btn{display:inline-block;padding:6px 14px;border:1px solid var(--accent);border-radius:999px;font-size:14px;font-weight:600;text-decoration:none}
.meta{font-size:13px;color:var(--muted);margin-bottom:24px}
.list{list-style:none;padding:0}
.list li{margin:0 0 12px}
.list a{display:block;text-decoration:none;color:inherit;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px}
.list a:hover{border-color:var(--accent)}
.list strong{display:block;line-height:1.5}
.list span{font-size:13px;color:var(--muted)}
footer{border-top:1px solid var(--line);font-size:13px;color:var(--muted)}
footer .in{max-width:760px;margin:0 auto;padding:20px 16px 40px}
footer a{color:var(--muted);margin-right:14px}
"""


def page(title, body, root, desc, path, article=False, canonical=True):
    full_title = title if title == SITE else f"{title}｜{SITE}"
    amazon = ("<p>Amazonのアソシエイトとして、" + esc(SITE) + "は適格販売により収入を得ています。</p>") if HAS_AMAZON else ""
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
{f'<link rel="canonical" href="{BASE}/{path}">' if canonical else ""}
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="{'article' if article else 'website'}">
{f'<meta property="og:url" content="{BASE}/{path}">' if canonical else ""}
<link rel="stylesheet" href="{root}assets/style.css">
</head>
<body>
<header class="top"><div class="in">
<a class="logo" href="{root}">{esc(SITE)}</a>
<nav><a href="{root}tools/game-audio-calc/">ツール</a><a href="{root}#articles">記事</a></nav>
</div></header>
<main>
{body}
</main>
<footer><div class="in">
<p><a href="{root}about/">運営者情報</a><a href="{root}privacy/">プライバシーポリシー・免責事項</a></p>
{amazon}
<p>&copy; {CFG['updated'][:4]} {esc(SITE)}</p>
</div></footer>
</body>
</html>
"""


def itch_box():
    if not CFG.get("itch_url"):
        return ""
    return (f'<div class="boxwrap"><a class="box own" href="{esc(CFG["itch_url"])}" target="_blank" rel="noopener">'
            f'<span class="tag">{esc(CFG.get("itch_label","当サイト運営者の商品（販売中）"))}</span><strong>{esc(CFG["itch_title"])}</strong>'
            f'<span>{esc(CFG["itch_desc"])}</span><span class="go">itch.ioで見る →</span></a></div>')


def rakuten_url(base):
    kw = RAKUTEN_ITEMS.get(base, "")
    if not (RAKUTEN_ID and kw):
        return ""
    from urllib.parse import quote
    target = quote(f"https://search.rakuten.co.jp/search/mall/{quote(kw)}/", safe="")
    return f"https://hb.afl.rakuten.co.jp/hgc/{RAKUTEN_ID}/?pc={target}&m={target}"


def shop_links(key):
    base = re.sub(r"^(AMAZON|RAKUTEN|UNITY)_", "", key)
    out = []
    if rakuten_url(base):
        out.append(("楽天市場", rakuten_url(base)))
    for prefix, shop in (("AMAZON_", "Amazon"), ("UNITY_", "Unity Asset Store")):
        if LINKS.get(prefix + base):
            out.append((shop, LINKS[prefix + base]))
    return out


def aff_box(key, name, desc):
    shops = shop_links(key)
    if not shops:
        return ""
    btns = "".join(f'<a class="btn" href="{esc(u)}" target="_blank" rel="sponsored noopener">{shop}で見る →</a>' for shop, u in shops)
    return (f'<div class="boxwrap"><div class="box"><span class="tag">広告</span><strong>{esc(name)}</strong>'
            f'<span>{esc(desc)}</span><span class="btns">{btns}</span></div></div>')


def tool_box(root):
    return (f'<div class="boxwrap"><a class="box toolbox" href="{root}tools/game-audio-calc/">'
            '<span class="tag">無料ツール</span><strong>ゲーム音響計算機</strong>'
            '<span>音量のdB変換、BGMのループ長、ファイルサイズをブラウザで計算できます。</span>'
            '<span class="go">ツールを開く →</span></a></div>')


def shortcodes(text, root):
    text = text.replace("[[tool]]", tool_box(root))
    text = text.replace("[[itch]]", itch_box())

    def aff(m):
        parts = m.group(1).split("|")
        return aff_box(parts[0], parts[1], parts[2] if len(parts) > 2 else "")
    return re.sub(r"\[\[aff:([^\]]+)\]\]", aff, text)


def parse(md_path):
    raw = md_path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)", raw, re.S)
    meta = dict(line.split(": ", 1) for line in m.group(1).splitlines() if ": " in line)
    meta["order"] = int(meta.get("order", 99))
    return meta, m.group(2)


def write(rel, content):
    out = DIST / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")


def disclosure(body, what="この記事"):
    aff = 'rel="sponsored' in body
    own = 'class="box own"' in body or 'class="card own"' in body
    if aff and own:
        text = f"{what}には広告（アフィリエイトリンク）と、当サイト運営者が販売している商品の紹介が含まれます。リンクから商品が購入されると、当サイトに報酬が支払われることがあります。"
    elif aff:
        text = f"{what}には広告（アフィリエイトリンク）が含まれます。リンクから商品が購入されると、当サイトに報酬が支払われることがあります。"
    elif own:
        text = f"{what}には、当サイト運営者が販売している商品の紹介が含まれます。"
    else:
        return ""
    return f'<p class="pr">【PR】{text}</p>'


def build():
    if DIST.exists():
        shutil.rmtree(DIST)
    write("assets/style.css", CSS.strip() + "\n")
    urls = [""]

    # articles
    articles = sorted((a for a in (parse(p) for p in (ROOT / "content/articles").glob("*.md"))
                       if a[0].get("draft", "").strip() != "true"), key=lambda a: a[0]["order"])
    lastmod = {"": CFG["updated"]}
    for meta, text in articles:
        root = "../../"
        body_html = markdown.markdown(shortcodes(text, root), extensions=["tables", "fenced_code"])
        pub = meta.get("published", CFG["updated"]).strip()
        upd = meta.get("updated", pub).strip()
        dates = f"公開日：{pub}" + (f"　更新日：{upd}" if upd != pub else "")
        body = (f'<article><h1>{esc(meta["title"])}</h1>{disclosure(body_html)}'
                f'<div class="meta">{dates}</div>{body_html}</article>')
        path = f'articles/{meta["slug"]}/'
        write(path + "index.html", page(meta["title"], body, root, meta["description"], path, article=True))
        urls.append(path)
        lastmod[path] = upd

    # index
    items = "".join(
        f'<li><a href="articles/{m["slug"]}/"><strong>{esc(m["title"])}</strong><span>{esc(m["description"])}</span></a></li>'
        for m, _ in articles)
    top = f'{tool_box("")}{itch_box()}'
    body = (f'<h1>{esc(SITE)}</h1>{disclosure(top, "このページ")}<p>{esc(CFG["site_description"])}</p>'
            f'{top}<h2 id="articles">記事一覧</h2><ul class="list">{items}</ul>')
    write("index.html", page(SITE, body, "", CFG.get("index_description", CFG["site_description"]), ""))

    # about
    op = esc(CFG["operator_name"]) or "（運営者名を config.json に記入してください）"
    ct = esc(CFG["contact"]) or "（連絡先を config.json に記入してください）"
    body = (f'<h1>運営者情報</h1><table><tr><th>サイト名</th><td>{esc(SITE)}</td></tr>'
            f'<tr><th>運営者</th><td>{op}</td></tr><tr><th>連絡先</th><td>{ct}</td></tr>'
            f'<tr><th>内容</th><td>{esc(CFG["site_description"])}</td></tr></table>'
            '<p>当サイトは、ゲーム用の効果音素材と制作ツールを販売している個人が運営しています。'
            '記事内で紹介する運営者自身の商品には、「当サイト運営者のツール（販売中）」のように表示しています。</p>'
            + ('<p>販売中の商品（itch.io）：' + '、'.join(f'<a href="{esc(x["url"])}" target="_blank" rel="noopener">{esc(x["name"])}</a>' for x in CFG.get("itch_products", [])) + '</p>' if CFG.get("itch_products") else "")
            + '<p>当サイトはアフィリエイトプログラムで収入を得ることがあります。紹介する商品は、公式の仕様や出版社の情報をもとに選んでおり、'
            '実際に使っていない商品を体験談として紹介することはありません。</p>')
    write("about/index.html", page("運営者情報", body, "../", f"{SITE}の運営者情報です。", "about/"))
    urls.append("about/")

    # privacy
    if HAS_AMAZON:
        amazon_p = ("<p>当サイトは、Amazon.co.jpを宣伝しリンクすることによってサイトが紹介料を獲得できる手段を提供することを目的に設定された"
                    "アフィリエイトプログラムである、Amazonアソシエイト・プログラムの参加者です。</p>")
    else:
        amazon_p = ""
    joined = [n for n, on in (("楽天アフィリエイト", HAS_RAKUTEN), ("Unity Affiliate Program", HAS_UNITY)) if on]
    joined_p = f"<p>当サイトは、{'、'.join(joined)}を利用しています。</p>" if joined else ""
    if not (HAS_AMAZON or joined):
        joined_p = "<p>当サイトは、アフィリエイトプログラムへの参加を予定しています。参加後は、このページで参加しているプログラムを明記します。</p>"
    revised = CFG.get("privacy_revised", "")
    body = f"""<h1>プライバシーポリシー・免責事項</h1>
<h2>広告について</h2>
<p>当サイトは、アフィリエイトプログラムを利用して商品やサービスを紹介することがあります。広告を含むページには、ページの冒頭に「【PR】」と表示します。</p>
{amazon_p}{joined_p}
<p>アフィリエイトリンクをクリックすると、リンク先の事業者が成果の計測のためにCookieを使用することがあります。Cookieはブラウザの設定で無効にできます。</p>
<h2>アクセス解析について</h2>
<p>当サイトでは現在、アクセス解析ツールを使用していません。導入する場合は、ツール名と取得する情報をこのページに記載します。</p>
<h2>ツールの入力内容について</h2>
<p>当サイトの計算ツールに入力した値は、お使いのブラウザ内でのみ処理され、外部に送信されません。</p>
<h2>個人情報の取り扱い</h2>
<p>お問い合わせの際にいただいたお名前やメールアドレスは、ご返信のためだけに使用し、法令に基づく場合を除き第三者に提供しません。お問い合わせ先は<a href="../about/">運営者情報</a>に記載しています。</p>
<h2>免責事項</h2>
<p>当サイトの情報は、できる限り正確なものを掲載するよう努めていますが、内容の正確性や完全性を保証するものではありません。素材の利用規約やソフトウェアの仕様は変更されることがあるため、利用前には必ず公式の情報を確認してください。当サイトの情報を利用したことで生じた損害について、当サイトは責任を負いかねます。</p>
<h2>著作権について</h2>
<p>当サイトの文章やツールの無断転載を禁止します。引用の際は出典として当サイトへのリンクを記載してください。</p>
<h2>本ポリシーの変更</h2>
<p>本ポリシーの内容は予告なく変更することがあります。変更後の内容は、本ページに掲載した時点から適用します。</p>
<p class="meta">制定日：{CFG['privacy_established']}{('　最終改定日：' + revised) if revised else ''}</p>"""
    write("privacy/index.html", page("プライバシーポリシー・免責事項", body, "../", f"{SITE}のプライバシーポリシーと免責事項です。", "privacy/"))
    urls.append("privacy/")

    # tool
    tool = (ROOT / "tools/game-audio-calc.html").read_text(encoding="utf-8")
    book = shop_links("BOOK_SFX")
    if book:
        tool = tool.replace('<div class="tag">広告・Amazon</div>', f'<div class="tag">広告・{book[0][0]}</div>')
    repl = {"ITCH_URL": CFG.get("itch_url", ""), "AFF_AMAZON_BOOK_SFX": book[0][1] if book else ""}
    for key, url in repl.items():
        pattern = re.compile(r'\s*<!--[^>]*' + key + r'[^>]*-->\s*<a class="card[^"]*" href="' + key + r'".*?</a>', re.S)
        if url:
            tool = tool.replace(f'href="{key}"', f'href="{esc(url)}"')
        else:
            tool = pattern.sub("", tool)
    if '<a class="card' not in tool:
        tool = re.sub(r'\s*<!-- Recommendations -->\s*<section class="block">.*?</section>', "", tool, flags=re.S)
    tool = tool.replace("<!--PR-->", disclosure(tool, "このページ"))
    tool = re.sub(r"<!--\s*=====.*?-->", "", tool, flags=re.S)
    tool = tool.replace('<div class="wrap">',
                        f'<div class="wrap">\n  <p style="margin:0 0 12px;font-size:14px"><a href="../../" style="color:var(--accent)">← {esc(SITE)}</a></p>', 1)
    tool = tool.replace("<footer>計算はすべてお使いのブラウザ内で行われます。</footer>",
                        '<footer>計算はすべてお使いのブラウザ内で行われます。<br>'
                        '<a href="../../articles/unity-volume-db/" style="color:var(--muted)">Unityの音量をdBに変換する方法</a> ／ '
                        '<a href="../../articles/bgm-loop-calc/" style="color:var(--muted)">BGMのループ長の計算方法</a> ／ '
                        '<a href="../../articles/wav-vs-ogg/" style="color:var(--muted)">WAVとOGGの選び方</a> ／ '
                        '<a href="../../about/" style="color:var(--muted)">運営者情報</a> ／ '
                        '<a href="../../privacy/" style="color:var(--muted)">プライバシーポリシー</a>'
                        + (f'<br>Amazonのアソシエイトとして、{esc(SITE)}は適格販売により収入を得ています。' if HAS_AMAZON else "")
                        + '</footer>')
    tool = tool.replace("</head>", f'<link rel="canonical" href="{BASE}/tools/game-audio-calc/">\n</head>', 1)
    write("tools/game-audio-calc/index.html", tool)
    urls.append("tools/game-audio-calc/")

    # 404, robots, sitemap
    write("404.html", page("ページが見つかりません", f'<h1>ページが見つかりません</h1><p><a href="{SITE_ROOT}">トップページへ戻る</a></p>',
                           SITE_ROOT, "お探しのページは見つかりませんでした。", "404.html", canonical=False))
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    sm = "".join(f"<url><loc>{BASE}/{u}</loc><lastmod>{lastmod.get(u, CFG['updated'])}</lastmod></url>" for u in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    write(".nojekyll", "")
    print(f"built {len(urls)} pages → {DIST}")


if __name__ == "__main__":
    build()
