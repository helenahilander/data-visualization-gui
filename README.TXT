

# Numeerisen datan visualisointikirjasto

## Esittely

Ohjelmakirjasto, jolla voidaan visualisoida numeerista dataa graafisesti

## Tiedosto- ja kansiorakenne

  doc-kansio:
   - data1.csv ja data2.csv ovat esimerkkitiedostoja, jotka voidaan lukea ohjelmaan graafisen käyttöliittymän avulla. 
   (tiedostot tulee ensin tallentaa koneelle)
   - tekninensuunnitelma.pdf ja yleissuunitelma.pdf ovat alustavia ohjelman suunnitelmia, mutta nykyinen ohjelmaa eroaa niistä.
   -dokumentaatio.pdf sisältää lopullisen dokumentaation ohjelmasta

  src-kansio:
    -sisältää kaiken ohjelmaan tarvittavan koodin (5 eri moduulia): data.py, datareadingerror.py, mainwindow.py, readfile.py, readfiletest.py


## Asennusohje

  - Tarvittavat kirjastot:
    - PyQt5 (asennusohje 20.4.2019: https://www.riverbankcomputing.com/static/Docs/PyQt5/installation.html)


## Käyttöohje

  - Tallenna data1.csv ja data2.csv koneelle. Ohjelma käynnistetään ajamalla mainwindow.py tiedosto komentoriviltä, esim kirjoittamalla: python <tiedoston sijainti> .

