#!/usr/bin/env python3
"""Regenerates products/<room>/README.md, products/README.md and products/termekek.csv from products/_data/*.json.
Usage: python3 products/_data/generate.py   (optional: products/_data/linkcheck.json = {url: http_status})"""
import json, glob, os, csv, collections
from move_in import ROOM_NOTES
HERE=os.path.dirname(os.path.abspath(__file__)); P=os.path.dirname(HERE); BT=chr(96)
ROOMS=[("00-altalanos-hangulat","Az egész házra (függöny, karnis, kosár, növény, képkeret, babavédelem)","—"),("01-eloszoba","Előszoba","10,60 m² · Norwich Arena"),("02-konyha","Konyha","13,57 m² · Norwich Arena"),("03-etkezo","Étkező","10,93 m² · Norwich Arena"),("04-nappali","Nappali","20,99 m² · Norwich Arena"),("05-halo","Háló","16,22 m² · fa parketta"),("06-szoba","Szoba (babaszoba)","10,63 m² · fa parketta"),("07-dolgozo","Dolgozó","12,78 m² · fa parketta"),("08-szoba","Szoba (gyerek / vendég)","11,55 m² · fa parketta"),("09-eloter","Előtér","3,92 m² · Norwich Arena"),("10-wc","WC","1,63 m² · kerámia"),("11-haztartasi","Háztartási helyiség","5,01 m² · kerámia"),("12-furdo","Fürdők (kádas és zuhanyzós)","Kádas: 4,75 m² · zuhanyzós: méret ellenőrizendő · kerámia"),("13-kozlekedo","Közlekedő","3,47 m² · Norwich Arena"),("14-gardrob","Gardrób","2,79 m² · nyitott kérdés (nem parketta)"),("16-17-terasz","Terasz","41,65 m² · fagyálló kerámia")]
TIER_ORDER={"ajánlott":0,"olcsóbb":1,"alternatíva":2,"prémium":3,"figyelőlista":4}; TIER_ICON={"ajánlott":"⭐ ajánlott","olcsóbb":"💰 olcsóbb","prémium":"💎 prémium","alternatíva":"Alternatíva","figyelőlista":"Figyelőlista"}
items=[]
for f in sorted(glob.glob(os.path.join(HERE,"*.json"))):
    if os.path.basename(f) in ("linkcheck.json","pricecheck.json","pricecheck_manual.json"): continue
    items+=json.load(open(f,encoding="utf-8"))
lc={}
if os.path.exists(os.path.join(HERE,"linkcheck.json")): lc=json.load(open(os.path.join(HERE,"linkcheck.json")))
def ft(n): return f"{int(n):,}".replace(","," ")+" Ft"
def esc(s): return str(s or "").replace("|","/").replace("\n"," ").strip()
def currency(x): return x.get("currency", "HUF")
def amount(x): return x["price_eur"] if currency(x)=="EUR" else x["price_huf"]
def price(x): return f"{amount(x):g} €" if currency(x)=="EUR" else ft(amount(x))
def budgetable(x):
    return currency(x)=="HUF" and x.get("availability")!="out_of_stock" and x.get("budget_include",True)
def tier_label(x):
    label=TIER_ICON.get(x["tier"],x["tier"])
    return label+(f" ({esc(x['recommendation_condition'])})" if x.get("recommendation_condition") else "")
by=collections.defaultdict(list)
for x in items:
    if type(x.get("priority")) is not int or x["priority"] not in (1,2) or not x.get("priority_reason"):
        raise ValueError(f"Hiányzó/hibás beköltözési prioritás: {x.get('name')}")
    if x["priority"]==1 and (not x.get("decision_status") or not x.get("next_step")):
        raise ValueError(f"Hiányzó P1 döntési státusz/következő lépés: {x.get('name')}")
    by[x["room"]].append(x)
if set(by)-set(ROOM_NOTES):
    raise ValueError(f"Hiányzó helyiség-prioritási brief: {set(by)-set(ROOM_NOTES)}")
def priority_total(rows, level):
    return sum(x["price_huf"]*int(x.get("qty",1) or 1) for x in rows
               if x["priority"]==level and x["tier"]=="ajánlott" and budgetable(x))
