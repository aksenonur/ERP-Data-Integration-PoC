import sqlite3
import pandas as pd
import numpy as np
import logging

# Log yapılandırması
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_10k_dirty_data(file_path='raw_data.csv'):
    """CV iddiasını doğrulayan 10.000+ satırlık kurumsal kirli veri seti üretir."""
    logging.info("10.000+ satırlık ham ERP veri seti simülasyonu oluşturuluyor...")
    np.random.seed(42)
    num_rows = 10500

    item_codes = [f"PRD-{i:04d}" for i in range(100, 600)] + [None] * 20  # Hatalı/Eksik kodlar
    suppliers = [f"SUP-{i:03d}" for i in range(1, 25)]
    descriptions = ['Hydraulic Valve', 'Control Sensor', 'Turbine Blade', 'Gasket Seal', 'Actuator Arm', 'Pressure Gauge']

    data = {
        'item_code': np.random.choice(item_codes, num_rows),
        'description': np.random.choice(descriptions, num_rows),
        'quantity': np.random.choice([10, 20, 50, 100, None], num_rows, p=[0.3, 0.3, 0.25, 0.1, 0.05]), # Boş miktarlar
        'unit_price': np.random.choice([150.0, 240.5, -99.0, 45.0, 12.5, 0.0], num_rows, p=[0.35, 0.3, 0.05, 0.15, 0.1, 0.05]), # Negatif/Sıfır fiyatlar
        'supplier_id': np.random.choice(suppliers, num_rows),
        'date': pd.date_range(start='2026-01-01', periods=num_rows, freq='h').strftime('%Y-%m-%d')
    }
    
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    logging.info(f"{len(df)} satırlık '{file_path}' dosyası oluşturuldu.")

def clean_and_ingest():
    file_path = 'raw_data.csv'
    db_path = 'erp_system.db'
    
    # 1. 10.000+ Satırlık Veriyi Otomatik Üret
    generate_10k_dirty_data(file_path)
    
    # 2. Ham Veriyi Oku ve İşle
    df = pd.read_csv(file_path)
    initial_count = len(df)
    
    # 3. Data Validation (Doğrulama ve Temizleme)
    invalid_rows = df[df['item_code'].isnull() | (df['unit_price'] <= 0) | df['quantity'].isnull()]
    
    # Hatalı verileri log dosyasına aktar
    invalid_rows.to_csv('migration_errors.log', index=False)
    
    # Temiz verileri filtrele
    clean_df = df.dropna(subset=['item_code', 'quantity', 'unit_price']).copy()
    clean_df = clean_df[clean_df['unit_price'] > 0].copy()
    
    clean_df['quantity'] = clean_df['quantity'].astype(int)
    clean_df['total_value'] = clean_df['quantity'] * clean_df['unit_price']
    
    success_rate = (len(clean_df) / initial_count) * 100
    logging.info(f"İşlenen Toplam Veri: {initial_count} satır.")
    logging.info(f"Ayıklanan Hatalı Veri: {len(invalid_rows)} satır -> 'migration_errors.log' dosyasına yazıldı.")
    logging.info(f"Başarıyla Temizlenen Veri: {len(clean_df)} satır (Başarı Oranı: %{success_rate:.2f})")
    
    # 4. İlişkisel Veritabanına Akış (SQL Ingestion)
    conn = sqlite3.connect(db_path)
    clean_df.to_sql('stok_envanter', conn, if_exists='replace', index=False)
    conn.close()
    
    logging.info("Temizlenen veriler SQLite veritabanına ('stok_envanter' tablosu) aktarıldı.")

if __name__ == "__main__":
    clean_and_ingest()
