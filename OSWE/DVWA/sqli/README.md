script menggunakan threading (`concurrent.future`) yang lumayan cepet dibanding script SQLi yang sebelumnya dibuat/pada skeleton script saya punya

yang high sedikit makan waktu est: 20-25 menit (no idea kenapa) setelah dikasih thread, sebelumnya bisa 40-45 menit :<
```
python3 .\med.py -t localhost:4280 -s e70e732fdcaaa0fdcdb18b4d89e093d3
python3 .\med.py -t localhost:4280 -s e70e732fdcaaa0fdcdb18b4d89e093d3 -v (if you want use proxy)
```