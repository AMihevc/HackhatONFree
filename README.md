# Prispevek ekipe Free - Arnes HackhatON 2024
* **Ekipa:** Free
* **Člani:** Timotej Petrič, Anže Mihevc, Aljaž Grdadolnik, Domen Vilar
* **izziv:** [1. Napovedovanje poplav](https://hackathon.si/izziv-1/)

# Naslov rešitve
Poplavko - Asistent za napovedovanje in pripravo na poplave

# Spletni naslovi
- [Github](https://github.com/AMihevc/HackhatONFree)
- [Zenodo](https://zenodo.org/records/11189599)

# Splošni opis rešitve
Razvili smo spletno aplikacijo Poplavko, katere glavna funkcionalnost je napovedovanje poplav in prikaz napovedi na uporabniku prijazen način. Napovedi za posamezne regije prikazujemo na zemljevidu, podobno kot smo navajeni na vremenskih napovedih. Napoved temelji na vremenskih podatkih in višini vodostaja, prikazana pa je lahko kot: nizka verjetnost poplave, srednja verjetnost poplave, visoka verjetnost poplave.

Poleg napovedi prikazujemo tudi zgodovinsko karto poplavnih območij, ki jo lahko uporabnik po želji vklopi ali izklopi. V drugem zavihku naše aplikacije se nahaja prijazen digitalni asistent, ki lahko odgovarja na vprašanja o napovedi, kako se pripraviti na poplave ali kaj storiti, če je do poplave že prišlo. Asistent bo vnaprej pripravljen na uporabnika, saj bomo poskrbeli, da bo vedel, kakšna je naša napoved poplav za naslednji teden. Deluje na podobni tehnologiji kot ChatGPT, zato je zelo vsestranski in pozna odgovore na širok razpon vprašanj.

Uporabniki ne potrebujejo stalno obiskovati spletne strani, saj se lahko preko elektronske pošte naročijo na e-napoved. Tako bodo ob izbranih intervalih prejemali e-pošto z napovedjo poplav ali pa se lahko naročijo samo na "pomembna" obvestila.

# Ideje za nadaljnji razvoj
Eden glavnih razlogov za hude poplave v preteklem letu so bili zanemarjeni travniki, "odtoki", poplavne ravnice in struge mnogih rek v Sloveniji. V prihodnosti bi lahko v našo aplikacijo dodali zavihek, kjer bi agregirali in grafično prikazovali podatke o onesnaženih območjih in spremljali postopek čiščenja slovenskih vodotokov. Kot vir teh podatkov bi lahko uporabili spletno stran [DRSV](https://www.gov.si/novice/2024-04-24-odstranjevanje-odpadkov-na-vodnih-in-priobalnih-zemljiscih/) ali se povezali s kolegi iz geografije, ki so bolj na tekočem s procesom čiščenja.

Trenutno model deluje na podlagi zgodovinskih podatkov, vendar s časom dobivamo nove podatke, ki bi jih lahko uporabili za izboljšanje natančnosti naših napovedi. Uporabnikom bi lahko dali možnost vnosa dejanskih posledic poplav in na podlagi teh podatkov dodali nove regije in izboljšali napovedi.

Izboljšanje uporabniške izkušnje in bolj modern uporabniški vmesnik za še lažje navigiranje po naši spletni strani in vseh funkcionalnostih, ki jih ponuja.

# Tehnologija
Za razvoj prototipa naše aplikacije smo uporabili naslednje tehnologije:
- Frontend (spletna stran, ki jo vidi uporabnik): ogrodje Vue.js
- Backend (storitev, ki napoveduje): ogrodje FastAPI, napisano v Pythonu
- Obdelava podatkov in učenje modela: programski jezik Python, knjižnice pandas, sklearn
- Za poganjanje programov in modelov smo uporabili superračunalnik ARNES, kjer smo hranili tudi vmesne podatke. Uporabljali smo skupni prostor, da smo olajšali sodelovanje znotraj ekipe.
- Za razvoj smo uporabili git in GitHub za lažje sodelovanje in sledenje kodi. S tem podpiramo načela odprte znanosti.
- Naše podatke smo naložili tudi na portal Zenodo, s čimer smo dodali k zbirki odprtih podatkov, ki so na voljo vsem za nadaljnje projekte.

# Viri podatkov
- Arhiv ARSO za vreme, [opozorilna karta OPSI](https://podatki.gov.si/dataset/opozorilna-karta-poplav), [arhiv ARSO za višino vodostajev slovenskih rek](https://vode.arso.gov.si/hidarhiv/pov_arhiv_tab.php)
- Podatke smo črpali iz portala OPSI, arhiva ARSO in nekatere podatke so nam priskrbeli tudi mentorji. Vsi podatki so odprte narave in dostopni vsem, zato smo se odločili, da tudi mi svoje podatke ponudimo na razpolago vsakomur, ki bi jih želel uporabiti.

# Model
Preizkusili smo več različnih modelov. Zaradi časovnih omejitev za treniranje smo za trenutni prototip aplikacije izbrali klasifikator Random Forest, ki napoveduje verjetnosti za poplavo glede na višino vodostaja na danem datumu. Z več časa bi lahko natrenirali boljše modele, kot so nevronske mreže. Prav tako bi z več časa lahko izboljšali naše podatke in natančneje določili mejne vrednosti za visoko, srednjo in nizko verjetnost poplav. (Glej [Arhiv ARSO za višino vodostajev slovenskih rek](https://vode.arso.gov.si/hidarhiv/pov_arhiv_tab.php) - ekstremni dogodki).

Rezultati modela so naslednji:

|               | natančnost | obnovitev | f1-score | podpora |
|---------------|------------|-----------|----------|---------|
| 0             | 0.63       | 0.67      | 0.65     | 916     |
| 1             | 0.57       | 0.58      | 0.57     | 835     |
| 2             | 1.00       | 0.03      | 0.05     | 74      |
| natančnost    |            |           | 0.60     | 1825    |
| povprečje     | 0.73       | 0.43      | 0.43     | 1825    |
| uteženo povp. | 0.62       | 0.60      | 0.59     | 1825    |

# UNESCO
Razvoj sistema za napovedovanje poplav bi lahko imel pozitivne učinke na različne vidike družbe in okolja. Z gradnjo modela za napovedovanje poplav bi si prizadevali izpolnjevati cilje trajnostnega razvoja, kot jih je opredelila UNESCO.
- Cilj 2: Sistem bi lahko pomagal kmetijskim skupnostim pri boljšem načrtovanju pridelave hrane, saj bi jim omogočil, da se pravočasno pripravijo na morebitne poplave, ki bi lahko uničile pridelek.
- Cilj 3: Lahko se poskusimo pripraviti na zdravstvena tveganja, povezana s poplavami (npr. bolezni, ki se prenašajo zaradi poplav, poškodbe in duševne težave)
- Cilj 6: Sistem pomaga pri učinkovitejšem upravljanju z vodnimi viri, saj pomaga zagotavljati dostop do čiste vode zaradi izvajanja ukrepov za zmanjšanje onesnaženja med poplavami.
- Cilj 9: Razvoj sistema zahteva inovativne tehnologije in razvoj ter posodobitev obstoječe infrastrukture
- Cilj 11: Sistem za napovedovanje poplav omogoča pravočasno opozarjanje in pripravo na morebitne poplave, kar zmanjšuje tveganje za škodo na infrastrukturi, izgubo življenj in premoženja. Tako lahko pomaga mestom in skupnostim načrtovati odporno infrastrukturo, zmanjšuje tveganja za poškodbe mesta zaradi poplav in spodbuja trajnostni razvoj mest in infrastrukture
- Cilj 15: Poplave pogosto povzročijo škodo na okolju, kot je erozija tal, onesnažena voda in izguba življenjskega prostora za živali in rastline. Sistem omogoča boljšo
- Cilj 17: Razvoj sistema zahteva sodelovanje med vladami, organizacijami in skupnostmi na globalnem nivoju za doseganje trajnostnega razvoja
