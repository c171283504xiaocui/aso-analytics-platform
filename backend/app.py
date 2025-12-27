@echo off
chcp 65001 >nul
echo ====================================
echo ASO Analytics Platform 项目初始化
echo ====================================
echo.

set PROJECT_NAME=aso-analytics-platform

echo 📁 创建项目目录...
mkdir %PROJECT_NAME%
cd %PROJECT_NAME%

REM 创建后端目录
echo 📁 创建后端结构...
mkdir backend

REM 创建 requirements.txt
echo Flask==3.0.0> backend\requirements.txt
echo flask-cors==4.0.0>> backend\requirements.txt
echo requests==2.31.0>> backend\requirements.txt
echo google-play-scraper==1.2.4>> backend\requirements.txt
echo gunicorn==21.2.0>> backend\requirements.txt

REM 创建前端目录
echo 📁 创建前端结构...
mkdir frontend\src
mkdir frontend\public

REM 创建 package.json
(
echo {
echo   "name": "aso-analytics-frontend",
echo   "version": "1.0.0",
echo   "type": "module",
echo   "scripts": {
echo     "dev": "vite",
echo     "build": "vite build",
echo     "preview": "vite preview"
echo   },
echo   "dependencies": {
echo     "react": "^18.2.0",
echo     "react-dom": "^18.2.0",
echo     "recharts": "^2.10.0",
echo     "lucide-react": "^0.263.1"
echo   },
echo   "devDependencies": {
echo     "@vitejs/plugin-react": "^4.2.0",
echo     "vite": "^5.0.0",
echo     "tailwindcss": "^3.4.0"
echo   }
echo }
) > frontend\package.json

REM 创建 .gitignore
(
echo __pycache__/
echo node_modules/
echo dist/
echo .env
echo *.log
echo .DS_Store
) > .gitignore

REM 创建 README.md
(
echo # ASO数据分析平台
echo.
echo 一个强大的ASO数据分析工具
echo.
echo ## 快速开始
echo.
echo ### 后端
echo ```bash
echo cd backend
echo pip install -r requirements.txt
echo python app.py
echo ```
echo.
echo ### 前端
echo ```bash
echo cd frontend
echo npm install
echo npm run dev
echo ```
) > README.md

echo.
echo ====================================
echo ✅ 项目结构创建完成!
echo ====================================
echo.
echo 📂 项目位置: %CD%
echo.
echo 下一步需要手动操作:
echo   1. 复制 backend/app.py 代码到 backend 目录
echo   2. 复制 frontend/src/App.jsx 代码到 frontend/src 目录
echo   3. 创建 frontend/src/index.js 和 frontend/index.html
echo.
echo 启动项目:
echo   后端: cd backend ^&^& python app.py
echo   前端: cd frontend ^&^& npm install ^&^& npm run dev
echo.
echo 部署到GitHub:
echo   git init
echo   git add .
echo   git commit -m "Initial commit"
echo   git remote add origin https://github.com/你的用户名/%PROJECT_NAME%.git
echo   git push -u origin main
echo.
pause
