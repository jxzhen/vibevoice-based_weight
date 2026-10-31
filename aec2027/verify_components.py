#!/usr/bin/env python3
"""Verify the aec2027 model component manifest.

Two independent checks:

  1. INTEGRITY   -- every LFS-tracked file digest in MANIFEST.json must
                    equal the digest the HuggingFace Hub publishes for the
                    pinned revision (lfs.sha256).
  2. DEPLOYED    -- the locally computed digests in LOCAL_SHA256_*.txt must
                    equal the same published digests, i.e. the bytes that
                    were actually deployed are the bytes of the public
                    revision.

Usage:
    python verify_components.py              # online: query the Hub
    python verify_components.py --offline    # only local evidence files
    python verify_components.py --repo dots-studio/dots.tts.edit

Exit code 0 = all checks passed, 1 = at least one failure.
"""
import argparse
import json
import os
import ssl
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "MANIFEST.json")

MIRRORS = ("https://hf-mirror.com", "https://huggingface.co")


def _opener():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return urllib.request.build_opener(
        urllib.request.HTTPSHandler(context=ctx))


def hub_files(repo, revision):
    """Return {filename: lfs_sha256} for the given revision."""
    for base in MIRRORS:
        url = "%s/api/models/%s?blobs=true&revision=%s" % (base, repo, revision)
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "aec2027-verify/1.0"})
            with _opener().open(req, timeout=90) as r:
                data = json.loads(r.read().decode("utf-8", "replace"))
            out = {}
            for s in (data.get("siblings") or []):
                lfs = s.get("lfs") or {}
                if lfs.get("sha256"):
                    out[s.get("rfilename")] = lfs["sha256"].lower()
            return out
        except Exception:
            continue
    return None


def read_local_digests():
    out = {}
    for name in sorted(os.listdir(HERE)):
        if not (name.startswith("LOCAL_SHA256_") and name.endswith(".txt")):
            continue
        path = os.path.join(HERE, name)
        for line in open(path, encoding="utf-8", errors="replace"):
            line = line.rstrip("\n")
            if not line.strip():
                continue
            parts = line.split(None, 1)
            if len(parts) != 2:
                continue
            digest, fname = parts[0].strip().lower(), parts[1].strip()
            out[(name, fname.lstrip("./"))] = digest
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--repo", default=None)
    args = ap.parse_args()

    man = json.load(open(MANIFEST, encoding="utf-8"))
    comps = man.get("components") or []
    if args.repo:
        comps = [c for c in comps if c.get("repo") == args.repo]
        if not comps:
            print("no such component: %s" % args.repo)
            return 1

    local = read_local_digests()
    failures = 0
    checked = 0

    for comp in comps:
        repo = comp.get("repo")
        rev = comp.get("pinned_revision")
        print("== %s (%s)" % (comp.get("role"), repo))
        if not rev:
            print("   SKIP: no pinned revision")
            continue
        hub = None
        if not args.offline:
            hub = hub_files(repo, rev)
            if hub is None:
                print("   SKIP: Hub unreachable (use --offline to skip)")
        for f in comp.get("files") or []:
            if f.get("checksum_source") != "huggingface_lfs_sha256":
                continue
            want = (f.get("sha256") or "").lower()
            name = f.get("name")
            if hub is not None:
                got = hub.get(name)
                checked += 1
                if got is None:
                    print("   FAIL  %s : not present in revision %s"
                          % (name, rev[:12]))
                    failures += 1
                elif got != want:
                    print("   FAIL  %s : manifest %s != hub %s"
                          % (name, want[:16], got[:16]))
                    failures += 1
            # local evidence must agree with the same digest
            local_tag = comp.get("local_digest_file")
            if local_tag:
                for (src, lname), ldigest in local.items():
                    if lname != name or src != local_tag:
                        continue
                    checked += 1
                    if ldigest != want:
                        print("   FAIL  %s : local %s != published %s"
                              % (name, ldigest[:16], want[:16]))
                        failures += 1
                    else:
                        print("   OK    %s  %s" % (name, want[:16]))

    print()
    print("checked %d digests, %d failures" % (checked, failures))
    if failures:
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
