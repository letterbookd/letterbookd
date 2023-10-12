# letterbookd 📖

Bringing you, your books, and readers together.

*Tugas Kelompok Proyek Tengah Semester kelompok A09 untuk mata kuliah Pemrograman Berbasis Platform Semester Ganjil 2023/2024.*

## Anggota Kelompok A09

> Wahyu Hidayat - `2206081894`  
> Muhammad Milian Alkindi - `2206081856`  
> Evelyn Paramesti Hotmauli Silalahi `2206031012`  
> Rana Koesumastuti `2206083496`  
> Muhammad Syahrul Khaliq `2206083092`  

## Cerita aplikasi yang diajukan serta manfaatnya

***Letterbookd*** adalah aplikasi yang bertujuan untuk menyatukan pembaca dengan buku dan pembaca buku lainnya.
Dengan menggunakan aplikasi ini, pembaca dapat menyimpan buku dari katalog ke *Library* personal mereka, memberikan ulasan
untuk buku yang sudah dibaca, dan juga melihat ulasan buku oleh pembaca lainnya.
Buku-buku yang ada di dalam *library* personal dapat diatur status *tracking*nya untuk memudahkan pengguna melacak status buku mereka.

## Daftar modul yang akan diimplementasikan

### Guest `[developer: semua]`

Landing page untuk pengunjung yang belum melakukan login aplikasi.
Halaman ini akan menampilkan fitur-fitur yang dimiliki aplikasi dengan tujuan mengubah pengunjung menjadi pengguna (Reader).

### Authenticate `[developer: semua]`

Modul ini akan menghandle sign in dan sign up ke aplikasi.

### Library `[developer: Muhammad Milian Alkindi]`

- `CREATE` Menambahkan buku ke *library* Reader
- `DELETE` Mengeluarkan buku dari *library* Reader
- `UPDATE` Mengubah status *tracking* buku dalam *library*
  - Status Tracking: `FINISHED`, `READING`, `ON HOLD`, `DROPPED`, `UNTRACKED`
- `READ` Mengembalikan buku dalam *library* sesuai filter dan sort

### Catalog `[developer: Evelyn Paramesti Hotmauli Silalahi]`

- `CREATE` Menambahkan buku ke katalog **\[LIBRARIAN-ONLY\]**
- `DELETE` Menghapus buku dari katalog **\[LIBRARIAN-ONLY\]**
- `UPDATE` Mengedit data buku yang ada di katalog **\[LIBRARIAN-ONLY\]**
- `READ` Mengembalikan buku dalam katalog sesuai filter dan sort

### Review `[developer: Rana Koesumastuti]`

- `CREATE` Menambahkan review dari Reader untuk suatu buku
- `DELETE` Menghapus review suatu buku oleh Reader
- `UPDATE` Mengedit review suatu buku oleh Reader, Mengupdate *overall* rating buku
- `READ` Mengembalikan review buku sesuai filter dan sort

## Forum `[developer: Muhammad Syahrul Khaliq]`

- `CREATE` Membuat *post* baru di forum atau *reply* ke suatu *post*
- `DELETE` Menghapus *post* atau *reply* milik sendiri
- `UPDATE` Mengedit isi dari *post* atau *reply*
- `READ` Menampilkan halaman utama forum dan *thread* suatu *post* dalam forum

### Reader `[developer: Wahyu Hidayat]`

- `UPDATE` Mengubah display name dan bio di profile page
- `UPDATE` Mengubah settings/preferences Reader
- `READ` Menampilkan halaman profile Reader

## Sumber dataset katalog buku

[https://www.kaggle.com/datasets/jalota/books-dataset/data](https://www.kaggle.com/datasets/jalota/books-dataset/data)

## Role atau peran pengguna beserta deskripsinya

- `Guest / Logged Out`: Dapat mengakses landing page, *sign in* (login) dan *sign up* (register)
- `Reader`: Dapat menambahkan buku dari katalog ke *Library* personal. Buku yang sudah ada bisa diganti status *tracking*nya. Juga dapat memposting ulasan/review buku yang sudah ada di *library*
- `Librarian`: Mengelola katalog buku dengan menambah, mengeedit, dan menghapus buku dari katalog
- `Admin`: Administrator via `django-admin`.
