#!/usr/bin/env python3
"""Regenerates products/<room>/README.md, products/README.md and products/termekek.csv from products/_data/*.json.
Usage: python3 products/_data/generate.py   (optional: products/_data/linkcheck.json = {url: http_status})"""
import json, glob, os, csv, collections
HERE=os.path.dirname(os.path.abspath(__file__)); P=os.path.dirname(HERE); BT=chr(96)
ROOMS=[("00-altalanos-hangulat","Az egész házra (függöny, izzó, kilincs, kosár, növény)","—"),("01-eloszoba","Előszoba","10,60 m² · Norwich Arena"),("02-konyha","Konyha","13,57 m² · Norwich Arena"),("03-etkezo","Étkező","10,93 m² · Norwich Arena"),("04-nappali","Nappali","20,99 m² · Norwich Arena"),("05-halo","Háló","16,22 m² · fa parketta"),("06-szoba","Szoba (babaszoba)","10,63 m² · fa parketta"),("07-dolgozo","Dolgozó","12,78 m² · fa parketta"),("08-szoba","Szoba (gyerek / vendég)","11,55 m² · fa parketta"),("09-eloter","Előtér","3,92 m² · Norwich Arena"),("10-wc","WC","1,63 m² · kerámia"),("11-haztartasi","Háztartási helyiség","5,01 m² · kerámia"),("12-furdo","Fürdő","4,75 m² · kerámia"),("13-kozlekedo","Közlekedő","3,47 m² · Norwich Arena"),("14-gardrob","Gardrób","2,79 m² · nyitott kérdés (nem parketta)"),("16-17-terasz","Terasz","41,65 m² · fagyálló kerámia")]
TIER_ORDER={"ajánlott":0,"olcsóbb":1,"prémium":2}; TIER_ICON={"ajánlott":"⭐ ajánlott","olcsóbb":"💰 olcsóbb","prémium":"💎 prémium"}
items=[]
for f in sorted(glob.glob(os.path.join(HERE,"*.json"))):
    if os.path.basename(f) in ("linkcheck.json","pricecheck.json","pricecheck_manual.json"): continue
    items+=json.load(open(f,encoding="utf-8"))
lc={}
if os.path.exists(os.path.join(HERE,"linkcheck.json")): lc=json.load(open(os.path.join(HERE,"linkcheck.json")))
def ft(n): return f"{int(n):,}".replace(","," ")+" Ft"
def esc(s): return str(s or "").replace("|","/").replace("\n"," ").strip()
by=collections.defaultdict(list)
for x in items: by[x["room"]].append(x)
summary=[]
for key,name,meta in ROOMS:
    rows=by.get(key,[]); d=os.path.join(P,key); os.makedirs(d,exist_ok=True)
    out=[f"# {key} — {name}","","| | |","| --- | --- |",f"| **Helyiség** | {meta} |",f"| **Termékek** | {len(rows)} db |",f"| **Árak ellenőrizve** | 2026-09-20 |",
         f"| **Inspirációs képek** | [{BT}../../inpiration/{key}/{BT}](../../inpiration/{key}/README.md) |",""]
    if not rows:
        out+=["> ⏳ **Még nincs feltöltve** – a kutatás folyamatban van.",""]
        summary.append((key,name,0,0,0,0)); open(os.path.join(d,"README.md"),"w",encoding="utf-8").write("\n".join(out)); continue
    cats=[]; 
    for x in rows:
        if x["category"] not in cats: cats.append(x["category"])
    rec=sum(x["price_huf"]*int(x.get("qty",1) or 1) for x in rows if x["tier"]=="ajánlott")
    # per category min / max path
    lo=hi=0
    for c in cats:
        cr=[x for x in rows if x["category"]==c]
        tot=[x["price_huf"]*int(x.get("qty",1) or 1) for x in cr]; lo+=min(tot); hi+=max(tot)
    out+=["## Költség ebben a helyiségben","","| Forgatókönyv | Összeg |","| --- | --- |",
          f"| ⭐ Csak az **ajánlott** tételek (javasolt darabszámmal) | **{ft(rec)}** |",f"| 💰 Minden kategóriából a legolcsóbb | {ft(lo)} |",f"| 💎 Minden kategóriából a legdrágább | {ft(hi)} |","",
          "> A darabszám javaslat (pl. 6 szék, 2 éjjeliszekrény). Az árak a bolt weboldalán 2026-09-20-án látott árak – vásárlás előtt nézd meg újra, az akciók változnak.",""]
    out+=["## Termékek","",f"⭐ = ezt venném · 💰 = olcsóbb, még vállalható · 💎 = jobb minőség, még észszerű áron",""]
    for c in cats:
        cr=sorted([x for x in rows if x["category"]==c],key=lambda x:TIER_ORDER.get(x["tier"],9))
        out+=[f"### {c}","","| | Termék | Bolt – hol kapható | Anyag / szín | Méret | Ár | Db |","| --- | --- | --- | --- | --- | --- | --- |"]
        for x in cr:
            st=lc.get(x["url"]); warn=" ⚠️ link" if st and str(st)!="200" else ""
            pn=f" <br>*{esc(x['price_note'])}*" if x.get("price_note") else ""
            out.append(f"| {TIER_ICON.get(x['tier'],x['tier'])} | [{esc(x['name'])}]({x['url']}){warn} | **{esc(x['store'])}** – {esc(x['where'])} | {esc(x['material_color'])} | {esc(x['size'])} | **{ft(x['price_huf'])}**{pn} | {x.get('qty',1)} |")
        out.append("")
        for x in cr:
            out.append(f"- **{esc(x['name'])}** – {esc(x['why'])}"+(f" ⚠️ *{esc(x['caveat'])}*" if x.get("caveat") else "")+(" *(ár listaoldalról)*" if x.get("verified")=="listing" else ""))
        out.append("")
    open(os.path.join(d,"README.md"),"w",encoding="utf-8").write("\n".join(out))
    summary.append((key,name,len(rows),rec,lo,hi))
