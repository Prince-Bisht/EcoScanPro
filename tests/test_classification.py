import pytest
from services.image_processing import prepare
def test_corrupt_image():
    with pytest.raises(ValueError): prepare(b'not an image')
