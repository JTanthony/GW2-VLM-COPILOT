import hashlib
import io
import json
from pathlib import Path
import sys
import time
from tempfile import TemporaryDirectory
import threading
import unittest
from unittest.mock import MagicMock,patch
import zipfile

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from waypoint.storage.downloads import (
    Resource, DownloadCancelled, extract_archive, install_resource, safe_path,
)


class Response(io.BytesIO):
    def __init__(self, payload, status=200, headers=None):
        super().__init__(payload)
        self.status=status
        self.headers=headers or {}


def resource(payload, archive=False):
    return Resource('test','Test resource','https://example.com/resource','https://example.com',
                    'runtime.zip' if archive else 'model.gguf',
                    'runtime/test' if archive else 'Models',
                    len(payload),hashlib.sha256(payload).hexdigest(),
                    ('llama-server.exe',) if archive else ())


class DownloadTests(unittest.TestCase):
    def test_setup_downloads_fill_paths_and_save_valid_configuration(self):
        import tkinter as tk
        from waypoint.ui.setup import configure
        with TemporaryDirectory() as temp:
            root_path=Path(temp)
            def install(item,root,cancel,progress):
                target=Path(root)/item.folder/(item.expected[0] if item.expected else item.filename)
                target.parent.mkdir(parents=True,exist_ok=True)
                target.touch()
                progress('Downloading',item.size,item.size)
                return target
            def mainloop(root):
                def widgets(parent):
                    yield parent
                    for child in parent.winfo_children():
                        yield from widgets(child)
                buttons={w.cget('text'):w for w in widgets(root) if isinstance(w,tk.Button)}
                buttons['Download selected'].invoke()
                deadline=time.monotonic()+5
                while str(buttons['Download selected'].cget('state'))=='disabled' and time.monotonic()<deadline:
                    root.update()
                    time.sleep(.01)
                self.assertEqual(str(buttons['Download selected'].cget('state')),'normal')
                buttons['Save and open app'].invoke()
            with patch('waypoint.ui.setup.data_root',return_value=root_path), \
                 patch('waypoint.ui.setup.install_resource',side_effect=install), \
                 patch.object(tk.Tk,'mainloop',mainloop):
                self.assertTrue(configure())
            config=json.loads((root_path/'config/inference.local.json').read_text('utf-8'))
            self.assertEqual(config['model_family'],'gemma')
            self.assertTrue(Path(config['executable']).is_file())
            self.assertTrue(Path(config['model_path']).is_file())
            self.assertTrue(Path(config['projector_path']).is_file())

    def test_download_verifies_and_reuses_existing_model(self):
        payload=b'verified synthetic model'
        item=resource(payload)
        opener=MagicMock()
        opener.open.return_value=Response(payload)
        with TemporaryDirectory() as temp:
            root=Path(temp)
            target=install_resource(item,root,threading.Event(),lambda *args:None,opener)
            self.assertEqual(target.read_bytes(),payload)
            opener.open.reset_mock()
            self.assertEqual(install_resource(item,root,threading.Event(),lambda *args:None,opener),target)
            opener.open.assert_not_called()

    def test_resume_download_and_server_ignoring_range(self):
        payload=b'complete file bytes'
        item=resource(payload)
        for supports_range in (True,False):
            with self.subTest(supports_range=supports_range),TemporaryDirectory() as temp:
                root=Path(temp)
                cache=root/'local-data/resource-downloads'
                cache.mkdir(parents=True)
                (cache/(item.filename+'.part')).write_bytes(payload[:5])
                opener=MagicMock()
                opener.open.return_value=Response(payload[5:] if supports_range else payload,
                    206 if supports_range else 200,
                    {'Content-Range':f'bytes 5-{len(payload)-1}/{len(payload)}'})
                result=install_resource(item,root,threading.Event(),lambda *args:None,opener)
                self.assertEqual(result.read_bytes(),payload)
                self.assertEqual(opener.open.call_args.args[0].get_header('Range'),'bytes=5-')

    def test_checksum_failure_preserves_previous_model(self):
        payload=b'expected'
        item=resource(payload)
        opener=MagicMock();opener.open.return_value=Response(b'corrupt!')
        with TemporaryDirectory() as temp:
            root=Path(temp);target=root/'Models/model.gguf'
            target.parent.mkdir()
            target.write_bytes(b'previous')
            with self.assertRaisesRegex(ValueError,'Checksum verification failed'):
                install_resource(item,root,threading.Event(),lambda *args:None,opener)
            self.assertEqual(target.read_bytes(),b'previous')
            self.assertFalse((root/'local-data/resource-downloads/model.gguf.part').exists())

    def test_cancel_keeps_partial_download_for_retry(self):
        payload=b'x'*(2*1024*1024)
        item=resource(payload)
        cancel=threading.Event()
        opener=MagicMock();opener.open.return_value=Response(payload)
        def progress(phase,completed,total):
            if phase=='Downloading' and completed:
                cancel.set()
        with TemporaryDirectory() as temp:
            root=Path(temp)
            with self.assertRaises(DownloadCancelled):
                install_resource(item,root,cancel,progress,opener)
            self.assertEqual((root/'local-data/resource-downloads/model.gguf.part').stat().st_size,1024*1024)
            self.assertFalse((root/'Models/model.gguf').exists())

    def test_archive_extracts_and_verified_manifest_reuses_installed_files(self):
        stream=io.BytesIO()
        with zipfile.ZipFile(stream,'w') as archive:
            archive.writestr('llama-server.exe',b'synthetic exe')
            archive.writestr('library.dll',b'synthetic dll')
        payload=stream.getvalue();item=resource(payload,archive=True)
        opener=MagicMock();opener.open.return_value=Response(payload)
        with TemporaryDirectory() as temp:
            root=Path(temp)
            target=install_resource(item,root,threading.Event(),lambda *args:None,opener)
            self.assertEqual(target.read_bytes(),b'synthetic exe')
            self.assertEqual((target.parent/'library.dll').read_bytes(),b'synthetic dll')
            opener.open.reset_mock()
            install_resource(item,root,threading.Event(),lambda *args:None,opener)
            opener.open.assert_not_called()
            manifest=json.loads((root/'local-data/resource-downloads/test.json').read_text())
            self.assertEqual(manifest['sha256'],item.sha256)

    def test_archive_traversal_is_rejected_before_publication(self):
        for malicious in ('../outside.exe','C:/outside.exe','/outside.exe','..\\outside.exe'):
            with self.subTest(path=malicious),TemporaryDirectory() as temp:
                root=Path(temp);archive_path=root/'bad.zip'
                with zipfile.ZipFile(archive_path,'w') as archive:
                    archive.writestr('llama-server.exe',b'synthetic exe')
                    archive.writestr(malicious,b'bad')
                with self.assertRaisesRegex(ValueError,'Unsafe resource file path'):
                    extract_archive(resource(archive_path.read_bytes(),True),archive_path,
                                    root/'runtime',root,threading.Event(),lambda *args:None)
                self.assertFalse((root/'runtime').exists())

    def test_lock_is_released_after_failure(self):
        item=resource(b'complete')
        opener=MagicMock();opener.open.side_effect=TimeoutError()
        with TemporaryDirectory() as temp:
            root=Path(temp)
            with self.assertRaises(TimeoutError):
                install_resource(item,root,threading.Event(),lambda *args:None,opener)
            opener.open.side_effect=None;opener.open.return_value=Response(b'complete')
            self.assertTrue(install_resource(item,root,threading.Event(),lambda *args:None,opener).is_file())


if __name__=='__main__':
    unittest.main()
