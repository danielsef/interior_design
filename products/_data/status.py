#!/usr/bin/env python3
"""Rewrites the live status block at the top of products/FOLYTATAS.md. Usage: status.py '<room>=<text>' ..."""
import os, re, sys, json, glob, collections, datetime
HERE=os.path.dirname(os.path.abspath(__file__)); P=os.path.dirname(HERE); fp=os.path.join(P,"FOLYTATAS.md")
sp=os.path.join(HERE,"_wip","status.json"); st=json.load(open(sp)) if os.path.exists(sp) else {}
for a in sys.argv[1:]:
    k,v=a.split("=",1); st[k]=v
os.makedirs(os.path.dirname(sp),exist_ok=True); json.dump(st,open(sp,"w"),ensure_ascii=False,indent=1)
cnt=collections.Counter()
for f in glob.glob(os.path.join(HERE,"*.json")):
    if os.path.basename(f) in ("linkcheck.json","pricecheck.json","pricecheck_manual.json"): continue
    for x in json.load(open(f,encoding="utf-8")): cnt[x["room"]]+=1
wip=collections.Counter()
for f in glob.glob(os.path.join(HERE,"_wip","*.json")):
    if os.path.basename(f)=="status.json": continue
    try:
        for x in json.load(open(f,encoding="utf-8")): wip[x["room"]]+=1
    except Exception: pass
rooms=["00-altalanos-hangulat","01-eloszoba","10-wc","11-haztartasi","12-furdo"]
now=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
blk=["<!-- status:start -->",f"## Élő státusz – a hiányzó 5 helyiség (frissítve: {now})","","| Mappa | Állapot | Kész termék | Folyamatban (mentve, még ellenőrizetlen) |","| --- | --- | --- | --- |"]
for r in rooms: blk.append(f"| `{r}` | {st.get(r,'⏳ kutatás fut')} | {cnt.get(r,0) or '–'} | {wip.get(r,0) or '–'} |")
blk+=["",f"Összesen a listában: **{sum(cnt.values())} termék**.","<!-- status:end -->",""]
s=open(fp,encoding="utf-8").read()
s=re.sub(r"<!-- status:start -->.*?<!-- status:end -->\n*","",s,flags=re.S)
head,rest=s.split("\n",1)
open(fp,"w",encoding="utf-8").write(head+"\n\n"+"\n".join(blk)+rest.lstrip("\n"))
print("\n".join(blk[1:-2]))