def priority_section(key, rows):
    note=ROOM_NOTES[key]
    out=["## Beköltözési prioritás", "",
         "**Prio 1:** a minimális beköltözéshez szükséges új beszerzés, a jelzett feltételekkel. **Prio 2:** körülbelül fél évig halasztható, vagy csak későbbi cserejelölt. Ez külön szempont az ajánlott/olcsóbb/prémium minősítéstől.", "",
         "**Induló minimum:** "+note["minimum"], "",
         "**Ráér később:** "+note["later"], ""]
    if note.get("check"): out += ["**Feltétel / kiváltás:** "+note["check"], ""]
    if note.get("unpriced"): out += ["> **Még külön ellenőrizendő, nem árazott:** "+note["unpriced"], ""]
    first=[]
    for x in rows:
        if x["priority"]==1:
            entry=(x["category"], x["priority_reason"], x.get("priority_condition",""))
            if entry not in first: first.append(entry)
    if first:
        out += ["### Prio 1 – előre sorolt tételek", "", "| Tételkör | Miért / milyen feltétellel? |", "| --- | --- |"]
        for category, reason, condition in first:
            out.append(f"| {esc(category)} | {esc(reason)}"+(f" **Feltétel:** {esc(condition)}" if condition else "")+" |")
        out.append("")
    else:
        out += ["**A jelenlegi listán nincs Prio 1 termék ebben a helyiségben.** A még nem árazott vagy meglévő elemek állapotát ettől külön kell ellenőrizni.", ""]
    out += ["| Ajánlott tételek fázisonként | Listázott összeg |", "| --- | --- |",
            f"| Prio 1 – beköltözéshez előre sorolt | **{ft(priority_total(rows,1))}** |",
            f"| Prio 2 – későbbi új beszerzés | **{ft(priority_total(rows,2))}** |", "",
            "> Ezek a korábbi teljes tervezett darabszámokkal számolt, feltételes részösszegek; nem a legolcsóbb beköltözési kosár árai. Egy szükséglethez egy megfelelő megoldást válassz. A meglevővel kiváltott cserejelölt, a kizárt referencia, EUR-os vagy elfogyott termék és az árazatlan hiány nem szerepel bennük. A szükséges induló darabszámok és az átfedések még pontosítandók.", ""]
    p1cats={x["category"] for x in rows if x["priority"]==1}
    uncovered=[c for c in sorted(p1cats) if not any(x["category"]==c and x["priority"]==1 and x["tier"]=="ajánlott" and budgetable(x) for x in rows)]
    if uncovered: out += ["> **Prio 1 funkció, de nincs az ajánlott HUF-részösszegben számolható jelölt:** "+", ".join(uncovered)+". Ez nem nulla költség.", ""]
    return out
