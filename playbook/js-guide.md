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

## The Zen of JavaScript

> Readability counts.  
> Explicit intent is better than hidden behaviour.  
> Simple control flow is better than clever syntax.  
> Predictable state is better than convenient mutation.  
> A small module with a clear purpose is better than a universal helper.  
> Data should have one unsurprising shape.  
> Errors should carry context and should never disappear silently.  
> Asynchrony should be visible, owned, and cancellable when practical.  
> Dependencies should earn their place.  
> Compatibility should be deliberate, not accidental.  
> The platform is a dependency; know which platform you target.  
> If an abstraction is hard to explain, reconsider it.  

These are working principles rather than language doctrine. JavaScript permits
many styles; a codebase should deliberately choose a small, coherent subset.

---

## Development Standards

Standards are useful only when they help developers produce clean, honest, and
maintainable code. Languages, runtimes, and teams change, so rules must remain
open to question. The point is discipline, not obedience. Every small decision
—the name of a variable, the shape of a function, the location of a constant,
or the boundary of a module—should be made with intent.

> Write code a programmer can hold in one mind.  
> If you cannot reason about it, you cannot trust it.  
> Write for the next programmer.  
> Clever code is expensive when nobody can understand it.  
> Let one business change require one code change in one place.  
> Design for tests.  
> Use the language of the domain, not private vocabulary.  
> Treat mutable state with suspicion.  
> Avoid scattered magic values.  
> Give every module, class, and function one reason to exist.  
> Delete dead code.  
> Before adding a helper, dependency, or abstraction, check whether the codebase already has the answer.  
> Leave the code a little cleaner than you found it.  

### JavaScript design principles

- Declare the supported runtimes and language targets.
- Follow the project's formatter, linter, module, and import conventions.
- Prefer `const`; use `let` only when reassignment communicates necessary state.
- Never use `var`.
- Use strict equality (`===` and `!==`) unless coercive comparison is
  intentional and documented.
- Prefer ESM for new code unless the target environment requires another module
  system.
- Keep module initialization cheap and free of surprising side effects.
- Prefer platform and standard-library capabilities unless a dependency clearly
  earns its place.
- Validate data at external boundaries. Values from requests, storage,
  environment variables, and third-party services are untrusted.
- Use modern syntax when it improves clarity, not merely because it is shorter.
- Avoid modifying built-in prototypes and shared global state.
- Make runtime-specific APIs and assumptions visible at module boundaries.

---

## TypeScript

TypeScript should make contracts and invariants visible. It should guide the
design rather than obscure it.

### Compiler configuration

- Enable `strict`.
- Adopt additional safety options appropriate to the project, such as
  `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes`.
- Keep emitted modules and module resolution aligned with the actual runtime.
- Do not weaken the project configuration to accommodate one difficult module.
- Check source and test code with the same seriousness.

### Type boundaries

- Require explicit types at public APIs and important system boundaries.
- Prefer inference for local values when the inferred type is clear and precise.
- Validate unknown runtime input before treating it as a domain type.
- Accept the broadest useful input and return the narrowest truthful output.
- Model optional values deliberately; do not use `null` and `undefined`
  interchangeably without a convention.
- Narrow broad or optional values as early as practical.
- Use `unknown` for values whose shape is not yet known.
- Avoid `any`. When it is unavoidable, contain it at a boundary and document
  why it is safe.

```ts
function parseOrder(value: unknown): Order {
  if (!isOrder(value)) {
    throw new InvalidOrderError("Order payload is invalid");
  }

  return value;
}
```

### Type design

- Prefer unions that model real alternatives over broad bags of optional
  properties.
- Use discriminated unions when behavior depends on a finite set of states.
- Introduce generics only when they remove duplication or enforce a useful
  relationship between values.
- Prefer structural contracts over inheritance hierarchies.
- Use `interface` for extendable object contracts and `type` for unions,
  aliases, and compositions; follow the local convention when either works.
- Use `readonly` where it communicates an invariant.
- Avoid type assertions. Prove or validate the type when practical.
- Do not use enums automatically. Consider literal unions or `as const` objects
  when their runtime behavior is a better fit.

