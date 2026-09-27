# COLLAPSE: ShopLite

> "AI fixes flaky tests by cheating. COLLAPSE makes Bob prove the real cause first."

ShopLite is an e-commerce demo application designed for the COLLAPSE hackathon project.
It contains realistic cart, pricing, inventory, and order domain logic, along with a suite
of reliable baseline tests and 3 planted flaky tests representing the primary categories
of flakiness.

---

## Baseline Commitment & Ground Truth Proof

To prove that COLLAPSE makes Bob discover and prove the true root cause rather than
being graded after the fact, our ground truth is formally committed before any Bob run:

- **Ground Truth Commit Hash:** `f16b4243d596fea837966e9c2246f5b413090f36`
- **Ground Truth Document:** [`GROUND_TRUTH.md`](GROUND_TRUTH.md)
- **Anti-Cheating Test Policy:** [`TEST_POLICY.md`](TEST_POLICY.md)

---

## Architecture & Project Structure

```
d:/ibm bob/
â”œâ”€â”€ shoplite/            # Core application domain (Cart, Inventory, Orders, Promotions)
â”œâ”€â”€ tests/               # Reliable baseline tests + planted flaky tests
â”œâ”€â”€ engine/              # Person A's 5 engine commands (detect, prove, check, verify, report)
â”œâ”€â”€ results/             # Structured JSON evidence (summary.json, detect.json, etc.)
â”œâ”€â”€ dashboard/           # Person D's live web dashboard (index.html)
â”œâ”€â”€ .bob/                # Person C's Bob configuration, rules, and Observer mode
â””â”€â”€ bob_sessions/        # Bob task screenshots and session logs
```

---

## Setup & Running Tests

### 1. Setup
```bash
pip install -r requirements.txt
```

### 2. Run All Tests
```bash
pytest tests/ -v
```

### 3. Reproduce Each Flaky Test Deterministically

#### Flaky Test 1: Set-Order / Hash Randomization
```bash
PYTHONHASHSEED=0 pytest tests/test_flaky_set_order.py -v
PYTHONHASHSEED=2 pytest tests/test_flaky_set_order.py -v
```

#### Flaky Test 2: Time-Based Race
```bash
pytest tests/test_flaky_timing.py -v
```

#### Flaky Test 3: Shared-State / Order Dependence
```bash
pytest tests/test_flaky_shared_state.py -v        # Passes alone / in default order
pytest tests/ -p randomly -v                       # Fails when mutating test runs first
```
