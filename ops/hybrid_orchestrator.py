#!/usr/bin/env python3
"""Bounded 24/7 hybrid orchestrator; advisory scheduler, never release authority."""
from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path

ROOT=Path(os.environ.get('MEDIAHUB_ROOT','/home/mediahub/dev/mediahub-os-autonomous')).resolve()
STATE=ROOT/'.autonomous'; LANES=Path('/home/mediahub/dev/parallel-lanes')
ROLES=('planner','explorer','builder','reviewer','tester','security','optimizer')

def sh(*args):
    return subprocess.run(args,cwd=ROOT,text=True,capture_output=True,check=False).stdout.strip()

def snapshot():
    head=sh('git','rev-parse','HEAD')
    tree=sh('git','rev-parse','HEAD^{tree}')
    clean=not bool(sh('git','status','--porcelain'))
    r4=sh('git','merge-base','--is-ancestor','471f709f5633feab7aeb62dd3ea52effad6d2bc4','HEAD')==''
    lanes=sorted(p.name for p in LANES.iterdir() if p.is_dir()) if LANES.is_dir() else []
    observed_path=STATE/'observed_head.json'
    observed=None
    if observed_path.exists():
        try:
            observed=json.loads(observed_path.read_text(encoding='utf-8'))
        except (OSError, ValueError):
            observed={'valid':False}
    reconciliation='INITIALIZED' if observed is None else ('MATCH' if observed.get('head')==head and observed.get('tree')==tree else 'DRIFT')
    current={'head':head,'tree':tree}
    observed_path.write_text(json.dumps(current,sort_keys=True)+'\n',encoding='utf-8')
    return {'ts':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'head':head,'tree':tree,'clean':clean,'r4_ancestry':r4,'roles':list(ROLES),'lanes':lanes,'openrouter_key':bool(os.environ.get('OPENROUTER_API_KEY')),'reconciliation':reconciliation}

while not (STATE/'STOP').exists():
    s=snapshot(); STATE.mkdir(parents=True,exist_ok=True)
    (STATE/'orchestrator.json').write_text(json.dumps(s,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    time.sleep(30)
