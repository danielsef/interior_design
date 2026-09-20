# A terméklisták frissítése

A következő kutatási kör módszere és a tulajdonosi válaszok: [beszerzési döntési napló](../beszerzesi-modszer.md). Mind a 188 aktív kategória követelménye és forráslefedettsége: [kategória-felülvizsgálat](../kategoria-felulvizsgalat.md). Ez dátumozott áttekintés; új termék/kategória felvételekor a lefedettségi számokat is frissíteni kell. A helyiségenkénti `KUTATASI-BRIEF.md` fájlokat a generátor nem írja felül, csak hivatkozik rájuk.

A helyiség-README-k, a fő README és a `termekek.csv` forrásai az itt lévő terméklistás JSON-fájlok. Újragenerálás a projekt gyökeréből: `python3 products/_data/generate.py`.

A `98-vasarlasi-felulvizsgalat.json` a 2026-09-20-i bolti összehasonlítás 14 új jelöltjét tartalmazza. A részletes indoklás: [vásárlási felülvizsgálat](../vasarlasi-felulvizsgalat-2026-09-20.md).

## Ár és készlet

- Meglévő HUF-tétel: numerikus `price_huf`; a hiányzó `currency` HUF-ot jelent.
- Közvetlen Kave Home-tétel: `currency: "EUR"`, numerikus `price_eur`, `price_huf: null`. Nem használunk ellenőrizetlen forintárat.
- `availability: "out_of_stock"`: a megadott változat elfogyott, kimarad minden forintos költségútból. A megjelenített ár ettől még megmarad.
- `orderable` / `in_stock`: az ellenőrzéskor látható állapot; `verify`: rendelés előtti ellenőrzés szükséges. A hiányzó állapot nem jelent igazolt készletet.
- `availability_note` és `verification_note`: a készlet, árforrás és ellenőrzési korlát olvasható leírása.
- `budget_include: false` szükség esetén kizár egy további tételt a költségutakból. Az EUR-os és elfogyott tételek ettől függetlenül mindig kimaradnak.
- `recommendation_condition`: például próba vagy készletellenőrzés után. A feltételes HUF-ajánlás szerepel a tervezési csomagban.

Az új szék- és asztalajánlás a korábbit váltsa ki, ne duplázza meg az ajánlott csomagot. A meglévő lista néhány kategóriájában több, együtt használt ajánlott tétel szerepel; ezeket a frissítés megőrzi. Az alternatívák ugyanazt a tervezett mennyiséget fedjék le: hat karfás szék összevethető hat karfa nélküli székkel; a négy + két darabos kevert változat külön megjegyzés, nem hozzáadandó csomag.

## Export és összesítés

A CSV pontosvesszős, UTF-8 BOM-os export. Az eredeti oszlopok sorrendje megmarad, utánuk a pénznem, eredeti egységár/részösszeg, készlet, költségútba számítás és ajánlási feltétel szerepel. EUR-nál a Ft-os mezők üresek, nem nullák. A készlethiányos HUF-sorok ára látható, a kizárást a `Forintos költségútban` oszlop jelzi.

A forintos minimum/maximum csak a számolható tételekből választ kategóriánként. Ha egy kategóriának nincs ilyen tétele, a helyiségoldal külön megnevezi a kimaradást. A szállítás és a házszintű/helyiségenkénti tételek ismert átfedése nincs feloldva.

A mentett `pricecheck.json` és `linkcheck.json` történeti ellenőrzés. Nem szabad az eredményeiket az új teljes listára érvényes ellenőrzésként feltüntetni. A `pricecheck.py` HUF-ellenőrzője az EUR-os tételeket ellenőrizendőként hagyja.

## Beszerzési kör – tulajdonosi pontosítás

A világítás megvan; a fa párkányok RAL 1019 grey beige színben készülnek. Ezekhez ne adj új terméket vagy specifikációt. A tömörfa konyhabútor megrendelve, de kérésre a front, kőpult és fogantyúk megjelenésére továbbra is adunk javaslatot; a négy fogantyújelölt megmarad.

A kádas fürdő 4,75 m², szekrénye, mosdója és pultja megvan / megrendelve. A zuhanyzós fürdő szekrénye és mosdója is megvan, **pultja még nincs**, a bútor mérete/típusa és a helyiség területe még ismeretlen. A `12-furdo` mindkét fürdőt név szerint kezeli. Meglévő mosdó/szekrény helyett ne adj új jelöltet; a régi ÅLSKEN pult csak `budget_include: false` referenciaként marad az illeszkedés ellenőrzéséig.

