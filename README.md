# ERP Data Integration & Migration (Proof of Concept)

## Proje Kapsamı ve Mimari Yaklaşım
Kurumsal ERP geçişlerinde (migration) ve modül entegrasyonlarında karşılaşılan en kritik darboğaz, eski sistemlerden veya dış kaynaklardan gelen düzensiz/kirli veridir. 

Bu proje; veri bütünlüğünü sağlamak amacıyla geliştirilmiş bir **Proof of Concept (PoC)** çalışmasıdır. Senaryo gereği dış sistemlerden alınan ham verinin Python (Pandas) ile veri temizleme ve doğrulama süreçlerinden geçirilerek, kurumsal bir ERP veritabanı şemasına (SQL) güvenli bir şekilde entegre edilmesini simüle eder.

### Öne Çıkan Özellikler
- **Data Validation:** Eksik, hatalı ve negatif fiyatlı verilerin otomasyonla tespiti.
- **Exception Logging:** Hatalı verilerin ayıklanarak `migration_errors.log` dosyasına aktarılması.
- **Automated Ingestion:** Temizlenen verinin ilişkisel veritabanı (SQLite) tablosuna otomatik yazılması.
- **Business Logic:** Parça başı toplam maliyetlerin (`total_value`) hesaplanarak veritabanı şemasına eklenmesi.

### Kullanılan Teknolojiler
- **Dil:** Python 3.x
- **Kütüphaneler:** Pandas, Logging
- **Veritabanı:** SQLite / SQL