summary=[]
for key,name,meta in ROOMS:
    rows=by.get(key,[]); d=os.path.join(P,key); os.makedirs(d,exist_ok=True)
    out=[f"# {key} — {name}","","| | |","| --- | --- |",f"| **Helyiség** | {meta} |",f"| **Termékek** | {len(rows)} db |",f"| **Áradatok dátuma** | 2026-09-20 |",
         f"| **Inspirációs képek** | [{BT}../../inpiration/{key}/{BT}](../../inpiration/{key}/README.md) |",""]
    out += [f"> **Követelmények és források felülvizsgálata:** [a helyiség összes kategóriája](../kategoria-felulvizsgalat.md#{key}) · [közös beszerzési módszer és döntések](../beszerzesi-modszer.md). A követelményfelmérés nem jelent új teljes ár- vagy készletellenőrzést.", ""]
    if os.path.exists(os.path.join(d,"P1-LEZARAS.md")):
        out += ["> **P1 döntési lap:** [javasolt összeállítás, teljes funkciólista és nyitott feltételek](P1-LEZARAS.md) · [házszintű P1 állapot](../P1-KUTATASI-ALLAPOT.md). A „javaslat kész” nem jelenti, hogy a termék már megrendelt vagy beépített.", ""]
    if os.path.exists(os.path.join(d,"KUTATASI-BRIEF.md")):
        out += ["> **Aktuális kutatási brief:** [megerősített igények és nyitott kérdések](KUTATASI-BRIEF.md). Az új követelményekhez a korábbi termékjelöltek illeszkedését még ellenőrizni kell.", ""]
    if os.path.exists(os.path.join(d,"OSSZEHASONLITAS.md")):
        out += ["> **Új termék-összehasonlítás:** [konkrét alternatívák, csomagárak és fennmaradó feltételek](OSSZEHASONLITAS.md).", ""]
    if key=="12-furdo":
        out += ["> **Két külön fürdő:** a kádas 4,75 m²; a zuhanyzós mérete még nincs megadva. A kádas fürdő szekrénye, mosdója és pultja megvan / megrendelve, ezért nincsenek a listában. A zuhanyzós fürdő szekrénye és mosdója is megvan; csak a pult hiányzik. A korábbi referenciapult illeszkedése nem igazolt, ezért kizártuk az összesítésből. Az egyedi pult ára hiányzó költség, nem nulla. [Anyagjavaslat](../anyagvalasztas-konyha-kandallo-furdopult.md). A közös kiegészítők darabszáma előzetes.", ""]
    if key=="02-konyha":
        out += ["> **A tömörfa konyhabútor meg van rendelve.** A fogantyúk kérésre megmaradtak. A front és kőpult megjelenésére külön [anyagjavaslat](../anyagvalasztas-konyha-kandallo-furdopult.md) készült. Aktuális kérés: [világoszöld kőpult – három mintajelölt és hazai források](VILAGOSZOLD-KOPULT.md); szín és teljes ár még nyitott. A bárszék és a szabadon álló kiegészítők illeszkedését a kész bútorhoz kell ellenőrizni. A csap megvan, a mosogató a legújabb helyesbítés szerint még hiányzik. A fogantyú és hulladékgyűjtő a rendelés része; a fogantyújavaslat stílusreferencia.", ""]
    if not rows:
        out+=["> ⏳ **Még nincs feltöltve** – a kutatás folyamatban van.",""]
        summary.append((key,name,0,0,0,0)); open(os.path.join(d,"README.md"),"w",encoding="utf-8").write("\n".join(out)); continue
    out += priority_section(key, rows)
    cats=[]; 
    for x in rows:
        if x["category"] not in cats: cats.append(x["category"])
    cats.sort(key=lambda c:min(x["priority"] for x in rows if x["category"]==c))
    rec=sum(x["price_huf"]*int(x.get("qty",1) or 1) for x in rows if x["tier"]=="ajánlott" and budgetable(x))
    # per category min / max path
    lo=hi=0; omitted=[]
    for c in cats:
        cr=[x for x in rows if x["category"]==c and budgetable(x)]
        if not cr:
            omitted.append(c)
            continue
        tot=[x["price_huf"]*int(x.get("qty",1) or 1) for x in cr]; lo+=min(tot); hi+=max(tot)
    out+=["## Költség ebben a helyiségben","","| Számítás | Összeg |","| --- | --- |",
          f"| ⭐ Csak az **ajánlott** tételek (javasolt darabszámmal) | **{ft(rec)}** |",f"| 💰 Kategóriánként a legolcsóbb sor összege | {ft(lo)} |",f"| 💎 Kategóriánként a legdrágább sor összege | {ft(hi)} |","",
          "> A darabszám javaslat. A forintos költségutak az EUR-os, készlethiányos, meglévővel kiváltott és külön kizárt referenciatételeket kihagyják; ezek ára nem nulla. A feltételes ajánlások szerepelnek a tervezési összegben. A kategóriánkénti alsó/felső összeg nem összeillő bevásárlócsomag: az opcionális és egymást átfedő tételeket külön kell kiválasztani. A szállítás nincs benne; az ár és készlet rendelés előtt ellenőrizendő.",""]
    if omitted: out += ["> A forintos költségutakból kimaradó kategória (nincs számolható tétel): **"+", ".join(omitted)+"**.",""]
    out+=["## Termékek","",f"⭐ = első javaslat, feltételekkel · 💰 = olcsóbb referencia · 💎 = magasabb árú összevetés",""]
    for c in cats:
        cr=sorted([x for x in rows if x["category"]==c],key=lambda x:(x["priority"],TIER_ORDER.get(x["tier"],9)))
        levels=sorted({x["priority"] for x in cr})
        phase=" / ".join(f"Prio {level}" for level in levels)
        out+=[f"### {c} — {phase}","","| Prio | | Termék | Bolt – hol kapható | Anyag / szín | Méret | Ár | Db |","| --- | --- | --- | --- | --- | --- | --- | --- |"]

        for x in cr:
            st=lc.get(x["url"]); warn=" ⚠️ link" if st and str(st)!="200" else ""
            pn=f" <br>*{esc(x['price_note'])}*" if x.get("price_note") else ""
            state=f" <br>*{esc(x['availability_note'])}*" if x.get("availability_note") else ""
            out.append(f"| **Prio {x['priority']}** | {tier_label(x)} | [{esc(x['name'])}]({x['url']}){warn} | **{esc(x['store'])}** – {esc(x['where'])} | {esc(x['material_color'])} | {esc(x['size'])} | **{price(x)}**{pn}{state} | {x.get('qty',1)} |")
        out.append("")
        for level in levels:
            details=list(dict.fromkeys(x["priority_reason"]+(" Feltétel: "+x["priority_condition"] if x.get("priority_condition") else "") for x in cr if x["priority"]==level))
            out.append(f"**Prio {level}:** "+" ".join(esc(t) for t in details))
            out.append("")
        exclusions=list(dict.fromkeys(x["budget_exclusion_reason"] for x in cr if x.get("budget_exclusion_reason")))
        if exclusions: out += ["> **A beszerzési összegből kizárva:** "+" ".join(esc(t) for t in exclusions), ""]
        for x in cr:
            out.append(f"- **{esc(x['name'])}** – {esc(x['why'])}"+(f" ⚠️ *{esc(x['caveat'])}*" if x.get("caveat") else "")+(" *(ár listaoldalról)*" if x.get("verified")=="listing" else ""))
            if x.get("decision_status"):
                out.append(f"  **Döntési státusz:** {esc(x['decision_status'])}. **Következő lépés:** {esc(x.get('next_step',''))}")
        out.append("")
    open(os.path.join(d,"README.md"),"w",encoding="utf-8").write("\n".join(out))
    summary.append((key,name,len(rows),rec,lo,hi))