```ts
type PaymentResult =
  | { status: "approved"; transactionId: string }
  | { status: "declined"; reason: DeclineReason };

function receiptFor(result: PaymentResult): Receipt | null {
  if (result.status === "declined") {
    return null;
  }

  return buildReceipt(result.transactionId);
}
```

### Suppressions and third-party types

- Avoid `@ts-ignore`.
- Use `@ts-expect-error` only for a known, intentional incompatibility and
  include a concise explanation.
- Prefer correcting or augmenting inaccurate third-party declarations over
  spreading assertions through the codebase.
- Remove suppressions when the underlying limitation no longer exists.
- Use typed fixtures, factories, mocks, and test utilities.

Type safety improves communication, tooling, refactor safety, and long-term
reliability. A type that cannot be understood quickly is still a liability.

---

## Naming Conventions

Names are part of the program. Read a name in the sentence where it will live
before committing to it.  
Choose names that reveal intent rather than implementation.  
Use the language of the domain, avoid unclear abbreviations, and prefer a longer
precise name over a short ambiguous one.

Follow these conventions:

- Use `camelCase` for variables, functions, methods, and object properties.
- Use `PascalCase` for classes and constructor functions.
- Use `UPPER_SNAKE_CASE` only for genuine module-level constants.
- Use kebab-case for module file names.
- Use private class fields (`#field`) when language-enforced privacy is useful.
- Do not prefix ordinary implementation details with underscores unless the
  project or an external API requires it.

### Naming data symbols

Use nouns for variables, constants, properties, and parameters.  
Collections deserve plural names, and individual elements deserve singular
names.

```js
for (const order of orders) {
  process(order);
}
```

Do not encode today's implementation into tomorrow's name. Names such as
`userMap`, `userArray`, and `cachedList` become misleading as the design evolves.
Name the concept, not its current container.

A boolean should read like a question:

```js
if (isAnonymous) {
  // ...
}

if (user.hasPermission) {
  // ...
}

if (order.isPaid) {
  // ...
}

if (canSubmit) {
  // ...
}
```

Avoid ambiguous names such as `flag`, `status`, `data`, `obj`, or `result` when
they do not explain their purpose.

Introduce explanatory symbols when they make the code clearer:

```js
const outOfStockProducts = products.filter((product) => product.stock <= 0);

for (const product of outOfStockProducts) {
  markAsUnavailable(product);
}
```

Every name should earn its place. If replacing it with `thing` changes nothing,
the name communicates nothing.

### Naming behaviour symbols

Function and method names should use expressive verbs that describe their
effect. Prefer `discardInactiveConnections` over
`inactiveConnectionsCleanup`.

```js
getProductPrice();
formatCurrency();
buildSearchPayload();
```

Use `get` for an operation that retrieves or computes a value, not automatically
for every property access. Use `is`, `has`, `can`, or `should` when they make a
boolean result read naturally.

A name should fit wherever it appears: in assignments, conditions, loops,
logging context, and function calls. Read those expressions aloud. If they
sound unnatural, rename the symbol.

```js
const pendingStatuses = new Set([
  OrderStatus.Open,
  OrderStatus.Processing,
  OrderStatus.AwaitingPayment,
]);

const pendingOrders = orders.filter((order) =>
  pendingStatuses.has(order.status),
);

for (const order of pendingOrders) {
  process(order);
}
```

---

## Events

An event names something that happened, not something that should happen.
Events describe facts; commands describe intent.

```js
// Events
orderPlaced;
paymentAuthorized;
emailSent;
userSignedIn;

// Commands
placeOrder;
authorizePayment;
sendEmail;
signInUser;
```

Prefer the past tense for events:

```js
userCreated;
orderCancelled;
paymentFailed;
cacheInvalidated;
```

Avoid imperative names such as `createUserEvent` and vague names such as
`completed`, `success`, or `updated`. An event should still make sense when it
appears alone in a log.

Include the business concept in the name:

```js
checkoutCompleted;
inventoryReserved;
refundIssued;
```

Use an `Event` suffix only when it distinguishes an event type from another
domain concept. Do not add it mechanically.

---

## Errors

An error should answer one question:

> What prevented the operation from succeeding?

It should not merely describe where the code happened to throw it.

Catch only errors that can be handled meaningfully. At application boundaries,
failures may be logged, translated, or isolated. Never silently discard them.

