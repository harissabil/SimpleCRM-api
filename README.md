# SimpleCRM API

API backend dengan Python Flask untuk manajemen data pelanggan dengan operasi CRUD.

## Fitur

Aplikasi ini menyediakan endpoint API untuk:

- Menambahkan data pelanggan baru
- Melihat daftar seluruh pelanggan
- Mengedit data pelanggan
- Menghapus data pelanggan

## Struktur Aplikasi

Aplikasi ini menggunakan Clean Architecture dengan pemisahan layer:

- **Controllers**: Menangani request dan response HTTP
- **Services**: Berisi logika bisnis
- **Repositories**: Bertanggung jawab untuk akses data
- **Models**: Representasi data
- **Schemas**: Validasi data
- **Routes**: Definisi endpoint API

## Teknologi

- Python 3.8+
- Flask: Web framework
- SQLAlchemy: ORM
- PostgreSQL: Database
- Marshmallow: Validasi dan serialisasi
- Flask-Migrate: Migrasi database

## Setup dan Instalasi

1. Clone repositori ini:
```
git clone <repository-url>
cd customer_management
```

2. Buat virtual environment:
```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. Install dependensi:
```
pip install -r requirements.txt
```

4. Setup database:
   - Pastikan PostgreSQL sudah terinstall
   - Buat database baru bernama `customer_management`
   - Update konfigurasi database di file `.env` jika diperlukan

5. Jalankan aplikasi:
```
python run.py
```

## API Endpoints

### Get All Customers
```
GET /api/customers/
```

### Get Customer by ID
```
GET /api/customers/<id>
```

### Create Customer
```
POST /api/customers/
```
Request body:
```json
{
  "name": "Nama Pelanggan",
  "email": "email@example.com",
  "phone_number": "+628123456789"
}
```

### Update Customer
```
PUT /api/customers/<id>
```
Request body:
```json
{
  "name": "Nama Baru",
  "email": "email_baru@example.com",
  "phone_number": "+628987654321"
}
```

### Delete Customer
```
DELETE /api/customers/<id>
```

## Pengujian

Untuk menjalankan test:
```
pytest
```

## Keamanan

Aplikasi ini menerapkan:
- Validasi input untuk mencegah data yang tidak valid
- Penggunaan SQLAlchemy parameterized queries untuk mencegah SQL Injection