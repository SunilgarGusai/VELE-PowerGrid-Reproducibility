#!/usr/bin/env python3
"""Build only tracked public repository sources as a reproducibility ZIP, not a manuscript."""
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
import subprocess, hashlib, json, argparse

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
DIST.mkdir(exist_ok=True)
parser = argparse.ArgumentParser(description="Create a checksum-verified, public-only tracked release archive")
parser.add_argument("--tag", default="v2.0.0", choices=["v2.0.0", "v2.1.0-review-freeze"])
args = parser.parse_args()
name = f"VELE_REPRODUCIBILITY_PUBLIC_{args.tag}.zip"
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
        info=ZipInfo(p,(2026,11,3,0,0,0) if args.tag.endswith('review-freeze') else (2026,10,30,0,0,0))
        info.compress_type=ZIP_DEFLATED
        info.external_attr=0o644<<16
        z.writestr(info,data)
        entries.append({"file":p,"sha256":hashlib.sha256(data).hexdigest()})
with ZipFile(archive) as z:
    assert z.testzip() is None
    assert sorted(z.namelist()) == sorted(paths)
    assert not any(x.lower().endswith((".docx",".pdf",".tex")) for x in z.namelist())
digest=hashlib.sha256(archive.read_bytes()).hexdigest()
(DIST/("SHA256SUMS_PUBLIC_V2_FINAL.txt" if args.tag.endswith("review-freeze") else "SHA256SUMS_PUBLIC_V2.txt")).write_text(digest+"  "+name+"\n",encoding="utf-8")
(DIST/("PUBLIC_V2_FINAL_FILE_HASHES.json" if args.tag.endswith("review-freeze") else "PUBLIC_V2_FILE_HASHES.json")).write_text(json.dumps(entries,indent=2)+"\n",encoding="utf-8")
print("PUBLIC_RELEASE_ARCHIVE_VERIFIED",args.tag,len(entries),digest)
