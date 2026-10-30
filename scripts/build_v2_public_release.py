#!/usr/bin/env python3
"""Build only tracked public repository sources as a reproducibility ZIP, not a manuscript."""
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
import subprocess, hashlib, json

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
DIST.mkdir(exist_ok=True)
name = "VELE_REPRODUCIBILITY_PUBLIC_v2.0.0.zip"
paths = [p.decode("utf-8") for p in subprocess.check_output(["git","ls-files","-z"],cwd=ROOT).split(b"\0") if p]
assert paths and "certified_cut_v2/build_source_cut_bounds.py" in paths
for p in paths:
    lo=p.lower()
    if lo.endswith((".docx",".doc",".tex",".pdf",".pptx",".pwb")) or lo.startswith(("submission/","manuscript/","private/")):
        raise RuntimeError("Private/manuscript path prohibited in public release: "+p)
archive = DIST / name
entries=[]
with ZipFile(archive,"w",ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(paths):
        data = (ROOT/p).read_bytes()
        info=ZipInfo(p,(2026,10,30,0,0,0))
        info.compress_type=ZIP_DEFLATED
        info.external_attr=0o644<<16
        z.writestr(info,data)
        entries.append({"file":p,"sha256":hashlib.sha256(data).hexdigest()})
with ZipFile(archive) as z:
    assert z.testzip() is None
    assert sorted(z.namelist()) == sorted(paths)
    assert not any(x.lower().endswith((".docx",".pdf",".tex")) for x in z.namelist())
digest=hashlib.sha256(archive.read_bytes()).hexdigest()
(DIST/"SHA256SUMS_PUBLIC_V2.txt").write_text(digest+"  "+name+"\n",encoding="utf-8")
(DIST/"PUBLIC_V2_FILE_HASHES.json").write_text(json.dumps(entries,indent=2)+"\n",encoding="utf-8")
print("PUBLIC_V2_RELEASE_ARCHIVE_VERIFIED",len(entries),digest)
