"""Download exact, source-attributed PGLib-OPF v23.07 cases with SHA-256 checks."""
from pathlib import Path
import urllib.request,hashlib,json
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'inputs';OUT.mkdir(exist_ok=True)
checks=json.loads((ROOT/'SOURCE_CASE_SHA256.json').read_text())
for name,digest in checks.items():
 sub='api/' if name.startswith('api_') else ''
 url='https://raw.githubusercontent.com/power-grid-lib/pglib-opf/v23.07/'+sub+(name[4:] if sub else name)
 req=urllib.request.Request(url,headers={'User-Agent':'VELE03-v2-validation'})
 try:
  data=urllib.request.urlopen(req,timeout=45).read()
 except Exception as e:raise RuntimeError('Cannot fetch published PGLib source '+url) from e
 sha=hashlib.sha256(data).hexdigest()
 if sha!=digest:raise RuntimeError(f'Source SHA mismatch for {name}: {sha} vs {digest}')
 (OUT/name).write_bytes(data)
 print('SOURCE_PIN_VERIFIED',name,sha)
print('ALL_FOUR_PGLIB_v23.07_SOURCES_VERIFIED')
