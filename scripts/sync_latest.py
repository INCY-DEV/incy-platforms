"""Mirror validated platform releases into the stable `latest` download tag."""
import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path

from update_manifest import DESKTOP, REPO


def gh(*args):
    return subprocess.check_output(['gh', *args], text=True)


def plan(manifest, read_release):
    result = []
    for platform in ('desktop', 'android'):
        version = manifest[platform]['version']
        if not re.fullmatch(r'\d+\.\d+\.\d+', version):
            raise ValueError('Invalid platform version')
        tag = f'{platform}-v{version}'
        release = read_release(tag)
        if release.get('draft') or release.get('prerelease') or release['tag_name'] != tag:
            raise ValueError(f'Not a published stable release: {tag}')
        names = {'Incy.apk'} if platform == 'android' else {n for group in DESKTOP.values() for n in group.values()}
        assets = {a['name']: a for a in release['assets'] if a.get('size', 0) > 0}
        if not names <= assets.keys():
            raise ValueError(f'Incomplete release {tag}: {sorted(names - assets.keys())}')
        result.append((tag, {name: assets[name] for name in sorted(names)}))
    return result


def verify(path, asset):
    if path.stat().st_size != asset['size']:
        raise ValueError(f'Asset size mismatch: {path.name}')
    checksum = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            checksum.update(chunk)
    digest = checksum.hexdigest()
    expected = asset.get('digest')
    if expected and expected != f'sha256:{digest}':
        raise ValueError(f'Asset digest mismatch: {path.name}')
    return digest


def main():
    manifest = json.loads(Path('RELEASE.json').read_text())
    releases = plan(manifest, lambda tag: json.loads(gh('api', f'repos/{REPO}/releases/tags/{tag}')))
    with tempfile.TemporaryDirectory(prefix='incy-latest-') as directory:
        root = Path(directory)
        paths, sums = [], []
        # Download and verify BOTH channels before touching the shared release.
        for tag, assets in releases:
            dest = root / tag
            dest.mkdir()
            patterns = [arg for name in assets for arg in ('--pattern', name)]
            gh('release', 'download', tag, '--repo', REPO, '--dir', str(dest), *patterns)
            for name, asset in assets.items():
                path = dest / name
                sums.append(f'{verify(path, asset)}  {name}')
                paths.append(str(path))
        checksums = root / 'SHA256SUMS'
        checksums.write_text('\n'.join(sorted(sums)) + '\n')
        paths.append(str(checksums))
        notes = root / 'notes.md'
        notes.write_text(
            f"Latest stable downloads: Desktop **{manifest['desktop']['version']}**, "
            f"Android **{manifest['android']['version']}**.\n\n"
            'Permanent download tag; files are updated independently by platform. '
            'For version history and Obtainium use `desktop-v*` / `android-v*` releases.\n'
        )
        # Listing distinguishes a missing tag from authentication/network errors.
        existing = json.loads(gh('api', f'repos/{REPO}/releases?per_page=100', '--paginate', '--slurp'))
        latest = next((r for page in existing for r in page if r['tag_name'] == 'latest'), None)
        if latest:
            gh('release', 'upload', 'latest', *paths, '--repo', REPO, '--clobber')
            gh('release', 'edit', 'latest', '--repo', REPO, '--title', 'INCY — Latest downloads',
               '--notes-file', str(notes), '--draft=false', '--prerelease=false', '--latest')
        else:
            gh('release', 'create', 'latest', *paths, '--repo', REPO, '--target', 'main',
               '--title', 'INCY — Latest downloads', '--notes-file', str(notes), '--latest')
        published = json.loads(gh('api', f'repos/{REPO}/releases/tags/latest'))
        actual = {a['name']: a for a in published['assets']}
        for file in paths:
            path = Path(file)
            verify(path, actual[path.name])
        print('latest verified: ' + ', '.join(tag for tag, _ in releases))


if __name__ == '__main__':
    main()
