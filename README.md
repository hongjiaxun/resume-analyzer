# 智能简历分析系统

AI 赋能的智能简历分析系统 —— Sidereus AI 笔试项目

## 功能概述

| 模块 | 功能 | 状态 |
|------|------|------|
| 简历上传与解析 | PDF 上传、多页解析、文本清洗 | ✅ |
| 关键信息提取 | AI 提取姓名/电话/邮箱/地址等 | ✅ |
| 简历评分与匹配 | 岗位需求匹配、评分计算 | ✅ |
| 结果返回与缓存 | JSON 结构化返回、缓存机制 | ✅ |
| 前端页面 | 交互式 Web 页面 | ✅ |

## 技术栈

- **后端**: Python + FastAPI
- **PDF 解析**: pdfplumber
- **AI 模型**: 通义千问 (DashScope API)
- **缓存**: 内存缓存（可选 Redis）
- **前端**: Vue 3 + Tailwind CSS

## 项目结构

```
├── backend/
│   ├── app/
│   │   ├── config.py          # 配置管理
│   │   ├── main.py            # FastAPI 应用入口
│   │   ├── models/
│   │   │   └── schemas.py     # Pydantic 数据模型
│   │   ├── routers/
│   │   │   └── resume.py      # API 路由
│   │   └── services/
│   │       ├── ai_service.py  # AI 模型调用
│   │       ├── cache_service.py # 缓存服务
│   │       └── pdf_parser.py  # PDF 解析
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   └── index.html             # 前端页面
└── README.md
```

## 快速开始

### 1. 环境准备

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
```

### 2. 配置 API Key

编辑 `.env` 文件，填入 DashScope API Key:

```
DASHSCOPE_API_KEY=your_api_key_here
```

> 获取 API Key: [DashScope 控制台](https://dashscope.console.aliyun.com/)

### 3. 启动后端

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API 文档: http://localhost:8000/docs

### 4. 启动前端

直接用浏览器打开 `frontend/index.html`，或使用本地服务器:

```bash
cd frontend
python -m http.server 3000
```

访问 http://localhost:3000

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/upload` | 上传并解析简历 (multipart/form-data, field: `file`) |
| POST | `/api/match/{resume_id}` | 简历与岗位匹配 (body: `{"description": "..."}`) |
| GET  | `/api/resumes` | 获取已上传简历列表 |

## 部署说明

### 后端部署 (阿里云函数计算 FC)

1. 打包 `backend/` 目录
2. 配置环境变量 `DASHSCOPE_API_KEY`
3. 设置入口函数为 `app.main:app`

### 前端部署 (GitHub Pages)

1. 将 `frontend/` 目录内容推送到 GitHub Pages 分支
2. 更新 `index.html` 中的 `API_BASE` 为后端实际地址
