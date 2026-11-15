"""Release OCR setup and runtime stay independent of developer recording/tools."""
import json,sys,unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from waypoint.ui.setup import setup_values
from waypoint.ocr.qwen import profile


class ReleaseOCRTests(unittest.TestCase):
    def test_packaged_recording_argument_is_rejected_before_setup(self):
        from tools.run_gui import launch
        with patch.object(sys,'frozen',True,create=True),patch.object(sys,'argv',['App.exe','--vision-review']),patch('waypoint.ui.setup.configure') as setup:
            with self.assertRaises(SystemExit) as result:launch()
        self.assertEqual(result.exception.code,2);setup.assert_not_called()

    def files(self,root):
        (root/'llama-server.exe').touch();(root/'model.gguf').touch()
        return {'executable':str(root/'llama-server.exe'),'model_path':str(root/'model.gguf')}

    def test_qwen_setup_does_not_require_a_gemma_model_or_projector(self):
        with TemporaryDirectory() as folder:
            root=Path(folder);values=self.files(root)
            (root/'ocr/tessdata').mkdir(parents=True);(root/'ocr/tesseract.exe').touch();(root/'ocr/tessdata/eng.traineddata').touch()
            values.update(ocr_folder=str(root/'ocr'),projector_path='missing-gemma-projector.gguf')
            config,settings=setup_values(values,'qwen')
            self.assertNotIn('projector_path',config);self.assertEqual(settings['selected_model'],'qwen')
            (root/'config').mkdir();(root/'config/inference.local.json').write_text(json.dumps(config),encoding='utf-8')
            self.assertEqual(profile(root)['model_path'],values['model_path'])

    def test_qwen_setup_requires_installed_english_ocr_data(self):
        with TemporaryDirectory() as folder:
            root=Path(folder);values=self.files(root);values['ocr_folder']=folder
            (root/'tesseract.exe').touch()
            with self.assertRaisesRegex(ValueError,'eng.traineddata'):setup_values(values,'qwen')

    def test_gemma_chat_setup_does_not_require_tesseract(self):
        with TemporaryDirectory() as folder:
            config,settings=setup_values(self.files(Path(folder)),'gemma')
            self.assertNotIn('ocr_executable',settings);self.assertNotIn('projector_path',config)

    def test_gemma_vision_companion_is_retained(self):
        with TemporaryDirectory() as folder:
            root=Path(folder);values=self.files(root);(root/'companion.gguf').touch()
            values['projector_path']=str(root/'companion.gguf')
            config,settings=setup_values(values,'gemma')
            self.assertEqual(config['projector_path'],values['projector_path'])
            self.assertEqual(settings['gemma_projector_path'],values['projector_path'])

    def test_legacy_source_imports_alias_the_runtime_not_a_second_implementation(self):
        from waypoint.experiments.ocr_landmarks import reader,qwen,nearby
        from waypoint.ocr import reader as runtime_reader,qwen as runtime_qwen,nearby as runtime_nearby
        self.assertIs(reader,runtime_reader);self.assertIs(qwen,runtime_qwen);self.assertIs(nearby,runtime_nearby)


if __name__=='__main__':unittest.main()
