# Interview Practice Exercise Generator

Generate a practice exercise for an AI-assisted coding interview. The format mirrors the Bloomberg workshop's "Pot Luck" example: a written spec, an existing codebase that does not fully match it, a shallow passing test suite, and one stubbed function the candidate implements after fixing the foundations.

The candidate will work on this later. Never reveal bugs in the chat, in the spec, or anywhere inside the exercise folder.

## Parameters

Use these if the user supplies them; otherwise use the defaults.

- `DOMAIN`: a specific domain, or `choose` (default)
- `DIFFICULTY`: `easy` (3 bugs), `medium` (4-5 bugs, default), `hard` (6-7 bugs)
- `TIME BOX`: 30-45 minutes (default)

## Step 1: Choose the domain

If `DOMAIN` is `choose`, internally propose 3 very different domains and pick the one least structurally similar to Pot Luck.

Recommended families:
- hotel room booking and billing
- warehouse inventory and fulfillment
- subscription billing and account lifecycle
- fleet dispatch and service windows
- patient appointment scheduling and insurance billing
- library loans and late fees
- meeting room reservations

Do not use any domain or mechanic from Pot Luck:
- games, draws, lotteries, prizes, prize tiers, or payout splits
- code assignment or random code generation
- digit matching or set-intersection matching
- a `close_draw()`-style lifecycle in disguise

The exercise must be a realistic product contract problem, not a toy puzzle.

## Step 2: Write the spec (`spec.md`)

A short product brief (about one page) containing:
- a short domain description
- 5-8 concrete business rules (a rules table is welcome)
- one worked example with fully computed numbers the candidate can predict by hand
- a generic task list (see below)
- a short "interview habits" note: identify ambiguities, state assumptions explicitly, predict before running, keep changes small

Ambiguity requirements:
- Make the spec ambiguous or underspecified in 4-6 places, the way a real spec would be.
- Do NOT flag the ambiguities in the spec.
- Good candidates: tie handling, rounding and leftover amounts, boundary inclusivity, behavior after a closed or finalized state, input validation, multiplicity (one person with several records), precedence between overlapping rules, illegal state transitions, units and types.
- Some rules must be stated firmly (these become verification items). Others must be left open (these become clarification items).
- At least some of the open items must be ones the starter code gets wrong under the intended interpretation (see Step 4), so that clarifying them leads to finding a bug.

The task list must be generic and must NOT name behaviors that contain bugs. Use this shape:

1. Identify anything that must be clarified before implementation.
2. Explain how you would model the domain's entities, state, and results.
3. Review the existing implementation against the spec.
4. Outline the tests you would want.
5. Fix bugs you find, then implement the stubbed function.

The spec must not include a bug list, the ambiguity answers, or the exact tests to write.

## Step 3: Write the code (`question.py`)

Python 3.11+, standard library only (plus pytest for tests).

Size and shape:
- 100-150 lines, realistic and coherent
- one main stateful class
- 2-3 frozen dataclasses
- a couple of small helper functions
- an injectable dependency (clock, ID source, or similar) so tests can be deterministic
- integer cents for money unless a float bug is one of the planted ones
- clean, natural-looking code

The stub:
- Exactly ONE function is stubbed with `raise NotImplementedError("candidate task")`.
- It is core business logic and depends on the existing helpers and state being correct.
- Its signature and return type are clearly defined by the dataclasses.
- The existing tests do not cover it.

## Step 4: Plant the bugs

Plant exactly N bugs, where N is set by `DIFFICULTY`. Each bug must be one of two kinds:

1. **Policy-independent:** it violates a rule the spec states firmly. Every candidate would agree it is wrong.
2. **Policy-dependent:** it violates the intended interpretation of one of the spec's ambiguities (the interpretation recorded in `answers.md`). It only becomes clearly a bug once the candidate has clarified the point. Example: the spec says "matches" without defining them, and the code counts shared digits anywhere instead of by position.

Include at least 1 policy-dependent bug at `easy`, and at least 2 at `medium` and `hard`. Every other bug may be either kind.

Fairness rules for policy-dependent bugs:
- The intended interpretation must be clearly the most reasonable reading, so a candidate who asks the question gets an unsurprising answer.
- The spec's worked example must be consistent with the intended interpretation, but it should not by itself settle the ambiguity (it is fine if the buggy code also produces the example's numbers).
- Each one must map to a specific entry in `answers.md`.
- The hidden test for it must encode the intended interpretation, and the answer key must say which ambiguity it depends on.

Every bug must also:
- be realistic, not silly
- be provable with one small test that fails for one clear reason

Required mix:
- `easy`: any 3 realistic bugs, including simple classes (boundary, formatting or representation, wrong comparison, missing state check, mutable state shared by reference).
- `medium` and `hard`: include all of the following, plus simple bugs to fill the count:
  - at least one **lifecycle or sequencing** bug
  - at least one bug that **only fails under a specific combination of inputs**
  - at least one bug involving an **interaction between two components**, not a single local line

Rules:
- No comments, names, docstrings, or log messages that hint at a bug.
- Bugs must not be fixable only by redesign. Each should have a small, minimal fix.
- Do not copy the Pot Luck bug sequence or a direct analogue of it (range off-by-one, lost leading zeros, set vs positional matching, missing closed-draw check, live list in a closed draw).

## Step 5: Write the shallow tests (`test_question.py`)

- 2-3 tests only, happy path only.
- They must PASS on the starter code.
- They must avoid every planted bug's edge condition, so passing gives false confidence.
- No test touches the stubbed function.
- They must not reveal where the bugs are.

## Step 6: Write the answer key

Write all answer material to a separate folder, `answer_key/`, a sibling of `exercise/`, never inside it and never in chat.

`answer_key/answers.md`: the ambiguity clarifications.
- each intentional ambiguity
- the reasonable interpretation chosen for each, and the alternative
- the expected business behavior once clarified

`answer_key/ANSWER_KEY.md`: the grading key.
- each planted bug: file, line, what is wrong, minimal fix, isolating test, and either the spec rule violated (policy-independent) or the ambiguity and intended interpretation it depends on (policy-dependent)
- "not bugs, but worth noticing" observations
- a correct reference implementation of the stubbed function
- the worked example with hand-computed expected output
- extra test cases for the stubbed function
- a short self-grading checklist

`answer_key/hidden_tests.py`: tests that fail on the starter code, one per planted bug (one clear failure reason each), plus tests for the reference implementation.

## Step 7: Verify before finishing

Run all of these and fix any failure:

1. The shallow tests pass on `question.py`.
2. The hidden tests run against the starter: each planted bug is caught by exactly one failing test, and nothing else fails.
3. The spec's worked example, run through the reference solution (with the bugs fixed), produces exactly the numbers in the spec.
4. The number of planted bugs equals N, and the required number of policy-dependent bugs is met, each mapped to an entry in `answers.md`.
5. Nothing in `exercise/` (names, comments, docstrings, spec, tests) hints at a bug.

## Output structure

```
exercise/
  spec.md
  question.py
  test_question.py
answer_key/
  answers.md
  ANSWER_KEY.md
  hidden_tests.py
```

## Final message

Output only:
- the file tree
- the commands to run the shallow tests

Do not include the bug list, the answer key, the ambiguity answers, hints, or commentary about what the bugs are. Do not paste spec or code into chat unless asked.
