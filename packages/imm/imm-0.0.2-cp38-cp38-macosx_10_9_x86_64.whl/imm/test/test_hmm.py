from math import log

import pytest

from imm import (
    HMM,
    Alphabet,
    MuteState,
    NormalState,
    Path,
    Sequence,
    SequenceTable,
    Step,
    TableState,
    lprob_invalid,
    lprob_zero,
)
from imm.testing import assert_allclose


def test_hmm_states():
    alphabet = Alphabet.create(b"ACGU", b"X")
    hmm = HMM.create(alphabet)

    S = MuteState.create(b"S", alphabet)
    hmm.add_state(S)

    seqt = SequenceTable.create(alphabet)
    seqt.add(Sequence.create(b"AGU", alphabet), log(0.8))
    seqt.add(Sequence.create(b"AGG", alphabet), log(0.2))

    M = TableState.create(b"M", seqt)
    hmm.add_state(M)

    with pytest.raises(ValueError):
        hmm.add_state(S)

    with pytest.raises(ValueError):
        hmm.add_state(M)

    assert len(hmm.states()) == 2


def test_hmm_trans_prob():
    alphabet = Alphabet.create(b"ACGU", b"X")
    hmm = HMM.create(alphabet)

    S = MuteState.create(b"S", alphabet)
    with pytest.raises(RuntimeError):
        hmm.set_start_lprob(S, log(0.4))
    hmm.add_state(S)

    E = MuteState.create(b"E", alphabet)
    with pytest.raises(RuntimeError):
        hmm.transition(S, E)

    with pytest.raises(ValueError):
        hmm.set_transition(S, E, lprob_zero())

    with pytest.raises(ValueError):
        hmm.set_transition(E, S, lprob_zero())

    with pytest.raises(ValueError):
        hmm.del_state(E)

    hmm.add_state(E)

    with pytest.raises(RuntimeError):
        hmm.set_transition(E, S, lprob_invalid())

    with pytest.raises(ValueError):
        hmm.normalize()

    hmm.set_transition(S, E, log(0.5))

    assert_allclose(hmm.transition(S, S), lprob_zero())
    assert_allclose(hmm.transition(S, E), log(0.5))
    assert_allclose(hmm.transition(E, S), lprob_zero())
    assert_allclose(hmm.transition(E, E), lprob_zero())

    with pytest.raises(ValueError):
        hmm.normalize()

    with pytest.raises(ValueError):
        hmm.normalize()

    hmm.set_start_lprob(S, log(0.4))
    hmm.set_transition(E, E, log(0.1))

    hmm.normalize()

    assert_allclose(hmm.transition(S, E), log(1.0))
    assert_allclose(hmm.transition(E, S), lprob_zero())
    assert_allclose(hmm.transition(S, S), lprob_zero())
    assert_allclose(hmm.transition(E, E), log(1.0))


