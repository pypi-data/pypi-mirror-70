from __future__ import annotations

from typing import Generic, Type, TypeVar

from ._cdata import CData
from ._ffi import ffi, lib
from ._state import State

__all__ = ["Step"]

T = TypeVar("T", bound=State)


class Step(Generic[T]):
    """
    Path step.

    A step is composed of a state and an emitted sequence length. The user should not need to
    directly call the constructor of this class but instead use the methods from the `Path` class.

    Parameters
    ----------
    imm_step
        Step pointer.
    state
        State.
    """

    def __init__(self, imm_step: CData, state: T):
        if imm_step == ffi.NULL:
            raise RuntimeError("`imm_step` is NULL.")
        self._imm_step = imm_step
        self._state = state

    @classmethod
    def create(cls: Type[Step], state: T, seq_len: int) -> Step:
        """
        Create a path step.

        Parameters
        ----------
        state
            State.
        seq_len
            Sequence length.
        """
        imm_step = lib.imm_step_create(state.imm_state, seq_len)
        if imm_step == ffi.NULL:
            raise RuntimeError("Could not create step.")
        return cls(imm_step, state)

    @property
    def imm_step(self) -> CData:
        return self._imm_step

    @property
    def state(self) -> T:
        return self._state

    @property
    def seq_len(self) -> int:
        return lib.imm_step_seq_len(self.imm_step)

    def __del__(self):
        if self._imm_step != ffi.NULL:
            lib.imm_step_destroy(self._imm_step)

    def __str__(self) -> str:
        state = lib.imm_step_state(self._imm_step)
        name: str = ffi.string(lib.imm_state_get_name(state)).decode()
        return f"<{name},{self.seq_len}>"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}:{str(self)}>"
