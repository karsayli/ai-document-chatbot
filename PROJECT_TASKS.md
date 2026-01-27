# Proje Yapılacaklar Listesi

Bu dokümantasyon, projenin 3 iterasyonu için yapılması gereken tüm görevleri içermektedir.

---

## 📋 1. İTERASYON (Hafta 1-5)

### ✅ Versiyonlama ve Paketleme
- [ ] **Versiyon 1.0.0** için installation package oluştur
  - [ ] Backend için deployment paketi hazırla
  - [ ] Frontend için build paketi hazırla
  - [ ] Installation script'leri oluştur
- [ ] **Git tag oluştur**: `v1.0.0`
- [ ] Tag'ı GitLab'a push et

### 📘 Admin Guide (Yönetici Kılavuzu)
- [ ] **ADMIN_GUIDE.md** dosyası oluştur
  - [ ] Sistem gereksinimleri (hardware, software)
  - [ ] Kurulum adımları (step-by-step)
  - [ ] Sistem yapılandırması
  - [ ] Kullanıcı yönetimi (varsa)
  - [ ] Backup ve restore prosedürleri
  - [ ] Sistem bakımı ve güncelleme
  - [ ] Sorun giderme (troubleshooting)
  - [ ] Güvenlik ayarları

### 🚀 CI/CD Pipeline
- [ ] **`.gitlab-ci.yml`** dosyası oluştur
  - [ ] Build stage (backend ve frontend)
  - [ ] Test stage (varsa)
  - [ ] Deploy stage
  - [ ] Environment variables yapılandırması
- [ ] **Alternatif**: Manuel deployment talimatları dokümante et
  - [ ] Deployment adımları
  - [ ] Rollback prosedürleri
  - [ ] Environment setup

### ⚙️ Configuration Instructions
- [ ] **CONFIGURATION.md** dosyası oluştur
  - [ ] Config dosyalarının konumları
    - [ ] Backend: `.env` dosyası
    - [ ] Frontend: environment variables
  - [ ] Tüm parametrelerin açıklaması
  - [ ] Default değerler
  - [ ] Örnek konfigürasyon dosyaları
  - [ ] API key'lerin yapılandırması
  - [ ] Port ve host ayarları

### 🌐 Environment and Dependencies
- [ ] **ENVIRONMENT.md** dosyası oluştur
  - [ ] Sistem gereksinimleri
    - [ ] Python versiyonu (3.8+)
    - [ ] Node.js versiyonu (18+)
    - [ ] npm versiyonu
  - [ ] Backend dependencies listesi (`requirements.txt` açıklaması)
  - [ ] Frontend dependencies listesi (`package.json` açıklaması)
  - [ ] **Dockerfile** oluştur (containerized deployment için)
    - [ ] Backend Dockerfile
    - [ ] Frontend Dockerfile
    - [ ] docker-compose.yml (opsiyonel)
  - [ ] Diğer gerekli sistemler
    - [ ] ChromaDB setup
    - [ ] API servisleri (Google Gemini, OpenAI)

### 📝 Logging Instructions
- [ ] **LOGGING.md** dosyası oluştur
  - [ ] Log dosyalarının konumları
    - [ ] Backend log dosyaları
    - [ ] Frontend log dosyaları (varsa)
  - [ ] Logging konfigürasyonu
  - [ ] Log seviyeleri (DEBUG, INFO, WARNING, ERROR)
  - [ ] Log rotation ayarları
  - [ ] Log formatı açıklaması

---

## 📋 2. İTERASYON (Hafta 6-9)

### ✅ Versiyonlama ve Paketleme
- [ ] **Versiyon 2.0.0** için installation package oluştur
  - [ ] Güncellenmiş deployment paketleri
  - [ ] Changelog ekle
- [ ] **Git tag oluştur**: `v2.0.0`
- [ ] Tag'ı GitLab'a push et

### 👤 User Manual (Kullanıcı Kılavuzu)
- [ ] **USER_MANUAL.md** dosyası oluştur
  - [ ] Ürünün fonksiyonlarının açıklaması
    - [ ] Use case'ler bazında açıklama
    - [ ] Her özelliğin detaylı kullanımı
  - [ ] Sistem ekranlarının açıklaması
    - [ ] Ana ekran görüntüleri (screenshots)
    - [ ] Her ekranın özellikleri
    - [ ] UI elementlerinin açıklaması
  - [ ] Adım adım kullanım kılavuzu
    - [ ] İlk kullanım
    - [ ] Doküman yükleme
    - [ ] Sohbet başlatma
    - [ ] Sorgu örnekleri
  - [ ] Sık sorulan sorular (FAQ)

### 🔒 Vulnerability Checks
- [ ] **Vulnerability scanning** entegrasyonu
  - [ ] Backend için: `safety` veya `pip-audit` kullan
  - [ ] Frontend için: `npm audit` kullan
- [ ] **`.gitlab-ci.yml`** dosyasına vulnerability check stage ekle
  - [ ] Automated security scanning
  - [ ] Dependency vulnerability checks
  - [ ] Sonuçları raporla
- [ ] **SECURITY.md** dosyası oluştur
  - [ ] Tespit edilen güvenlik açıkları (varsa)
  - [ ] Düzeltmeler ve önlemler
  - [ ] Güvenlik best practices