def test_hmm_likelihood():
    alphabet = Alphabet.create(b"ACGU", b"X")
    hmm = HMM.create(alphabet)

    S = MuteState.create(b"S", alphabet)
    hmm.add_state(S, log(1.0))

    E = MuteState.create(b"E", alphabet)
    hmm.add_state(E, lprob_zero())

    M1 = NormalState.create(
        b"M1", alphabet, [log(0.8), log(0.2), lprob_zero(), lprob_zero()],
    )
    hmm.add_state(M1, lprob_zero())

    M2 = NormalState.create(
        b"M2", alphabet, [log(0.4 / 1.6), log(0.6 / 1.6), lprob_zero(), log(0.6 / 1.6)]
    )
    hmm.add_state(M2, lprob_zero())

    hmm.set_transition(S, M1, log(1.0))
    hmm.set_transition(M1, M2, log(1.0))
    hmm.set_transition(M2, E, log(1.0))
    hmm.set_transition(E, E, log(1.0))
    hmm.normalize()

    p = hmm.likelihood(
        Sequence.create(b"AC", alphabet),
        Path.create(
            [
                Step.create(S, 0),
                Step.create(M1, 1),
                Step.create(M2, 1),
                Step.create(E, 0),
            ]
        ),
    )
    assert_allclose(p, log(0.3))

    p = hmm.likelihood(
        Sequence.create(b"AA", alphabet),
        Path.create(
            [
                Step.create(S, 0),
                Step.create(M1, 1),
                Step.create(M2, 1),
                Step.create(E, 0),
            ]
        ),
    )
    assert_allclose(p, log(0.2))

    p = hmm.likelihood(
        Sequence.create(b"AG", alphabet),
        Path.create(
            [
                Step.create(S, 0),
                Step.create(M1, 1),
                Step.create(M2, 1),
                Step.create(E, 0),
            ]
        ),
    )
    assert_allclose(p, lprob_zero())

    p = hmm.likelihood(
        Sequence.create(b"AU", alphabet),
        Path.create(
            [
                Step.create(S, 0),
                Step.create(M1, 1),
                Step.create(M2, 1),
                Step.create(E, 0),
            ]
        ),
    )
    assert_allclose(p, log(0.3))

    p = hmm.likelihood(
        Sequence.create(b"CC", alphabet),
        Path.create(
            [
                Step.create(S, 0),
                Step.create(M1, 1),
                Step.create(M2, 1),
                Step.create(E, 0),
            ]
        ),
    )
    assert_allclose(p, log(0.075))

    p = hmm.likelihood(
        Sequence.create(b"CA", alphabet),
        Path.create(
            [
                Step.create(S, 0),
                Step.create(M1, 1),
                Step.create(M2, 1),
                Step.create(E, 0),
            ]
        ),
    )
    assert_allclose(p, log(0.05))

    p = hmm.likelihood(
        Sequence.create(b"CG", alphabet),
        Path.create(
            [
                Step.create(S, 0),
                Step.create(M1, 1),
                Step.create(M2, 1),
                Step.create(E, 0),
            ]
        ),
    )
    assert_allclose(p, lprob_zero())

    p = hmm.likelihood(
        Sequence.create(b"CG", alphabet),
        Path.create(
            [
                Step.create(S, 0),
                Step.create(M1, 1),
                Step.create(M2, 1),
                Step.create(E, 0),
            ]
        ),
    )
    assert_allclose(p, lprob_zero())

    p = hmm.likelihood(
        Sequence.create(b"CU", alphabet),
        Path.create(
            [
                Step.create(S, 0),
                Step.create(M1, 1),
                Step.create(M2, 1),
                Step.create(E, 0),
            ]
        ),
    )
    assert_allclose(p, log(0.075))

    p = hmm.likelihood(
        Sequence.create(b"GC", alphabet),
        Path.create(
            [
                Step.create(S, 0),
                Step.create(M1, 1),
                Step.create(M2, 1),
                Step.create(E, 0),
            ]
        ),
    )
    assert_allclose(p, lprob_zero())

    p = hmm.likelihood(
        Sequence.create(b"GA", alphabet),
        Path.create(
            [
                Step.create(S, 0),
                Step.create(M1, 1),
                Step.create(M2, 1),
                Step.create(E, 0),
            ]
        ),
    )
    assert_allclose(p, lprob_zero())

    p = hmm.likelihood(
        Sequence.create(b"GG", alphabet),
        Path.create(
            [
                Step.create(S, 0),
                Step.create(M1, 1),
                Step.create(M2, 1),
                Step.create(E, 0),
            ]
        ),
    )
    assert_allclose(p, lprob_zero())

    p = hmm.likelihood(
        Sequence.create(b"GU", alphabet),
        Path.create(
            [
                Step.create(S, 0),
                Step.create(M1, 1),
                Step.create(M2, 1),
                Step.create(E, 0),
            ]
        ),
    )
    assert_allclose(p, lprob_zero())

    p = hmm.likelihood(
        Sequence.create(b"UC", alphabet),
        Path.create(
            [
                Step.create(S, 0),
                Step.create(M1, 1),
                Step.create(M2, 1),
                Step.create(E, 0),
            ]
        ),
    )
    assert_allclose(p, lprob_zero())

    p = hmm.likelihood(
        Sequence.create(b"UA", alphabet),
        Path.create(
            [
                Step.create(S, 0),
                Step.create(M1, 1),
                Step.create(M2, 1),
                Step.create(E, 0),
            ]
        ),
    )
    assert_allclose(p, lprob_zero())

    p = hmm.likelihood(
        Sequence.create(b"UG", alphabet),
        Path.create(
            [
                Step.create(S, 0),
                Step.create(M1, 1),
                Step.create(M2, 1),
                Step.create(E, 0),
            ]
        ),
    )
    assert_allclose(p, lprob_zero())

    p = hmm.likelihood(
        Sequence.create(b"UU", alphabet),
        Path.create(
            [
                Step.create(S, 0),
                Step.create(M1, 1),
                Step.create(M2, 1),
                Step.create(E, 0),
            ]
        ),
    )
    assert_allclose(p, lprob_zero())

    M3 = NormalState.create(
        b"M2", alphabet, [log(0.4), log(0.6), lprob_zero(), log(0.6)],
    )

    with pytest.raises(ValueError):
        hmm.likelihood(
            Sequence.create(b"UU", alphabet),
            Path.create(
                [
                    Step.create(S, 0),
                    Step.create(M1, 1),
                    Step.create(M3, 1),
                    Step.create(E, 0),
                ]
            ),
        )