# CSV
with open(os.path.join(P,"termekek.csv"),"w",newline="",encoding="utf-8-sig") as fh:
    w=csv.writer(fh,delimiter=";"); w.writerow(["Helyiség","Kategória","Szint","Termék","Bolt","Hol kapható","Anyag / szín","Méret","Ár (Ft)","Ármegjegyzés","Javasolt db","Összesen (Ft)","Link","Miért illik","Mire figyelj","Ellenőrzés módja","Ellenőrizve","Link állapot","Pénznem","Eredeti ár","Eredeti részösszeg","Készlet / feltétel","Forintos költségútban","Ajánlás feltétele","Beköltözési prioritás","Prioritás indoka","Prioritás feltétele","Költségkizárás indoka","Döntési státusz","Következő lépés"])
    order={k:i for i,(k,_,_) in enumerate(ROOMS)}
    for x in sorted(items,key=lambda x:(order.get(x["room"],99),x["category"],TIER_ORDER.get(x["tier"],9))):
        q=int(x.get("qty",1) or 1)
        huf_total=x["price_huf"]*q if currency(x)=="HUF" else ""
        w.writerow([x["room"],x["category"],x["tier"],x["name"],x["store"],x["where"],x["material_color"],x["size"],x.get("price_huf"),x.get("price_note",""),q,huf_total,x["url"],x["why"],x.get("caveat",""),x.get("verification_note") or ("termékoldal" if x.get("verified")=="product_page" else "listaoldal"),x.get("checked",""),lc.get(x["url"],""),currency(x),amount(x),amount(x)*q,x.get("availability_note",""),"igen" if budgetable(x) else "nem",x.get("recommendation_condition",""),f"Prio {x['priority']}",x["priority_reason"],x.get("priority_condition",""),x.get("budget_exclusion_reason",""),x.get("decision_status","P2 – későbbi választás"),x.get("next_step","")])
