import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from sync_latest import DESKTOP, plan, verify


class LatestTest(unittest.TestCase):
    def fixture(self):
        manifest = {'desktop': {'version': '3.9.0'}, 'android': {'version': '3.7.9'}}
        desktop = {n for group in DESKTOP.values() for n in group.values()}
        releases = {tag: {'tag_name': tag, 'assets': [{'name': n, 'size': 3} for n in names]}
                    for tag, names in [('desktop-v3.9.0', desktop), ('android-v3.7.9', {'Incy.apk'})]}
        return manifest, releases

    def test_combines_complete_independent_channels(self):
        manifest, releases = self.fixture()
        result = plan(manifest, releases.__getitem__)
        self.assertEqual([tag for tag, _ in result], ['desktop-v3.9.0', 'android-v3.7.9'])
        self.assertEqual(len(result[0][1]), 11)
        self.assertEqual(set(result[1][1]), {'Incy.apk'})

    def test_rejects_partial_draft_and_prerelease_before_publication(self):
        for kind in ['missing', 'draft', 'prerelease']:
            manifest, releases = self.fixture()
            release = releases['desktop-v3.9.0']
            if kind == 'missing':
                release['assets'].pop()
            else:
                release[kind] = True
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                plan(manifest, releases.__getitem__)

    def test_asset_integrity(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp, 'Incy.apk')
            path.write_bytes(b'apk')
            digest = hashlib.sha256(b'apk').hexdigest()
            self.assertEqual(verify(path, {'size': 3, 'digest': 'sha256:' + digest}), digest)
            for asset in [{'size': 4}, {'size': 3, 'digest': 'sha256:incorrect'}]:
                with self.assertRaises(ValueError):
                    verify(path, asset)

    def test_manifest_stays_pinned_but_readme_stays_latest_after_updates(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            root.joinpath('RELEASE.json').write_text('{"desktop":{"version":"3.9.0"}}')
            root.joinpath('README.md').write_text('[APK](https://github.com/INCY-DEV/incy-platforms/releases/download/android-v3.7.0/Incy.apk)')
            release = root / 'event.json'
            for version in ['3.7.9', '3.8.0']:
                release.write_text(json.dumps({'tag_name': f'android-v{version}', 'assets': [{'name': 'Incy.apk', 'size': 3}]}))
                subprocess.run([sys.executable, str(ROOT / 'scripts/update_manifest.py'), str(release)], cwd=root, check=True)
                self.assertIn('/download/latest/Incy.apk', root.joinpath('README.md').read_text())
                manifest = json.loads(root.joinpath('RELEASE.json').read_text())
                self.assertIn(f'/android-v{version}/', manifest['android']['download'])
                self.assertEqual(manifest['desktop']['version'], '3.9.0')


if __name__ == '__main__':
    unittest.main()
