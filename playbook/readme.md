# The Clean Coder's Playbook

##### Disclaimer

> _"I hate code, and I want as little of it as possible in our products."_ – J.
> Diederich

We do not create value by writing more code; we create value by adding more
features. This document should therefore be read as guidance for judgement, not
a catalogue of rituals. Prefer clarity over cleverness, consistency over
personal taste, and maintainability over short-term convenience. Add code when
it earns its place; remove it when it no longer does.

---

## The Zen of Python

> Beautiful is better than ugly. Explicit is better than implicit. Simple is
> better than complex. Complex is better than complicated. Flat is better than
> nested. Sparse is better than dense. Readability counts. Special cases aren't
> special enough to break the rules. Although practicality beats purity. Errors
> should never pass silently. Unless explicitly silenced. In the face of
> ambiguity, refuse the temptation to guess. There should be one—and preferably
> only one—obvious way to do it. Although that way may not be obvious at first
> unless you're Dutch. Now is better than never. Although never is often better
> than right now. If the implementation is hard to explain, it's a bad idea. If
> the implementation is easy to explain, it may be a good idea. Namespaces are
> one honking great idea—let's do more of those!

These principles, written by Tim Peters and available by running
`python -m this`, set the direction for the rules that follow. Apply them with
judgement: readability and maintainability matter more than mechanical
conformance.

---

## Development Standards

Standards are useful only when they help developers produce clean, honest, and
maintainable code. Languages, frameworks, and teams change, so rules must remain
open to question. The point is discipline, not obedience. Every small decision
—the name of a variable, the shape of a function, the location of a constant,
or the boundary of a module—should be made with intent.

> Write code a programmer can hold in one mind. If you cannot reason about it,
> you cannot trust it. Write for the next programmer. Clever code is expensive
> when nobody can understand it. Let one business change require one code change
> in one place. Design for tests. Use the language of the domain, not private
> vocabulary. Treat mutable state with suspicion. Avoid scattered magic values.
> Give every module, class, and function one reason to exist. Delete dead code.
> Before adding a helper, dependency, or abstraction, check whether the codebase
> already has the answer. Leave the code a little cleaner than you found it.

### Python design principles

- Support the Python versions declared by the project.
- Follow the project's formatter, linter, type checker, and import conventions.
- Use type annotations for public APIs and other important boundaries.
- Prefer inference for local values when the inferred type is clear and precise.
- Avoid `Any` where a more useful type can be expressed.
- Accept abstract input types such as `Iterable` or `Mapping` when the
  implementation does not require a concrete collection.
- Return precise, predictable types. Avoid changing return shape according to
  undocumented conditions.
- Use `None` deliberately and represent optional values with `T | None`.
- Narrow broad or optional values as early as practical.
- Prefer small data classes, named tuples, protocols, or typed dictionaries over
  unstructured dictionaries when the data has a stable shape.
- Use typed fixtures, factories, mocks, and test utilities.
- Do not suppress type-checking or lint errors without documenting why the
  suppression is necessary.
- Validate data at untyped boundaries. Type annotations do not perform runtime
  validation.
- Prefer standard-library solutions unless a dependency clearly earns its place.

Type annotations improve communication, tooling, refactor safety, and long-term
reliability. They should clarify the design rather than compensate for a
confusing abstraction.

---

## Naming Conventions

Names are part of the program. Read a name in the sentence where it will live
before committing to it.

Choose names that reveal intent rather than implementation. Use the language of
the domain, avoid unclear abbreviations, and prefer a longer precise name over a
short ambiguous one.

Follow Python's established naming conventions:

- Use `snake_case` for variables, functions, methods, and modules.
- Use `PascalCase` for classes and exceptions.
- Use `UPPER_SNAKE_CASE` for module-level constants.
- Prefix implementation details with a single underscore when they are not part
  of the public API.
- Do not use double leading underscores merely to indicate privacy. Name
  mangling exists primarily to avoid accidental clashes in subclasses.

### Naming data symbols

Use nouns for variables, constants, attributes, and parameters. Collections
deserve plural names, and individual elements deserve singular names.

```python
for order in orders:
    process(order)
```

