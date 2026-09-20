#!/usr/bin/env python3
"""Independent second price check for every product in _data/*.json.
IKEA: search API by article number. Others: structured price data (JSON-LD / meta) on the product page.
Writes _data/pricecheck.json = {url: {"status": ok|diff|unknown, "found": [...]}}"""
import json,glob,re,os,subprocess,urllib.request,urllib.parse,datetime,concurrent.futures as cf
HERE=os.path.dirname(os.path.abspath(__file__))
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
SKIP={"linkcheck.json","pricecheck.json","pricecheck_manual.json"}
items=[]
for f in sorted(glob.glob(os.path.join(HERE,"*.json"))):
    if os.path.basename(f) in SKIP: continue
    items+=json.load(open(f,encoding="utf-8"))
def ikea(x):
    m=re.search(r"-(s?\d{8})/?$",x["url"])
    if not m: return []
    a=m.group(1).lstrip("s")
    url="https://sik.search.blue.cdtapps.com/hu/hu/search-result-page?"+urllib.parse.urlencode({"q":a,"size":5,"types":"PRODUCT"})
    d=json.load(urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"}),timeout=25))
    return [int(it["product"]["salesPrice"]["numeral"]) for it in d["searchResultPage"]["products"]["main"]["items"] if a in it.get("product",{}).get("pipUrl","")]
def other(x):
    h=subprocess.run(["curl","-sL","--max-time","30","-A",UA,x["url"]],capture_output=True,timeout=45).stdout.decode("utf-8","ignore")
    pr=set()
    for m in re.finditer(r'"price"\s*:\s*"?(\d+(?:[.,]\d+)?)"?',h):
        try: pr.add(int(float(m.group(1).replace(",","."))))
        except Exception: pass
    for m in re.finditer(r'(?:product:price:amount|og:price:amount)"\s+content="(\d+(?:\.\d+)?)"',h): pr.add(int(float(m.group(1))))
    for m in re.finditer(r'(\d{1,3}(?:[  .]\d{3})+)\s*Ft',h):
        try: pr.add(int(re.sub(r"\D","",m.group(1))))
        except Exception: pass
    return sorted(pr)
def chk(x):
    if x.get("currency","HUF")!="HUF":
        return x["url"],{"status":"unknown","found":[],"listed":x.get("price_eur"),"currency":x.get("currency"),"name":x["name"],"room":x["room"],"err":"EUR: the HUF checker cannot verify currency; use the regional product page"}
    try: found=ikea(x) if "ikea.com" in x["url"] else other(x)
    except Exception as e: return x["url"],{"status":"unknown","found":[],"err":str(e)[:60]}
    st="ok" if x["price_huf"] in found else ("diff" if found and "ikea.com" in x["url"] else ("unknown" if not found else "diff"))
    return x["url"],{"status":st,"found":found[:8],"listed":x["price_huf"],"name":x["name"],"room":x["room"]}
with cf.ThreadPoolExecutor(8) as ex: res=dict(ex.map(chk,items))
mp=os.path.join(HERE,"pricecheck_manual.json")
if os.path.exists(mp):
    for u,note in json.load(open(mp,encoding="utf-8")).items():
        if u in res and res[u]["status"]!="ok": res[u]["status"]="ok"; res[u]["manual"]=note
res["_meta"]={"date":datetime.date.today().isoformat(),"items":len(items),"ok":sum(1 for x in items if res.get(x["url"],{}).get("status")=="ok")}
json.dump(res,open(os.path.join(HERE,"pricecheck.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)
print(res["_meta"])
for k,v in res.items():
    if k!="_meta" and v["status"]!="ok": print(v["status"],v.get("room"),v.get("name","")[:50],"listed",v.get("listed"),"found",v.get("found"))