Az első szűrés után 310 jelölt maradt: 46 világítási, 2 kádas szekrény/pult, 2 zuhanyzós szekrény, 3 mosdó és 1 leeresztő jelölt kikerült a korábbi 364-ből. A külön magasszekrény opcionális. A régi ár-/linkellenőrzések változatlan történeti állományok, nem aktív beszerzési listák.

Az egyedi felületek [anyagválasztási briefje](../anyagvalasztas-konyha-kandallo-furdopult.md) külön dokumentum; az ár még nem ismert, ezért nem szabad nulla árú JSON-termékként vagy költségként felvenni. A kategóriánkénti alsó/felső összeg nem kész kosár; az ajánlott csomag darabszámait és átfedéseit rendelés előtt véglegesíteni kell.

## Beköltözési prioritás

Minden aktív termék kötelező mezői: `priority` (1 vagy 2), `priority_reason` (indoklás); opcionális `priority_condition` (mikor érvényes/vált a besorolás). A prioritás független a `tier` ajánlási/árszinttől. Prio 1 az induláskor szükséges funkcióhoz még szükséges beszerzés, Prio 2 a kb. fél évig halasztható fejlesztés vagy későbbi cserejelölt. Az egy kategóriában szereplő termékek eltérhetnek: például a kiságylepedő P1, a muszlintakaró P2.

A helyiségek induló minimumát, halasztható részét, feltételeit és árazatlan hiányait a `move_in.py` tartalmazza. A generátor ezekből minden helyiségoldal tetejére összefoglalót ír; a terméksorokon külön Prio oszlop van. A kategóriákat P1 szerint előre rendezi, egyébként megőrzi a forrássorrendet.

A CSV végére négy oszlop került: `Beköltözési prioritás`, `Prioritás indoka`, `Prioritás feltétele`, `Költségkizárás indoka`. Az előző 24 oszlop megmaradt. A P1/P2 összegek az ajánlott, költségbe számító HUF-sorok teljes tervezett darabszámával készülnek; összegük az ajánlott csomag. Ezek nem teljes minimálkosár-árak: a még árazatlan alapdarabok és a valódi induló mennyiségek külön pontosítandók.

**Megerősített változás:** a dolgozóasztalt és széket hozzák. Az ezekhez tartozó új jelöltek P2 csereopciók, `budget_include: false` és `budget_exclusion_reason` mellett. Ez a mező a fürdőpult-referencia kizárásának okát is tárolja. A 08-as szoba megerősítve vendég-/tartalékszoba, teljes listája P2. A többi hozott darabról nincs tételes leltár; ne nevezz konkrét terméket meglévőnek pusztán abból, hogy a funkció már megoldott.

A `97-etkezo-alternativak.json` négy új, 2026-09-20-án ellenőrzött alternatívát ad hozzá (összesen 314 aktív sor). Az étkező összehasonlítása a helyiség `OSSZEHASONLITAS.md` fájljában olvasható; a generátor ezt is belinkeli.

A `96-kanape-alternativak.json` egy 2026-09-20-án ellenőrzött Rocky figyelőlistás sort ad hozzá: **315 rekord**. A Rocky és a két korábbi egyenes IKEA-kanapé `budget_include: false`; a kanapé funkció továbbra is P1, költsége hiányzó tétel. A [kanapé-összehasonlítás](../04-nappali/OSSZEHASONLITAS.md) a szállított árat és a kizárások okát is tartalmazza.

A `95-halo-alternativak.json` három 180×200-as ágyalternatívát ad hozzá: **318 rekord**. A három régi 140/160-as ágy kizárt referencia; a teljes fekhely még nem ajánlott csomag. Az új tételek `why` és `caveat` mezője külön nevezi meg a stílusbeli illeszkedést, kompromisszumot és hiányzó ellenőrzést.

A `94-halo-matrac-agyracs.json` két matracot és két ágyrácsot ad hozzá: **322 rekord, 188 helyiség–kategória**. Mind a négy P1, de `budget_include: false` a hiányzó komfort-/terhelhetőségi és kompatibilitási igazolás miatt. A rács egységára mellett `qty: 2`; az ágyba eleve foglalt rácsot nem kell újra hozzáadni. [Kutatási eredmény és feltételes csomagárak](../05-halo/MATRAC-OSSZEHASONLITAS.md).
