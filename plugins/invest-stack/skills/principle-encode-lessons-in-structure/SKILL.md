---
name: principle-encode-lessons-in-structure
description: "Apply when a review, a verification pass, or Ped catches the same kind of mistake a second time. Fix it in a script, schema or playbook step, not with another reminder. Adapted from pstack."
user-invocable: false
---

# Encode Lessons in Structure

- A wrong number twice means `portfolio_math.py` gets a check that fails loudly.
- A missing field twice means the ledger schema or the CSV import gets that field.
- A skipped step twice means the playbook step moves earlier or merges with the step people do remember.
- A style complaint from Ped twice means a rule in **unslop-th** with his example.
- Log each lesson in `LESSONS.md` at the repo root: date, what went wrong, what structure changed, the commit.