Use errors for exceptional failure, not ordinary branching. When absence or
failure is an expected outcome, consider returning `null`, a result object, or
another explicit domain value.

### Name the problem, not the implementation

Good:

```js
class ProductNotFound extends Error {}
class PaymentDeclined extends Error {}
class SessionExpired extends Error {}
```

Poor:

```js
class ServiceError extends Error {}
class HelperError extends Error {}
```

The poor names describe a technical location rather than the problem.

End error class names with `Error` only if it makes sense. A name like
`ProductNotFoundError` or `PaymentFailedError` repeat the erroneuos state
semantically. Use a built-in error when its meaning is accurate; create a domain
error when callers need domain-specific handling or context.


### Carry structured context

Use the error name for the category and properties for details:

```js
class PaymentFailed extends Error {
  constructor(message, { reason, cause } = {}) {
    super(message, { cause });
    this.name = "PaymentFailed";
    this.reason = reason;
  }
}
```

Do not create an error class for every sentence. Create distinct types around
decisions callers genuinely need to make.

Preserve the original cause when translating errors:

```js
try {
  await paymentGateway.charge(payment);
} catch (error) {
  if (error instanceof GatewayDeclined) {
    throw new PaymentDeclined(payment.id, { cause: error });
  }

  throw error;
}
```

---

## Functions

Give each function one clear responsibility and keep it at one level of
abstraction. Prefer small functions, but do not split cohesive logic merely to
satisfy a line-count rule.

- Keep parameter lists focused. Introduce a meaningful options object when
  several parameters travel together.
- Use object parameters when several positional arguments would be unclear.
- Use default parameters instead of manual undefined checks when the semantics
  are equivalent.
- Return early when a guard clause makes the main path easier to see.
- Separate pure calculation from input/output where practical.
- Make side effects visible in the function's name or API.
- Avoid boolean parameters that make calls difficult to understand.
- Do not use rest parameters to hide an unclear interface.

```js
function addItem(order, product, { quantity = 1 } = {}) {
  if (quantity <= 0) {
    throw new RangeError("quantity must be positive");
  }

  return order.withItem(product, { quantity });
}
```

---

## Control Flow

Structured programming builds behaviour from three basic control structures:

1. **Sequence** — execute operations in a clear order.
2. **Selection** — choose a path with `if`, `else`, or `switch`.
3. **Iteration** — repeat behaviour with loops or collection operations.

Compose these structures through functions instead of arbitrary jumps or hidden
transfers of control. A reader should be able to determine what executes next
from the code immediately in view.

Each block should have one clear entry point. Prefer normal completion, guard
clauses, `return`, `break`, and `continue` over state flags that indirectly
control later behaviour. Multiple returns are acceptable when they make the
paths explicit and keep the main path clear.

```js
function shippingCost(order) {
  if (order.isDigital) {
    return 0;
  }

  if (order.destination == null) {
    throw new MissingDestination();
  }

  return rateFor(order.destination, order.weight);
}
```

Do not force a function into a single return statement when doing so requires
extra mutation, flags, or nesting.


### Keep the main path visible

Handle invalid input, exceptional states, and trivial cases early. Guard clauses
prevent the main behaviour from drifting deeper into nested blocks.

Prefer:

```js
function submit(order) {
  if (order.isEmpty) {
    throw new EmptyOrder();
  }

  if (!order.customer.canPurchase) {
    throw new PurchaseNotAllowed();
  }

  const payment = collectPayment(order);
  return createReceipt(order, payment);
}
```

Avoid:

```js
function submit(order) {
  if (!order.isEmpty) {
    if (order.customer.canPurchase) {
      const payment = collectPayment(order);
      return createReceipt(order, payment);
    }
    throw new PurchaseNotAllowed();
  }
  throw new EmptyOrder();
}
```

Deep nesting is a design signal, not merely a formatting problem. Simplify the
condition, return early, extract cohesive behaviour, or reconsider the data
model before adding another level.


### Write conditions that reveal intent

Give a complex condition a domain name when that name explains the decision.

```js
const isEligibleForRefund =
  order.isPaid &&
  !order.isRefunded &&
  order.age <= REFUND_WINDOW;

if (isEligibleForRefund) {
  issueRefund(order);
}
```

