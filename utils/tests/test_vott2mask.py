from pathlib import Path

import numpy as np
from PIL import Image
import pytest

from output_processors.vott2mask import vott_to_masks


@pytest.fixture
def vott_json_path():
    return Path('tests/data/test-export.json')


@pytest.mark.parametrize('expected_image_path', [
    Path('tests/data/mailbox1.png'),
    Path('tests/data/pencil1.png'),
    Path('tests/data/pencil2.png')
])
def test_vott_to_masks(tmp_path, vott_json_path, expected_image_path):
    vott_to_masks(annotation_file=vott_json_path, mask_dir=tmp_path)
    expected_image = np.array(Image.open(expected_image_path))
    actual_image = np.array(Image.open(tmp_path / expected_image_path.name))
    assert not np.any(expected_image - actual_image)


# def test_get_args():
#     return