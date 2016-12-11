
#Viikko 46
* Matias

  * Mitä tein:
    * Aloitin frontin tekemisen. Valitsin UI kirjastoksi Reactin. Pystytin devaus-ympäristön ja tutustuin Webpackin ja Reactin toimintaan.

  * Mitä opin:
    * React oli jo ennästään jonkin verran tuttu, mutta opin myös uutta sekä palautui mieleen asioita sen toimintaperiaatteista ja käytöstä.

  * Mitä seuraavaksi:
    * Ohjelma ei vielä käytä backendin dataa. Seuraavaksi yhdistetään siihen.

* Mikko
  * Mitä tein:
    * Asensin kehitysympäristön Pythonin Flaskia varten.
    * Tutustuin Finnkinon ja OMDB:n API:in
    * Suunnittelin yhdessä Matiaksen kanssa rajapintaa
    
  * Mitä opin:
    * Python ja Flask olivat ennestään tuttuja mutta vaativat vähän asioiden palauttelua mieleen.
  
  * Mitä seuraavaksi:
    * Finnkinon ja OMDB:n API:sta pitäisi saada dataa pihalle.
    * Backend pitäisi laittaa jonnekin pyörimään
    
#Viikko 47:
  * Mitä tein:
    * Sain Pythonin hakemaan dataa Finnkinon XML -apista
    * Asensin backendin Herokuun ja päivittymään automaattisesti
    
  * Mitä opin:
    * En oikeastaan ollut käyttänyt Herokua aikaisemmin mutta sen käyttäminen oli yllättävän helppoa.
    * Pythonissa on ihan kätevät XML-työkalut
   
  * Mitä seuraavaksi:
    * Ulos saatava data pitäisi muotoilla hieman paremmin
    * Lisää rajapintoja

#Viikko 48:
* Matias
  * Mitä tein:
    * Frontend käyttää nyt backendilta saatavaa dataa REST-rajapinnan kautta.

  * Mitä opin:
    * Otin uuden axios-kirjaston käyttöön ja tutustuin siihen. Axios on promiseihin perustuva HTTP-kirjasto, joka soveltuu hyvin esim REST-rajapitojen kanssa keskusteluun. REST-rajapinnan käyttämisestä ja datan yhdistelystä opin myös.

  * Mitä seuraavaksi:
    * Viimeistellään ulkoasua ja lisätään uusia kenttiä elokuvista.

* Mikko
  * Mitä tein:
    * Korjasin Matiaksen huomaamia bugeja rajapinnassa
    * Parantelin rajapinnan tuottamaa dataa
    
  * Mitä opin:
    * Tutkailin vaihtoehtoisia kirjastoja kuten Flask-Restful -kirjasto, Hug ja Connexion
      * Connexion vaikutti kätevältä, jos toteuttaa rajapinnan ensin esim. Swagger-editorilla
      * Hug ja Flask-Restful soveltuvat Swaggerin pulttaamiseen jälkikäteen
  
  * Mitä seuraavaksi:
    * Swagger-ui
    * Rajapinnan hiontaa

#Viikko 49+50:
* Matias
  * Mitä tein:
    * Pientä hienosäätöä ulkoasun ja ohjelman toiminnan suhteen.

  * Mitä opin:
    * Selainten HTML5 geolocationin käyttö tuli uutena asiana.

  * Mitä seuraavaksi:
    * Esitetään valmis työ.

* Mikko
  * Mitä tein:
    * Otin Flask-Restful -kirjaston käyttöön Swagger-dokumentaation luomiseksi
  
  * Mitä opin:
    * Migraatio Flaskista Flask-Resftuliin tapahtui yllättävän kivuttomasti
    * Heroku tarjoaa SSL:n implisiittisesti
  
  * Mitä seuraavaksi:
    * Esitetään valmis työ
    * Ehkä pieni performance upgrade ennen demoa

    