# CSV
with open(os.path.join(P,"termekek.csv"),"w",newline="",encoding="utf-8-sig") as fh:
    w=csv.writer(fh,delimiter=";"); w.writerow(["Helyiség","Kategória","Szint","Termék","Bolt","Hol kapható","Anyag / szín","Méret","Ár (Ft)","Ármegjegyzés","Javasolt db","Összesen (Ft)","Link","Miért illik","Mire figyelj","Ellenőrzés módja","Ellenőrizve","Link állapot"])
    order={k:i for i,(k,_,_) in enumerate(ROOMS)}
    for x in sorted(items,key=lambda x:(order.get(x["room"],99),x["category"],TIER_ORDER.get(x["tier"],9))):
        q=int(x.get("qty",1) or 1)
        w.writerow([x["room"],x["category"],x["tier"],x["name"],x["store"],x["where"],x["material_color"],x["size"],x["price_huf"],x.get("price_note",""),q,x["price_huf"]*q,x["url"],x["why"],x.get("caveat",""),"termékoldal" if x.get("verified")=="product_page" else "listaoldal",x.get("checked",""),lc.get(x["url"],"")])
# README
stores=collections.Counter(x["store"] for x in items); done=[s for s in summary if s[2]]; todo=[s for s in summary if not s[2]]
R=["# Terméklista – wooden coastal","",
"2026-09-20 · Konkrét, **Magyarországon megvásárolható** termékek helyiségenként: név, link, ár, hol kapható. A mappaszerkezet megegyezik az [inspirációs mappáéval](../inpiration/README.md), a válogatás a [belsőépítészeti irányelveket](../principles/Wooden%20coastal%20%E2%80%93%20erdei%20hat%C3%A1s%C3%BA%20bels%C5%91%C3%A9p%C3%ADt%C3%A9szeti%20ir%C3%A1nyelvek%20a%20h%C3%A1zhoz.md) követi.","",
(f"> **Állapot: {len(done)} / {len(summary)} helyiség kész, {len(items)} termék.** Hátravan: " + ", ".join(BT+t[0]+BT for t in todo) + (" – lásd [FOLYTATAS.md](FOLYTATAS.md)." if os.path.exists(os.path.join(P,"FOLYTATAS.md")) else ".")) if todo else f"> **Állapot: mind a {len(summary)} helyiség kész, {len(items)} termék.**","",
"## Helyiségek","","| Mappa | Helyiség | Termék | ⭐ Ajánlott csomag | 💰 Legolcsóbb út | 💎 Legdrágább út |","| --- | --- | --- | --- | --- | --- |"]
for k,n,c,rec,lo,hi in summary:
    R.append(f"| [{BT}{k}{BT}]({k}/README.md) | {n} | {c} | **{ft(rec)}** | {ft(lo)} | {ft(hi)} |" if c else f"| [{BT}{k}{BT}]({k}/README.md) | {n} | ⏳ hiányzik | – | – | – |")
