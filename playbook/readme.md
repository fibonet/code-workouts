# The Clean Coder's Playbook

Software should be easy to understand, easy to verify, and inexpensive to
change.

This playbook begins with the discipline of structured programming and the
feedback-driven practices of eXtreme Programming:

- Structured programming guides how we construct understandable code.
- eXtreme Programming guides how we safely discover, validate, and evolve it.

The rules that follow are guidance for engineering judgement, not a catalogue
of rituals. Apply them in context, challenge them with evidence, and prefer the
principle behind a rule over mechanical compliance.

Use this playbook when designing code, reviewing changes, and establishing team
conventions. It provides questions and defaults, not universal rules. The
language-specific guides turn these principles into concrete conventions and
examples.

> _"Design and programming are human activities; forget that and all is lost."_  
> Bjarne Stroustrup, 1991


## How to Read This Playbook

The guidance is organised as a hierarchy:

> **Values → Principles → Practices → Context-specific rules → Examples**

Values and principles should remain durable. Practices and rules may change
with the language, system, team, and problem.

The major sections below state principles. Their bullet points describe
practices that commonly support those principles; teams should turn them into
context-specific rules only when their environment justifies doing so.

For example:

- **Value:** Simplicity
- **Principle:** Build only what is currently justified
- **Practice:** YAGNI
- **Rule:** Do not add an extension point without a known second use case
- **Example:** Start with a switch; introduce a registry when runtime
  extensibility becomes necessary

"Keep it simple" is a durable principle. "Always use a switch" is not.


## Control Flow

- Build control flow from sequence, selection, and iteration.
- Keep control flow explicit and locally understandable.
- Prefer early returns when they reduce nesting and make preconditions clear.
- Avoid unstructured jumps, hidden execution, and unnecessary recursion.
- Keep each unit at one consistent level of abstraction.
- Make exceptional paths as deliberate and understandable as successful paths.

A reader should be able to follow the execution of a unit without reconstructing
the whole system in their head.

For example, guard clauses can make preconditions explicit and keep the main
path visible:

```ts
// Harder to follow
function submit(order: Order): Receipt {
  if (!order.isEmpty) {
    if (order.customer.canPurchase) {
      return createReceipt(collectPayment(order));
    }
    throw new PurchaseNotAllowed();
  }
  throw new EmptyOrder();
}

// Main path remains visible
function submit(order: Order): Receipt {
  if (order.isEmpty) {
    throw new EmptyOrder();
  }

  if (!order.customer.canPurchase) {
    throw new PurchaseNotAllowed();
  }

  const payment = collectPayment(order);
  return createReceipt(payment);
}
```


## Decomposition

- Divide systems into cohesive modules with explicit responsibilities.
- Let each function perform one conceptual operation.
- Hide implementation details behind small, stable interfaces.
- Prefer composition over deep inheritance and shared mutable state.
- Keep dependencies visible and directed.
- Introduce abstractions after understanding the concrete cases they represent.

Decomposition should reduce the amount of context needed to understand a
change. A boundary that merely moves complexity elsewhere is not an
improvement.

Keep dependencies visible by passing capabilities into the operation that uses
them:

```ts
type Charge = (amount: Money) => Promise<Payment>;

async function checkout(
  order: Order,
  charge: Charge,
): Promise<Receipt> {
  const payment = await charge(order.total);
  return Receipt.for(order, payment);
}

const receipt = await checkout(order, stripeGateway.charge);
```

The domain operation does not need to know which payment provider performs the
charge, and a test can supply the same capability without infrastructure.


## Stop Writing Classes

If an object is created only to call one method and is then discarded, use a
function instead. A class with two methods—one of them the constructor—is a
strong signal that the class adds ceremony without providing useful state or
behaviour.

```ts
// Unnecessary lifecycle and indirection
class ReceiptFormatter {
  constructor(private readonly currency: Currency) {}

  format(receipt: Receipt): string {
    return `${receipt.total.toString()} ${this.currency.code}`;
  }
}

const output = new ReceiptFormatter(currency).format(receipt);

// The operation is the abstraction
function formatReceipt(receipt: Receipt, currency: Currency): string {
  return `${receipt.total.toString()} ${currency.code}`;
}

const output = formatReceipt(receipt, currency);
```

