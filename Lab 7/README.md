# L6_L7_04 — Shipping Quotation

Lab 7: Fuzz Testing with Hypothesis

## About

A set of property-based fuzz tests targeting dimensional weight formulas, tracking label code formats, and manifest payload parsing routines to detect malformed string crashes.

## Files

| File | Description |
|------|-------------|
| `processor.py` | The module under test (buggy starter code) |
| `test_processor.py` | Starter test file to complete using Hypothesis |

Keep all your Lab 7 work in this `LAB7` folder.

Refer to the lab handout for instructions.

## Completion notes

- `processor.py` is the original module under test and should remain unchanged.
- `test_processor.py` contains the Hypothesis-based fuzz tests.
- Install dependencies with: `python -m pip install pytest hypothesis`
- Run the tests from this folder with: `python -m pytest -v`
