"""Keep versioned update feeds and permanent README download links."""
import argparse
import json
import re
from pathlib import Path

REPO = "INCY-DEV/incy-platforms"
DESKTOP = {
    "windows": {"x64": "incy-windows-setup.exe", "arm64": "incy-windows-setup.exe",
                "x64_portable": "incy-windows-portable.zip", "arm64_portable": "incy-windows-portable.zip"},
    "macos": {"arm64": "incy-macos-arm64.dmg", "intel": "incy-macos-intel.dmg"},
    "linux": {"x64_deb": "incy-linux-x64.deb", "arm64_deb": "incy-linux-arm64.deb",
              "x64_rpm": "incy-linux-x64.rpm", "arm64_rpm": "incy-linux-arm64.rpm",
              "x64_arch": "incy-linux-x64.pkg.tar.zst", "x64_portable": "incy-linux-x64-portable.zip",
              "arm64_portable": "incy-linux-arm64-portable.zip"},
}

def android_apk_version(entry):
    match = re.fullmatch(
        rf'https://github\.com/{re.escape(REPO)}/releases/download/android-v(\d+\.\d+\.\d+)/Incy\.apk',
        entry.get('download', ''),
    )
    return match.group(1) if match else None


def update(manifest, release):
    match = re.fullmatch(r"(android|desktop)-v(\d+\.\d+\.\d+)", release["tag_name"])
    if not match or release.get("draft") or release.get("prerelease"):
        raise ValueError("Expected a published stable android-vX.Y.Z or desktop-vX.Y.Z release")
    platform, version = match.groups()
    entry = dict(manifest.get(platform, {}))
    old = entry.get("version", "0.0.0")
    current_versions = [old]
    if platform == 'android' and (apk_version := android_apk_version(entry)):
        current_versions.append(apk_version)
    candidate = tuple(map(int, version.split('.')))
    if any(candidate < tuple(map(int, current.split('.'))) for current in current_versions):
        return {}  # Publishing an older version must not roll back clients or downloads.
    names = {a["name"] for a in release["assets"] if a.get("size", 0) > 0}
    required = {"Incy.apk"} if platform == "android" else {n for group in DESKTOP.values() for n in group.values()}
    if not required <= names:
        raise ValueError(f"Release assets not ready: missing {sorted(required - names)}")
    urls = {n: f"https://github.com/{REPO}/releases/download/{release['tag_name']}/{n}" for n in required}
    # Keep a manually pinned Android announcement when reprocessing the same APK.
    same_android_apk = platform == 'android' and entry.get('download') == urls['Incy.apk']
    entry.update(version=old if same_android_apk and 'version' in entry else version,
                 name=f"INCY {'Android' if platform == 'android' else 'Desktop'} {version}")
    if platform == 'android':
        entry['download'] = urls['Incy.apk']
    else:
        for os_name, assets in DESKTOP.items():
            entry[os_name] = {key: urls[name] for key, name in assets.items()}
    manifest[platform] = entry
    return urls

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('release', type=Path)
    args = parser.parse_args()
    path = Path('RELEASE.json')
    manifest = json.loads(path.read_text())
    payload = json.loads(args.release.read_text())
    releases = payload if isinstance(payload, list) else [payload]
    # Reconcile both channels: GitHub concurrency can replace pending runs.
    # A later event must also include a previously queued platform update.
    newest = {}
    for release in releases:
        match = re.fullmatch(r"(android|desktop)-v(\d+\.\d+\.\d+)", release.get("tag_name", ""))
        if not match or release.get("draft") or release.get("prerelease"):
            continue
        platform, version = match.groups()
        key = tuple(map(int, version.split('.')))
        if platform not in newest or key > newest[platform][0]:
            newest[platform] = (key, release)
    if not newest:
        raise ValueError('No published stable platform release found')
    urls = {}
    for _, release in newest.values():
        urls.update(update(manifest, release))
    if not urls:
        print('Older release: manifest unchanged')
        return
    readme = Path('README.md')
    text = readme.read_text()
    for name, url in urls.items():
        pattern = rf"https://github\.com/{re.escape(REPO)}/releases/(?:latest/download|download/[^/\s)]+)/{re.escape(name)}(?=[\s)\"<>]|$)"
        text = re.sub(pattern, lambda _: f"https://github.com/{REPO}/releases/download/latest/{name}", text)
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    readme.write_text(text)

if __name__ == '__main__':
    main()
