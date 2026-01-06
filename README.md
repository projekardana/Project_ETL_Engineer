# ETL Pipeline Fashion Data

Proyek ini merupakan implementasi **ETL Pipeline** untuk mengumpulkan data fashion dari website, mengubahnya menjadi format terstruktur, dan menyimpannya ke berbagai storage, termasuk CSV, PostgreSQL, dan Google Sheets.  

Proyek ini merupakan proyek submission hasil pembelajaran Fundamental Pemrosesan Data dari Dicoding Academy dan sebagai penunjang dalam pembuatan portofolio. Oleh Karena itu menampilkan kemampuan:  

- Web scraping menggunakan `**requests**` & `**BeautifulSoup**`  
- Transformasi data menggunakan `**pandas**`  
- Load Penyimpanan data ke `**CSV, PostgreSQL, dan Google Sheets**`  
- Penulisan `**unit test**` untuk memastikan kualitas kode lebih baik dan rapih tanp bug.

--------------------
## Struktur Folder

```
├── tests
    └── test_extract.py
    └── test_transform.py
    └── test_load.py
├── utils
    └── extract.py
    └── transform.py
    └── load.py
├── main.py
├── requirements.txt
├── submission.txt
├── products.csv
├── google-sheets-api.json
```
---------------------

## Cara Menjalankan Proyek Submission

1. **Running ETL Skrip Python**  
```
python main.py
```

2. **Running Unit Testing**
```
python3 -m pytest tests
```
3. **Lihat Hasil Coverage Hasil testing**
```
coverage run -m pytest tests
coverage report -m
```
---------------------

## **URL Google Sheets API** 


https://docs.google.com/spreadsheets/d/1k8X9_esOGsy5dCqJ8yemGfLAOPjr2uWECPqRK8QXIh8

----------------------

## **Requirements**

**Python 3.9+**

**Libraries:** `requests`, `beautifulsoup4`, ``pandas``, `SQLAlchemy`, `psycopg2-binary`, `google-api-python-client`, `google-auth`

`.env` file untuk menyimpan konfigurasi database dan Google Sheets credentials, Database PostgreSQL