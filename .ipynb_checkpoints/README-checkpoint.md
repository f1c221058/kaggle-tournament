# Crypto Dashboard

Dashboard interaktif untuk menganalisis harga aset kripto berdasarkan data historis.  
Dibangun menggunakan **Streamlit**, **Pandas**, dan **Plotly**.  

> Created by  **Kevin Synagogue Panjaitan**

---

## Fitur Utama

- Memuat data crypto dari file CSV
- Filter berdasarkan:
  - Nama koin (`name`)
  - Rentang tanggal (`Date`)
- Menampilkan KPI ringkas:
  - Total Volume
  - Rata-rata harga penutupan (Close)
  - Persentase perubahan harga
- Visualisasi interaktif:
  - Line chart harga Close
  - Bar chart Volume harian
- Tabel ringkasan per koin:
  - Harga awal–akhir
  - Rata-rata
  - Min–max
  - Total volume
  - Persentase perubahan
- UI bersih dan responsif
- Cache data untuk akselerasi

---

##  Struktur CSV

File CSV yang digunakan harus memiliki kolom minimum berikut:

| Kolom   | Keterangan |
|---------|------------|
| Date    | Tanggal data |
| Open    | Harga pembukaan |
| High    | Harga tertinggi |
| Low     | Harga terendah |
| Close   | Harga penutupan |
| Volume  | Volume transaksi |
| name    | Nama koin |

> **Catatan:**  
Kolom `ticker` opsional.

---

##  Requirements

Install library berikut:

```bash
pip install streamlit pandas plotly
``` 
```bash
streamlit run app1.py

```