Before introducing a class, ask whether the language already provides the data
structure you need. A thin wrapper around a map, list, tuple, or record is not a
domain model unless it adds meaningful invariants or behaviour. Prefer the
built-in representation until the domain demands more.

Apply the same pressure to the structure surrounding a class:

- Keep namespaces shallow. They prevent name collisions; they should not encode
  an elaborate taxonomy.
- Do not create a module merely to hold one class or one exception.
- Introduce a custom exception only when callers can handle the failure more
  meaningfully than they could with an existing error type.
- Judge an API by the code required to use it. Layers that only forward a call
  or rename a value are costs, not abstractions.

Use a class when instances have a meaningful identity or lifecycle, preserve
state across operations, or protect invariants by keeping related behaviour and
data together. Do not introduce one merely to give a single operation a noun.


## Simplicity

- Implement the simplest design that satisfies the current requirements.
- Do not build speculative flexibility.
- Prefer obvious code over clever code.
- Remove duplication when doing so reveals a useful concept.
- Do not force superficially similar code into one abstraction when its reasons
  to change are different.
- Optimise only when evidence identifies a meaningful problem.
- Delete code, configuration, and dependencies that no longer earn their place.

Simple does not mean simplistic. A simple design makes its essential complexity
visible without adding accidental complexity.

Start with the concrete requirement rather than an abstraction for imagined
variation:

```python
# One known case: keep it direct.
def shipping_cost(order: Order) -> Money:
    return FLAT_SHIPPING_RATE
```

Introduce alternatives when the domain actually requires them:

```python
def shipping_cost(order: Order) -> Money:
    match order.delivery_method:
        case DeliveryMethod.STANDARD:
            return Money("5.00")
        case DeliveryMethod.EXPRESS:
            return Money("15.00")
```

There is no need for a strategy hierarchy until the known cases justify one.


## Correctness

- Express contracts and invariants through types, interfaces, validation, and
  tests.
- Validate data at system boundaries.
- Handle errors explicitly; never silently discard meaningful failures.
- Keep side effects visible, contained, and observable.
- Test observable behaviour rather than implementation details.
- Add a reproducible test for every defect when practical.
- Make invalid states difficult to represent.

Correctness is not established by tests alone. It comes from clear contracts,
sound design, executable checks, and production evidence working together.

Keep validation and side effects at visible boundaries so the domain operation
can work with trusted values:

```python
def handle_checkout(payload: object) -> Receipt:
    request = CheckoutRequest.parse(payload)
    order = repository.get(request.order_id)

    receipt = checkout(order)
    repository.save(order)

    return receipt
```

Use domain types to validate values once and make invalid states difficult to
pass deeper into the system:

```ts
class Quantity {
  private constructor(readonly value: number) {}

  static from(value: number): Quantity {
    if (!Number.isInteger(value) || value <= 0) {
      throw new InvalidQuantity(value);
    }

    return new Quantity(value);
  }
}
```

Separate decisions from effects when doing so makes the behaviour easier to
verify:

```python
def decide_discount(order: Order) -> Discount:
    if order.total >= MONEY_100:
        return Discount.percent(10)

    return Discount.none()


def complete_order(order: Order, repository: OrderRepository) -> None:
    discount = decide_discount(order)
    order.apply(discount)
    repository.save(order)
```

Test the observable contract rather than the private steps used to implement
it:

```ts
it("rejects checkout when the order is empty", async () => {
  const order = Order.empty();

  await expect(checkout(order, charge))
    .rejects.toBeInstanceOf(EmptyOrder);

  expect(charge).not.toHaveBeenCalled();
});
```


## Incremental Development

- Work in small, complete, verifiable changes.
- Keep the main branch working and releasable throughout development.
- Integrate frequently.
- Refactor continuously while tests protect existing behaviour.
- Separate behavioural changes from structural changes when that improves
  reviewability.
