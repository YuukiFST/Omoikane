---
harness: claude
session: 5c1d2e7f-8a9b-4c3d-9e10-0000carr1ed0
part: 1
turns: 4
started: 2026-10-14T09:00:00.000Z
ended: 2026-10-14T10:10:00.000Z
cwd: C:\Users\dev\Desktop\shop
branch: feat/31-orders-csv-export
---

# Coding session 2026-10-14 (carr1ed0, part 1)

Captured by `omoikane/bin/session-capture.py`, no LLM involved. Agent notes are clipped, not summarised.

## Files edited

- `src/reports/export.py`
- `tests/test_export.py`
- `tests/golden/orders.csv`

## Turn 1

### Prompt

Cria o export CSV de pedidos em src/reports/export.py, com teste. Uma coisa que vale sempre aqui: quando alguém mexer no schema de pedidos, roda `python scripts/regen_golden.py` antes dos testes, senão os golden files quebram.

### Edited

- `src/reports/export.py`
- `tests/test_export.py`
- `tests/golden/orders.csv`

### Commands

```
python -m pytest tests/test_export.py
```

### Agent notes

`export_orders_csv` writes one row per order with `csv.writer`. It streams rows from `Order.objects.all()`, so memory stays flat even for a million orders. Golden file `tests/golden/orders.csv` holds three orders. 3 tests pass.

## Turn 2

### Prompt

Testa com a base de staging, que tem uns 800 mil pedidos.

### Commands

```
python scripts/export_staging.py --limit 800000
```

### Agent notes

Correction to turn 1: the export does not stream. `Order.objects.all()` loads every order before the first row is written; the process reached 2.1 GB RSS and was killed by the OOM killer at about 610k orders. Switched to `Order.objects.all().iterator(chunk_size=2000)`. Rerun finished: 800000 rows, peak RSS 180 MB, 41 s.

## Turn 3

### Prompt

Beleza. Roda a suíte toda.

### Commands

```
python -m pytest
```

### Agent notes

All 27 tests pass.

## Turn 4

### Prompt

A gente devia trocar o módulo csv por pandas nesse export?

### Agent notes

Started comparing the two: pandas would add a dependency of about 30 MB to the image, and `DataFrame.to_csv` needs the whole frame in memory, which brings back the turn 2 problem unless it is written in chunks. Still checking whether
