#!/usr/bin/env python3
import json, os, urllib.request, urllib.error, urllib.parse, time

BASE=os.environ.get("GATEWAY_URL","http://new-api:3000").rstrip("/")
USER=os.environ["NEW_API_ADMIN_USERNAME"]; PASSWORD=os.environ["NEW_API_ADMIN_PASSWORD"]
HC=os.environ.get("HEALTH_CHECK_ENABLED","true").lower() == "true"

def req(method,path,payload=None,token=None):
    data=json.dumps(payload).encode() if payload is not None else None
    h={"Accept":"application/json"}
    if data: h["Content-Type"]="application/json"
    if token: h["Authorization"]="Bearer "+token
    r=urllib.request.Request(BASE+path,data=data,headers=h,method=method)
    with urllib.request.urlopen(r,timeout=30) as x:
        return json.loads(x.read().decode() or "{}")

def http_status(url,headers=None,data=None,method="GET"):
    r=urllib.request.Request(url,data=data,headers=headers or {},method=method)
    with urllib.request.urlopen(r,timeout=15) as x: return x.status

for _ in range(60):
    try:
        if req("GET","/api/status").get("success"): break
    except Exception: pass
    time.sleep(2)
else: raise SystemExit("new-api unhealthy")

try: req("POST","/api/setup",{"username":USER,"password":PASSWORD,"confirmPassword":PASSWORD,"SelfUseModeEnabled":True,"DemoSiteEnabled":False})
except Exception: pass
login=req("POST","/api/user/login",{"username":USER,"password":PASSWORD})
token=login["data"]["access_token"]
cfg=json.load(open("/config/channels.json",encoding="utf-8"))
existing=req("GET","/api/channel/search?page_size=100",token=token)["data"]["items"]
names={x.get("name") for x in existing}

def credential(c):
    if c.get("key_envs"):
        return "\n".join(v for v in (os.environ.get(k,"").strip() for k in c["key_envs"]) if v)
    return os.environ.get(c.get("key_env",""),"").strip()

def health(c,key):
    if not HC or not c.get("health_check"): return True
    name=c["id"]
    try:
        if name=="gemini":
            url="https://generativelanguage.googleapis.com/v1beta/models?key="+urllib.parse.quote(key,safe="")
            return http_status(url)==200
        if name=="groq":
            return http_status("https://api.groq.com/openai/v1/models",{"Authorization":"Bearer "+key})==200
    except urllib.error.HTTPError as e:
        print("WARNING:",c["name"],"health-check HTTP",e.code,"; skipping channel")
    except Exception as e:
        print("WARNING:",c["name"],"health-check failed:",e,"; skipping channel")
    return False

for c in cfg["channels"]:
    if c.get("status",1) != 1: print("disabled until scheduled expansion:",c["name"]); continue
    key=credential(c)
    if not key: print("skip",c["name"],"missing credential"); continue
    if not health(c,key):
        print("WARNING:",c["name"],"test-and-skip health check failed; channel will not be created")
        continue
    base_url=os.environ.get(c.get("base_url_env",""),"") or c.get("base_url","")
    api_version=os.environ.get(c.get("api_version_env",""),"")
    payload={"mode":"multi_to_single" if c.get("multi_key") else "single","multi_key_mode":c.get("multi_key_mode","random"),
             "channel":{"name":c["name"],"type":c["type"],"key":key,"base_url":base_url,
             "models":",".join(c["models"]),"group":"default","priority":c["priority"],"weight":c["weight"],
             "status":1,"auto_ban":1,"test_model":c.get("test_model","")}}
    if api_version: payload["channel"]["other"]=api_version
    if c["name"] in names: print("exists",c["name"]); continue
    out=req("POST","/api/channel",payload,token=token)
    if not out.get("success"): raise SystemExit("channel create failed: "+str(out))
    print("created",c["name"])
print("gateway-init complete")