Do not encode today's implementation into tomorrow's name. Names such as
`user_dict`, `user_list`, and `cached_array` become misleading as the design
evolves. Name the concept, not its current container.

A boolean should read like a question:

```python
if is_anonymous:
    ...

if user.has_permission:
    ...

if order.is_paid:
    ...

if can_submit:
    ...
```

Avoid ambiguous names such as `flag`, `status`, `data`, `obj`, or `result` when
they do not explain their purpose.

Introduce explanatory symbols when they make the code clearer:

```python
out_of_stock_products = [
    product for product in products if product.stock <= 0
]

for product in out_of_stock_products:
    mark_as_unavailable(product)
```

Every name should earn its place. If replacing it with `thing` changes nothing,
the name communicates nothing.

### Naming behaviour symbols

Function and method names should use expressive verbs that describe their
effect. Prefer `discard_inactive_connections` over
`inactive_connections_cleanup`.

```python
get_product_price()
format_currency()
build_search_payload()
```

Use `get_` for an operation that retrieves or computes a value, not
automatically for every property access. Use `is_`, `has_`, `can_`, or
`should_` when they make a boolean result read naturally.

A name should fit wherever it appears: in assignments, conditions, loops,
logging context, and function calls. Read those expressions aloud. If they
sound unnatural, rename the symbol.

```python
pending_statuses = {
    OrderStatus.OPEN,
    OrderStatus.PROCESSING,
    OrderStatus.AWAITING_PAYMENT,
}

pending_orders = [
    order for order in orders if order.status in pending_statuses
]

for order in pending_orders:
    process(order)
```

---

## Events

An event names something that happened, not something that should happen.
Events describe facts; commands describe intent.

```python
# Events
order_placed
payment_authorized
email_sent
user_signed_in

# Commands
place_order
authorize_payment
send_email
sign_in_user
```

Prefer the past tense for events:

```python
user_created
order_cancelled
payment_failed
cache_invalidated
```

Avoid imperative names such as `create_user_event` and vague names such as
`completed`, `success`, or `updated`. An event should still make sense when it
appears alone in a log.

Include the business concept in the name:

```python
checkout_completed
inventory_reserved
refund_issued
```

Use an `Event` suffix only when it distinguishes an event type from another
domain concept. Do not add it mechanically.

---

## Exceptions

An exception should answer one question:

> What prevented the operation from succeeding?

It should not merely describe where the code happened to raise it.

Catch the narrowest exception you can handle. Never use a bare `except`, and do
not catch `Exception` unless you are at a deliberate boundary where failures
are logged, translated, or isolated. Do not silently discard exceptions.

Use exceptions for exceptional failure, not ordinary branching. When absence or
failure is an expected outcome, consider returning `None`, a result object, or
another explicit domain value.

### Name the problem, not the implementation

Good:

```python
class ProductNotFoundError(Exception):
    ...


class PaymentDeclinedError(Exception):
    ...


class SessionExpiredError(Exception):
    ...
```

Poor:

```python
class ServiceError(Exception):
    ...


class HelperError(Exception):
    ...
```

The poor names describe a technical location rather than the problem.

End exception class names with `Error` when doing so makes their role clear and
matches standard Python practice. Use an existing built-in exception when its
meaning is accurate; create a domain exception when callers need domain-specific
handling or context.

### Carry structured context

Use the exception name for the category and attributes for details:

```python
from typing import Literal


PaymentFailureReason = Literal[
    "declined",
    "expired_card",
    "insufficient_funds",
]


class PaymentFailedError(Exception):
    def __init__(
        self,
        message: str,
        *,
        reason: PaymentFailureReason,
    ) -> None:
        super().__init__(message)
        self.reason = reason
```

Do not create an exception class for every sentence. Create distinct types
around decisions callers genuinely need to make.

Preserve the original cause when translating exceptions:

```python
try:
    payment_gateway.charge(payment)
except GatewayDeclinedError as error:
    raise PaymentDeclinedError(payment.id) from error
```

---

## Functions

Give each function one clear responsibility and keep it at one level of
abstraction. Prefer small functions, but do not split cohesive logic merely to
satisfy a line-count rule.

- Keep parameter lists focused. Introduce a meaningful object when several
  parameters travel together.
