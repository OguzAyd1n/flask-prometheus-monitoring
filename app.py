from flask import Flask, Response, jsonify, request
import time
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY, Gauge
import psutil
import os
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler

# Logging yapılandırması
logging.basicConfig(
    handlers=[RotatingFileHandler('app.log', maxBytes=100000, backupCount=3)],
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Metrikler
REQUEST_COUNT = Counter('http_requests_total', 'Toplam HTTP istek sayısı', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'HTTP istek gecikmesi', ['method', 'endpoint'])
ERROR_COUNT = Counter('http_errors_total', 'Toplam HTTP hata sayısı', ['method', 'endpoint', 'error_type'])
MEMORY_USAGE = Histogram('memory_usage_bytes', 'Bellek kullanımı')
CPU_USAGE = Histogram('cpu_usage_percent', 'CPU kullanımı')
ACTIVE_USERS = Gauge('active_users', 'Aktif kullanıcı sayısı')
REQUEST_SIZE = Histogram('http_request_size_bytes', 'HTTP istek boyutu')
RESPONSE_SIZE = Histogram('http_response_size_bytes', 'HTTP yanıt boyutu')

def get_system_metrics():
    process = psutil.Process(os.getpid())
    MEMORY_USAGE.observe(process.memory_info().rss)
    CPU_USAGE.observe(process.cpu_percent())
    ACTIVE_USERS.set(len(psutil.users()))

@app.before_request
def before_request():
    request.start_time = time.time()
    REQUEST_COUNT.labels(method=request.method, endpoint=request.path).inc()
    REQUEST_SIZE.observe(len(request.get_data()))

@app.after_request
def after_request(response):
    latency = time.time() - request.start_time
    REQUEST_LATENCY.labels(method=request.method, endpoint=request.path).observe(latency)
    RESPONSE_SIZE.observe(len(response.get_data()))
    return response

@app.route('/')
def hello():
    try:
        get_system_metrics()
        time.sleep(0.1)  # Yapay gecikme
        return jsonify({
            'message': 'Merhaba Dünya!',
            'status': 'success',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Hata oluştu: {str(e)}")
        ERROR_COUNT.labels(method='GET', endpoint='/', error_type='internal_error').inc()
        return jsonify({
            'message': 'Bir hata oluştu',
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/metrics')
def metrics():
    return Response(generate_latest(REGISTRY), mimetype='text/plain')

@app.route('/health')
def health_check():
    try:
        get_system_metrics()
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'system': {
                'cpu_percent': psutil.cpu_percent(),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent
            }
        })
    except Exception as e:
        logger.error(f"Sağlık kontrolü hatası: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@app.route('/api/status')
def status():
    try:
        get_system_metrics()
        return jsonify({
            'status': 'running',
            'uptime': time.time() - psutil.boot_time(),
            'system': {
                'cpu_count': psutil.cpu_count(),
                'memory_total': psutil.virtual_memory().total,
                'memory_available': psutil.virtual_memory().available,
                'disk_total': psutil.disk_usage('/').total,
                'disk_free': psutil.disk_usage('/').free
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Durum kontrolü hatası: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found_error(error):
    ERROR_COUNT.labels(method=request.method, endpoint=request.path, error_type='not_found').inc()
    return jsonify({
        'message': 'Sayfa bulunamadı',
        'status': 'error'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    ERROR_COUNT.labels(method=request.method, endpoint=request.path, error_type='internal_error').inc()
    return jsonify({
        'message': 'Sunucu hatası',
        'status': 'error'
    }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)