from __future__ import annotations

from operator import neg
from typing import List
from typing import Tuple

from hypothesis.strategies import integers
from hypothesis.strategies import lists

from functional_itertools import CIterable
from tests import given
from tests import parametrize
from tests.strategies import Case
from tests.strategies import CASES


@given(
    x=lists(
        lists(integers(), min_size=1, max_size=10).map(tuple),
        min_size=1,
        max_size=10,
    ),
)
@parametrize("case", CASES)
def test_map_nested(x: List[Tuple[int, ...]], case: Case) -> None:
    y = case.cls(x).map(_parallel_map_neg, parallel=True, processes=1)
    assert isinstance(y, case.cls)
    assert case.cast(y) == case.cast(max(map(neg, x_i)) for x_i in case.cast(x))


def _parallel_map_neg(x: List[int]) -> int:
    return CIterable(x).map(neg, parallel=True, processes=1).max()
