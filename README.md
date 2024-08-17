# Tietokannat ja web-ohjelmointi kurssin harjoitustyö

## Välipalautus

Sovelluksen toiminnallisuus pitäisi olla viimeistelyjä vaille valmis. Tarkoitus kurssin loppuajan keskittyä sovelluksen ulkonäköön ja virheiden löytämiseen ja korjaamiseen, tietoturvaan ja siihen ettei käyttäjillä ole pääsyä sellaiseen tietoon ja sivuihin joihin tällä ei ole oikeuksia. 

Sovellus täyttää tällä hetkellä ominaisuuksiltaan alussa asetetut vaatimukset eli:
- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- Opiskelija näkee listan kursseista ja voi liittyä kurssille.
- Opiskelija voi lukea kurssin tekstimateriaalia sekä ratkoa kurssin tehtäviä.
- Opiskelija pystyy näkemään tilaston, mitkä kurssin tehtävät hän on ratkonut.
- Opettaja pystyy luomaan uuden kurssin, muuttamaan olemassa olevaa kurssia ja poistamaan kurssin.
- Opettaja pystyy lisäämään kurssille tekstimateriaalia ja tehtäviä. Tehtävä voi olla ainakin monivalinta tai tekstikenttä, johon tulee kirjoittaa oikea vastaus.
- Opettaja pystyy näkemään kurssistaan tilaston, keitä opiskelijoita on kurssilla ja mitkä kurssin tehtävät kukin on ratkonut."

Ominaisuuksia joita olisi kiva vielä lisätä:
- Kuvat

### Käynnistysohje

#### Lataa ja pura ZIP tiedosto koneelle, siirry kansioon. Luo .env-tiedosto kansioon ja kirjoita tiedostoon:

DATABASE_URL= "tähän tietokannan paikallinen osoite"

SECRET_KEY= "tähän salainen avain"

#### Aktivoi virtuaaliympäristö ja suorita seuraavat komennot:

python3 -m venv venv

source venv/bin/activate

pip install -r ./requirements.txt

psql < schema.sql

#### Sovellus käynnistyy komennolla:

flask run


## Harjoitustyön aihe

Harjoitustyön aihe on valittu kurssiin valmiista aihe-ehdotuksista, Opetussovellus, ja sen ominaisuudet ovat samat.

"Sovelluksen avulla voidaan järjestää verkkokursseja, joissa on tekstimateriaalia ja automaattisesti tarkastettavia tehtäviä. Jokainen käyttäjä on opettaja tai opiskelija."

Lisäksi sovelluksessa olisi tarkoitus pystyä lisäämään myös kuvatehtäviä.
