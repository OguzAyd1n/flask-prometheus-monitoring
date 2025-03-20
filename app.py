from flask import Flask, Response, jsonify
import time
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY
import psutil
import os

app = Flask(__name__)

# Metrikler
REQUEST_COUNT = Counter('http_requests_total', 'Toplam HTTP istek sayısı', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'HTTP istek gecikmesi', ['method', 'endpoint'])
ERROR_COUNT = Counter('http_errors_total', 'Toplam HTTP hata sayısı', ['method', 'endpoint', 'error_type'])
MEMORY_USAGE = Histogram('memory_usage_bytes', 'Bellek kullanımı')
CPU_USAGE = Histogram('cpu_usage_percent', 'CPU kullanımı')

def get_system_metrics():
    process = psutil.Process(os.getpid())
    MEMORY_USAGE.observe(process.memory_info().rss)
    CPU_USAGE.observe(process.cpu_percent())

@app.route('/')
def hello():
    start_time = time.time()
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    
    try:
        get_system_metrics()
        time.sleep(0.1)  # Yapay gecikme
        REQUEST_LATENCY.labels(method='GET', endpoint='/').observe(time.time() - start_time)
        return jsonify({
            'message': 'Merhaba Dünya!',
            'status': 'success'
        })
    except Exception as e:
        ERROR_COUNT.labels(method='GET', endpoint='/', error_type='internal_error').inc()
        return jsonify({
            'message': 'Bir hata oluştu',
            'status': 'error'
        }), 500

@app.route('/metrics')
def metrics():
    return Response(generate_latest(REGISTRY), mimetype='text/plain')

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time()
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)