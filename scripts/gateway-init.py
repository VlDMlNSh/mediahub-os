#!/usr/bin/env python3
import json, os, urllib.request, urllib.error, urllib.parse, time

base=os.environ.get("GATEWAY_URL","http://new-api:3000").rstrip("/")
user=os.environ["NEW_API_ADMIN_USERNAME"]
password=os.environ["NEW_API_ADMIN_PASSWORD"]

def req(method,path,payload=None,token=None):
    data=json.dumps(payload).encode() if payload is not None else None
    h={"Accept":"application/json"}
    if data: h["Content-Type"]="application/json"
    if token: h["Authorization"]="Bearer "+token
    r=urllib.request.Request(base+path,data=data,headers=h,method=method)
    with urllib.request.urlopen(r,timeout=30) as x:
        return json.loads(x.read().decode() or "{}")

for _ in range(60):
    try:
        if req("GET","/api/status").get("success"): break
    except Exception: pass
    time.sleep(2)
else: raise SystemExit("new-api unhealthy")

try:
    req("POST","/api/setup",{"username":user,"password":password,"confirmPassword":password,"SelfUseModeEnabled":True,"DemoSiteEnabled":False})
except Exception:
    pass

login=req("POST","/api/user/login",{"username":user,"password":password})
token=login["data"]["access_token"]
cfg=json.load(open("/config/channels.json",encoding="utf-8"))
existing=req("GET","/api/channel/search?page_size=100",token=token)["data"]["items"]
names={x.get("name") for x in existing}

for c in cfg["channels"]:
    if c["name"] in names: continue
    keyvars=c.get("key_envs")
    if keyvars:
        key="\n".join(v for v in (os.environ.get(k,"").strip() for k in keyvars) if v)
    else:
        key=os.environ.get(c.get("key_env",""),"").strip()
    if not key:
        print("skip",c["name"],"missing credential")
        continue
    if c.get("test_and_skip"):
        g=os.environ.get("GEMINI_API_KEY","").strip()
        if not g:
            print("skip Gemini missing credential")
            continue
        try:
            u="https://generativelanguage.googleapis.com/v1beta/models?key="+urllib.parse.quote(g,safe="")
            with urllib.request.urlopen(urllib.request.Request(u,method="GET"),timeout=15) as x:
                if x.status != 200: raise RuntimeError("health status")
        except Exception as e:
            print("skip Gemini health-check failed",e)
            continue
    base_url=os.environ.get(c.get("base_url_env",""),"") or c.get("base_url","")
    payload={"mode":"multi_to_single" if c.get("multi_key") else "single","multi_key_mode":c.get("multi_key_mode","random"),
             "channel":{"name":c["name"],"type":c["type"],"key":key,"base_url":base_url,
             "models":",".join(c["models"]),"group":"default","priority":c["priority"],"weight":c["weight"],
             "status":c.get("status",1),"auto_ban":1,"test_model":c["test_model"]}}
    out=req("POST","/api/channel",payload,token=token)
    if not out.get("success"): raise SystemExit("channel create failed: "+str(out))
    print("created",c["name"])
print("gateway-init complete")
