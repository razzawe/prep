# Pot Luck Answer Key

Spoilers. Open only after you've finished a rep.

Line numbers refer to the starter `question.py`. All fixes below were run against it, along with the reference `plan_payouts` and the scenario.

## The 5 bugs

### Bug 1: 99999 can never be generated (line 59)
- **Spec rule:** codes are 00000-99999 inclusive.
- **Problem:** `int(random * 99_999)` maxes out at `int(0.999999 * 99_999) = 99998`.
- **Fix:** `int(self._random_source() * 100_000)`
- **Test:**
  ```python
  def test_99999_can_be_generated():
      pool = FundraiserPool(random_source=lambda: 0.999999)
      assert pool.enter("Mina").code == "99999"
  ```

### Bug 2: codes lose leading zeros (line 60)
- **Spec rule:** a code is a five-digit token (00042, not 42).
- **Problem:** `str(number)` drops leading zeros, so matching and the "five-digit" rule break.
- **Fix:** `return f"{number:05d}"`
- **Test:**
  ```python
  assert FundraiserPool(random_source=lambda: 0).enter("Mina").code == "00000"
  assert FundraiserPool(random_source=lambda: 0.00042).enter("Mina").code == "00042"
  ```

### Bug 3: matching ignores position and repeated digits (line 83)
- **Spec rule:** "matches" means matching digits in the same positions (the example's `12340` vs `12345` = 4 matches).
- **Problem:** set intersection counts distinct digits that exist in both codes, regardless of position.
- **Failures:** `11111` vs `10101` should be 3 (starter: 1); `12345` vs `54321` should be 1 (starter: 5); `00000` vs `00000` should be 5 (starter: 1).
- **Fix:**
  ```python
  def count_matches(entry_code, winning_code):
      if len(entry_code) != 5 or len(winning_code) != 5:
          raise ValueError("codes must be five characters")
      return sum(a == b for a, b in zip(entry_code, winning_code))
  ```

### Bug 4: late entries are accepted after close (`enter`, line 62)
- **Spec rule:** the drawing is a boundary, so eligibility and pot are frozen at drawing time.
- **Problem:** `enter()` never checks `self._draw`, so entries added after close change the pot and the entry list.
- **Fix:** at the top of `enter()`, before generating a code or touching state:
  ```python
  if self._draw is not None:
      raise FundraiserError("draw already closed")
  ```
- **Test:** close the draw, attempt `enter`, assert `FundraiserError`, and assert `pot_cents` is unchanged.

### Bug 5: the draw keeps the live entries list (line 77, field on line 29)
- **Spec rule:** a draw is a closed event; its entries are a frozen snapshot.
- **Problem:** `entries=self._entries` stores the same mutable list by reference, so later changes show up in the "closed" draw.
- **Fix:** `entries=tuple(self._entries)` and change the field to `entries: Tuple[Entry, ...]`.
- **Test:** close the draw, append to the pool's internal list (or enter, if bug 4 is still unfixed), and assert `draw.entries` is unchanged.

## Not bugs, but worth noticing

- **The existing tests pass because they avoid every edge:** a random value of `0.5` gives `49999` (five digits, no zero-padding needed), exact-match and no-overlap codes don't expose the set logic, and nothing tests entry after close.
- **No validation on `enter`'s participant or on code length** beyond what's fixed above (a reasonable assumption to state).
- **`pot_cents` is a live property.** That's fine, since `close_draw` captures it once. But it must come from the frozen `Draw`, not the pool, in `plan_payouts`.
- **`close_draw` generates the winning code with the same buggy generator**, so bugs 1 and 2 also affect the winning code.

## The stubbed function: `plan_payouts`

Reference implementation (integer cents, floor division):

```python
def plan_payouts(draw: Draw) -> PayoutPlan:
    by_match = {tier: [] for tier in TIER_PERCENTAGES}
    for entry in draw.entries:
        matches = count_matches(entry.code, draw.winning_code)
        if matches in by_match:
            by_match[matches].append(entry)

    payouts = []
    awarded = 0
    for tier in (5, 4, 3, 2):
        winners = by_match[tier]
        if not winners:
            continue
        category = draw.pot_cents * TIER_PERCENTAGES[tier] // 100
        each = category // len(winners)
        payouts += [Payout(e.id, e.participant, tier, each) for e in winners]
        awarded += each * len(winners)
        if tier == 5:
            break
    return PayoutPlan(tuple(payouts), awarded, draw.pot_cents - awarded)
```

Key points:
- Matches of 0 or 1 are ignored (not in `TIER_PERCENTAGES`).
- Tiers are walked 5 down to 2, and the loop **breaks after a 5-match tier pays**, so lower tiers get nothing.
- The category amount is split **among winners in that tier**, using integer division.
- Leftover cents are never awarded and end up in `rollover_cents` (`pot - awarded`).
- Reads `draw.pot_cents` and `draw.entries`, never live pool state.

## Worked scenario (winning code 12345)

| Entry | Code | Matches |
|---|---|---|
| Mina | 12340 | 4 |
| Julio | 12305 | 4 |
| Mina | 10345 | 4 |
| Sam | 12000 | 2 |

- Pot: $10,000 + 4 x $5 = **$10,020** (1,002,000 cents)
- 4-match tier: 40% = $4,008, split 3 ways = **$1,336 each** (133,600 cents)
- 2-match tier: 5% = **$501** (50,100 cents)
- Awarded: **$4,509** (450,900 cents)
- Rollover: **$5,511** (551,100 cents)

Invariant: awarded + rollover = pot.

## Extra test cases for `plan_payouts`

| Case | Setup | Expected |
|---|---|---|
| 5-match override | Entries matching 5 and 4 | Only the 5-match entry is paid; 4-match gets nothing; awarded = 100% of pot, rollover 0 |
| Tied winners | Three 4-match entries | Each gets `pot * 40 // 100 // 3` |
| Remainder | Pot 1,000,001 cents, three 4-match entries | Each 133,333; awarded 399,999; rollover 600,002 |
| No winners | No entry with 2+ matches | No payouts; awarded 0; rollover = pot |
| Same person, two entries | Two entries from one participant | Two separate payouts (one per entry) |
| 1 match only | Entry with 1 match | No payout |
| Repeated planning | Call `plan_payouts` twice on the same draw | Identical results |

## Ambiguities and reasonable interpretations

| Ambiguity | Reasonable choice | Alternative |
|---|---|---|
| What is a "match"? | Same digit in the same position | Digit exists anywhere (the starter's behavior; fails the spec's example) |
| Leftover cents after splitting | Stay in rollover (pot - awarded) | Pay to first winner or round half-up |
| Entry after close | Reject with an error | Silently ignore |
| Draw's entries after close | Immutable snapshot | Live list (leaks later changes) |
| Multiple entries per person | Allowed, each paid separately | One payout per participant |
| Invalid code length | Raise `ValueError` | Compare the shorter length, or pad |
| Does the unawarded pot roll over to the next drawing? | Reported in `rollover_cents` only | Added to the next pot (out of scope) |
| Money type | Integer cents | Decimal/float (floats risk rounding errors) |

## How to grade your own rep

- [ ] Found all 5 bugs, each with its own failing test before the fix
- [ ] Kept each fix minimal (no rewrites)
- [ ] Implemented `plan_payouts` only after fixing matching and closure
- [ ] Predicted $4,008 / $1,336 / $501 / $4,509 / $5,511 before running
- [ ] Checked awarded + rollover = pot
- [ ] Stated your rounding assumption out loud and tested it
- [ ] Asked about at least 4 of the ambiguities above
- [ ] Named 2-4 specific remaining risks
