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

The point is not obedience. The point is discipline. Every small decision (
