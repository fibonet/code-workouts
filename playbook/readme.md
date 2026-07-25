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

> Types exist to make intent explicit. Explicit is better than implicit. Static
> guarantees are better than runtime surprises. But not at the cost of clarity.
> _Any_ type is a last resort, not a convenience. Type safety should guide
> design, not fight it. When types become hard to model, _reconsider the
> abstraction_. _Simple_ is better than _complex_, Although _complex_ is better
> than _complicated_. Inference is powerful, but _annotations_ document intent.
> Use both thoughtfully. APIs should be _typed_ at their _boundaries_. Internal
> details can evolve; _contracts must not_. Narrow types as early as possible.
> Broad types leak uncertainty. _Union types_ model reality better than
> over-generalisation. _Discriminated unions_ make it explicit. Avoid
> _unnecessary generics_. Introduce them only when they remove duplication or
> enforce invariants. A type that cannot be understood quickly is a liability.
> _Immutability_ reduces mental overhead. _Readonly_ is a tool, not a
> restriction. _Errors_ should be represented in types when possible. _Unchecked
> exceptions_ are implicit contracts. _Null_ and _undefined_ must be handled
> deliberately. Absence is part of the type system. _Third-party types_ deserve
> scrutiny. Trust, but verify. Consistency across the code base outweighs local
> preference. Strict mode is not strict enough – use it anyway. Types improve
> _communication_ between developers. The code should _explain itself before
> comments_ are needed. Prefer evolving types over bypassing them. Shortcuts
> become long-term constraints. The goal is not perfect types, but reliable
> systems. Perfection that blocks progress is failure. "Works at runtime" is not
> sufficient.

---

## Development Standards

For as long as we have been writing programs, we have been trying to write rules
for writing programs. Every generation of developers has produced its
commandments, style guides, best practices, and sacred conventions, usually with
the noblest of intentions: to make code easier to read, easier to change, and
less painful to live with. And yet, time has not been kind to most of these
rules. Languages change. Frameworks rise and fall. Teams grow, split, and forget
why a rule existed in the first place. A standard that once protected us can, if
followed blindly, become just another source of needless ceremony.

So should we abandon standards altogether? Of course not. A poor rule,
consistently applied and openly questioned, is often better than a thousand
private preferences competing in the same codebase.

The point is not obedience. The point is discipline. Every small decision (the
name of a variable, the shape of a function, the location of a constant, the
boundary of a module) should be made with intent.

Standards are useful only when they serve one purpose: helping developers
produce clean, honest, maintainable code.

> Write code a programmer can hold in one mind. If you can't reason about it,
> you can't trust it. Write for the next programmer. Clever code is expensive
> when nobody can understand it. Let business change cause one code change, in
> one place. Design for tests. Untested code is faith, not engineering. Name
> things well. Use the language of the domain, not your own private vocabulary.
> Treat mutable state with suspicion. Prefer code that behaves the same every
> time. Don't scatter magic numbers and strings. Give them names. Put them where
> they belong. Don't abbreviate unless everyone knows the abbreviation. Saving
> keystrokes is not worth losing clarity. Give every file, class, and function
> one reason to exist. Cohesion makes change safe. Delete dead code. Comments
> that replace code, unused imports, abandoned experiments, and forgotten
> dependencies only make the system harder to read. Before adding another
> helper, dependency, or abstraction, ask whether the codebase already has the
> answer. Leave the code a little cleaner than you found it. Small improvements
> compound. Big rewrites rarely do.

### TypeScript design orientation principles

- All code should be strongly typed
- Avoid `any` wherever possible
- Prefer explicit interfaces and type definitions over implicit typing
- Use typed mocks and strongly typed test utilities in tests
- Prefer ESM-friendly implementations and modern module patterns
- Avoid `@ts-expect-error` unless absolutely necessary and properly justified
- Avoid `@ts-ignore` and never suppress errors without documenting the
  underlying issue
- Ensure public APIs, utilities, and shared components expose predictable and
  maintainable typings
- Prefer type safety and explicit contracts over loosely typed implementations

Strong typing improves maintainability, developer experience, refactor safety,
and long-term reliability across the codebase.

---

## Naming Conventions

Names are not decorations. They are part of the program. Read a name in the
sentence where it will live before you commit to it.

Spend more time naming than typing. A good name is cheaper than a good comment,
and it keeps paying that debt back every time the code is read.

Name things so the code reads like a story. If the sentence sounds awkward, the
name is probably wrong.

Choose names that reveal intent, not implementation. Readers should understand
_why_ something exists before they need to understand _how_ it works.

Make names answer questions, not raise them. Every moment of doubt becomes a
pause in the reader's flow.

### Naming data symbols

Use nouns for variables, constants and parameters, but remember that English
grammar still matters: collections deserve plural names, and individual elements
deserve singular names.

```ts
for (const order of orders) {
    ...
}
```

