"""Build only articles/ from its own Markdown snapshots and catalog."""
from pathlib import Path
from html import escape
import json
import re
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
md = MarkdownIt('commonmark', {'html': True, 'breaks': False}).enable('table')
items = sorted(json.loads((ROOT / '_content/catalog.json').read_text(encoding='utf-8')), key=lambda x: x['date'], reverse=True)
e = escape

def shell(title, description, body, prefix='', script=False):
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} · Wenbin's Research Notes</title><meta name="description" content="{e(description, quote=True)}">
<script src="{prefix}assets/theme.js"></script><link rel="stylesheet" href="{prefix}assets/style.css"></head>
<body><a class="back" style="position:absolute;left:-10000px" onfocus="this.style.left='20px'" onblur="this.style.left='-10000px'" href="#main">跳转到正文</a>
<header class="topbar"><nav class="wrap nav" aria-label="主导航"><a class="brand" href="{prefix}index.html"><span>W.</span>Research Notes</a><div class="nav-actions"><a href="{prefix}../">个人主页 ↗</a><button type="button" class="theme" data-theme-toggle>切换主题</button></div></nav></header>
{body}<footer class="footer"><div class="wrap"><span>WENBIN YANG · 学习、实践与研究</span><span>机器人 / 具身智能 / 开发工具</span></div></footer>
{'<script src="assets/app.js" defer></script>' if script else ''}</body></html>'''

def card(item):
    tags = ''.join(f'<span class="tag">{e(t)}</span>' for t in item['tags'])
    search = ' '.join([item['title'], item['summary'], item['category'], *item['tags']])
    return f'''<a class="card" data-card data-category="{e(item['category'])}" data-search="{e(search, quote=True)}" href="{item['slug']}/index.html">
<div class="cover {item['color']}" aria-hidden="true"><small>FIELD NOTES / {e(item['label'])}</small><strong>{e(item['cover'])}</strong><em>{e(item['subtitle'])}</em></div>
<div class="card-body"><div class="tags">{tags}</div><h3>{e(item['title'])}</h3><p>{e(item['summary'])}</p><div class="card-foot"><strong>阅读全文 ↗</strong><span>{item['minutes']} 分钟阅读</span></div></div></a>'''

for item in items:
    if not re.fullmatch(r'[a-z0-9-]+', item['slug']):
        raise ValueError('Invalid article slug')
    source = (ROOT / '_content' / (item['slug'] + '.md')).read_text(encoding='utf-8')
    source = re.sub(r'\A---\s*\n.*?\n---\s*\n', '', source, count=1, flags=re.S)
    # The original first heading is represented by the page title.
    source = re.sub(r'\A\s*# [^\n]*\n', '', source, count=1)
    tokens = md.parse(source)
    toc = []
    for i, token in enumerate(tokens):
        if token.type == 'heading_open':
            anchor = f'section-{len(toc) + 1}'
            token.attrSet('id', anchor)
            toc.append((anchor, tokens[i + 1].content, token.tag))
    content = md.renderer.render(tokens, md.options, {})
    def existing_image(match):
        if not (ROOT.parent / match.group(1).lstrip('/')).is_file():
            return '<p class="archive-note">原笔记此处的配图暂缺。</p>'
        return match.group(0)
    content = re.sub(r'<img\b[^>]*src="(/images/[^\"]+)"[^>]*>', existing_image, content)
    content = content.replace('<d>', '')
    content = content.replace('src="/images/', 'src="../../images/')
    content = content.replace('<table>', '<div class="table-wrap"><table>').replace('</table>', '</table></div>')
    toc_html = ''.join(f'<a href="#{anchor}">{e(title)}</a>' for anchor, title, level in toc if level == 'h2')
    body = f'''<main id="main" class="wrap"><a class="back" href="../index.html">← 返回文章库</a><header class="article-hero"><p class="eyebrow">{e(item['label'])} / 学习笔记</p><h1>{e(item['title'])}</h1><p class="intro">{e(item['summary'])}</p><div class="article-meta">原笔记日期 {item['date']} · Wenbin Yang · 约 {item['minutes']} 分钟阅读</div><div class="tags">{''.join(f'<span class="tag">{e(t)}</span>' for t in item['tags'])}</div></header>
<div class="reading"><article class="prose"><div class="archive-note">收录自本站已有笔记，保留当时的内容记录。软件版本、服务价格与接口信息以原笔记日期为背景。</div>{content}<hr><a href="../index.html">← 继续浏览文章库</a></article><aside class="toc"><details open><summary>本篇目录</summary>{toc_html}</details></aside></div></main>'''
    target = ROOT / item['slug']
    target.mkdir(exist_ok=True)
    (target / 'index.html').write_text(shell(item['title'], item['summary'], body, '../'), encoding='utf-8')

groups = ''
for date in sorted({x['date'] for x in items}, reverse=True):
    batch = [x for x in items if x['date'] == date]
    groups += f'<section class="group" data-group><h2 class="date-heading"><time datetime="{date}">{date.replace("-", " / ")}</time><span>{len(batch)} 篇笔记</span></h2><div class="grid">' + ''.join(card(x) for x in batch) + '</div></section>'
filters = ''.join(f'<button type="button" class="filter" data-filter="{e(c)}" aria-pressed="{str(c == "全部").lower()}">{e(c)}</button>' for c in ['全部', *dict.fromkeys(x['category'] for x in items)])
body = f'''<main id="main" class="wrap"><section class="hero"><div><p class="eyebrow">WENBIN'S RESEARCH JOURNAL</p><h1>把探索，<br>写成可回看的笔记。</h1><p class="intro">记录机器人与具身智能的学习路径，整理工具实践与研究思考。让每一次尝试，都有迹可循。</p><div class="tags"><span class="tag">研究笔记</span><span class="tag">工程实践</span><span class="tag">持续积累</span></div></div><div class="search-panel"><div class="search-top"><strong>探索文章库</strong><span id="result-count" aria-live="polite">{len(items)} 篇已收录</span></div><label for="search">搜索标题、摘要与标签</label><input id="search" type="search" placeholder="例如：ROS、导航、AI PPT" autocomplete="off"><p class="hint">用空格分隔多个关键词，寻找你感兴趣的内容。</p></div></section>
<div class="library-tools"><div class="filters" role="group" aria-label="文章分类">{filters}</div><span class="sort">按原笔记日期 · 最新优先</span></div>
<noscript><p>文章列表可直接浏览；搜索、分类与主题切换需要启用 JavaScript。</p></noscript>{groups}<section id="empty" class="empty" hidden><h2>暂时没有匹配的文章</h2><p>试试其他关键词，或返回全部文章。</p><button id="reset" type="button">清空筛选</button></section></main>'''
(ROOT / 'index.html').write_text(shell('文章库', 'Yang Wenbin 的研究与实践笔记：机器人、具身智能与开发工具。', body, script=True), encoding='utf-8')
print(f'Built article library and {len(items)} article pages under {ROOT}')
