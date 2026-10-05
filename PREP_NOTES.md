# AI-Assisted Interview Cheat Sheet

**Graded on:** visible reasoning and ownership, not just working code.
**Rule:** if you can't explain it, don't ship it.
**Expected output:** a working fix plus tests that prove the behavior.

## The loop

1. **Read spec**: summarize rules as a checklist (no AI needed first)
2. **Clarify**: list ambiguities, pick an interpretation yourself, add a test for each
3. **Map code**: ask AI where things live, then verify in the files
4. **Diagnose**: one failing test per spec rule, each failing for one reason
5. **Patch small**: one bug at a time, rerun test then suite
6. **Implement stub**: only after foundations are fixed
7. **Validate**: predict by hand, run, check invariants
8. **Name risks**: what's still untested or assumed

## Clarify checklist

Matching (positional?) | Boundaries (inclusive?) | Validation | Closure | Snapshot/immutability | Rounding remainder | Multiple entries | Ties | Rule precedence

Say: *"I'm assuming X; I'll add a test so that assumption is explicit."*

## What to map

- Code generation (range, formatting)
- Closing a draw (what state is captured)
- Stubbed function (signature, return type)
- Matching helper
- Entry flow (closed-state check?)
- Dataclasses (frozen? mutable fields?)
- Injectable dependency (random source)
- Existing tests (what they skip)
##### Example
i.e. In question.py, point me to the functions responsible for:
1. generating entry codes
2. closing a draw
3. calculating payouts
##
For each, give the symbol name and a one-line description. Do not edit files.
## Common bugs

Off-by-one at endpoints | lost leading zeros | set vs positional matching | no check after closed state | mutable list stored by reference | floats for money | lost rounding remainder | lower tiers paid after 5-match

## Validate

- Predict output before running
- Invariant: awarded + rollover = pot
- Pot Luck check (code 12345): pot $10,020, 4-match $1,336 each x3, 2-match $501, awarded $4,509, rollover $5,511

## Prompts (narrow, single-goal)

- **Summarize:** "Read spec.md only. Summarize rules as a checklist, list assumptions to clarify. No implementation."
- **Map:** "Point me to the functions for X, Y, Z. Symbol name + one line. Don't edit files."
- **Challenge:** "List up to five likely violations of these rules, with the smallest input that exposes each. Don't patch."
- **Tests:** "Propose a minimal deterministic test matrix for <function>."
- **Review:** "Review this diff against the contract. Call out assumptions and what tests still don't prove."

Never: "solve it" or "rewrite it". Let AI surface ambiguities; you resolve them.

## Say out loud

- "Here are the rules I'm extracting."
- "I'm assuming X, so I'm adding a test."
- "I used AI to narrow the search, then verified it myself."
- "Here's the case I expect to fail, and why."
- "I kept this change small because..."
- "Remaining risks are..."

## Pitfalls

Accepting the first AI answer | trusting AI's description without opening the file | going silent | big refactors | skipping the spec | trusting passing tests

## Practice

Fresh AI session, timer, talk out loud.

1. Pot Luck, no tests, no time limit
2. Generated exercise with shallow tests, 60 min
3. New domains, 45 min, someone changing a requirement mid-way

After each rep: bugs missed? ambiguities never raised? assumptions reasonable? AI claims verified? one thing to improve.


## When to create tests
You create tests at several points, each for a different purpose.

### 1. During clarify: assumption tests (write the name or a stub now, fill in later)
Every time you say "I'm assuming X," jot down a test for it. These are decisions you made, so the test records them. Example: "leftover cents stay in rollover" becomes a test with a pot that doesn't divide evenly.

### 2. During diagnose: failing tests, before any fix
This is where most of your tests get written. For each spec rule, write one small test that should fail on the current code, run it, and confirm it fails for the reason you predicted. Only then fix. Doing it in this order proves the bug exists, proves your fix works, and gives you evidence to point at.

### 3. Before implementing the stubbed function: plan the cases
Write the test list (not necessarily the code) before writing the function: the worked example, a single top-tier winner, tied winners, leftover cents, no winners, and the 5-match override. Writing at least the worked-example test first is a good habit, since you already know the expected numbers.

### 4. After implementing: fill in and run
Run the planned tests, predict the worked example by hand before running, and add the invariant check (awarded + rollover = pot).

### 5. At the end: gaps
Add tests for any assumptions or risks you named that still lack coverage.

Rule of thumb

A test for a bug comes before its fix.
A test for a new function comes before or alongside its implementation, never after as an afterthought.
A test for an assumption comes as soon as you state it.