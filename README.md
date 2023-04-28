<h1>Kasityosovellus</h1>

Sovelluksen avulla käyttäjä voi pitää kirjaa omista käsityöprojekteista, tehdä oman ohjeen (esim. neuleohjeen) sekä katsella muiden aloittamia projekteja ja ohjeita. 
Ideana on, että käyttäjä pystyy hallinnoimaan omia juttujaan ja katselemaan/kommentoimaan toisten käyttäjien juttuja.
<p>
Sovelluksen ominaisuuksia:
<p>
<li>Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen. 

<li>Käyttäjä näkee omat projektit ja voi poistaa niitä. 

<li>Käyttäjä voi lisätä omalle projektille aloituspäivämäärän, päätöspäivämäärän ja tiedon siitä mitä materiaalia ja ohjetta on käyttänyt. 

<li>Käyttäjä voi laatia oman käsityöohjeen ja antaa sille vaikeusasteen.

<li>Käyttäjä voi katsella muiden ohjeita ja projekteja ja kommentoida niitä (tähdet ja kommentit) ja lukea muiden kommentteja. 

<li>Käyttäjä voi poistaa omia kommentteja ja viestejä.

<li>Käyttäjä pystyy luomaan uuden projektin/ohjeen ja poistamaan sen. 

<li> Käyttäjä pystyy keskustelemaan muiden käyttäjien kanssa yhteisellä keskustelupalstalla.
<p>
Tällä hetkellä sovellukseen on mahdollista kirjautua sisään, luoda tunnus ja kirjautua ulos.
Lisäksi sovellus antaa virheviestin, jos tunnusta luodessa yritetään luoda jo käytössä oleva tunnus tai salasanat eivät täsmää.
Sovellus antaa virheen myös, jos kirjaudutaan väärillä tunnuksilla tai salasana on liian lyhyt.
Sovelluksessa pystyy tällä hetkellä lähettämään viestejä yleiselle keskustelualueelle sekä lisäämään uusia projekteja ja ohjeita.
Ohjeita ja projekteja voi muut käyttäjät kommentoida.
Omia ohjeita, projekteja, kommentteja ja viestejä voi myös poistaa.
Sovelluksessa pääsee klikkaamalla projektin/ohjeen nimeä projektin/ohjeen sivulle.
<p>
Olen lisännyt sovelluksen fly.io:n, mutta se ei valitettavasti ole testattavissa siellä.
<p>
<h2>Sovelluksen testaamisohjeet paikallisesti:</h2>
<p>
Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:
<p>
DATABASE_URL=tietokannan-paikallinen-osoite
<p>
SECRET_KEY=salainen-avain
<p>
Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla
<li><i>$ python3 -m venv venv</i>
<li><i>$ source venv/bin/activate</i>
<li><i>$ pip install -r ./requirements.txt</i> (päivitetty 25.4.2023)
<p>
Määritä vielä tietokannan skeema komennolla
<p>
<i>$ psql < schema.sql</i>
<p>
Nyt voit käynnistää sovelluksen komennolla
<p>
<i>$ flask run<i/>
