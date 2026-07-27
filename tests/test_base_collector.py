import pytest

from src.collectors.base import BaseCollector


def test_base_collector_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError):
        BaseCollector()
