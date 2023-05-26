import pytest
from src.enums.enums import ErrorMessage


@pytest.mark.parametrize('value, cl, result', [
    ('bvh', str, True),
    ('cdh', int, False),
    (10.0, float, True),
    (10.0, int, False)
])
def test_validator(value, cl, result):
    assert isinstance(value, cl) == result, ErrorMessage.WRONG_INSTANCE_RESULT.value

