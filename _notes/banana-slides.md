---
title: "banana-slides 基于nana banaba pro的原生AI PPT引用"
date: 2026-03-25
excerpt: "从零开始上手banana-slides"
tags:
- AI PPT
layout: note
---

# Banana-slides 基于AI的PPT智能生成工具 

## 一、关于Banana-slides
### 1.基本介绍
Banana-slides是一个基于原生AI PPT生成应用，能够在几分钟内从想法到演示文稿，
无需繁琐排版，可以通过口头描述修改，实现真正的Vibe PPT。
具备文本图片自动提取，素材上传和自然语言修改功能。

### 2.资源链接

- 项目链接:https://github.com/Anionex/banana-slides
- 使用案例：https://github.com/Anionex/banana-slides/issues/2
- 从0开始部署:https://github.com/ShellMonster/banana-slides/blob/docs-deploy-tutorial/docs/NEWBIE_DEPLOYMENT.md




## 二、 Banana功能介绍


### 1. 灵活多样的创作路径
支持**想法**、**大纲**、**页面描述**三种起步方式，满足不同创作习惯。
- **一句话生成**：输入一个主题，AI 自动生成结构清晰的大纲和逐页内容描述。
- **自然语言编辑**：支持以 Vibe 形式口头修改大纲或描述（如"把第三页改成案例分析"），AI 实时响应调整。
- **大纲/描述模式**：既可一键批量生成，也可手动调整细节。


### 2. 强大的素材解析能力
- **多格式支持**：上传 PDF/Docx/MD/Txt 等文件，后台自动解析内容。
- **智能提取**：自动识别文本中的关键点、图片链接和图表信息，为生成提供丰富素材。
- **风格参考**：支持上传参考图片或模板，定制 PPT 风格。


### 3. "Vibe" 式自然语言修改
不再受限于复杂的菜单按钮，直接通过**自然语言**下达修改指令。
- **局部重绘**：对不满意的区域进行口头式修改（如"把这个图换成饼图"）。
- **整页优化**：基于 nano banana pro🍌 生成高清、风格统一的页面。


### 4. 开箱即用的格式导出
- **多格式支持**：一键导出标准 **PPTX** 或 **PDF** 文件。
- **完美适配**：默认 16:9 比例，排版无需二次调整，直接演示。

### 5. 可自由编辑的pptx导出（Beta迭代中）
- **导出图像为高还原度、背景干净的、可自由编辑图像和文字的PPT页面**
- 相关更新见 https://github.com/Anionex/banana-slides/issues/121

<br>

> 注：随着新功能添加,对比可能过时


## 三、Banana Docker本地部署

Banana slides 最简单的部署方式是使用Docker Compose 🐳，快速启动前后端服务。

### 1. 系统要求
<d>

<details>
  <summary>📒 Windows/Mac用户说明</summary>

如果你使用 **Windows 或 macOS**，请先安装 **Docker Desktop**，并确保 Docker 正在运行（Windows 可检查系统托盘图标；macOS 可检查菜单栏图标），然后按文档中的相同步骤操作。

> **提示**：如果遇到问题，Windows 用户请在 Docker Desktop 设置中启用 **WSL 2 后端**（推荐）；同时确保端口 **3000** 和 **5000** 未被占用。
</details>

<details>
    <summary>Linux 用户说明</summary>

使用 **Linux**，只需要先安装docker即可。要求和Windows类似
</details>

### 2.代码获取
1. 代码复制
```bash 
git clone https://github.com/Anionex/banana-slides
cd banana-slides
```
2. 拉取并部署镜像
```bash
# 在项目目录下运行镜像
docker compose up -d
```

3.前端和后端访问链接:
``` bash
https://localhost:3000 #前端
https://localhost:5000 #后端

```
### 3. API获取和配置
Banana-slides 支持 `gemini` 和 `Open AI`标准格式的API密钥。支持的API格式

| API 格式 | 适用平台 | 图片生成 | 分辨率设置 |
|---------|---------|---------|-----------|
| **Gemini 格式** | Google Gemini、AIHubMix、本地 Ollama 等 | ✅ 支持 | ✅ **可选 1K/2K/4K** |
| **OpenAI 格式** | OpenAI、其他兼容平台、本地 vLLM 等 | ⚠️ 取决于平台 | ❌ 固定分辨率 |