- Prefer keyword-only parameters when positional arguments would be unclear.
- Avoid mutable default arguments.
- Return early when a guard clause makes the main path easier to see.
- Separate pure calculation from input/output where practical.
- Make side effects visible in the function's name or API.
- Do not use `*args` and `**kwargs` to hide an unclear interface.

```python
def add_item(
    order: Order,
    product: Product,
    *,
    quantity: int = 1,
) -> Order:
    if quantity <= 0:
        raise ValueError("quantity must be positive")

    return order.with_item(product, quantity=quantity)
```

---

## Modules and Packages

Use lowercase `snake_case` for Python module and package names:

```text
product_card.py
mobile_navigation.py
payment_processing/
```

Names should be descriptive and predictable. Keep code that changes together
close together, and organize packages around features or domain responsibilities
rather than technical type hierarchies.

Avoid catch-all modules such as `utils.py`, `helpers.py`, `constants.py`, or
`types.py`. A focused module name should explain what belongs inside it.

Start with a module that serves one clear purpose. Split it when it becomes
difficult to understand, preserving cohesion rather than applying an arbitrary
line limit.

Keep package initialization lightweight. Avoid import-time side effects and
surprising work in `__init__.py`.

Treat a leading underscore as the signal for non-public modules and symbols.
Define `__all__` only when an explicit export list improves the package API.

---

## Data and State

Prefer immutable values when they reduce the number of states a reader must
track. Mutation is acceptable when it is local, explicit, and simpler than
copying.

- Use a data class for a record with a stable named structure.
- Consider `frozen=True` when instances represent values.
- Do not use a class when a function or simple data structure communicates the
  design better.
- Avoid shared mutable global state.
- Return new collections when mutating an input would surprise the caller.
- Use properties for inexpensive attribute-like access, not hidden network,
  database, or otherwise costly operations.

```python
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class Money:
    amount: Decimal
    currency: str
```

---

## Comments and Documentation

Code should explain what it does. Comments should explain why a decision exists,
identify a non-obvious constraint, or preserve context that cannot be expressed
in code.

- Keep comments accurate or remove them.
- Do not narrate straightforward code.
- Document public APIs according to the project's docstring convention.
- Describe externally visible behavior, parameters, return values, raised
  exceptions, and important side effects where they are not already obvious.
- Give TODOs an owner or issue reference when the project workflow supports it.
- Never leave commented-out code; version control already preserves history.

---

## Testing

Tests are executable descriptions of behavior.

- Name tests after the behavior and condition they verify.
- Follow Arrange–Act–Assert when it improves readability, without adding
  ceremonial comments.
- Test public behavior rather than private implementation details.
- Prefer small, typed fixtures and factories.
- Mock at system boundaries, not every collaborator.
- Keep tests deterministic. Control time, randomness, environment, and external
  services explicitly.
- Assert the important outcome, not every incidental detail.
- Add a regression test when fixing a defect when practical.

```python
def test_checkout_rejects_an_expired_coupon() -> None:
    order = order_with_coupon(expires_on=date(2025, 1, 1))

    with pytest.raises(InvalidCouponError):
        checkout(order, today=date(2025, 1, 2))
```

---

## Backlog Chapters

These sections remain to be developed as the standards evolve:

- [ ] Async Python — task ownership, cancellation, timeouts, blocking work, and
      structured concurrency.
- [ ] Resource management — context managers, cleanup, files, connections, and
      transaction boundaries.
- [ ] Imports and dependency direction — absolute versus relative imports,
      circular dependencies, and package boundaries.
- [ ] Logging and observability — structured context, levels, tracing, and
      exception reporting.
- [ ] Configuration — environment variables, secrets, validation, and startup
      failures.
- [ ] Persistence — transaction scope, query boundaries, migrations, and domain
      mapping.
- [ ] Concurrency — threads, processes, synchronization, and shared state.
- [ ] Security — input validation, serialization, subprocesses, paths, and
      dependency hygiene.

---

## References

- [PEP 8 — Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP 20 — The Zen of Python](https://peps.python.org/pep-0020/)
- [Python typing documentation](https://docs.python.org/3/library/typing.html)
- [Python exceptions documentation](https://docs.python.org/3/tutorial/errors.html)