---

## 📋 3. İTERASYON (Hafta 10-13)

### ✅ Versiyonlama ve Paketleme
- [ ] **Versiyon 3.0.0** için installation package oluştur
  - [ ] Final deployment paketleri
  - [ ] Changelog güncelle
- [ ] **Git tag oluştur**: `v3.0.0`
- [ ] Tag'ı GitLab'a push et

### 👨‍💻 Developer Guide (Geliştirici Kılavuzu)
- [ ] **DEVELOPER_GUIDE.md** dosyası oluştur
  - [ ] Development environment hazırlama adımları
    - [ ] Gerekli araçların kurulumu
    - [ ] Repository clone
    - [ ] Dependencies kurulumu
    - [ ] Environment setup
  - [ ] Kullanılan kütüphaneler ve paketler
    - [ ] Backend dependencies detaylı açıklama
    - [ ] Frontend dependencies detaylı açıklama
    - [ ] Her kütüphanenin amacı
  - [ ] Kodlama konvansiyonları
    - [ ] Python kodlama standartları (PEP 8)
    - [ ] JavaScript/React kodlama standartları
    - [ ] Proje özel kuralları
    - [ ] Link to standard conventions
  - [ ] Proje yapısı açıklaması
    - [ ] Backend mimarisi
    - [ ] Frontend mimarisi
    - [ ] Dosya organizasyonu
  - [ ] Development workflow
    - [ ] Branch stratejisi
    - [ ] Commit mesaj kuralları
    - [ ] Code review process
  - [ ] Testing (varsa)
    - [ ] Test çalıştırma
    - [ ] Test yazma kuralları
  - [ ] Debugging rehberi
  - [ ] API dokümantasyonu (Swagger/OpenAPI)

### 📐 Design Documentation
- [ ] **DESIGN.md** dosyası oluştur
  - [ ] Implementation prensipleri
  - [ ] Mimari tasarım
  - [ ] Veri akışı diyagramları
  - [ ] Sistem bileşenleri
  - [ ] Teknoloji seçim gerekçeleri
  - [ ] RAG sistemi mimarisi
  - [ ] API tasarım prensipleri

---

## 📋 GENEL GÖREVLER (Tüm İterasyonlar)

### 📚 Dokümantasyon Güncellemeleri
- [ ] **README.md** güncelle
  - [ ] Her iterasyonda yeni özellikleri ekle
  - [ ] Versiyon bilgilerini güncelle
  - [ ] Link'leri diğer dokümantasyonlara ekle
- [ ] **CHANGELOG.md** oluştur ve güncelle
  - [ ] Her versiyon için değişiklikleri listele

### 🔄 Sürekli Güncellemeler
- [ ] Her iterasyonda önceki çıktıları güncelle
  - [ ] Admin Guide güncellemeleri
  - [ ] Configuration güncellemeleri
  - [ ] Environment güncellemeleri
- [ ] Tüm dokümantasyonların tutarlılığını kontrol et
- [ ] Design documentation'ı her iterasyonda güncelle

### 🏷️ Git Yönetimi
- [ ] Her iterasyon sonunda tag oluştur
- [ ] Tag'ları GitLab'a push et
- [ ] Release notes hazırla (opsiyonel)

---

## 📁 Oluşturulacak Dosya Yapısı

```
AI-CHATBOTv2-main/
├── README.md (güncellenecek)
├── CHANGELOG.md (yeni)
├── ADMIN_GUIDE.md (1. iterasyon)
├── CONFIGURATION.md (1. iterasyon)
├── ENVIRONMENT.md (1. iterasyon)
├── LOGGING.md (1. iterasyon)
├── USER_MANUAL.md (2. iterasyon)
├── SECURITY.md (2. iterasyon)
├── DEVELOPER_GUIDE.md (3. iterasyon)
├── DESIGN.md (3. iterasyon)
├── .gitlab-ci.yml (1. iterasyon)
├── Dockerfile (backend) (1. iterasyon)
├── Dockerfile (frontend) (1. iterasyon)
└── docker-compose.yml (opsiyonel)
```

---

## ⚠️ Önemli Notlar

1. **Her iterasyonda önceki çıktıları güncelle**: Tüm dokümantasyonlar güncel ve doğru olmalı
2. **Design documentation**: Implementation prensipleri her iterasyonda güncellenmeli
3. **Versiyonlama**: Semantic versioning kullan (MAJOR.MINOR.PATCH)
4. **Tag'lar**: Her iterasyon sonunda mutlaka tag oluştur ve push et
5. **CI/CD**: Pipeline'ı her iterasyonda test et ve güncelle
6. **Güvenlik**: Vulnerability checks her iterasyonda çalıştırılmalı

---

## 📅 Zaman Çizelgesi

- **1. İterasyon**: Hafta 1-5 → Admin Guide, CI/CD, Configuration, Environment, Logging
- **2. İterasyon**: Hafta 6-9 → User Manual, Vulnerability Checks
- **3. İterasyon**: Hafta 10-13 → Developer Guide, Design Documentation

---

**Son Güncelleme**: 2026-01-27
