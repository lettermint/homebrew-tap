"""Reject a cask that would replace a newer stable version."""

import json
import os
from pathlib import Path
import re
import subprocess


def cask_version(text):
    matches = re.findall(r'^\s*version "((?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*))"$', text, re.MULTILINE)
    if len(matches) != 1:
        raise ValueError("One stable cask version is required.")
    return tuple(map(int, matches[0].split(".")))


candidate = cask_version(Path("Casks/lettermint.rb").read_text())
if os.environ.get("GITHUB_EVENT_NAME") == "pull_request":
    subprocess.run(["git", "fetch", "origin", "+refs/heads/main:refs/remotes/origin/main"], check=True)
    current = subprocess.run(["git", "show", "refs/remotes/origin/main:Casks/lettermint.rb"], capture_output=True, text=True)
    if current.returncode == 0 and cask_version(current.stdout) >= candidate:
        raise ValueError("The cask must be newer than the version on main.")
pages = json.loads(subprocess.check_output(["gh", "api", "--paginate", "--slurp", "repos/lettermint/lettermint-cli/releases?per_page=100"], text=True))
versions = []
for release in (item for page in pages for item in page):
    if release["draft"] or release["prerelease"]:
        continue
    match = re.fullmatch(r"v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", release["tag_name"])
    if match:
        versions.append(tuple(map(int, match.groups())))
if not versions or candidate != max(versions):
    raise ValueError("Only the newest published stable release can update the cask.")
print(".".join(map(str, candidate)))
