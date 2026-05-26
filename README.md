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
- **AI 模型**: 小米 MiMo (OpenAI 兼容 API)
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

编辑 `.env` 文件，填入小米 MiMo API Key:

```
MIMO_API_KEY=your_api_key_here
MIMO_BASE_URL=https://token-plan-cn.xiaomimimo.com/v1
MIMO_MODEL=mimo-v2.5-pro
```

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

1. 进入 [函数计算控制台](https://fcnext.console.aliyun.com/)，创建 **Web 函数**
2. 运行环境选择 **自定义运行时 / Python 3.12**
3. 启动命令：`bash startup.sh`
4. 监听端口：`9000`
5. 执行超时时间：`300` 秒
6. 环境变量添加 `MIMO_API_KEY`
7. 上传 `backend.zip`（项目根目录打包）
8. 创建 HTTP 触发器，关闭签名认证

### 前端部署 (GitHub Pages)

1. 代码已配置 `gh-pages` 分支自动部署
2. 访问地址: https://hongjiaxun.github.io/resume-analyzer/
3. 前端 `API_BASE` 已指向 FC 后端地址

### 线上演示

- **前端**: https://hongjiaxun.github.io/resume-analyzer/
- **后端 API**: https://xingshi-hdloanlgmq.cn-hangzhou.fcapp.run/