# README
stores=collections.Counter(x["store"] for x in items); done=[s for s in summary if s[2]]; todo=[s for s in summary if not s[2]]
R=["# Terméklista – wooden coastal","",
"> **P1 esetén itt kezdj:** [teljes helyiséglista, döntési státuszok és függő feladatok](P1-KUTATASI-ALLAPOT.md). A kutatási javaslat, a tulajdonosi választás és a megvalósult beszerzés külön állapot.", "",
"> **Beköltözés: 2026. október 30.** [Beszerzési módszer és döntési napló](beszerzesi-modszer.md) · [Kategóriakövetelmények és forráslefedettség](kategoria-felulvizsgalat.md). Étkező: 6 szék férjen el; háló: 180×200 cm matrac; kanapé: kb. 300×200 cm, L alakú, ágyazható, inkább puha. A korábbi jelöltek új követelmények szerinti termékszintű felülvizsgálata folyamatban van.","",
"2026-09-20 · Termékjelöltek magyarországi beszerzéshez: név, link, ár, anyag, méret és beszerzési feltételek. A készlethiányos tételek figyelőlistán szerepelnek. A mappaszerkezet megegyezik az [inspirációs mappáéval](../inpiration/README.md), a válogatás a [belsőépítészeti irányelveket](../principles/Wooden%20coastal%20%E2%80%93%20erdei%20hat%C3%A1s%C3%BA%20bels%C5%91%C3%A9p%C3%ADt%C3%A9szeti%20ir%C3%A1nyelvek%20a%20h%C3%A1zhoz.md) követi.","",
(f"> **Állapot: {len(done)} / {len(summary)} helyiségcsoport listázva, {len(items)} termékjelölt.** Hátravan: " + ", ".join(BT+t[0]+BT for t in todo) + (" – lásd [FOLYTATAS.md](FOLYTATAS.md)." if os.path.exists(os.path.join(P,"FOLYTATAS.md")) else ".")) if todo else f"> **Állapot: mind a {len(summary)} helyiségcsoport listázva, {len(items)} termékjelölt.**","",
"> **Beépített vásárlási felülvizsgálat:** [XXXLutz, Kave Home, H&M Home, JYSK és Mömax – összehasonlítás](vasarlasi-felulvizsgalat-2026-09-20.md). Az aktuális P1 döntési lapok felülírják a korábbi rangsorokat; az étkezőszékeknél a frissebb Carryhome/TONSTAD összevetést kell olvasni. Az EUR-os és készlethiányos alternatívák kimaradnak a forintos költségutakból.","",
"> **Beszerzési kör pontosítva:** a világítás megvan; a tömörfa konyhabútor és mindkét fürdő szekrénye/mosdója megrendelve / megvan, a kádas fürdő pultjával együtt. A fa párkányok RAL 1019 grey beige színben készülnek. A konyhai fogantyúk megmaradnak; a front, konyhai kőpult, kandallóburkolat és a hiányzó zuhanyzós fürdőpult [külön anyagjavaslatot](anyagvalasztas-konyha-kandallo-furdopult.md) kapott, utóbbi felületek ára még nincs az összegben. A 4,75 m²-es kádas és az ismeretlen méretű zuhanyzós fürdőt a `12-furdo` mappa külön nevezi meg.","",
"## Beköltözési ütemezés","",
"**Prio 1:** induláshoz szükséges funkció és a még szükséges új beszerzés. **Prio 2:** körülbelül fél évig halasztható fejlesztés. A termékoldalak tetején helyiségenként ott a minimum, a halasztható rész és a feltétel; minden terméksor külön Prio jelölést kapott.","",
"**Megerősített meglévő elemek:** a korábban rögzített konyha/fürdőbútorok és világítás mellett a dolgozóasztalt és a széket is hozzátok. Az új asztal-/székjelöltek csak későbbi csereopciók, a költségekből kizárva. A 08-as szoba megerősítve vendég-/tartalékszoba, teljes berendezése Prio 2. Megvan a hűtő, főzőlap, sütő, mosógép, páraelszívó, csap, edények–étkészlet és felnőtt ágynemű; a takarítóeszközöket hozzátok. A fogantyú és hulladékgyűjtő a konyharendelés része. A mosogató még hiányzik; a babavédelem megoldottnak jelezve.","",
"**A Prio 1 nem teljes beköltözési költségvetés.** A költségbe számító ajánlott termékek részösszege; több nagy tétel választásra/ajánlatra vár. Hat étkezőszék már rögzített induló mennyiség. Hiányzó költség a megfelelő fekhely, gardrób, kanapé, függöny, egyedi pult és kivitelezés; a megerősített meglévő gépek és ágynemű nem új vásárlások. A drága, végleges tartó vagy dekor nem válik szükségessé attól, hogy az alapfunkció szükséges.","",
"| Helyiség | Prio 1 ajánlott részösszeg | Prio 2 ajánlott részösszeg |","| --- | --- | --- |"]
for key,name,_ in ROOMS:
    R.append(f"| [{name}]({key}/README.md) | **{ft(priority_total(by[key],1))}** | {ft(priority_total(by[key],2))} |")
