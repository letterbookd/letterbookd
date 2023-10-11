# letterbookd 📖

*Bringing you, your books, and readers together.*

## Anggota Kelompok

> Wahyu Hidayat [**@wahyuhiddayat**](https://www.github.com/wahyuhiddayat)  
> Muhammad Milian Alkindi [**@mmalkindi**](https://www.github.com/mmalkindi)  
> Evelyn Paramesti Hotmauli Silalahi [**@evelynphs**](https://www.github.com/evelynphs)  
> Rana Koesumastuti [**@facesofgoblin**](https://www.github.com/facesofgoblin)  
> Muhammad Syahrul Khaliq [**@Amertaaa**](https://www.github.com/Amertaaa)  

## Cerita aplikasi yang diajukan serta manfaatnya

***Letterbookd*** adalah aplikasi yang bertujuan untuk membawa pembaca dengan buku dan pembaca buku lainnya.
Dengan menggunakan aplikasi ini, pembaca dapat menyimpan buku ke *Library* personal mereka, memberikan ulasan
untuk buku yang sudah dibaca, dan juga melihat ulasan buku oleh pembaca lainnya.

## Daftar modul yang akan diimplementasikan

1. Auth: Handling seputar akun pengguna
   - `CREATE` Membuat akun baru dengan Sign Up
   - `READ` Mengembalikan informasi akun
   - `UPDATE` Mengubah username dan password akun
   - `DELETE` Menghapus akun
2. Library: Handling seputar *library* pengguna
   - `CREATE` Menambahkan buku ke *library* User
   - `DELETE` Mengeluarkan buku dari *library* User
   - `UPDATE` Mengubah status *tracking* buku dalam *library*
     - Status Tracking: `FINISHED`, `READING`, `ON HOLD`, `DROPPED`, `UNTRACKED`
   - `READ` Mengembalikan buku dalam *library* sesuai filter dan sort
     - Tracking Status
     - Favorited
     - Reviewed
3. Catalog: Handling seputar katalog buku
   - `CREATE` Menambahkan buku ke katalog **\[LIBRARIAN-ONLY\]**
   - `DELETE` Menghapus buku dari katalog **\[LIBRARIAN-ONLY\]**
   - `UPDATE` Mengedit data buku yang ada di katalog **\[LIBRARIAN-ONLY\]**
   - `READ` Mengembalikan buku dalam katalog sesuai filter dan sort
     - Title
     - In library / Not in library
     - Favorite count
     - Review count
4. Review
   - `CREATE` Menambahkan review dari User untuk suatu buku
   - `DELETE` Menghapus review suatu buku oleh User
   - `UPDATE` Mengedit review suatu buku oleh User, Mengupdate *overall* rating buku
   - `READ` Mengembalikan review buku sesuai filter dan sort
     - Review stars
     - User's tracking status on review
5. User
   - `UPDATE` Mengubah display name dan bio di profile page
   - `UPDATE` Mengubah settings/preferences User
   - `READ` Menampilkan halaman profile User

## Sumber dataset katalog buku

[https://www.kaggle.com/datasets/jalota/books-dataset/data](https://www.kaggle.com/datasets/jalota/books-dataset/data)

## Account Roles / Priveleges

- `Reader`: Review, Track, Favorite, Search books from the catalogue
- `Librarian`: Manages the book catalogue (add, edit, delete)
- `Admin`: Administrator via `django-admin`.
