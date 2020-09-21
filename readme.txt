Program treba opencv i pysimplegui kako bi se pokrenuo.

Oba ova dependencya se mogu dobiti preko pip-a.

pip3 install opencv-python
(https://opencv.org/)

pip3 install pysimplegui
(https://pypi.org/project/PySimpleGUI/)
Moguće je da je potrebno instalirati tkinter. Na linuxu se ovo može zgrabit sa apt-get
a za windowse nisam siguran

Nakon što su instalirani, dovoljno je napisati python3 main.py

Kako bi program radio potrebno je učitati dvije datoteke. Prva je opis točaka.
Ovo je provideano u datoteci result.txt

Druga datoteka je odgovarajući video - klip od 15 sekundi, dodatno ga stavim na teamse

Nakon toga, kada loading bar završi s učitavanjem moguće je koristiti program.

Neke funkcije u programu nedostaju. Dodatno, učitavanje labela točaka (sa izlaza modela) je trenutno hardecodeano.
