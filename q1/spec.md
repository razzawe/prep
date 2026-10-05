# Pot Luck

A community fundraiser runs a pooled cash drawing to determine prizes.

## Rules

- **Starting pot:** $10,000 (sponsor), plus $5 added per entry.
- **Code assignment:** the system assigns a random 5-digit code
  (00000-99999) to each entry.
- **Drawing:** a winning 5-digit code is generated at drawing time, and the
  pot is calculated at drawing time.
- **Reverse-order rule:** tiers are handled in reverse (5 matches first).
  If 5 matches claim 100%, lower tiers get nothing. Tiers split among winners.

## Payout tiers (% of pot)

| Matches | Share of pot |
|---------|--------------|
| 5       | 100%         |
| 4       | 40%          |
| 3       | 20%          |
| 2       | 5%           |
| 1       | 0% (no payout) |

## Example

Winning code: `12345`

| Participant | Code    | Matches |
|-------------|---------|---------|
| Mina        | `12340` | 4       |
| Julio       | `12305` | 4       |
| Mina        | `10345` | 4       |
| Sam         | `12000` | 2       |

3 entries match 4 numbers and 1 entry matches 2 numbers:

- 4-match entries split 40% of the pot.
- The 2-match entry receives 5%.

## Your task

1. Identify anything in the problem context that must be clarified before
   implementation.
2. Explain how you would model entries, a draw, and payout results.
3. Outline the payout calculation and the tests you would want.
4. Identify bugs or issues in the existing code and fix them.
5. Implement `plan_payouts` in `question.py`.
