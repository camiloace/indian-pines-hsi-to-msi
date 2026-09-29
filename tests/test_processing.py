import unittest
from pathlib import Path
import numpy as np
from hsi_processing import standard_channels, wavelengths, aggregate_bands, spatial_features, normalize_image

class ProcessingTests(unittest.TestCase):
    def test_alignment_and_missing_cirrus(self):
        ids = standard_channels(200)
        self.assertEqual(len(ids), 200)
        self.assertEqual(ids[102:105].tolist(), [103,109,110])
        wave = wavelengths(Path(__file__).resolve().parents[1]/'data/wavelenght.csv', ids)
        cube = np.broadcast_to(wave, (2,3,200))
        with self.assertRaisesRegex(ValueError, 'B9'):
            aggregate_bands(cube, wave)
        out, records = aggregate_bands(cube, wave, missing='skip')
        self.assertEqual(out.shape, (2,3,8))
        self.assertFalse(records[-1]['included'])
        self.assertAlmostEqual(out[0,0,0], (439.25+449.07)/2)

    def test_full_cube_has_nine_intervals(self):
        ids=standard_channels(220)
        wave=wavelengths(Path(__file__).resolve().parents[1]/'data/wavelenght.csv',ids)
        out, records=aggregate_bands(np.broadcast_to(wave,(2,3,220)),wave)
        self.assertEqual(out.shape,(2,3,9))
        self.assertEqual(records[-1]['count'],3)

    def test_constant_input(self):
        cube=np.full((12,12,2),7.)
        e,m=spatial_features(cube, area_threshold=4)
        np.testing.assert_array_equal(e,np.zeros_like(cube))
        np.testing.assert_array_equal(m,cube)
        np.testing.assert_array_equal(normalize_image(cube),np.zeros_like(cube))

    def test_bad_alignment_rejected(self):
        with self.assertRaises(ValueError):
            aggregate_bands(np.ones((2,3,200)),np.arange(201))

if __name__=='__main__': unittest.main()
