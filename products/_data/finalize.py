#!/usr/bin/env python3
"""Validate a finished _wip JSON, link-check it, move it into _data/, regenerate all pages.
Usage: python3 products/_data/finalize.py <file-in-_wip> [--keep-bad-links]"""
import json, os, sys, subprocess, shutil, collections, concurrent.futures as cf
HERE=os.path.dirname(os.path.abspath(__file__)); src=sys.argv[1]
REQ=["room","category","name","store","where","material_color","size","price_huf","url","tier","qty","why","verified"]
d=json.load(open(src,encoding="utf-8")); assert isinstance(d,list) and d, "empty"
bad=[]
for i,x in enumerate(d):
    miss=[k for k in REQ if k not in x or x[k] in (None,"")]
    if miss: bad.append((i,x.get("name"),"missing",miss))
    if not isinstance(x.get("price_huf"),int) or x.get("price_huf",0)<=0: bad.append((i,x.get("name"),"price",x.get("price_huf")))
    if x.get("tier") not in ("ajánlott","olcsóbb","prémium"): bad.append((i,x.get("name"),"tier",x.get("tier")))
    if not str(x.get("url","")).startswith("http"): bad.append((i,x.get("name"),"url",x.get("url")))
    x.setdefault("price_note",""); x.setdefault("caveat",""); x.setdefault("checked","2026-09-20")
    try: x["qty"]=int(x.get("qty",1) or 1)
    except Exception: x["qty"]=1
print("items:",len(d),"rooms:",dict(collections.Counter(x["room"] for x in d)),"verified:",dict(collections.Counter(x["verified"] for x in d)))
if bad:
    print("SCHEMA PROBLEMS:"); [print("  ",b) for b in bad]; sys.exit(1)
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
def chk(u):
    try:
        r=subprocess.run(["curl","-s","-o","/dev/null","-L","--max-time","25","-A",UA,"-w","%{http_code}",u],capture_output=True,text=True,timeout=40); return u,r.stdout.strip()
    except Exception: return u,"ERR"
urls=sorted({x["url"] for x in d})
with cf.ThreadPoolExecutor(10) as ex: res=dict(ex.map(chk,urls))
print("links:",dict(collections.Counter(res.values())))
for u,s in res.items():
    if s!="200": print("  ",s,u)
lcp=os.path.join(HERE,"linkcheck.json"); lc=json.load(open(lcp)) if os.path.exists(lcp) else {}
lc.update(res); json.dump(lc,open(lcp,"w"),indent=1)
json.dump(d,open(src,"w",encoding="utf-8"),ensure_ascii=False,indent=1)
dst=os.path.join(HERE,os.path.basename(src)); shutil.move(src,dst); print("moved ->",dst)
subprocess.run([sys.executable,os.path.join(HERE,"generate.py")],check=True)
