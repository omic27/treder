# Check Rules Prompt

Validate trades against `config/risk_rules.json`.

Check for:
- leverage range violations
- daily trade count violations
- daily loss limit violations
- never_rules violations from trade notes/status

Output:
- List of detected violations with trade_id
- If data missing, return placeholders instead of assumptions
