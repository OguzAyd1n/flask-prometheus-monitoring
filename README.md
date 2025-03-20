# Flask Prometheus Monitoring Örneği

Bu proje, Flask web uygulamalarında Prometheus metrik toplama sisteminin nasıl entegre edileceğini gösteren bir örnek uygulamadır.

## Özellikler

- Flask web uygulaması
- Prometheus metrik toplama
- Performans izleme
- HTTP istek sayısı ve yanıt süresi metrikleri

## Kurulum

1. Sanal ortam oluşturun ve aktifleştirin:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac için
.venv\Scripts\activate     # Windows için
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

3. Uygulamayı çalıştırın:
```bash
python app.py
```

## Kullanım

- Ana sayfa: http://localhost:5000
- Metrikler sayfası: http://localhost:5000/metrics

## Prometheus Entegrasyonu

Prometheus'u bu uygulamaya bağlamak için:

1. Prometheus'u yükleyin
2. `prometheus.yml` dosyasına aşağıdaki yapılandırmayı ekleyin:
```yaml
scrape_configs:
  - job_name: 'flask-app'
    static_configs:
      - targets: ['localhost:5000']
```

## Lisans

MIT 