> 其他兼容平台和中转可以参考



### 4. 网页运行

1. 启动docker 服务
```bash
docker compose up -d 
```

---
**启动成功预计输出**

```
[+] Running 3/3
 ✔ Network banana-slides-network       Created
 ✔ Container banana-slides-backend      Started
 ✔ Container banana-slides-frontend     Started
```

---

2. 打开浏览器并访问网页
```
https://localhost:3000

```
![alt text](image.png)
![alt text](1.jpg)
   网页设置中只需填写以下三项：

   | 配置项 | 说明 | 填写示例 |
   |--------|------|---------|
   | **API 格式** | 选择 `Gemini 格式` 或 `OpenAI 格式` | `Gemini 格式`（推荐） |
   | **API Base** | API 服务地址（参考下方填写规则） | `https://aihubmix.com/gemini` |
   | **API Key** | 你获取的 API 密钥 | `AIzaSy...` |

   > 💡 **兼容性说明**：只要是兼容标准 **OpenAI v1** 或 **Gemini v1beta** 格式的 API 服务都可以使用：
   > - **云端服务**：AIHubMix、Google Gemini、OpenAI 等
   > - **本地服务**：Ollama、vLLM、LocalAI 等本地部署的模型服务

   **API Base 填写规则**：

   | 使用场景 | API 格式 | API Base 填写示例 |
   |---------|---------|-------------------|
   | **AIHubMix（推荐）** | Gemini 格式 | `https://aihubmix.com/gemini` ✅ **需要**包含 `/gemini` 路径 |
   | **Google 官方** | Gemini 格式 | `https://generativelanguage.googleapis.com` ⚠️ 不要加 `/v1beta` |
   | **本地 Ollama** | Gemini 格式 | `http://localhost:11434` ⚠️ 不要加 `/v1beta` |
   | **AIHubMix** | OpenAI 格式 | `https://aihubmix.com/v1` ✅ 需要加 `/v1` |
   | **OpenAI 官方** | OpenAI 格式 | `https://api.openai.com/v1` ✅ 需要加 `/v1` |
   | **本地 vLLM** | OpenAI 格式 | `http://localhost:8000/v1` ✅ 需要加 `/v1` |

   > ⚠️ **重要提示**：
   > - **AIHubMix Gemini 格式**的 API Base 需要填写完整路径 `https://aihubmix.com/gemini`
   > - **Google 官方 Gemini 格式**只需填写域名，**不要**在后面添加 `/v1beta`，系统会自动拼接
   > - **OpenAI 格式**的 API Base 需要填写完整路径，例如 `https://api.openai.com/v1`
   > - **本地服务**确保已启动，地址格式为 `http://localhost:端口号`




## 四、使用技巧
**参考教程**:https://github.com/ShellMonster/banana-slides/blob/docs-deploy-tutorial/docs/NEWBIE_DEPLOYMENT.md
**使用案例**:https://github.com/ShellMonster/banana-slides/blob/docs-deploy-tutorial/docs/TUTORIAL_SLIDES.md






## 五、 技术架构

### 前端技术栈
- **框架**：React 18 + TypeScript
- **构建工具**：Vite 5
- **状态管理**：Zustand
- **路由**：React Router v6
- **UI组件**：Tailwind CSS
- **拖拽功能**：@dnd-kit
- **图标**：Lucide React
- **HTTP客户端**：Axios

### 后端技术栈
- **语言**：Python 3.10+
- **框架**：Flask 3.0
- **包管理**：uv
- **数据库**：SQLite + Flask-SQLAlchemy
- **AI能力**：Google Gemini API
- **PPT处理**：python-pptx
- **图片处理**：Pillow
- **并发处理**：ThreadPoolExecutor
- **跨域支持**：Flask-CORS




