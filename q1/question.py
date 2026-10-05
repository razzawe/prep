from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable, List, Optional, Tuple

SEED_POT_CENTS = 10_000_00
ENTRY_FEE_CENTS = 5_00

# percentage of the pot awarded to each match tier
TIER_PERCENTAGES = {5: 100, 4: 40, 3: 20, 2: 5}


class FundraiserError(Exception):
    pass


@dataclass(frozen=True)
class Entry:
    id: int
    participant: str
    code: str


@dataclass(frozen=True)
class Draw:
    winning_code: str
    pot_cents: int
    entries: List[Entry]


@dataclass(frozen=True)
class Payout:
    entry_id: int
    participant: str
    match_count: int
    amount_cents: int


@dataclass(frozen=True)
class PayoutPlan:
    payouts: Tuple[Payout, ...]
    awarded_cents: int
    rollover_cents: int


class FundraiserPool:
    def __init__(self, random_source: Callable[[], float] = random.random):
        self._random_source = random_source
        self._entries: List[Entry] = []
        self._next_id = 1
        self._draw: Optional[Draw] = None

    @property
    def pot_cents(self) -> int:
        return SEED_POT_CENTS + ENTRY_FEE_CENTS * len(self._entries)

    def _generate_code(self) -> str:
        number = int(self._random_source() * 99_999)
        return str(number)

    def enter(self, participant: str) -> Entry:
        entry = Entry(
            id=self._next_id,
            participant=participant,
            code=self._generate_code(),
        )
        self._next_id += 1
        self._entries.append(entry)
        return entry

    def close_draw(self) -> Draw:
        if self._draw is None:
            self._draw = Draw(
                winning_code=self._generate_code(),
                pot_cents=self.pot_cents,
                entries=self._entries,
            )
        return self._draw


def count_matches(entry_code: str, winning_code: str) -> int:
    return len(set(entry_code) & set(winning_code))


def plan_payouts(draw: Draw) -> PayoutPlan:
    raise NotImplementedError("candidate task")