def test_hmm_viterbi_1():
    alphabet = Alphabet.create(b"ACGU", b"X")
    hmm = HMM.create(alphabet)

    S = MuteState.create(b"S", alphabet)
    hmm.add_state(S, log(1.0))

    E = MuteState.create(b"E", alphabet)
    hmm.add_state(E, lprob_zero())

    M1 = NormalState.create(
        b"M1", alphabet, [log(0.8), log(0.2), lprob_zero(), lprob_zero()],
    )
    hmm.add_state(M1, lprob_zero())

    M2 = NormalState.create(
        b"M2", alphabet, [log(0.4 / 1.6), log(0.6 / 1.6), lprob_zero(), log(0.6 / 1.6)],
    )
    hmm.add_state(M2, lprob_zero())

    hmm.set_transition(S, M1, log(1.0))
    hmm.set_transition(M1, M2, log(1.0))
    hmm.set_transition(M2, E, log(1.0))
    hmm.set_transition(E, E, log(1.0))
    hmm.normalize()

    hmm.set_transition(E, E, lprob_zero())
    assert_allclose(hmm.transition(E, E), lprob_zero())
    assert_allclose(hmm.transition(S, S), lprob_zero())
    assert_allclose(hmm.transition(S, E), lprob_zero())
    assert_allclose(hmm.transition(E, S), lprob_zero())

    dp = hmm.create_dp(E)
    results = dp.viterbi(Sequence.create(b"AC", alphabet))
    assert len(results) == 1
    assert_allclose(results[0].loglikelihood, log(0.3))


def test_hmm_viterbi_2():
    alphabet = Alphabet.create(b"AC", b"X")
    hmm = HMM.create(alphabet)

    S = MuteState.create(b"S", alphabet)
    hmm.add_state(S, log(1.0))

    E = MuteState.create(b"E", alphabet)
    hmm.add_state(E, lprob_zero())

    M1 = NormalState.create(b"M1", alphabet, [log(0.8), log(0.2)])
    hmm.add_state(M1, lprob_zero())

    M2 = NormalState.create(b"M2", alphabet, [log(0.4), log(0.6)])
    hmm.add_state(M2, lprob_zero())

    hmm.set_transition(S, M1, log(1.0))
    hmm.set_transition(M1, M2, log(1.0))
    hmm.set_transition(M2, E, log(1.0))
    hmm.set_transition(E, E, log(1.0))
    hmm.normalize()
    hmm.set_transition(E, E, lprob_zero())

    dp = hmm.create_dp(E)
    score = dp.viterbi(Sequence.create(b"AC", alphabet))[0].loglikelihood
    assert_allclose(score, log(0.48))

    score = dp.viterbi(Sequence.create(b"AA", alphabet))[0].loglikelihood
    assert_allclose(score, log(0.32))

    score = dp.viterbi(Sequence.create(b"CA", alphabet))[0].loglikelihood
    assert_allclose(score, log(0.08))

    score = dp.viterbi(Sequence.create(b"CC", alphabet))[0].loglikelihood
    assert_allclose(score, log(0.12))

    hmm.set_transition(M1, E, log(1.0))

    dp = hmm.create_dp(E)
    score = dp.viterbi(Sequence.create(b"AC", alphabet))[0].loglikelihood
    assert_allclose(score, log(0.48))

    score = dp.viterbi(Sequence.create(b"AA", alphabet))[0].loglikelihood
    assert_allclose(score, log(0.32))


