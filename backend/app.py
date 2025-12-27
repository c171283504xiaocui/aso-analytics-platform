"""
ASO Analytics Platform - Backend API
Flask REST API for App Store and Google Play data
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import threading
import time

app = Flask(__name__)

# CORS配置 - 允许所有来源 (生产环境应该限制)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:5173", "*"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# 配置
API_BASE_URL = "https://itunes.apple.com"
CACHE_TTL = 3600  # 缓存1小时
PORT = int(os.environ.get('PORT', 5000))

# 内存数据存储
data_store = {
    'apps': {},
    'keywords': {},
    'rankings': {},
    'trends': {},
    'last_update': {}
}


class AppStoreAPI:
    """App Store数据采集类"""
    
    def __init__(self):
        self.base_url = API_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def search(self, keyword: str, country: str = "cn", limit: int = 50) -> List[Dict]:
        """搜索应用"""
        url = f"{self.base_url}/search"
        params = {
            'term': keyword,
            'country': country,
            'entity': 'software',
            'limit': limit
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            apps = []
            for item in data.get('results', []):
                apps.append({
                    'id': str(item.get('trackId')),
                    'name': item.get('trackName', ''),
                    'developer': item.get('artistName', ''),
                    'category': item.get('primaryGenreName', ''),
                    'price': item.get('price', 0),
                    'rating': round(item.get('averageUserRating', 0), 1),
                    'ratingCount': item.get('userRatingCount', 0),
                    'version': item.get('version', ''),
                    'description': (item.get('description', '') or '')[:200] + '...',
                    'iconUrl': item.get('artworkUrl512', ''),
                    'url': item.get('trackViewUrl', '')
                })
            
            return apps
        except Exception as e:
            print(f"搜索失败: {e}")
            return []
    
    def get_app(self, app_id: str, country: str = "cn") -> Optional[Dict]:
        """获取应用详情"""
        url = f"{self.base_url}/lookup"
        params = {'id': app_id, 'country': country}
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('resultCount', 0) > 0:
                item = data['results'][0]
                return {
                    'id': str(item.get('trackId')),
                    'name': item.get('trackName', ''),
                    'developer': item.get('artistName', ''),
                    'category': item.get('primaryGenreName', ''),
                    'rating': round(item.get('averageUserRating', 0), 1),
                    'ratingCount': item.get('userRatingCount', 0),
                    'version': item.get('version', ''),
                    'description': item.get('description', ''),
                    'releaseNotes': item.get('releaseNotes', ''),
                    'price': item.get('price', 0),
                    'iconUrl': item.get('artworkUrl512', ''),
                    'screenshots': item.get('screenshotUrls', [])
                }
            return None
        except Exception as e:
            print(f"获取应用失败: {e}")
            return None
    
    def get_top_charts(self, country: str = "cn", limit: int = 50) -> List[Dict]:
        """获取排行榜"""
        url = f"{self.base_url}/{country}/rss/topfreeapplications/limit={limit}/json"
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            apps = []
            entries = data.get('feed', {}).get('entry', [])
            
            for idx, entry in enumerate(entries):
                app_id = entry.get('id', {}).get('attributes', {}).get('im:id', '')
                apps.append({
                    'rank': idx + 1,
                    'name': entry.get('im:name', {}).get('label', ''),
                    'developer': entry.get('im:artist', {}).get('label', ''),
                    'category': entry.get('category', {}).get('attributes', {}).get('label', ''),
                    'iconUrl': entry.get('im:image', [{}])[-1].get('label', '') if entry.get('im:image') else '',
                    'appId': app_id,
                    'id': app_id,
                    'url': entry.get('link', {}).get('attributes', {}).get('href', '')
                })
            
            return apps
        except Exception as e:
            print(f"获取排行榜失败: {e}")
            return []


# 初始化API
app_store_api = AppStoreAPI()


# ============= API路由 =============

@app.route('/')
def index():
    """首页"""
    return jsonify({
        'name': 'ASO Analytics API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': [
            '/api/health',
            '/api/search',
            '/api/app/<app_id>',
            '/api/rankings',
            '/api/keywords/analyze',
            '/api/trends/<app_id>',
            '/api/dashboard/stats'
        ]
    })


@app.route('/api/health')
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'cache_size': len(data_store['apps'])
    })


@app.route('/api/search')
def search_apps():
    """搜索应用"""
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({'error': '缺少keyword参数'}), 400
    
    country = request.args.get('country', 'cn')
    limit = int(request.args.get('limit', 50))
    
    # 检查缓存
    cache_key = f"{keyword}_{country}"
    if cache_key in data_store['keywords']:
        cache_data = data_store['keywords'][cache_key]
        if datetime.now() - cache_data['timestamp'] < timedelta(seconds=CACHE_TTL):
            return jsonify(cache_data['data'])
    
    # 采集新数据
    apps = app_store_api.search(keyword, country, limit)
    
    result = {
        'keyword': keyword,
        'total': len(apps),
        'apps': apps,
        'timestamp': datetime.now().isoformat()
    }
    
    # 保存到缓存
    data_store['keywords'][cache_key] = {
        'data': result,
        'timestamp': datetime.now()
    }
    
    return jsonify(result)


@app.route('/api/app/<app_id>')
def get_app_detail(app_id):
    """获取应用详情"""
    country = request.args.get('country', 'cn')
    
    # 检查缓存
    cache_key = f"{app_id}_{country}"
    if cache_key in data_store['apps']:
        cache_data = data_store['apps'][cache_key]
        if datetime.now() - cache_data['timestamp'] < timedelta(seconds=CACHE_TTL * 6):
            return jsonify(cache_data['data'])
    
    # 采集新数据
    app_detail = app_store_api.get_app(app_id, country)
    
    if not app_detail:
        return jsonify({'error': '应用不存在'}), 404
    
    # 保存到缓存
    data_store['apps'][cache_key] = {
        'data': app_detail,
        'timestamp': datetime.now()
    }
    
    return jsonify(app_detail)


@app.route('/api/rankings')
def get_rankings():
    """获取排行榜"""
    country = request.args.get('country', 'cn')
    limit = int(request.args.get('limit', 50))
    
    # 检查缓存
    cache_key = f"rankings_{country}"
    if cache_key in data_store['rankings']:
        cache_data = data_store['rankings'][cache_key]
        if datetime.now() - cache_data['timestamp'] < timedelta(seconds=CACHE_TTL):
            return jsonify(cache_data['data'])
    
    # 采集新数据
    apps = app_store_api.get_top_charts(country, limit)
    
    result = {
        'country': country,
        'total': len(apps),
        'apps': apps,
        'timestamp': datetime.now().isoformat()
    }
    
    # 保存到缓存
    data_store['rankings'][cache_key] = {
        'data': result,
        'timestamp': datetime.now()
    }
    
    return jsonify(result)


@app.route('/api/keywords/analyze', methods=['POST'])
def analyze_keywords():
    """分析关键词"""
    data = request.get_json()
    keywords = data.get('keywords', [])
    
    if not keywords:
        return jsonify({'error': '缺少keywords参数'}), 400
    
    results = []
    for keyword in keywords:
        apps = app_store_api.search(keyword, country='cn', limit=50)
        
        if apps:
            total_ratings = sum(app.get('ratingCount', 0) for app in apps)
            avg_rating = sum(app.get('rating', 0) for app in apps) / len(apps)
            
            results.append({
                'keyword': keyword,
                'appCount': len(apps),
                'totalRatings': total_ratings,
                'avgRating': round(avg_rating, 2),
                'competitionLevel': 'high' if len(apps) > 30 else 'medium' if len(apps) > 15 else 'low',
                'hotScore': min(100, int(total_ratings / 1000))
            })
        else:
            results.append({
                'keyword': keyword,
                'appCount': 0,
                'totalRatings': 0,
                'avgRating': 0,
                'competitionLevel': 'low',
                'hotScore': 0
            })
    
    return jsonify({
        'keywords': results,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/trends/<app_id>')
def get_app_trends(app_id):
    """获取应用趋势数据 (模拟)"""
    trends = []
    base_date = datetime.now() - timedelta(days=7)
    
    for i in range(7):
        date = base_date + timedelta(days=i)
        trends.append({
            'date': date.strftime('%m-%d'),
            'downloads': 45000 + (i * 2000) + (i % 2 * 1000),
            'ranking': max(1, 5 - i % 3),
            'rating': round(4.5 + (i * 0.05), 1)
        })
    
    return jsonify({
        'appId': app_id,
        'trends': trends,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/dashboard/stats')
def get_dashboard_stats():
    """获取Dashboard统计数据"""
    stats = {
        'totalApps': len(data_store['apps']),
        'totalKeywords': len(data_store['keywords']),
        'cacheHitRate': 85.5,
        'lastUpdate': datetime.now().isoformat()
    }
    
    return jsonify(stats)


# ============= 错误处理 =============

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': '接口不存在'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': '服务器内部错误'}), 500


# ============= 主程序 =============

if __name__ == '__main__':
    print("=" * 60)
    print("ASO Analytics API 启动中...")
    print("=" * 60)
    print(f"\n服务运行在: http://0.0.0.0:{PORT}")
    print("\n可用接口:")
    print("  GET  /api/health              - 健康检查")
    print("  GET  /api/search              - 搜索应用")
    print("  GET  /api/app/<app_id>        - 获取应用详情")
    print("  GET  /api/rankings            - 获取排行榜")
    print("  POST /api/keywords/analyze    - 分析关键词")
    print("  GET  /api/trends/<app_id>     - 获取趋势数据")
    print("  GET  /api/dashboard/stats     - Dashboard统计")
    print("\n" + "=" * 60 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=PORT,
        debug=os.environ.get('FLASK_ENV') != 'production'
    )
