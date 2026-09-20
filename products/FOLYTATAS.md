# Folytatás – hol tart a munka

Utolsó frissítés: **2026-09-20, kb. 10:50** · A munkamenetet a tulajdonos állította meg. Ez a fájl mindent tartalmaz, ami a folytatáshoz kell – a korábbi beszélgetés nélkül is. **Ha minden kész, ez a fájl törölhető** (a tulajdonos kérése).

## Prompt a folytatáshoz (másik sessionben ezt írd be)

```text
Folytasd a terméklista-munkát. Olvasd el a products/FOLYTATAS.md fájlt és a products/_data/KUTATASI-BRIEF.md-t, és csináld végig a „Hátravan" szakasz három pontját: (1) fürdők + WC bútor és kiegészítők, (2) sárgaréz-revízió a törölt fekete vasalat-tételek pótlására, (3) a 00-altalanos-hangulat hiányzó kategóriái. Helyiségenként mentsd az adatot a products/_data/_wip/ mappába, és amint egy helyiség kész, zárd le a products/_data/finalize.py-jal, és frissítsd a státuszt ebben a fájlban. A végén futtasd a products/_data/pricecheck.py-t, és ha minden megvan, töröld a products/FOLYTATAS.md-t. Ami nem illik a stílusba, azt ne tartsd meg – töröld.
```

## Állapot

| Mappa | Állapot | Termék |
| --- | --- | --- |
| `00-altalanos-hangulat` | 🟡 nagyrészt kész – hiányzó kategóriák lent | 33 |
| `01-eloszoba` | ✅ kész (esernyőtartó pótlandó, lásd revízió) | 22 |
| `02-konyha` | 🟡 kész, de a **konyhai csaptelep és a bútorfogantyú törölve** (fekete volt) – pótlandó sárgarézben | 10 |
| `03-etkezo` · `04-nappali` · `06-szoba` · `07-dolgozo` · `14-gardrob` · `16-17-terasz` | ✅ kész | – |
| `05-halo` · `08-szoba` | ✅ kész (az antracit fali olvasólámpa törölve – opcionálisan pótolható fehérben / sárgarézben) | – |
| `09-eloter` · `13-kozlekedo` | 🟡 a közös **mennyezeti lámpa törölve** (antracit volt) – pótlandó; a 13-asban most csak a futószőnyeg van | – |
| `11-haztartasi` | ✅ kész (csap, seprűsín, akasztó törölve – pótlandó, lásd revízió) | 18 |
| `10-wc` · `12-furdo` | ⏳ **nincs kész** – 11 semleges tétel munkaanyagként a `_data/_wip/10-12-wc-furdo.json`-ban | – |

Összesen a kész listában: **241 termék**; mindegyik linkje 200-at adott, és a független árellenőrzésen mind a 241 ár egyezett (2026-09-20). A pontos számokat a `products/README.md` mutatja (a `generate.py` írja).

## Döntések és tények, amik a mai napon derültek ki (mindegyik be van vezetve az irányelvbe és a briefbe)

