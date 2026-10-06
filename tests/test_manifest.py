import copy
import importlib.util
import unittest
from pathlib import Path
spec = importlib.util.spec_from_file_location('manifest', Path(__file__).parents[1] / 'scripts/update_manifest.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class ManifestTest(unittest.TestCase):
    def release(self, tag, names):
        return {'tag_name':tag, 'assets':[{'name':n,'size':1} for n in names]}
    def test_android_leaves_desktop_and_ios_unchanged(self):
        data = {'desktop':{'version':'3.8.8'},'ios':{'version':'2.6.2'}}
        original = copy.deepcopy(data)
        m.update(data, self.release('android-v3.7.0', ['Incy.apk']))
        self.assertEqual(original['desktop'], data['desktop'])
        self.assertEqual(original['ios'], data['ios'])
        self.assertIn('/android-v3.7.0/Incy.apk', data['android']['download'])
    def test_desktop_leaves_android_unchanged(self):
        data = {'android':{'version':'3.7.0','download':'kept'}}
        names = {n for group in m.DESKTOP.values() for n in group.values()}
        m.update(data, self.release('desktop-v3.8.8', names))
        self.assertEqual('kept', data['android']['download'])
        self.assertIn('/desktop-v3.8.8/', data['desktop']['windows']['x64'])
    def test_incomplete_and_wrong_platform_releases_are_rejected(self):
        for tag,names in [('android-v3.7.0',['setup.exe']), ('desktop-v3.8.8',['Incy.apk']), ('v3.7.0',['Incy.apk'])]:
            data = {}
            with self.assertRaises(ValueError):m.update(data,self.release(tag,names))
            self.assertEqual({},data)
    def test_old_release_cannot_downgrade(self):
        data={'android':{'version':'3.8.0'}}
        self.assertEqual({},m.update(data,self.release('android-v3.7.0',['Incy.apk'])))
        self.assertEqual('3.8.0',data['android']['version'])

if __name__ == '__main__':unittest.main()