- Prefer positive conditions when they are easier to understand.
- Avoid comparing booleans explicitly with `true` or `false`.
- Use strict equality unless coercion is deliberate.
- Use `value == null` only when intentionally checking for both `null` and
  `undefined`.
- Do not rely on truthiness when `false`, `0`, `""`, `null`, and `undefined`
  have different meanings.
- Keep assignments and other side effects out of conditions.
- Extract a named predicate when several boolean operators obscure the decision.
- Use `some()` and `every()` when they express a collection-wide question
  directly.

Use nullish coalescing when only missing values should trigger a default:

```js
const retryCount = options.retryCount ?? DEFAULT_RETRY_COUNT;
```

Do not use `||` for that purpose when `0`, `false`, or an empty string is a valid
value.

Ternary expressions are appropriate for one small choice:

```js
const label = account.isActive ? "active" : "inactive";
```

Use a normal conditional when either branch performs work, contains another
condition, or is difficult to scan. Avoid nested ternary expressions.


### Choose the right iteration

Use `for...of` when processing iterable values. Use `while` when repetition is
controlled by a changing condition.

```js
for (const order of pendingOrders) {
  process(order);
}
```

- Iterate over values directly instead of managing indexes unnecessarily.
- Use a traditional `for` loop when the index or update expression is essential
  to the algorithm.
- Use `Object.keys()`, `Object.values()`, or `Object.entries()` for plain object
  properties.
- Do not use `for...in` for array values.
- Use `break` when the required result has been found.
- Use `continue` for a small guard that keeps the loop body clear.
- Avoid modifying a collection while iterating over it unless the behaviour is
  explicit and safe.
- Ensure every `while` loop makes visible progress toward termination.
- Avoid labelled statements; simplify or extract nested control flow instead.

Use `map`, `filter`, `find`, `some`, and `every` when their names describe the
operation directly. Use `reduce` only when the accumulation remains easy to
understand.

```js
const paidOrderIds = orders
  .filter((order) => order.isPaid)
  .map((order) => order.id);
```

Prefer a loop when a chain performs side effects, requires early termination, or
needs several intermediate decisions. Remember that `forEach` cannot be stopped
with `break` or `return` from the enclosing function, and it does not await an
asynchronous callback.


### Use `switch` for one discriminant

Use `switch` when selecting behaviour from a closed set of values belonging to
one concept. Prefer `if` and `else` for ranges, unrelated predicates, or simple
boolean decisions.

```js
switch (paymentResult.status) {
  case "approved":
    return createReceipt(paymentResult.transactionId);

  case "declined":
    throw new PaymentDeclined(paymentResult.reason);

  default:
    throw new UnsupportedPaymentStatus(paymentResult.status);
}
```

End each case deliberately with `return`, `throw`, or `break`. If fallthrough is
intentional, keep the cases adjacent and document the reason. A `default` branch
should handle an unknown value meaningfully; it should not conceal an incomplete
domain model.


### Keep exceptional flow exceptional

Errors transfer control beyond the current statement, so use them deliberately.

- Keep `try` blocks as narrow as practical.
- Catch only failures the current scope can handle or translate.
- Remember that JavaScript permits any value to be thrown; narrow or normalize a
  caught value before relying on its properties.
- Use `finally` for cleanup that must occur whether the operation succeeds or
  fails.
- Never use thrown values as a substitute for an ordinary loop or conditional.
- Preserve the original error with `cause` when translating it.

The structure should tell the story: establish the preconditions, perform the
work, and make every exit path deliberate.

---

## Modules and Packages

Use descriptive kebab-case module file names:

```text
product-card.js
mobile-navigation.js
payment-processing/
```

Names should be descriptive and predictable. Keep code that changes together
close together, and organize modules around features or domain responsibilities
rather than technical type hierarchies.

Avoid catch-all modules such as `utils.js`, `helpers.js`, `constants.js`, or
`types.js`. A focused module name should explain what belongs inside it.

Start with a module that serves one clear purpose. Split it when it becomes
difficult to understand, preserving cohesion rather than applying an arbitrary
line limit.

Keep exports deliberate. Prefer named exports for reusable modules and use
default exports only when they improve the local convention. Avoid barrel files
that conceal dependency direction or create cycles.

Do not mix module systems within a package without a documented compatibility
reason.

---

## Data and State

