"""Room-specific move-in assumptions; product priorities live in the JSON records."""

ROOM_NOTES = {
    "00-altalanos-hangulat": {
        "minimum": "A ténylegesen szükséges babavédelem és az első naptól használt alvóhelyek sötétítése/belátásvédelme. A sötétítéshez induláskor a háló és babaszoba saját rolójával számolunk, így nem kell a teljes házas függönycsomagot is megvenni.",
        "later": "A végleges fényszűrők, teljes karnisrendszer, dekor, növények, képkeretek és összehangolt kosárcsalád ráérnek.",
        "check": "Ha a beköltözési sötétítést függönnyel oldjátok meg, annak karnisa és bélése együtt Prio 1, a szobai roló helyett. A használt szőnyeg szükséges alátétjét vele együtt kell beszerezni.",
    },
    "01-eloszoba": {
        "minimum": "Egy fogas, lábtörlő és kijelölt hely a nedves cipőknek; az előszoba teljes bútorozása nélkül is használható.",
        "later": "Cipősszekrény, kabátos gardrób, pad, tükör, szőnyeg és dekor később választható a tényleges tárolási igény alapján.",
    },
    "02-konyha": {
        "minimum": "A megrendelt konyha legyen használatra kész: működő mosogató/csap, munkafelület, nyitható frontok és alap ételkészítő felszerelés. Új csap/fogantyú csak akkor kell, ha még nincs a rendelésben.",
        "later": "Bárszék, futószőnyeg, egységes kerámia tárolók és gyümölcskosár; az étkezőasztal kiváltja a szigetnél ülést.",
        "check": "A H&M konyharuhák készlethiányos jelöltek. A funkció Prio 1, a konkrét mintára nem kell várni. A kőpult és front véglegesítését érdemes a konyha szerelése előtt rendezni.",
        "unpriced": "A lista nem teljes konyhafelszerelés: szükség szerint edény, evőeszköz, tányér/pohár, hulladékgyűjtő és a még hiányzó gépek is kellenek. A kőpult egyedi ára nincs az összegben.",
    },
    "03-etkezo": {
        "minimum": "Egy használható asztal és annyi ülőhely, ahányat naponta használtok; szükség esetén a baba megfelelő etetőszéke.",
        "later": "A hat székből a vendéghelyek, a tálaló, étkezőszőnyeg, asztali futó és váza ráérnek.",
        "check": "Megerősített követelmény: az asztalnál hat normál szék férjen el kényelmesen. Még nyitott, hogy alapméretben vagy bővítve; a beköltözéskor megvett székek száma sincs külön rögzítve. Az ISLEV ajánlása üléspróbához kötött.",
    },
    "04-nappali": {
        "minimum": "Egy közös ülő-/pihenőhely; a kandalló és a használatba vett berendezés szükséges védelme.",
        "later": "Dohányzóasztal, plusz fotel, TV-szekrény, tálaló, dekorációs szőnyegek, párnák és plédek. A játszóhelynek meglévő megfelelő megoldás is használható.",
        "check": "Kanapé: kb. 300×200 cm, L alakú, inkább puha, alkalmi ágy két felnőttnek; a megfelelő jelöltek legalacsonyabb teljes szállított árát keressük, előzetes árplafon nélkül. Fix vagy mosható kárpit elfogadható. Az oldalirány és a komfort még ellenőrizendő. A kandalló pusztán dekoratív burkolata halasztható, ha a berendezés használaton kívül vagy a kivitelező szerint kész, használható állapotban van. A működéshez szükséges befejezés nem Prio 2. A poros burkolási munkát célszerű a kanapé beköltöztetése előtt elvégezni, ha belefér.",
        "unpriced": "A megfelelő kanapé költsége hiányzik az ajánlott összegből; ez nem nulla költség; nincs előre rögzített kategóriaárplafon. A korábbi ajánlott kanapé 169 900 Ft-os kizárása nem megtakarítás. A kandalló burkolati/rendszerbefejezésének egyedi költsége sincs a termékösszegben.",
    },
    "05-halo": {
        "minimum": "Teljes, használható fekhely, megfelelő méretű alap ágynemű és sötétítés. Az alap ruhatárolással a gardróbban számolunk.",
        "check": "Egy közös 180×200-as matrac; ágyneműtartó előny, de nem kötelező. A megfelelő csomagok közül a legalacsonyabb teljes árat keressük. A külső méret, kompatibilis ágyrács és matrackomfort ellenőrizendő. Két matrac- és két ágyrácsjelölt már árazott, de a komfort/kompatibilitás igazolásáig kimarad a költségutakból.",
        "later": "Éjjeliszekrény, külön komód, ágyvégi pad, szőnyeg, tükör, díszpárnák és végleges fényszűrő függöny.",
        "unpriced": "Az új ágykeret még alternatíva, nincs az ajánlott összegben; a régi 100 000 Ft-os keret kivétele nem megtakarítás. A kiválasztott csomag szállítása, matracvédő, lepedő, paplan és párna még hiányzik. A listázott ágykeret/huzat nem automatikusan teljes alvási csomag.",
    },
    "06-szoba": {
        "minimum": "A baba ténylegesen használt fekhelye, hozzá illő matrac és lepedő, valamint az alvóhely sötétítése.",
        "later": "Külön szoptatós fotel, végleges polc/kosarak, dekorációs szőnyeg és külön pelenkázóbútor, ha a pelenkázás más megfelelő meglévő megoldással rendezett.",
        "check": "A gyermek beköltözéskor egyéves lesz. Az alvás helye még nyitott: ha kezdetben a szülői hálóban lesz, ugyanazokat a szükséges darabokat oda kell ütemezni, nem második garnitúrát venni. Az Ágynemű/takaró kategórián belül a lepedő Prio 1, a külön muszlintakaró Prio 2.",
        "unpriced": "A meglévő készlettől függő alap babaápolási és pelenkázási kellékek nem teljes körűen részei ennek a bútorlistának.",
    },
    "07-dolgozo": {
        "minimum": "A dolgozóasztalt és a széket hozzátok, így ezekre nincs új beköltözési beszerzés. Használatkor a szükséges fényvédelem és kábelelrendezés marad előre sorolt feladat.",
        "later": "Új asztal/szék csak cserejelölt; tárolóbútor, polc, szőnyeg és dekor szintén halasztható.",
        "check": "A napi munkavégzés indulása nincs külön rögzítve: a roló és kábelelrendezés akkor Prio 1, amikor használatba veszitek a munkahelyet. A hozott bútorok helyett listázott új jelöltek minden költségútból ki vannak véve.",
    },
    "08-szoba": {
        "minimum": "Megerősítve vendég-/tartalékszoba: új bútor nélkül is várhat, nincs önálló Prio 1 vásárlás.",
        "later": "A teljes vendégszobai berendezés: ágy, szekrény, íróasztal/szék, textilek és tárolók.",
        "check": "Ha később mindennapi hálószoba lesz, a fekhely, ágynemű, sötétítés és alap ruhatárolás előre sorolandó.",
    },
    "09-eloter": {
        "minimum": "Maradjon szabad az átjárás és az ajtónyitás; nincs szükség új bútorra a beköltözéshez.",
        "later": "Konzolasztal, tükör, kép, tálka és kosár: mind Prio 2.",
    },
    "10-wc": {
        "minimum": "A meglévő WC/kézmosó működjön; legyen kéztörlő, szappan, WC-papír és tisztítóeszköz. A végleges falra szerelt tartók nem feltételek.",
        "later": "Design szifon és sarokszelep szín miatti cseréje, dekorpolc, külön tükör és végleges sárgaréz tartók.",
        "check": "A két WC-kefe a korábbi listában a külön WC-t és a kádas fürdő WC-jét együtt fedi. Csak a ténylegesen használt helyekhez szükséges darabszámot kell most megvenni; egyszerűbb megfelelő kefe is elég.",
        "unpriced": "A szappan, WC-papír és tisztítószer fogyóeszköz, ára nincs a terméklistában.",
    },
    "11-haztartasi": {
        "minimum": "Működő mosás és szárítás, valamint megfelelően elzárt hely a tisztítószereknek/eszközöknek.",
        "later": "A teljes szekrénysor, második mosogató/csap, munkalap, design szennyeskosarak és kényelmi rendszerezők.",
        "check": "Az összeépítő készlet és a kényelmi magasító külön funkció: egymásra helyezett gépeknél a megfelelő összeépítő elem a használat előfeltétele. A konkrét géphez illeszkedését ellenőrizni kell.",
        "unpriced": "Ha nem hozzátok/nincs megrendelve, a mosógép és alap takarítóeszközök költsége külön hiányzik. A gépek nem részei a jelenlegi termékösszegnek.",
    },
    "12-furdo": {
        "minimum": "Legalább egy teljesen működő fürdő. A kádas fürdő szekrénye, mosdója és pultja megvan/megrendelve; ennek beépítésével, alap törölközőkkel, szükséges kilépővel/csúszásvédelemmel és egy használható mosdótükörrel számolunk.",
        "later": "A második fürdő pultja/tükre, külön magas tároló, végleges sárgaréz kiegészítők, szennyestartó, kádpolc és pad, ha a kész kádas fürdő elegendő.",
        "check": "A zuhanyzós fürdő pultja csak akkor Prio 2, ha a kádas fürdő indulásra teljesen használható és elegendő. Ha ez nem teljesül, vagy mindkét fürdő napi használata szükséges, a hiányzó pultot előre kell venni. A működéshez szükséges elemeket a későbbi fürdő használata előtt be kell fejezni.",
        "unpriced": "A zuhanyzós fürdő egyedi pultjának ára továbbra is hiányzik; a nem igazoltan illeszkedő ÅLSKEN referencia nem része az összegnek.",
    },
    "13-kozlekedo": {
        "minimum": "Szabad, használható útvonal; nincs új Prio 1 termék.",
        "later": "A futószőnyeg fél év múlva is megvehető.",
    },
    "14-gardrob": {
        "minimum": "Egy alap ruhatárolási megoldás és a szükséges vállfák, ha nincs más megfelelő tároló.",
        "later": "Összehangolt kosarak, puff és állótükör; meglévő ruhatároló esetén a végleges gardróbrendszer is.",
        "check": "A hálószobai komód és a gardrób nem egyszerre kötelező minimum. Indulásra itt számolunk a ruhák tárolásával; a kiválasztott egy megoldás váltsa ki a másikat.",
    },
    "16-17-terasz": {
        "minimum": "Új kültéri bútor nem kell a minimális beköltözéshez; a kijárat és szükséges közlekedés legyen használható.",
        "later": "A teljes kültéri étkező/lounge, árnyékoló, párnák, kaspók és tárolók. Az ápolást/huzatot a később megvett bútorhoz kell ütemezni.",
    },
}
