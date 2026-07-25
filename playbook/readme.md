# The Clean Coder's Playbook

##### Disclaimer
> *"I hate code, and I want as little of it as possible in our products."* – J. Diederich

We do not create value by writing more code; we create value by adding more features.
This document should therefore be read as guidance for judgement, not a catalogue of rituals. Prefer clarity over cleverness, consistency over personal taste, and maintainability over short-term convenience. Add code when it earns its place; remove it when it no longer does.

---

## Table of Contents
- [🧭 The Zen of TypeScript gurus](#-the-zen-of-typescript-gurus)
- [Development Standards](#development-standards)
  - [TypeScript design orientation principles](#typescript-design-orientation-principles)
- [Naming Conventions](#naming-conventions)
  - [Naming data symbols](#naming-data-symbols)
  - [Naming behaviour symbols](#naming-behaviour-symbols)
  - [Events](#events)
    - [Include the business concept in the name](#include-the-business-concept-in-the-name)
  - [Exceptions](#exceptions)
    - [Name the problem, not the implementation](#name-the-problem-not-the-implementation)
    - [Describe the violated expectation](#describe-the-violated-expectation)
  - [File Naming](#file-naming)
  - [React Components](#react-components)
  - [Hooks](#hooks)
- [Backlog chapters](#backlog-chapters)
  - [High-priority placeholders](#high-priority-placeholders)
  - [Medium-priority placeholders](#medium-priority-placeholders)
- [References](#references)
  - [Coding Standards - Front-end](#coding-standards---front-end)
  - [Code Review Guidelines](#code-review-guidelines)

---

## 🧭 The Zen of TypeScript gurus

> Types exist to make intent explicit.
> Explicit is better than implicit.
> Static guarantees are better than runtime surprises.
> But not at the cost of clarity.
> *Any* type is a last resort, not a convenience.
> Type safety should guide design, not fight it.
> When types become hard to model, *reconsider the abstraction*.
> *Simple* is better than *complex*,
> Although *complex* is better than *complicated*.
> Inference is powerful, but *annotations* document intent.
> Use both thoughtfully.
> APIs should be *typed* at their *boundaries*.
> Internal details can evolve; *contracts must not*.
> Narrow types as early as possible.
> Broad types leak uncertainty.
> *Union types* model reality better than over-generalisation.
> *Discriminated unions* make it explicit.
> Avoid *unnecessary generics*.
> Introduce them only when they remove duplication or enforce invariants.
> A type that cannot be understood quickly is a liability.
> *Immutability* reduces mental overhead.
> *Readonly* is a tool, not a restriction.
> *Errors* should be represented in types when possible.
> *Unchecked exceptions* are implicit contracts.
> *Null* and *undefined* must be handled deliberately.
> Absence is part of the type system.
> *Third-party types* deserve scrutiny.
> Trust, but verify.
> Consistency across the code base outweighs local preference.
> Strict mode is not strict enough – use it anyway.
> Types improve *communication* between developers.
> The code should *explain itself before comments* are needed.
> Prefer evolving types over bypassing them.
> Shortcuts become long-term constraints.
> The goal is not perfect types, but reliable systems.
> Perfection that blocks progress is failure.
> "Works at runtime" is not sufficient.

---

## Development Standards

For as long as we have been writing programs, we have been trying to write rules for writing programs.
Every generation of developers has produced its commandments, style guides, best practices, and sacred conventions, usually with the noblest of intentions: to make code easier to read, easier to change, and less painful to live with. And yet, time has not been kind to most of these rules. Languages change. Frameworks rise and fall. Teams grow, split, and forget why a rule existed in the first place. A standard that once protected us can, if followed blindly, become just another source of needless ceremony.

So should we abandon standards altogether? Of course not. A poor rule, consistently applied and openly questioned, is often better than a thousand private preferences competing in the same codebase.

The point is not obedience. The point is discipline. Every small decision (the name of a variable, the shape of a function, the location of a constant, the boundary of a module) should be made with intent.

Standards are useful only when they serve one purpose: helping developers produce clean, honest, maintainable code.

> Write code a programmer can hold in one mind. If you can't reason about it, you can't trust it.
> Write for the next programmer. Clever code is expensive when nobody can understand it.
> Let business change cause one code change, in one place.
> Design for tests. Untested code is faith, not engineering.
> Name things well. Use the language of the domain, not your own private vocabulary.
> Treat mutable state with suspicion. Prefer code that behaves the same every time.
> Don't scatter magic numbers and strings. Give them names. Put them where they belong.
> Don't abbreviate unless everyone knows the abbreviation. Saving keystrokes is not worth losing clarity.
> Give every file, class, and function one reason to exist. Cohesion makes change safe.
> Delete dead code. Comments that replace code, unused imports, abandoned experiments, and forgotten dependencies only make the system harder to read.
> Before adding another helper, dependency, or abstraction, ask whether the codebase already has the answer.
> Leave the code a little cleaner than you found it. Small improvements compound. Big rewrites rarely do.

### TypeScript design orientation principles

- All code should be strongly typed
- Avoid `any` wherever possible
- Prefer explicit interfaces and type definitions over implicit typing
- Use typed mocks and strongly typed test utilities in tests
- Prefer ESM-friendly implementations and modern module patterns
- Avoid `@ts-expect-error` unless absolutely necessary and properly justified
- Avoid `@ts-ignore` and never suppress errors without documenting the underlying issue
- Ensure public APIs, utilities, and shared components expose predictable and maintainable typings
- Prefer type safety and explicit contracts over loosely typed implementations

Strong typing improves maintainability, developer experience, refactor safety, and long-term reliability across the codebase.

---

## Naming Conventions

Names are not decorations. They are part of the program. Read a name in the sentence where it will live before you commit to it.

Spend more time naming than typing. A good name is cheaper than a good comment, and it keeps paying that debt back every time the code is read.

Name things so the code reads like a story. If the sentence sounds awkward, the name is probably wrong.

Choose names that reveal intent, not implementation. Readers should understand *why* something exists before they need to understand *how* it works.

Make names answer questions, not raise them. Every moment of doubt becomes a pause in the reader's flow.

### Naming data symbols

Use nouns for variables, constants and parameters, but remember that English grammar still matters: collections deserve plural names, and individual elements deserve singular names.

```ts
for (const order of orders) {
    ...
}
```

Never encode today's implementation into tomorrow's name. `userMap`, `userArray`, and `cachedList` become lies as the design evolves. Name the concept, not the container.

A boolean should read like a question:

```ts
if (isAnonymous) ...
if (user.hasPermission) ...
if (order.isPaid) ...
if (isLoading) ...
if (hasError) ...
if (canSubmit) ...
if (shouldRender) ...
```

Avoid ambiguous or unclear names such as:

```ts
if (loadingFlag) ...
if (status) ...
if (checkError) ...
```

Do not be afraid to introduce explanatory symbols when they make the code clearer:

```ts
const outOfStockProducts = products.filter(product => product.stock <= 0);

for (const product of outOfStockProducts) {
    product.colour = "grey";
}
```

Every name should earn its place. If replacing it with `thing` changes nothing, the name tells you nothing. Avoid generic names that say nothing about their contents, such as `data`, `object`, or `instance`.

### Naming behaviour symbols

Function names should use expressive verbs that describe the effect. Prefer `discardInactiveConnections` over `inactiveConnectionsCleanup`.

Examples:

```ts
getProductPrice()
formatCurrency()
buildSearchPayload()
```

Do not abbreviate thought. Saving four characters is not worth costing every reader four seconds.

If two names are easy to confuse, they are wrong, even if both are technically correct.

A name should fit naturally everywhere it appears: in assignments, conditions, loops, and method calls. Read those lines aloud. If they sound unnatural, rename them. Good code should read like plain English.

```ts
const pendingStatuses = new Set([
    OrderStatus.Open,
    OrderStatus.Processing,
    OrderStatus.AwaitingPayment,
]);

const pendingOrders = orders.filter(order => pendingStatuses.has(order.status));

while (pendingOrders.length > 0) {
    const order = pendingOrders.shift();
    ...
}
```

The code explains itself.

Name symbols by looking at how they are used, not only where they are declared. When choosing a name, imagine how it will look in different contexts:

```ts
if (?)
return ?;
for (const ? of ?)
logger.info({ ? });
process(?);
```

If every one of those lines reads naturally, you have probably found the right name. That is a surprisingly effective litmus test.

### Events

An event names something that happened, not something that should happen.

Events describe facts. Commands describe intent.

```ts
// ✓ Events
orderPlaced
paymentAuthorized
emailSent
userSignedIn

// ✗ Commands
placeOrder
authorizePayment
sendEmail
signInUser
```

Prefer the past tense. If it happened, say so.

```ts
userCreated
orderCancelled
paymentFailed
cacheInvalidated
```

Avoid:

```ts
createUserEvent
cancelOrderEvent
paymentFailure
cacheInvalidate
```

The `Event` suffix adds no information. The imperative tense (`createUser`, `cacheInvalidate`) blurs the line between events and commands. Nominalizations (`paymentFailure`) obscure the timeline — prefer `paymentFailed`.

#### Include the business concept in the name

Good:

```ts
checkoutCompleted
inventoryReserved
refundIssued
```

Poor:

```ts
completed
success
done
updated
```

An event should still make sense when it appears alone in a log.

### Exceptions

An error should answer one question:

> What prevented the operation from succeeding?

Not:

> Where did the code happen to throw?

TypeScript has no typed catch clause. Because you cannot dispatch on error type at the language level, error design must compensate: use structured data and narrow type guards instead of relying on class hierarchies alone.

Errors are not just failures. They are information. Give them names that describe the category and data that describe the cause.

#### Name the problem, not the implementation

Good:

```ts
ProductNotFound
PaymentDeclined
SessionExpired
InvalidCoupon
```

Poor:

```ts
ApiError
ServiceError
RepositoryError
HelperError
```

Those tell you where the error came from, not what happened.

Avoid the `Error` or `Exception` suffix altogether, as it is obvious from the code that anything that follows a throw statement is an exception. But you have to choose the name carefully to indicate the problem you want to capture.

#### Describe the violated expectation

Good:

```ts
MissingAuthorization
UnsupportedCurrency
DuplicateOrder
OrderAlreadyPaid
```

These read naturally:

```ts
throw new OrderAlreadyPaid(orderId);
```

Prefer errors that carry structured information over errors that rely only on class names.

Example:

```ts
class PaymentFailed extends Error {
  constructor(
    message: string,
    readonly reason: 'declined' | 'expired_card' | 'insufficient_funds',
  ) {
    super(message);
  }
}
```

Use error names for the category. Use properties for the details.

```
PaymentFailed
  └── reason: 'declined'

OrderSkipped
  └── reason: 'already_paid'

NotAuthorized
  └── reason: 'expired_token'
```

Rather than creating hundreds of classes:

```ts
PaymentDeclined
PaymentExpiredCard
PaymentInsufficientFunds
```

Unless those cases genuinely have different handling.

Do not create an error type for every sentence. Create types around decisions the caller must make.

### File Naming

Use hyphen-case, also known as kebab-case, for ordinary file names.

Examples:

```
product-card.tsx
mobile-navigation.ts
```

File names should be descriptive and predictable. Their location should also remain stable when the code is refactored.

Keep files that change together close together.

Avoid organising files around technical type hierarchies. Do not create catch-all files such as `constants.ts`, `types.ts`, `views.ts`, or `buttons.ts` just because a framework appears to encourage it. Prefer folders that group related features and responsibilities together.

Start with a single file that serves one clear purpose. When that file grows large enough to become difficult to understand, for example above 300 lines, split it in a sensible way that preserves cohesion.

### React Components

Use PascalCase for React component names and component file names.

Examples:

```
ProductCard.tsx
SearchFilters.tsx
```

- File names should match component names.
- Component names should clearly communicate responsibility and intent.

### Hooks

Custom hooks should:

- Always start with `use`.
- Clearly communicate behaviour or responsibility.

Examples:

```
useProductSearch.ts
useDebounce.ts
```

---

## Backlog chapters

These sections are intentionally kept as lightweight placeholders for now. We will address them one by one as the standards evolve.

### High-priority placeholders

- [ ] Functions / function design — size, responsibility, parameters, purity, guard clauses, and when to split behaviour.
- [ ] Error handling patterns — propagation, boundaries, throw vs return, typed errors, and React error boundaries.
- [ ] Comments and documentation — when comments help, when they hide problems, JSDoc expectations, and TODO/FIXME conventions.
- [ ] Testing conventions — test structure, naming, mocking philosophy, typed test utilities, and what belongs in unit/integration/e2e tests.
- [ ] Async patterns — async/await, floating promises, cancellation, retries, race conditions, and async error handling.
- [ ] Conditionals and control flow — guard clauses, early returns, nesting limits, ternaries, and readability of branching logic.

### Medium-priority placeholders

- [ ] Imports and module structure — ordering, barrel files, dependency direction, circular dependencies, and feature boundaries.
- [ ] Constants, enums, and configuration — magic values, placement, naming, union types vs enums, and environment configuration.
- [ ] Immutability in practice — readonly types, object and array updates, mutation boundaries, and when mutation is acceptable.
- [ ] React component patterns — props design, composition, component splitting, render logic, and controlled vs uncontrolled components.
- [ ] State management — local vs global state, derived state, lifting state, co-location, and avoiding duplicated state.
- [ ] Logging and observability — what to log, log levels, structured context, tracing, and useful diagnostics.

---

## References

### Coding Standards - Front-end

Detailed Read — https://kfplc.atlassian.net/wiki/spaces/NGE/pages/262348479

### Code Review Guidelines

Detailed Read — https://kfplc.atlassian.net/wiki/spaces/NGE/pages/255230201