R += [f"| **Összesen** | **{ft(priority_total(items,1))}** | **{ft(priority_total(items,2))}** |", "",
"> Csak az ajánlott, költségbe számító HUF-jelöltek összege. A meglévővel kiváltott, készlethiányos, EUR-os és kizárt referenciatételek kimaradnak; a nulla összeg nem igazolja, hogy minden funkció megoldott. Az átfedéseket és induló mennyiségeket még véglegesíteni kell.", "",
"## Helyiségek","","| Mappa | Helyiség | Termék | ⭐ Ajánlott csomag | 💰 Kategóriaösszeg, alsó | 💎 Kategóriaösszeg, felső |","| --- | --- | --- | --- | --- | --- |"]
for k,n,c,rec,lo,hi in summary:
    R.append(f"| [{BT}{k}{BT}]({k}/README.md) | {n} | {c} | **{ft(rec)}** | {ft(lo)} | {ft(hi)} |" if c else f"| [{BT}{k}{BT}]({k}/README.md) | {n} | ⏳ hiányzik | – | – | – |")
R+=[f"| | **Összesen (listázott helyiségcsoportok)** | **{len(items)}** | **{ft(sum(s[3] for s in summary))}** | {ft(sum(s[4] for s in summary))} | {ft(sum(s[5] for s in summary))} |","",
"> Az összegek **tájékoztató jellegűek**: a javasolt darabszámmal számolnak, de nem tartalmazzák a még fel nem vett szükségleteket, a már rendezett világítást, konyhabútort, kádas fürdőszobai mosdóösszeállítást és párkányokat, továbbá a burkolást, gépeket és szállítást. Egy-egy kategóriában több alternatíva van – nem kell mindet megvenni. Az alsó/felső kategóriaösszeg nem kész bevásárlócsomag: a házszintű és helyiségenkénti tételek ugyanazt a szükségletet is fedhetik. Az ajánlott összeg is tartalmaz házszintű/helyiségenkénti átfedéseket; nem teljes házköltségvetés.","",
"## Hogyan olvasd","",
"- A kulcstételeknél több jelölt szerepel: **⭐ ajánlott** (elsőként javasolt, a jelzett feltételekkel), **💰 olcsóbb** (alacsonyabb árú referencia), **💎 prémium** (magasabb árú összevetés; előnye külön igazolandó).",
"- **Alternatíva:** más anyag, méret vagy stílus miatt külön mérlegelendő. **Figyelőlista:** készlet-, határidő-, adat- vagy megfelelőségi akadály miatt visszatartott jelölt; nem mind elfogyott. A próba/készletellenőrzés feltételével ajánlott termékek benne vannak a tervezési csomagban.",
f"- **Deviza és készlet:** {sum(currency(x)=='EUR' for x in items)} tétel EUR-os, ellenőrzött forintár nélkül; {sum(x.get('availability')=='out_of_stock' for x in items)} tétel a megadott változatban elfogyott. Ezek, a meglévővel kiváltott dolgozóasztal-/székjelöltek és az illeszkedésre váró fürdőpult-referencia kimaradnak a forintos költségutakból; áruk nem nulla. A CSV külön jelöli a pénznemet, az eredeti árat és a költségútba számítást.",
"- A táblázat alatt tételenként ott van, **miért illik** az irányelvekhez, és ⚠️ jelöli, **mire figyelj** (pl. fólia és nem furnér, nem mosható, melegebb fa tónus – mintát kérni).",
f"- Az egész lista egyben, szűrhetően: [{BT}termekek.csv{BT}](termekek.csv) (pontosvesszővel tagolt, Excelben / Numbersben megnyílik).","",
"## Szűrők, amik szerint válogattam","",
"| Szempont | Szabály |","| --- | --- |",
"| Fa | világos–közép fa preferencia; tömörfa / furnér / dekor külön jelölve, a fal–RAL 1019 grey beige–padló–megrendelt bútor közös mintasorához illesztve |",
"| Fonott | rattan, juta, tengerifű, bambusz, vízi jácint – beltérben nincs műanyag utánzat |",
"| Textil | len, pamut, gyapjú előnyben; buklénál is külön szálösszetétel; műszálas kompromisszum jelölve; törtfehér–homok alap, **zsályazöld** akcentus, kék csak kis adagban |",
"| Fém | **szálcsiszolt sárgaréz** a meglévő szerelvényeken; az új felületet közös mintával ellenőrizzük; aranyszínű bevonat / antik tónus, fa vagy fehér tudatos kompromisszum lehet |",
"| Forma | könnyed forma, látszó lábak preferencia; stabil központi talp elfogadható; zárt tárolás szemmagasság alatt |",
"| Kisbaba | mosható huzat és játszófelület előnyben; tisztítási kompromisszum jelölve; stabil, szükség szerint rögzített bútor |",
"| Ár–érték | nincs előzetes kategóriaárplafon; a funkcióban, méretben, anyagban és színben megfelelő jelöltek legalacsonyabb teljes beszerzési árát keressük |","",
"## Boltok","","| Bolt | Termék |","| --- | --- |"]+[f"| {s} | {c} |" for s,c in stores.most_common()]+["",
"Az új válogatás az XXXLutz, Kave Home, H&M Home és JYSK termékoldalait is feldolgozza. A konkrét szállítási költség és határidő címfüggő; a készletkorlátokat az érintett sorok jelzik. A Mömax kompromisszumos jelöltje a felülvizsgálati jelentésben szerepel.","",
"## Hogyan lettek ellenőrizve","",
"- Az alaplista és a célzott bolti felülvizsgálat adatainak dátuma **2026-09-20**. A mostani fájlfrissítés a már elvégzett kutatást építi be; nem új teljes piaci ár- vagy készletellenőrzés.",
f"- {sum(1 for x in items if x.get('verified')=='product_page')} tétel ára a termékoldalról, {sum(1 for x in items if x.get('verified')=='listing')} tételé listaoldalról / az IKEA keresőjéből származik (ezeket a helyiség-README *(ár listaoldalról)* megjegyzéssel jelöli).",
f"- **Korábbi gépi linkellenőrzés:** {sum(1 for v in lc.values() if str(v)=='200')} / {len(lc)} URL adott 200-as választ. Ez a mentett ellenőrzés nem fedi le az újonnan felvett termékeket; azoknál megnyitott termékoldal volt a forrás." if lc else "- Linkellenőrzés még nem futott.",
(lambda pc: f"- **Mentett második árellenőrzés ({pc['_meta']['date']}):** a korábbi {pc['_meta']['items']} tételből {pc['_meta']['ok']} ára egyezett. Ez történeti eredmény, nem a most kibővített lista új ellenőrzése.")(json.load(open(os.path.join(HERE,"pricecheck.json"),encoding="utf-8"))) if os.path.exists(os.path.join(HERE,"pricecheck.json")) else "- Második árellenőrzés még nem futott.",
"- A készlet és az akciós ár naponta változhat. Szezonális tételeknél (terasz, szeptember vége) ez fokozottan igaz.",
f"- A nyers adatok: [{BT}_data/{BT}](_data/). A táblázatok újragenerálhatók: {BT}python3 products/_data/generate.py{BT}.",""]
notes=os.path.join(HERE,"megjegyzesek.md")
if os.path.exists(notes): R+=[open(notes,encoding="utf-8").read().rstrip(),""]
open(os.path.join(P,"README.md"),"w",encoding="utf-8").write("\n".join(R))
print(len(items),"products;",len(done),"rooms done;",len(todo),"missing:",[t[0] for t in todo])