- Prefer reversible decisions when uncertainty is high.
- Deliver the smallest useful slice and learn from it.

Small steps reduce risk, shorten feedback loops, and make mistakes easier to
locate and reverse.

A useful increment crosses the layers it needs to deliver verified behaviour;
it is not merely one unfinished architectural layer:

```text
Change 1: calculate the order total and test it
Change 2: expose the total through the checkout endpoint
Change 3: collect payment and record the outcome
Change 4: add production telemetry and failure handling
```


## Feedback

- Obtain feedback from tests, users, production telemetry, and teammates.
- Shorten the time between making a decision and learning whether it was
  correct.
- Treat code review as collaborative design, not merely approval.
- Prefer running software and measured outcomes over assumptions.
- Revise decisions when new evidence appears.
- Make failures fast, visible, and informative.

Feedback is valuable only when it can influence the work. Automate it where
possible and keep it close to the decision it evaluates.

Prefer structured, actionable telemetry over messages that lose the context of
an operation:

```python
logger.info(
    "checkout_completed",
    extra={
        "order_id": str(order.id),
        "payment_id": str(receipt.payment_id),
        "total": str(order.total),
    },
)
```

Record enough context to investigate behaviour, but do not log secrets or full
request payloads by default.


## Collective Maintainability

- Write code for the next reader.
- Follow shared conventions consistently.
- Use the language of the domain.
- Keep documentation close to the decisions it explains.
- Ensure important areas are understood by more than one person.
- Improve code whenever you work in it without expanding changes recklessly.
- Treat the codebase as a shared responsibility.

Maintainability is a property of both software and team practice. Code that
only one person can safely change is an operational risk.


## Sustainable Engineering

- Maintain a pace that preserves judgement and quality.
- Automate repetitive verification and delivery.
- Make releases routine, reversible, and observable.
- Address technical debt deliberately instead of allowing it to accumulate
  invisibly.
- Do not trade long-term system health for unexamined short-term speed.
- Keep operational responsibilities proportional to the team's capacity.

Sustainable work is not slower work. It avoids the recurring cost of exhaustion,
fragile systems, emergency releases, and preventable rework.


## Core eXtreme Programming Practices

The principles above are reinforced by a set of practical habits:

- **Test-first development:** clarify expected behaviour before or alongside
  implementation.
- **Continuous integration:** combine and verify changes frequently.
- **Refactoring:** improve the design without changing observable behaviour.
- **Simple design:** build what is needed now and keep the design open to
  evidence.
- **Pairing and collaboration:** solve difficult problems with more than one
  perspective.
- **Collective ownership:** allow any qualified team member to improve any part
  of the system.
- **Small releases:** deliver useful increments and learn from real use.
- **Sustainable pace:** preserve the team's ability to make sound decisions.

These practices support one another. Tests enable refactoring, small changes
enable frequent integration, and frequent feedback keeps simple designs honest.


## Applying the Playbook

When rules appear to conflict, ask:

1. Which choice makes the behaviour easiest to understand?
2. Which choice makes correctness easiest to verify?
3. Which choice is least expensive to change?
4. What evidence supports the additional complexity?
5. Can the decision be postponed until more is known?
6. Are inputs validated at the system boundary?
7. Are side effects and dependencies visible?
8. Does the change include verification proportionate to its risk?
9. Is each new abstraction supported by concrete cases?
10. Can another team member safely understand, operate, and change it?

Choose deliberately, document consequential trade-offs, and revise the decision
when the context changes.


## Language-specific Guidance

- [JavaScript and TypeScript](js-guide.md) — types, naming, errors, asynchronous
  work, modules, state, and testing.
- [Python](py-guide.md) — typing, naming, exceptions, control flow, packages,
  state, and testing.


## Foundations and Further Reading

This playbook draws particularly from:

- Edsger W. Dijkstra, *Notes on Structured Programming*.
- Kent Beck and Cynthia Andres, *eXtreme Programming Explained: Embrace
  Change*.
- Martin Fowler, *Refactoring: Improving the Design of Existing Code*.
- Jack Diederich, *Stop Writing Classes*, PyCon US 2012.
