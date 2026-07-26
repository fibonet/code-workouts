# Object Calisthenics

Object Calisthenics is a set of nine programming exercises introduced by Jeff Bay in *The ThoughtWorks Anthology*. The rules are deliberately restrictive. Their purpose is not to define a universal coding standard, but to force developers to practice encapsulation, cohesion, clear naming, and responsibility-driven object-oriented design.

Bay originally suggested applying the rules strictly to a small project of roughly 1,000 lines. After completing the exercise, the rules can be treated as design heuristics rather than absolute laws.

## The Nine Rules

1. Use only one level of indentation per method.
2. Do not use the `else` keyword.
3. Wrap all primitives and strings.
4. Use first-class collections.
5. Use only one dot per line.
6. Do not abbreviate names.
7. Keep all entities small.
8. Do not use classes with more than two instance variables.
9. Do not use getters, setters, or properties.

## 1. Use Only One Level of Indentation per Method

Deep indentation is often a sign that a method is doing too much. Extract nested logic into well-named methods so that each method stays at a consistent level of abstraction.

Instead of:

```ts
for (const order of orders) {
  if (order.isPaid) {
    for (const item of order.items) {
      ship(item);
    }
  }
}
```

Prefer:

```ts
for (const order of orders) {
  shipPaidOrder(order);
}
```

Durable principle: keep control flow shallow and each method focused on one conceptual operation.

## 2. Do Not Use the `else` Keyword

The exercise encourages guard clauses, early returns, polymorphism, and explicit alternatives. These techniques often make the main path easier to see.

Instead of:

```ts
function publish(article: Article) {
  if (article.isValid()) {
    article.publish();
  } else {
    reportValidationErrors(article);
  }
}
```

Prefer:

```ts
function publish(article: Article) {
  if (!article.isValid()) {
    reportValidationErrors(article);
    return;
  }

  article.publish();
}
```

Durable principle: reduce branching and make exceptional conditions explicit.

## 3. Wrap All Primitives and Strings

A primitive often carries domain meaning that its basic type cannot express. A dedicated type can validate its value and keep related behavior in one place.

Instead of passing a plain string everywhere:

```ts
function sendEmail(address: string) {
  // ...
}
```

Represent the concept explicitly:

```ts
class EmailAddress {
  constructor(readonly value: string) {
    if (!value.includes('@')) {
      throw new Error('Invalid email address');
    }
  }
}
```

Durable principle: represent important domain concepts explicitly, especially when they have validation rules or behavior.

## 4. Use First-Class Collections

If a class contains a collection, the exercise says that it should contain no other instance variables. Operations involving that collection should live with it.

Instead of repeatedly filtering a raw array:

```ts
const activeUsers = users.filter((user) => user.isActive);
```

Create an object that owns the collection behavior:

```ts
class Users {
  constructor(private readonly items: User[]) {}

  active(): User[] {
    return this.items.filter((user) => user.isActive);
  }
}
```

Durable principle: keep collection-specific rules and behavior close to the collection.

## 5. Use Only One Dot per Line

This is the rule commonly remembered as "do not use more than one dot on one line." It discourages reaching through one object to manipulate another object's internals.

Instead of:

```ts
dog.tail.wag();
```

Prefer:

```ts
dog.expressHappiness();
```

The caller should tell `dog` what outcome it wants instead of navigating through `dog` to find the object that performs the operation.

This rule is closely related to the Law of Demeter:

> An object should communicate only with its immediate collaborators.

The rule is not literally about punctuation. Fluent APIs, namespaces, optional chaining, and decimal numbers can contain multiple dots without violating the underlying design principle.

Durable principle: tell objects what to do; do not navigate and manipulate their internal object graphs.

## 6. Do Not Abbreviate Names

Abbreviations save a few keystrokes but transfer interpretation work to every reader. Use names that communicate their meaning in the current context.

Instead of:

```ts
const usrMgr = new UserManager();
```

Prefer:

```ts
const userManager = new UserManager();
```

Long names can also reveal an overly broad responsibility. If a clear name becomes awkwardly long, the underlying concept may need to be simplified or split.

Durable principle: choose clear, contextual names and avoid unnecessary decoding.

## 7. Keep All Entities Small

The original exercise imposes strict size limits on packages, classes, and methods. The exact numbers matter less than the pressure they create to separate responsibilities.

Small entities are easier to:

- understand;
- name;
- test;
- reuse;
- replace;
- review.

Durable principle: keep components cohesive and small enough to understand without excessive context.

## 8. Do Not Use Classes With More Than Two Instance Variables

This extreme constraint forces developers to look for groups of state that belong together as separate concepts.

For example:

```ts
class Customer {
  constructor(
    private readonly street: string,
    private readonly city: string,
    private readonly postalCode: string,
  ) {}
}
```

may reveal a missing abstraction:

```ts
class Address {
  constructor(
    private readonly street: string,
    private readonly city: string,
    private readonly postalCode: string,
  ) {}
}

class Customer {
  constructor(private readonly address: Address) {}
}
```

The example still gives `Address` three fields because the production lesson is cohesion, not blind compliance with the exercise.

Durable principle: group related state into cohesive concepts and keep object state minimal.

## 9. Do Not Use Getters, Setters, or Properties

Getters and setters can expose an object's internal representation while preserving only the appearance of encapsulation.

Instead of asking for data and making a decision elsewhere:

```ts
if (account.balance >= amount) {
  account.balance -= amount;
}
```

Ask the object to perform the behavior:

```ts
account.withdraw(amount);
```

The object can then protect its own invariants:

```ts
class Account {
  constructor(private balance: number) {}

  withdraw(amount: number) {
    if (amount > this.balance) {
      throw new Error('Insufficient funds');
    }

    this.balance -= amount;
  }
}
```

Durable principle: expose behavior instead of internal representation, and let objects protect their own invariants.

## From Exercises to Engineering Principles

| Exercise rule | Durable principle |
| --- | --- |
| One indentation level | Keep control flow shallow |
| No `else` | Prefer guard clauses and explicit alternatives |
| Wrap primitives | Represent domain concepts explicitly |
| First-class collections | Keep collection behavior with the collection |
| One dot per line | Tell objects what to do; do not navigate their internals |
| No abbreviations | Use clear, contextual names |
| Small entities | Keep responsibilities focused |
| Two instance variables | Prefer cohesive objects with little state |
| No getters or setters | Expose behavior instead of internal representation |

## How to Use These Rules

Object Calisthenics works best as a deliberate practice exercise:

1. Choose a small, self-contained project.
2. Apply all nine rules strictly.
3. Notice where each constraint creates friction.
4. Identify the design problem exposed by that friction.
5. Refactor toward clearer responsibilities and stronger encapsulation.
6. After the exercise, retain the principles without treating the literal rules as dogma.

The important question is not:

> Did this code obey every rule?

It is:

> What design weakness was the rule trying to make visible?

## Relationship to Extreme Programming

Object Calisthenics is not part of the original Extreme Programming rule set. However, it fits naturally with XP practices:

- simple design;
- continuous refactoring;
- test-driven development;
- shared coding standards;
- collective code ownership.

Extreme Programming describes how a team can safely evolve software through rapid feedback. Object Calisthenics provides exercises for improving the internal design of the code being evolved.

## References

- Jeff Bay, "Object Calisthenics," in *The ThoughtWorks Anthology*: <https://www.bennadel.com/resources/uploads/2012/objectcalisthenics.pdf>
- Mark Needham, "Object Calisthenics: First Thoughts": <https://www.markhneedham.com/blog/2008/11/06/object-calisthenics-first-thoughts/>