def test_hmm_viterbi_3():
    alphabet = Alphabet.create(b"AC", b"X")
    hmm = HMM.create(alphabet)

    S = MuteState.create(b"S", alphabet)
    hmm.add_state(S, log(1.0))

    E = MuteState.create(b"E", alphabet)
    hmm.add_state(E, lprob_zero())

    M1 = NormalState.create(b"M1", alphabet, [log(0.8), log(0.2)])
    hmm.add_state(M1, lprob_zero())

    D1 = MuteState.create(b"D1", alphabet)
    hmm.add_state(D1, lprob_zero())

    M2 = NormalState.create(b"M2", alphabet, [log(0.4), log(0.6)])
    hmm.add_state(M2, lprob_zero())

    D2 = MuteState.create(b"D2", alphabet)
    hmm.add_state(D2, lprob_zero())

    hmm.set_transition(S, M1, log(0.8))
    hmm.set_transition(S, D1, log(0.2))

    hmm.set_transition(M1, M2, log(0.8))
    hmm.set_transition(M1, D2, log(0.2))

    hmm.set_transition(D1, D2, log(0.2))
    hmm.set_transition(D1, M2, log(0.8))

    hmm.set_transition(D2, E, log(1.0))
    hmm.set_transition(M2, E, log(1.0))
    hmm.set_transition(E, E, log(1.0))
    hmm.normalize()
    hmm.set_transition(E, E, lprob_zero())

    dp = hmm.create_dp(E)
    results = dp.viterbi(Sequence.create(b"AC", alphabet))
    score = results[0].loglikelihood
    assert bytes(results[0].sequence) == b"AC"
    path = results[0].path
    steps = list(path)
    assert steps[0].seq_len == 0
    assert steps[1].seq_len == 1
    assert steps[2].seq_len == 1
    assert steps[3].seq_len == 0

    assert_allclose(score, log(0.3072))

    score = dp.viterbi(Sequence.create(b"AA", alphabet))[0].loglikelihood
    assert_allclose(score, log(0.2048))

    score = dp.viterbi(Sequence.create(b"A", alphabet))[0].loglikelihood
    assert_allclose(score, log(0.128))

    score = dp.viterbi(Sequence.create(b"AC", alphabet))[0].loglikelihood
    assert_allclose(score, log(0.3072))

    dp = hmm.create_dp(M2)
    score = dp.viterbi(Sequence.create(b"AC", alphabet))[0].loglikelihood
    assert_allclose(score, log(0.3072))

    hmm.del_state(E)

    dp = hmm.create_dp(M2)
    score = dp.viterbi(Sequence.create(b"AC", alphabet))[0].loglikelihood
    assert_allclose(score, log(0.3072))

    results = dp.viterbi(Sequence.create(b"ACAC", alphabet), 2)
    assert len(results) == 3

    assert_allclose(results[0].loglikelihood, log(0.3072))
    assert bytes(results[0].sequence) == b"AC"

    assert_allclose(results[1].loglikelihood, log(0.0512))
    assert bytes(results[1].sequence) == b"CA"

    assert_allclose(results[2].loglikelihood, log(0.3072))
    assert bytes(results[2].sequence) == b"AC"

    assert results[1].path[1].seq_len == 1
    assert results[1].path[1].state.name == b"M1"