R+=[f"| | **Összesen (kész helyiségek)** | **{len(items)}** | **{ft(sum(s[3] for s in summary))}** | {ft(sum(s[4] for s in summary))} | {ft(sum(s[5] for s in summary))} |","",
"> Az összegek **tájékoztató jellegűek**: a javasolt darabszámmal számolnak, de nem tartalmazzák a hiányzó helyiségeket, a konyhabútort, a burkolást, a gépeket és a szállítást. Egy-egy kategóriában több alternatíva van – nem kell mindet megvenni.","",
"## Hogyan olvasd","",
"- Minden kulcstételnél 2–3 lehetőség van: **⭐ ajánlott** (jó ár-érték, ezt venném), **💰 olcsóbb** (még vállalható), **💎 prémium** (jobb minőség, még észszerű áron).",
"- A táblázat alatt tételenként ott van, **miért illik** az irányelvekhez, és ⚠️ jelöli, **mire figyelj** (pl. fólia és nem furnér, nem mosható, melegebb fa tónus – mintát kérni).",
f"- Az egész lista egyben, szűrhetően: [{BT}termekek.csv{BT}](termekek.csv) (pontosvesszővel tagolt, Excelben / Numbersben megnyílik).","",
"## Szűrők, amik szerint válogattam","",
"| Szempont | Szabály |","| --- | --- |",
"| Fa | világos–közép tölgy (vagy kőris, nyír, akác kültéren), matt / olajozott; nincs sötét dió, magasfény, sárgás-vöröses tónus |",
"| Fonott | rattan, juta, tengerifű, bambusz, vízi jácint – beltérben nincs műanyag utánzat |",
"| Textil | len, pamut, gyapjú, bouclé; törtfehér–homok alap, **zsályazöld** akcentus, kék csak kis adagban |",
"| Fém | **matt fekete** (egy típus az egész házban); nincs fényes króm |",
"| Forma | alacsony, látszó lábak, néhány íves darab; zárt tárolás szemmagasság alatt |",
"| Fény | 2700 K, CRI 90+ ahol az adat elérhető |",
"| Kisbaba | levehető, mosható huzat; mosható szőnyeg ott, ahol eszik/játszik; falhoz rögzíthető bútor; lekerekített sarkok |",
"| Ár–érték | középkategória: kulcsdaraboknál tömörfa vagy valódi furnér előnyben; se a legolcsóbb, se luxus |","",
"## Boltok","","| Bolt | Termék |","| --- | --- |"]+[f"| {s} | {c} |" for s,c in stores.most_common()]+["",
"Az IKEA-hoz legközelebbi áruház Pilisjászfaluról **Budaörs**; a Bonami, vidaXL, Westwing csak webshop (házhoz szállítás). XXXLutz, Kave Home, H&M Home, lampak.hu oldalait a gépi lekérdezés ellen védik, ezért onnan nem került be ellenőrzött ár – ezeket érdemes személyesen / böngészőből megnézni alternatívának.","",
"## Hogyan lettek ellenőrizve","",
f"- Minden termék **termékoldalát (vagy listaoldalát) 2026-09-20-án megnyitottam**: pontos név, aktuális Ft ár, működő link. Ami nem volt elérhető, elfogyott vagy 404-et adott, kimaradt – semmi nincs emlékezetből beírva.",
f"- {sum(1 for x in items if x.get('verified')=='product_page')} tétel ára a termékoldalról, {sum(1 for x in items if x.get('verified')=='listing')} tételé listaoldalról / az IKEA keresőjéből származik (ezeket a helyiség-README *(ár listaoldalról)* megjegyzéssel jelöli).",
f"- **Linkellenőrzés:** {sum(1 for v in lc.values() if str(v)=='200')} / {len(lc)} link adott 200-as választ a lista írásakor." if lc else "- Linkellenőrzés még nem futott.",
(lambda pc: f"- **Második, független árellenőrzés ({pc['_meta']['date']}):** {pc['_meta']['ok']} / {pc['_meta']['items']} tétel ára egyezett a bolt aktuális árával (IKEA: kereső-API cikkszám szerint; többi bolt: a termékoldal áradata).")(json.load(open(os.path.join(HERE,"pricecheck.json"),encoding="utf-8"))) if os.path.exists(os.path.join(HERE,"pricecheck.json")) else "- Második árellenőrzés még nem futott.",
"- A készlet és az akciós ár naponta változhat. Szezonális tételeknél (terasz, szeptember vége) ez fokozottan igaz.",
f"- A nyers adatok: [{BT}_data/{BT}](_data/). A táblázatok újragenerálhatók: {BT}python3 products/_data/generate.py{BT}.",""]
notes=os.path.join(HERE,"megjegyzesek.md")
if os.path.exists(notes): R+=[open(notes,encoding="utf-8").read().rstrip(),""]
open(os.path.join(P,"README.md"),"w",encoding="utf-8").write("\n".join(R))
print(len(items),"products;",len(done),"rooms done;",len(todo),"missing:",[t[0] for t in todo])
