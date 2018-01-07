import json
import unittest
from typing import Sequence, List, Any, Tuple

import requests
from PIL import Image

import core

MultipleSizesImage = Tuple[type(Image), type(Image), type(Image)]

class SanityCheckTest(unittest.TestCase):
    def setUp(self):
        self.sanity_check()

    def assertNotEmpty(self, obj: Sequence) -> None:
        """Confirma se uma sequencia não está vazia"""
        self.assertGreater(len(obj), 0)

    def sanity_check(self):
        """confirma as condições ideais para o servidor de imagens remoto"""
        r = requests.get('http://54.152.221.29/images.json')  # type: requests.Response
        self.assertEqual(r.status_code, 200)
        self.assertIn('content-type', r.headers)
        self.assertRegex(r.headers['content-type'], r'application/json')
        self.assertNotEmpty(r.text)

        j = json.loads(r.text)
        self.assertNotEmpty(j)
        self.assertIn('images', j)
        r.close()

        imgs = j['images']  # type: List[Any]
        for img in imgs:
            self.assertNotEmpty(img)
            self.assertIn('url', img)
            self.assertNotEmpty(img['url'])
            r = requests.get(img['url'])  # type: requests.Response
            self.assertEqual(r.status_code, 200)
            self.assertIn('content-type', r.headers)
            self.assertRegex(r.headers['content-type'], r'image/jpeg')
            r.close()

    """
    Testa todo o processo de download dos arquivos originais, redimensionando-os e persistiendo em Mongo
    """
    def test_whole_process(self):


        # Download das imagens
        imgs = list(core.download_originals())  # type: List[type(Image)]
        self.assertGreater(len(imgs), 0)

        # Redimensiona as imagens
        resized_imgs = [core.resize_image(img) for img in imgs]  # type: List[MultipleSizesImage]
        self.assertEqual(len(resized_imgs), len(imgs))
        for small, medium, large in resized_imgs:
            self.assertTupleEqual((320, 240), small.size)
            self.assertTupleEqual((384, 288), medium.size)
            self.assertTupleEqual((640, 480), large.size)

        # Persiste as imagens no banco
        for small, medium, large in resized_imgs:
            self.assertTrue(core.persist_image(small))
            self.assertTrue(core.grid.exists(filename=small.filename))
            self.assertTrue(core.persist_image(medium))
            self.assertTrue(core.grid.exists(filename=medium.filename))
            self.assertTrue(core.persist_image(large))
            self.assertTrue(core.grid.exists(filename=large.filename))

        self.assertEqual(len(core.grid.list()), 3 * len(resized_imgs))


if __name__ == '__main__':
    unittest.main()