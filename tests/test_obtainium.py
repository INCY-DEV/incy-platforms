import json
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).parents[1]
class ObtainiumConfigTest(unittest.TestCase):
    def test_import_schema_and_filters_exclude_legacy_mixed_desktop_releases(self):
        app=json.loads((ROOT/'obtainium.json').read_text())[0]
        self.assertEqual('llc.itdev.incy',app['id'])
        settings=json.loads(app['additionalSettings'])
        title=re.compile(settings['filterReleaseTitlesByRegEx'])
        self.assertIsNotNone(title.search('Android v3.7.0'))
        self.assertIsNone(title.search('Desktop v3.8.8'))
        self.assertIsNone(title.search('Desktop v3.8.6'))
        self.assertFalse(settings['verifyLatestTag'])
        self.assertTrue(settings['fallbackToOlderReleases'])
        apk=re.compile(settings['apkFilterRegEx'])
        self.assertIsNotNone(apk.search('Incy.apk'))
        self.assertIsNone(apk.search('incy-windows-setup.exe'))
        self.assertIsNone(apk.search('another.apk'))
        self.assertEqual('3.7.0',re.search(settings['versionExtractionRegEx'],'android-v3.7.0')[0])