## 六、项目结构
```
banana-slides/
├── frontend/                    # React前端应用
│   ├── src/
│   │   ├── pages/              # 页面组件
│   │   │   ├── Home.tsx        # 首页（创建项目）
│   │   │   ├── OutlineEditor.tsx    # 大纲编辑页
│   │   │   ├── DetailEditor.tsx     # 详细描述编辑页
│   │   │   ├── SlidePreview.tsx     # 幻灯片预览页
│   │   │   └── History.tsx          # 历史版本管理页
│   │   ├── components/         # UI组件
│   │   │   ├── outline/        # 大纲相关组件
│   │   │   │   └── OutlineCard.tsx
│   │   │   ├── preview/        # 预览相关组件
│   │   │   │   ├── SlideCard.tsx
│   │   │   │   └── DescriptionCard.tsx
│   │   │   ├── shared/         # 共享组件
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Card.tsx
│   │   │   │   ├── Input.tsx
│   │   │   │   ├── Textarea.tsx
│   │   │   │   ├── Modal.tsx
│   │   │   │   ├── Loading.tsx
│   │   │   │   ├── Toast.tsx
│   │   │   │   ├── Markdown.tsx
│   │   │   │   ├── MaterialSelector.tsx
│   │   │   │   ├── MaterialGeneratorModal.tsx
│   │   │   │   ├── TemplateSelector.tsx
│   │   │   │   ├── ReferenceFileSelector.tsx
│   │   │   │   └── ...
│   │   │   ├── layout/         # 布局组件
│   │   │   └── history/        # 历史版本组件
│   │   ├── store/              # Zustand状态管理
│   │   │   └── useProjectStore.ts
│   │   ├── api/                # API接口
│   │   │   ├── client.ts       # Axios客户端配置
│   │   │   └── endpoints.ts    # API端点定义
│   │   ├── types/              # TypeScript类型定义
│   │   ├── utils/              # 工具函数
│   │   ├── constants/          # 常量定义
│   │   └── styles/             # 样式文件
│   ├── public/                 # 静态资源
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js      # Tailwind CSS配置
│   ├── Dockerfile
│   └── nginx.conf              # Nginx配置
│
├── backend/                    # Flask后端应用
│   ├── app.py                  # Flask应用入口
│   ├── config.py               # 配置文件
│   ├── models/                 # 数据库模型
│   │   ├── project.py          # Project模型
│   │   ├── page.py             # Page模型（幻灯片页）
│   │   ├── task.py             # Task模型（异步任务）
│   │   ├── material.py         # Material模型（参考素材）
│   │   ├── user_template.py    # UserTemplate模型（用户模板）
│   │   ├── reference_file.py   # ReferenceFile模型（参考文件）
│   │   ├── page_image_version.py # PageImageVersion模型（页面版本）
│   ├── services/               # 服务层
│   │   ├── ai_service.py       # AI生成服务（Gemini集成）
│   │   ├── file_service.py     # 文件管理服务
│   │   ├── file_parser_service.py # 文件解析服务
│   │   ├── export_service.py   # PPTX/PDF导出服务
│   │   ├── task_manager.py     # 异步任务管理
│   │   ├── prompts.py          # AI提示词模板
│   ├── controllers/            # API控制器
│   │   ├── project_controller.py      # 项目管理
│   │   ├── page_controller.py         # 页面管理
│   │   ├── material_controller.py     # 素材管理
│   │   ├── template_controller.py     # 模板管理
│   │   ├── reference_file_controller.py # 参考文件管理
│   │   ├── export_controller.py       # 导出功能
│   │   └── file_controller.py         # 文件上传
│   ├── utils/                  # 工具函数
│   │   ├── response.py         # 统一响应格式
│   │   ├── validators.py       # 数据验证
│   │   └── path_utils.py       # 路径处理
│   ├── instance/               # SQLite数据库（自动生成）
│   ├── exports/                # 导出文件目录
│   ├── Dockerfile
│   └── README.md
│
├── tests/                      # 测试文件目录
├── v0_demo/                    # 早期演示版本
├── output/                     # 输出文件目录
│
├── pyproject.toml              # Python项目配置（uv管理）
├── uv.lock                     # uv依赖锁定文件
├── docker-compose.yml          # Docker Compose配置
├── .env.example                 # 环境变量示例
├── LICENSE                     # 许可证
└── README.md                   # 本文件
```