import sys,json,unittest
from pathlib import Path
from unittest.mock import MagicMock
import cv2,numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from waypoint.inference.validation import validate_observation,BACKGROUND_SCHEMA,OBSERVATION_SCHEMA
from waypoint.assistant.local import Assistant
from waypoint.testing.vision_inputs import crop_panel

def observation():
    return dict(map='null',event=None,objective=None,timer='unknown',player_status='null',
        visible_text=['Crystal Oasis','Crystal Oasis','Map displayed: null','Story episode: null'],
        warnings=[],summary='Map view.',confidence=.9,needs_reasoning=True)

class VisionFocusTests(unittest.TestCase):
    def test_placeholders_and_repeated_text_do_not_become_evidence(self):
        result=validate_observation(json.dumps(observation()))
        self.assertIsNone(result['map']);self.assertIsNone(result['timer'])
        self.assertEqual(result['visible_text'],['Crystal Oasis'])

    def test_background_schema_is_bounded_and_separate_from_manual_questions(self):
        client=MagicMock(); client.complete.return_value=json.dumps(observation())
        assistant=Assistant(client)
        assistant.observe(b'fixture',background=True)
        options=client.complete.call_args.kwargs
        self.assertEqual(options['max_tokens'],384)
        self.assertEqual(options['schema']['properties']['warnings']['maxItems'],0)
        self.assertEqual(BACKGROUND_SCHEMA['properties']['visible_text']['maxItems'],8)
        assistant.observe(b'fixture',background=True,question='Read my gold balance')
        self.assertEqual(client.complete.call_args.kwargs['max_tokens'],512)
        self.assertEqual(OBSERVATION_SCHEMA['properties']['warnings']['maxItems'],30)

    def test_crop_preserves_native_text_pixels_without_resizing(self):
        image=np.zeros((1000,2000,3),dtype=np.uint8);image[10,10]=[17,23,42]
        png=cv2.imencode('.png',image)[1].tobytes()
        cropped=cv2.imdecode(np.frombuffer(crop_panel(png,'map'),dtype=np.uint8),cv2.IMREAD_COLOR)
        self.assertEqual(cropped.shape,(230,600,3))
        self.assertEqual(cropped[10,10].tolist(),[17,23,42])
        with self.assertRaises(ValueError):crop_panel(png,'unknown')
        with self.assertRaises(ValueError):crop_panel(b'invalid','map')
