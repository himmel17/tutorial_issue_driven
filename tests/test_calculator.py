import pytest

from calculator import add, multiply, subtract


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [(2, 3, 5), (-2, 3, 1), (0, 0, 0), (0.1, 0.2, 0.3)],
)
def test_add(a, b, expected):
    assert add(a, b) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [(5, 3, 2), (2, 5, -3), (-2, -3, 1), (0.3, 0.1, 0.2)],
)
def test_subtract(a, b, expected):
    assert subtract(a, b) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [(2, 3, 6), (-2, 3, -6), (5, 0, 0), (0.1, 0.2, 0.02)],
)
def test_multiply(a, b, expected):
    assert multiply(a, b) == pytest.approx(expected)