1. **A ház fémje: SZÁLCSISZOLT SÁRGARÉZ.** A beltéri ajtók és a nyílászárók kilincsei már ilyenek, a fürdők és a WC szerelvényei is. Kilincset **nem kell** keresni. Minden vasalat jellegű tétel (csaptelep, fogantyú, akasztó, sín, karnis, törölközőtartó) szálcsiszolt / matt sárgaréz legyen, vagy fa / fehér, ha sárgarézben nincs. Matt fekete csak kis adagban (egy-egy lámpa, kandallórács, kültér), vasalatként nem. Króm, nikkel, fényes arany sehol.
2. **Fürdők + WC: a burkolat, a szaniter és a szerelvények már KÉSZEN VANNAK** (helyszíni fotók). Fal: meleg szürke, beton hatású nagy lap + szürke rombusz–háromszög dekorsáv. Szerelvény: szálcsiszolt sárgaréz (kádtöltő, falsík alatti zuhany esőztetővel, **fali mosdókifolyók**, WC-csap). Fali WC-k, fehér Geberit nyomólap. A WC-ben kis fali Geberit kézmosó (~40×25 cm) **szekrény nélkül**, látszó fehér műanyag szifonnal. Csak **bútor és kiegészítő** hiányzik.
3. **Mosdószekrény-méretek:** *A fürdő* – **2 fali kifolyó, kb. 120 cm hely** → ~120 cm-es tölgy szekrény pulttal + **2 db** pultra ültetett, **csaplyuk nélküli** mosdó. *B fürdő* – **1 fali kifolyó, kb. 130 cm hely** → 100–120 cm-es tölgy szekrény pulttal + 1 csaplyuk nélküli, pultra ültetett mosdó. A kifolyók helye adott: rendelés előtt a kifolyók tengelytávját le kell mérni.
4. **Ami nem illik a stílusba, azt törölni kell, nem megőrizni.** A kiszűrt inspirációs képek mappája (`inpiration/_kiszurt/`, 66 kép) a Kukába került; a terméklistából is törlődnek a palettán kívüli tételek (nincs „elutasított" lista).
5. Fa parketta **csak** a 4 szobában (háló, 2 szoba, dolgozó) – korábbi javítás, kész.

## Hátravan

### 1. Fürdők + WC (`12-furdo`, `10-wc`) – új kutatás a fenti 2–3. pont szerint

Kimenet: `products/_data/_wip/10-12-wc-furdo.json` (a meglévő 11 semleges tételt – törölközők, BRANÄS kosár, bambusz készlet, csúszásgátló, fellépő, ÄNGSJÖN magasszekrény, WC-kosár, kis polc, kéztörlő – érdemes megtartani és kiegészíteni).

| Helyiség | Mit kell keresni (⭐/💰/💎 a kulcstételeknél) |
| --- | --- |
| `12-furdo` | **mosdószekrény tölgy / tölgy hatású, 120 cm (A, dupla) és 100–120 cm (B)**, fiókos, pulttal, beépített mosdó NÉLKÜL (IKEA ÄNGSJÖN / HAVBÄCK / TÄNNFORSEN + pult; Bonami / JYSK / szaniterboltok tömör tölgy vagy furnér prémiumnak) · **pultra ültetett fehér kerámia mosdó csaplyuk nélkül**, 38–45 cm (3 db kell összesen) · **tükör** vékony szálcsiszolt sárgaréz vagy tölgy kerettel (A: egy ~120 cm széles vagy 2 kerek; B: 1 db) · fedeles fonott szennyestartó · **törtfehér–homok törölközők** 2 fürdőre + kádkilépők (pamut) · **kiegészítők szálcsiszolt sárgarézben vagy fában**: törölközőtartó / akasztó, törölközőgyűrű, szappanadagoló (matt kerámia vagy sárgaréz), fogmosópohár, zuhanylehúzó; bambusz / teak ülőke vagy kádpolc · **IP44 fali lámpa** a tükör mellé sárgaréz + opál, 2700–3000 K · opcionális: walk-in zuhanyfal arany / sárgaréz profillal |
| `10-wc` | **design szifon szálcsiszolt sárgaréz / bronz**, 5/4", + sarokszelep (a látszó műanyag helyett) · **tükör** a kis kézmosó fölé: kerek 40–50 cm vagy magas keskeny, sárgaréz / tölgy kerettel · **WC-papír tartó + WC-kefe szálcsiszolt sárgaréz** (2 szett: WC + a kádas fürdő WC-je) · kis sárgaréz törölközőgyűrű / akasztó · kis IP44 lámpa sárgaréz / opál, 2700 K · opcionális: Geberit nyomólap sárgaréz hatású kivitelben |

Szaniterhez próbálható: szaniterplaza.hu, szaniteraruhaz.hu, furdoszobaszalon.hu, praktiker.hu, obi.hu, bauhaus.hu, mosdo.hu, emag.hu (termékoldal WebFetch-csel megy, a curl 511-et kap).

### 2. Sárgaréz-revízió – a törölt fekete vasalat-tételek pótlása

Kimenet: `products/_data/_wip/99-sargarez-revizio.json` (a `room` mező tételenként a megfelelő mappa).

| Mappa | Törölve (fekete volt) | Pótlandó |
| --- | --- | --- |
| `00-altalanos-hangulat` | HUGAD / RÄCKA fekete karnis (11 ablak), dupla karnis (3), SYRLIG fekete karika (33 cs.) | **karnis szálcsiszolt sárgaréz / arany színben** 210–385 cm-ig állítható vagy méretre, + hozzá illő karikák; alternatíva marad a fehér VIDGA mennyezeti sín (már a listában van – ezt érdemes „ajánlott"-ra emelni, ha nincs jó sárgaréz rúd) |
| `02-konyha` | 3 matt fekete konyhai csaptelep, BAGGANÄS fekete fogantyú (6) | **konyhai csaptelep szálcsiszolt sárgaréz / brushed gold**, 3 szinten (Ferro, Deante, Invena, Rea, Mexen, Franke, Blanco…) · **BAGGANÄS sárgaréz színű fogantyú** (IKEA – ellenőrizni) |
| `01-eloszoba` | TJUSIG fekete akasztó, NIPÅSEN fekete esernyőtartó | esernyőtartó rattan / sárgaréz (akasztónak a tölgy HÖVOLM maradt) |
| `11-haztartasi` | SALLSJÖN fekete csap, HULTARP fekete sín, TJUSIG fekete akasztó | háztartási csap szálcsiszolt sárgaréz (ha még nincs felszerelve – a tulajdonost megkérdezni) · seprűtartó sín fehér / fa · tölgy akasztó |
| `09-eloter` + `13-kozlekedo` | NYMÅNE antracit mennyezeti lámpa (2 db) | alacsony mennyezeti lámpa **fehér vagy sárgaréz + opál**, 2700 K, CRI 90 ha van (NYMÅNE fehér változat ellenőrizendő) |
| `05-halo`, `08-szoba` | NYMÅNE antracit fali olvasólámpa | opcionális: fali olvasólámpa fehér / sárgaréz |
| Pótlás nélkül törölve | Hagen dohányzóasztal (MDF + fekete fém), Rowico sötét tölgy konzol, SEGLARÖ antracit napernyő, RÅGKORN műanyag fonott-hatású kaspó | – |

### 3. `00-altalanos-hangulat` – még hiányzó kategóriák

Vékony **világos fa képkeretek** 3 méretben (IKEA RÖDALM / PLOMMONTRÄD / HOVSTA – ellenőrizni) + 2–3 konkrét erdei / botanikus print · **párnabelsők** 50x50 és 40x58/65 + **egy zsályazöld len párnahuzat** mint a ház referencia-zöldje · **babavédelem** (átlátszó sarokvédő, szekrényzár, bútorrögzítő – IKEA PATRULL / UNDVIKA) · **nagy matt kerámia padlókaspó** olajfának (Ø 30+ cm; a műanyag RÅGKORN törölve) · 2700 K-es átlátszó filament izzó (az IKEA LUNNOM 2200 K / CRI 80 – jelölve, jobb nem volt).

## Hogyan dolgozz

1. Szabályok és JSON-séma: [`_data/KUTATASI-BRIEF.md`](_data/KUTATASI-BRIEF.md) – benne a **kemény ellenőrzési szabály** (csak ténylegesen megnyitott termékoldal, látott név + Ft ár + működő link), a **menet közbeni mentés** szabálya, a boltok gépi elérhetősége, a sárgaréz-döntés és a fürdők helyszíni tényei.
2. Kutatás közben a fájl a `products/_data/_wip/` mappába kerül (ezt a generátor nem olvassa).
3. Lezárás helyiségenként: `python3 products/_data/finalize.py products/_data/_wip/<fájl>.json` – sémát ellenőriz, linkeket tesztel, áthelyezi a fájlt a `_data/`-ba, és újragenerálja az összes `README.md`-t és a `termekek.csv`-t.
4. A végén: `python3 products/_data/pricecheck.py` (független árellenőrzés: IKEA kereső-API + a többi bolt oldalának áradata; kézi ellenőrzések a `pricecheck_manual.json`-ban), majd `python3 products/_data/generate.py`.
5. Állandó megjegyzések a fő README aljára: `_data/megjegyzesek.md`.

**Tapasztalat:** a háttérkutatások kb. 20–28 perc alatt végeznek; a menet közbeni mentésre és az üzenetekre lassan reagálnak (a fürdő-kutatás 20 perc után sem vette át az átirányítást) – az új feltételeket eleve a kezdő feladatleírásba kell írni, nem utólag üzenni.

## Még nyitott kérdések a tulajdonos felé

- A **háztartási helyiség csaptelepe** fel van-e már szerelve (és milyen színben)?
- A **konyhai csaptelep** megvan-e már? (A konyhabútor asztalos munka.)
- **Költségkeret** helyiségenként vagy összesen.
- **Gardrób burkolata** (nem parketta – Norwich Arena vagy kerámia).
