# The Clean Coder's Playbook

Software should be easy to understand, easy to verify, and inexpensive to
change.

This playbook begins with the discipline of structured programming and the
feedback-driven practices of eXtreme Programming:

- Structured programming guides how we construct understandable code.
- Extreme Programming guides how we safely discover, validate, and evolve it.

The rules that follow are guidance for engineering judgement, not a catalogue
of rituals. Apply them in context, challenge them with evidence, and prefer the
principle behind a rule over mechanical compliance.


## How to Read This Playbook

The guidance is organised as a hierarchy:

> **Values → Principles → Practices → Context-specific rules → Examples**

Values and principles should remain durable. Practices and rules may change
with the language, system, team, and problem.

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


## Incremental Development

- Work in small, complete, verifiable changes.
- Keep the system working throughout development.
- Integrate frequently.
- Refactor continuously while tests protect existing behaviour.
- Separate behavioural changes from structural changes when that improves
  reviewability.
- Prefer reversible decisions when uncertainty is high.
- Deliver the smallest useful slice and learn from it.

Small steps reduce risk, shorten feedback loops, and make mistakes easier to
locate and reverse.


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

Choose deliberately, document consequential trade-offs, and revise the decision
when the context changes.


## Language-specific Guidance

- [JavaScript and TypeScript](js-guide.md)
- [Python](py-guide.md)
