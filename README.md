# letterbookd 📖

Bringing you, your books, and readers together.

*Tugas Kelompok Proyek Tengah Semester kelompok A09 untuk mata kuliah Pemrograman Berbasis Platform Semester Ganjil 2023/2024.*

## Anggota Kelompok A09

> Wahyu Hidayat [**@wahyuhiddayat**](https://www.github.com/wahyuhiddayat)  
> Muhammad Milian Alkindi [**@mmalkindi**](https://www.github.com/mmalkindi)  
> Evelyn Paramesti Hotmauli Silalahi [**@evelynphs**](https://www.github.com/evelynphs)  
> Rana Koesumastuti [**@facesofgoblin**](https://www.github.com/facesofgoblin)  
> Muhammad Syahrul Khaliq [**@Amertaaa**](https://www.github.com/Amertaaa)  

## Cerita aplikasi yang diajukan serta manfaatnya

***Letterbookd*** adalah aplikasi yang bertujuan untuk menyatukan pembaca dengan buku dan pembaca buku lainnya.
Dengan menggunakan aplikasi ini, pembaca dapat menyimpan buku ke *Library* personal mereka, memberikan ulasan
untuk buku yang sudah dibaca, dan juga melihat ulasan buku oleh pembaca lainnya.

## Daftar modul yang akan diimplementasikan

1. Auth: Handling seputar akun pengguna
   - `CREATE` Membuat akun baru lewat Sign Up
   - `READ` Mengembalikan informasi akun
   - `UPDATE` Mengubah username dan password akun
   - `DELETE` Menghapus akun
2. Library: Handling seputar *library* personal pengguna
   - `CREATE` Menambahkan buku ke *library* Reader
   - `DELETE` Mengeluarkan buku dari *library* Reader
   - `UPDATE` Mengubah status *tracking* buku dalam *library*
     - Status Tracking: `FINISHED`, `READING`, `ON HOLD`, `DROPPED`, `UNTRACKED`
   - `READ` Mengembalikan buku dalam *library* sesuai filter dan sort
3. Catalog: Handling seputar katalog buku
   - `CREATE` Menambahkan buku ke katalog **\[LIBRARIAN-ONLY\]**
   - `DELETE` Menghapus buku dari katalog **\[LIBRARIAN-ONLY\]**
   - `UPDATE` Mengedit data buku yang ada di katalog **\[LIBRARIAN-ONLY\]**
   - `READ` Mengembalikan buku dalam katalog sesuai filter dan sort
4. Review
   - `CREATE` Menambahkan review dari Reader untuk suatu buku
   - `DELETE` Menghapus review suatu buku oleh Reader
   - `UPDATE` Mengedit review suatu buku oleh Reader, Mengupdate *overall* rating buku
   - `READ` Mengembalikan review buku sesuai filter dan sort
5. Reader
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
