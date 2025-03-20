# Flask Prometheus Monitoring Örneği

Bu proje, Flask web uygulamalarında Prometheus metrik toplama sisteminin nasıl entegre edileceğini gösteren gelişmiş bir örnek uygulamadır.

## Özellikler

- Flask web uygulaması
- Prometheus metrik toplama
- Detaylı performans izleme
- Sistem metrikleri (CPU, Bellek, Disk)
- HTTP istek/yanıt metrikleri
- Hata izleme ve loglama
- Sağlık kontrolü
- Docker desteği
- Otomatik yeniden başlatma
- Detaylı API endpoint'leri

## Toplanan Metrikler

- HTTP istek sayısı (method ve endpoint bazında)
- HTTP istek gecikmesi
- HTTP istek/yanıt boyutları
- CPU kullanımı
- Bellek kullanımı
- Disk kullanımı
- Aktif kullanıcı sayısı
- Hata sayıları ve türleri

## Kurulum

### Yerel Kurulum

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

### Docker ile Kurulum

1. Docker imajını oluşturun:
```bash
docker build -t flask-prometheus-app .
```

2. Docker Compose ile çalıştırın:
```bash
docker-compose up
```

## API Endpoint'leri

- `/`: Ana sayfa
- `/metrics`: Prometheus metrikleri
- `/health`: Sağlık kontrolü
- `/api/status`: Detaylı sistem durumu

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

## Loglama

Uygulama logları `app.log` dosyasında tutulur ve otomatik olarak döndürülür:
- Maksimum log dosyası boyutu: 100KB
- Yedek log dosyası sayısı: 3

## Docker Compose Özellikleri

- Otomatik yeniden başlatma
- Sağlık kontrolü
- Geliştirme modu
- Volume bağlantısı
- Port yönlendirme

## Lisans

MIT 