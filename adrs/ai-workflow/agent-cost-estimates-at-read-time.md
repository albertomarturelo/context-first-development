<!-- Shareable ADR. Token budget: ~1,010. -->

# Dollar Estimates of Agent Usage, Computed at Read Time

## Status

`Accepted` — `<YYYY-MM-DD>`

## When to Use

Adopt this ADR when:

- [agent-telemetry-from-local-logs](agent-telemetry-from-local-logs.md)
  is in place and someone asks what a task or a month cost in money.
- Usage spans several models, providers or plans, so no single invoice
  answers per task.

Do NOT adopt it when the question is only relative (did a context change
make sessions cheaper): tokens answer that without a price table.

## Context

Tokens add up across agents; money does not. The price depends on the
model, the token type (uncached input, output, cache read, cache write
by duration), the tier (fast or priority modes, long context) and the
plan (flat subscriptions, contracted discounts). Some agents log billed
units per request, some log their own list-price estimate, some log
neither. Three failure modes follow: a dollar figure frozen into a
report at last quarter's price; a model missing from the price list
shown as $0; a list-price estimate read as the invoice.

## Decision

1. **Reports stay in tokens.** No dollar figure is published. Month
   files carry tokens per day, branch and model, so any reader can
   price them later.
2. **The reader computes dollars** (the local dashboard or the team
   view) from a price table, every time it renders.
3. **The team owns the price table**: a file next to the reader, not
   in the methodology or the skill. One entry per model and tier, a
   price per token type, and an effective-from date; usage is priced by
   the entry in force on its day. Contracted rates go there.
4. **Each token type is priced on its own.** Cache writes by duration
   when the agent tells them apart. A tier that depends on one
   request's size (long context) is split by the adapter into its own
   bucket, because a bucket no longer knows request sizes.
5. **Unknown is unpriced, never zero.** Tokens of a model or tier the
   table lacks get no dollar figure and a gap counter; any total that
   includes them is marked partial.
6. **Every figure is labelled an estimate** at list or contract price.
   Under a flat subscription it is the value consumed, not the spend.
7. **Billed units stay in their unit.** Credits or premium requests an
   agent logs are shown beside the estimate, converted only when the
   table gives a unit price. An agent's own dollar estimate is a cross-
   check, not the source: one method for every agent keeps them
   comparable.

## Alternatives Considered

1. **Publish dollars in the month files.** Freezes prices; two machines
   with different tables disagree; a price fix means republishing
   history.
2. **Ship a price list with the skill.** Stale within weeks, a token
   cost for every adopter, and blind to contracts.
3. **Use each agent's own figure.** Missing for some agents, and it
   mixes billed units with list-price estimates.
4. **Vendor billing exports.** The real invoice, but per seat or
   organisation, with no task or repository dimension. Complementary.
5. **No dollars.** Tokens suffice to compare context changes, but
   budget owners ask in money.

## Verifiable Consequences

A reader can confirm this ADR is being followed if:

- `git grep -i -E 'usd|price|cost' <telemetry-branch>` prints nothing.
- Every bucket in a month file names its model.
- Removing a model from the price table turns the affected totals into
  partial ones with a gap note; no total silently drops.
- Changing a price and rendering again changes the dollar figures with
  no new publish.
- Every dollar figure on screen is labelled an estimate.

## Trade-offs

- Someone maintains the table; without one there are no dollars.
- Estimates ignore invoice effects: free allowances, minimums, seat
  fees, taxes.
- A model per bucket makes month files larger.
- Per-request tiers depend on the adapter splitting them correctly;
  an agent that does not log the tier is priced at the base rate,
  flagged as such.
