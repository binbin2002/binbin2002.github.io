# 文章库

独立入口：`/articles/`（或 `/articles/index.html`）。现有首页、Notes、导航和 Jekyll 配置均不需要改动。部署后可直接访问此路径；原主页不会自动新增入口。

## 结构

- `index.html`：可直接访问的卡片首页，文章列表不依赖 JavaScript。
- `<文章名称>/index.html`：独立文章页。
- `assets/`：本栏目专用样式、主题切换、搜索和分类逻辑，无第三方运行时依赖。
- `_content/`：首批两篇原笔记的独立快照与 `catalog.json` 文章清单。修改快照不会改变 `_notes/`。
- `_tools/build.py`：生成本目录下的页面，不修改网站其他文件。

## 添加文章

1. 在 `_content/` 新建 `your-article.md`，正文用二级标题划分章节。
2. 在 `catalog.json` 中增加记录：沿用现有字段，`slug` 填 `your-article`，`date` 用 `YYYY-MM-DD`，`minutes` 为预计阅读分钟数。分类按钮会根据清单自动生成。`color` 可用空字符串（绿）或 `blue`。
3. 安装构建依赖：`py -m pip install markdown-it-py`。
4. 在仓库根目录运行 `py articles/_tools/build.py`。
5. 将新增源文件与生成的 HTML 一起提交，GitHub Pages 不需要运行此脚本。以下划线开头的内容和工具目录不作为普通静态目录发布。

也可直接添加完整的 `your-article/index.html`，并手动在首页添加卡片。但之后运行生成脚本会重新生成首页；需要长期管理的文章建议使用上述清单流程。生成器会覆盖清单中对应文章的 HTML，不要直接修改这些生成页面。

文章内图片可放到对应文章目录，通过 `images/example.png` 引用。首批笔记沿用仓库现有图片的相对路径。原笔记中的外部服务说明保持历史原文，并非重新验证后的最新教程。

## 本地预览

在仓库根目录运行 `py -m http.server 8000`，打开 `http://localhost:8000/articles/`。预览服务器不编译原有 Jekyll 主页，返回个人主页的链接需在实际 Jekyll/GitHub Pages 环境验证。

本栏目没有自动抓取论文、账号系统或后台服务；搜索范围为文章标题、摘要、分类和标签。页面可以直接加入现有 GitHub Pages 部署。
