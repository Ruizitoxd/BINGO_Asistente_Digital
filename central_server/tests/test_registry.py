import pytest

from app.core.module import BingoModule
from app.core.registry import ModuleRegistry


class FakeModule(BingoModule):
    def __init__(self, name, fail=False):
        self._name, self.fail = name, fail
        self.started = False
        self.stopped = False

    @property
    def name(self):
        return self._name

    async def initialize(self):
        if self.fail:
            raise RuntimeError("initialization failed")
        self.started = True

    def get_tools(self):
        return []

    async def shutdown(self):
        self.stopped = True


def test_register_and_list():
    registry = ModuleRegistry()
    registry.register(FakeModule("zeta"))
    registry.register(FakeModule("alpha"))
    assert registry.list_modules() == ["alpha", "zeta"]


def test_duplicate_rejected():
    registry = ModuleRegistry()
    registry.register(FakeModule("alpha"))
    with pytest.raises(ValueError):
        registry.register(FakeModule("alpha"))


def test_unknown_module():
    with pytest.raises(KeyError):
        ModuleRegistry().get("missing")


@pytest.mark.asyncio
async def test_lifecycle():
    registry = ModuleRegistry()
    first, second = FakeModule("first"), FakeModule("second")
    registry.register(first)
    registry.register(second)
    await registry.initialize_all()
    assert first.started and second.started
    await registry.shutdown_all()
    assert first.stopped and second.stopped


@pytest.mark.asyncio
async def test_failed_init_rolls_back_previous_modules():
    registry = ModuleRegistry()
    first, failing = FakeModule("first"), FakeModule("failing", fail=True)
    registry.register(first)
    registry.register(failing)
    with pytest.raises(RuntimeError):
        await registry.initialize_all()
    assert first.stopped