Prefer immutable values when they reduce the number of states a reader must
track. Mutation is acceptable when it is local, explicit, and simpler than
copying.

- Use objects for records with named fields and arrays for ordered collections.
- Use `Map` and `Set` when their semantics are genuinely required.
- Avoid shared mutable global state.
- Return new collections when mutating an input would surprise the caller.
- Do not use JSON serialization as a general-purpose cloning mechanism.
- Use classes when identity, invariants, or cohesive behavior justify them.
- Prefer plain functions and objects when a class adds no useful meaning.
- Keep object shapes stable; avoid conditionally attaching unrelated properties.

```js
function applyDiscount(order, discount) {
  return {
    ...order,
    total: order.total - discount,
  };
}
```

---

## Asynchronous Code

Asynchronous work must have clear ownership and failure behavior.

- Prefer `async` and `await` when they make control flow easier to follow.
- Always await, return, track to completion, or deliberately detach a promise.
- Document intentionally detached work and handle its rejection.
- Run independent operations concurrently; await dependent operations in order.
- Use `Promise.all` when every operation must succeed and
  `Promise.allSettled` when each outcome must be inspected.
- Propagate cancellation with `AbortSignal` when the platform and operation
  support it.
- Apply explicit timeouts at external boundaries.
- Avoid `new Promise` when an existing promise can be returned directly.
- Do not mix callback and promise styles within one interface.

```js
async function loadCheckout(orderId, { signal } = {}) {
  const [order, paymentMethods] = await Promise.all([
    loadOrder(orderId, { signal }),
    loadPaymentMethods({ signal }),
  ]);

  return { order, paymentMethods };
}
```

---

## Comments and Documentation

Code should explain what it does. Comments should explain why a decision exists,
identify a non-obvious constraint, or preserve context that cannot be expressed
in code.

- Keep comments accurate or remove them.
- Do not narrate straightforward code.
- Document public APIs according to the project's documentation convention.
- Describe externally visible behavior, parameters, return values, thrown
  errors, and important side effects where they are not already obvious.
- Give TODOs an owner or issue reference when the project workflow supports it.
- Never leave commented-out code; version control already preserves history.

---

## Testing

Tests are executable descriptions of behavior.

- Name tests after the behavior and condition they verify.
- Follow Arrange–Act–Assert when it improves readability, without adding
  ceremonial comments.
- Test public behavior rather than private implementation details.
- Prefer small fixtures and factories with predictable shapes.
- Mock at system boundaries, not every collaborator.
- Keep tests deterministic. Control time, randomness, environment, and external
  services explicitly.
- Await asynchronous assertions and ensure rejected promises fail the test.
- Assert the important outcome, not every incidental detail.
- Add a regression test when fixing a defect when practical.

```js
it("rejects checkout when the coupon has expired", () => {
  const order = orderWithCoupon({ expiresOn: "2025-01-01" });

  expect(() =>
    checkout(order, { today: "2025-01-02" }),
  ).toThrow(InvalidCouponError);
});
```

---

## Backlog Chapters

These sections remain to be developed as the standards evolve:

- [ ] Runtime boundaries — browsers, Node.js, workers, edge runtimes, and
      capability detection.
- [ ] Resource management — cleanup, disposables, streams, connections, and
      transaction boundaries.
- [ ] Imports and dependency direction — package exports, circular dependencies,
      and feature boundaries.
- [ ] Logging and observability — structured context, levels, tracing, and error
      reporting.
- [ ] Configuration — environment variables, secrets, validation, and startup
      failures.
- [ ] Persistence — transaction scope, query boundaries, migrations, and domain
      mapping.
- [ ] Concurrency — workers, shared memory, synchronization, and message passing.
- [ ] Security — input validation, serialization, prototype pollution,
      subprocesses, paths, and dependency hygiene.
- [ ] Package maintenance — lockfiles, upgrades, publishing, and supply-chain
      controls.

---

## References

- [MDN JavaScript Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide)
- [ECMAScript language specification](https://tc39.es/ecma262/)
- [Node.js ECMAScript modules](https://nodejs.org/api/esm.html)
- [TypeScript documentation](https://www.typescriptlang.org/docs/)
- [TypeScript compiler options](https://www.typescriptlang.org/tsconfig/)
