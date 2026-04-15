# Add Trade Prompt

Use this template to add a new trade record without changing CSV schema.

Required output:
- One CSV row matching `data/trades.csv` header order
- Missing values as placeholder `-`
- No fabricated numbers

Inputs:
- Trade date_time
- Side (long/short)
- Setup name
- Entry, stop_loss, tp1, tp2
- Leverage
- Deposit before trade
- Notes
