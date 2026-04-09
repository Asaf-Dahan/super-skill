# traces/

Execution traces capture what was attempted, what happened, and what
was inferred. Unlike DECISIONS.md (which records settled outcomes),
traces record the raw execution history that enables causal reasoning.

Use TRACE-TEMPLATE.md for the format.

Traces are referenced by ID (TRC-NNN) and can link to decisions (DEC-NNN),
evaluations (EVAL-NNN), or other traces to form causal chains.

Traces are never deleted. Superseded traces link to their replacement.
