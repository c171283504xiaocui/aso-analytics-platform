# 🚀 ASO数据分析平台

> 一个强大的应用市场优化(ASO)数据分析工具,支持App Store和Google Play数据采集与分析

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ 功能特性

- 🔍 **应用搜索** - 快速搜索App Store和Google Play应用
- 📊 **数据分析** - 实时分析下载量、评分、排名等关键指标
- 🎯 **关键词追踪** - 监控关键词热度和竞争程度
- 📈 **趋势分析** - 可视化应用排名和下载趋势
- 🏆 **排行榜** - 实时获取应用市场排行榜数据

## 🚀 快速开始

### 安装依赖
```bash
cd backend
pip install -r requirements.txt
```

### 启动服务
```bash
python app.py
```

服务将在 `http://localhost:5000` 启动

## 📖 API文档

### 搜索应用
```bash
GET /api/search?keyword=微信
```

### 获取应用详情
```bash
GET /api/app/{app_id}
```

### 获取排行榜
```bash
GET /api/rankings
```

### 关键词分析
```bash
POST /api/keywords/analyze
Content-Type: application/json

{
  "keywords": ["社交", "聊天", "视频"]
}
```

## 🛠️ 技术栈

- **Flask** - Python Web框架
- **Requests** - HTTP请求库
- **iTunes Search API** - App Store数据源
- **Google Play Scraper** - Google Play数据采集

## 🚀 部署

### Railway部署 (推荐)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

1. 点击上方按钮
2. 连接GitHub仓库
3. 自动部署完成

### Docker部署
```bash
docker build -t aso-api backend/
docker run -p 5000:5000 aso-api
```

## 📄 开源协议

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request!

## ⚠️ 免责声明

本项目仅供学习和研究使用,请遵守相关平台的服务条款。

---

Made with ❤️ by ASO Analytics Team
```

5. 滚动到底部,点击 **`Commit changes`**

✅ **README更新完成!**

---

### 第六步: 创建 LICENSE 文件

1. 回到仓库首页
2. 点击 **`Add file`** → **`Create new file`**
3. 文件名输入: `LICENSE`
4. 复制粘贴以下内容:
```
MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

5. 点击 **`Commit new file`**

---

## 🎉 完成! 你的项目已经在GitHub上了!

现在你的仓库地址是:
```
https://github.com/c171283504/aso-analytics-platform
```

### 📂 最终文件结构:
```
aso-analytics-platform/
├── backend/
│   ├── app.py
│   └── requirements.txt
├── .gitignore
├── README.md
└── LICENSE
