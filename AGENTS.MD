# AGENTS.md

These instructions apply to all Codex work in this repository.

Codex must prioritize correctness, testability, clear layering, and readable code. Do not start implementation from assumptions. Start from a referenced story or requirement, write tests first, place logic in the correct layer, and return clear outcomes for both successful and blocked actions.

The goal is to keep the code easy to understand, easy to test, and safe to change.

## How Codex Should Work

Before changing code:

1. Read the referenced story or task.
2. Identify the affected layer.
3. If requirements are unclear, stop and ask for clarification.
4. Write or update tests before implementation.
5. Run the relevant tests and confirm they fail for the expected reason.
6. Make the smallest implementation change needed.
7. Run tests again.
8. Refactor while keeping tests green.
9. Summarize what changed, what was tested, and any follow-up questions.

## Core Rules

- Use test-driven development.
- Use a layered architecture.
- Start implementation from stories referenced in the Codex interface.
- Do not write code when the story or requirements are unclear.
- Keep code readable and explicit.
- Put each piece of logic in the correct layer.
- Create helper functions for logic that is repeated or hard to read.
- Use inline comments when they make the code easier to understand.

## Story Sources

Stories may be referenced in the Codex prompt, issue tracker, project documentation, or another source provided by the user.

If a story ID, issue link, or requirement document is referenced:

- Read it before editing code.
- Treat it as the source of truth.
- Do not infer missing acceptance criteria.
- If the story conflicts with this file, ask which source should take precedence.
- If the story is unclear, contradictory, or incomplete, ask focused clarification questions before coding.

## Stop Conditions

Do not write or change code when:

- The story does not identify the user or business goal.
- Success and failure behavior are unclear.
- The affected system scope is unclear.
- The trusted data source is unknown.
- The requested change conflicts with existing behavior or documentation.
- A rule is described as both current behavior and future improvement.
- It is unclear whether the behavior applies to all member types or only specific member types.

When blocked, ask focused questions instead of guessing.

Useful questions include:

- Which user is this story for?
- What should the user see when this rule blocks an action?
- Is this a current-state rule or a future improvement?
- Should this behavior apply to all member types?
- What data source should be trusted for this behavior?
- Which parts of the system are in scope?

## Story-First Development

Development starts from a clear story.

Before writing tests or implementation code, confirm that the story explains:

- What problem we are solving
- Who the user is
- What behavior should change
- What should happen when the action succeeds
- What should happen when the action is blocked or fails
- Which parts of the system are in scope

If the story is not completely clear, do not start coding yet.

If something is unclear, contradictory, or likely to block development, ask the user to refine the requirements first.

## Test-Driven Development

Write tests before writing implementation code.

Use this cycle:

1. Write a failing test for the behavior we want.
2. Run the test and confirm that it fails for the expected reason.
3. Write the smallest amount of code needed to pass the test.
4. Run the tests again.
5. Refactor the code while keeping the tests green.

Tests should describe business behavior, not just technical details.

Good test focus:

- A member can borrow a book when all rules allow it.
- A suspended member is blocked from borrowing.
- A reference-only book cannot be borrowed by a normal member.
- A due date is calculated correctly.
- A clear reason is returned when an action is not allowed.

Avoid tests that only check implementation details, such as the name of a private helper function.

## Test Naming

Name tests after business behavior.

Prefer:

- `test_suspended_member_cannot_borrow_book`
- `test_reference_only_book_is_blocked_for_normal_member`
- `test_due_date_excludes_library_holidays`
- `test_blocked_checkout_returns_clear_reason`

Avoid:

- `test_helper`
- `test_checkout_works`
- `test_function_returns_false`
- `test_case_1`

## Layered Architecture

The application should be split into clear layers. Each layer has its own responsibility.

Use the existing project structure when it is clear. If the project structure is not clear yet, use these conceptual layers:

- Presentation layer
- Application layer
- Service layer
- Domain layer
- Data layer

### Presentation Layer

This layer handles user interaction.

Examples:

- Frontend screens
- Forms
- Buttons
- API route handlers
- Request and response formatting

Rules:

- Do not put business rules here.
- Do not calculate loan eligibility here.
- Do not directly access storage here unless the architecture explicitly allows it through a service.
- Keep request parsing and response formatting separate from business decisions.

### Application Layer

This layer coordinates use cases.

Examples:

- Check out a book
- Return a book
- Renew a loan
- Place a hold
- Show a member overview

Rules:

- Call service-layer logic to make decisions.
- Call repositories or data access helpers to load and save data.
- Keep orchestration readable.
- Return clear result objects that the frontend or API can use.
- Do not hide business rules inside orchestration code.

### Service Layer

This layer contains business logic and business decisions.

Examples:

- Checking if a member may borrow a book
- Calculating a due date
- Deciding whether a loan can be renewed
- Applying overdue fees
- Explaining why an action is blocked

Rules:

- Business rules belong here.
- Use domain objects as input and output.
- Keep rule outcomes explicit, especially when something is not allowed.
- Create helper functions when a rule becomes hard to read.
- Do not put request formatting, screen logic, or storage code here.

### Domain Layer

This layer contains the business objects and business concepts.

Examples:

- Book
- Member
- Loan
- Hold
- Policy
- Holiday
- Member type
- Loan state

Rules:

- Define the information the business works with.
- Keep objects clear and meaningful.
- Use names that match the business language.
- Keep this layer independent from the frontend.
- Do not put orchestration, API handling, or data access here.
- Only add small object-level helpers here when they describe the object itself.

### Data Layer

This layer handles storage and retrieval.

Examples:

- Reading CSV files
- Database queries
- Repository classes
- Data mapping

Rules:

- Do not put business rules here.
- Keep data access separate from decision making.
- Convert raw data into clear application or domain objects.
- Keep database queries, file access, and mapping logic isolated from business decisions.

## Project Structure

Use the existing folder structure if the project already has one.

If there is no clear structure yet, use folders that map to the architecture:

- `presentation/` or `routes/`: user interaction, API handlers, request/response formatting
- `application/`: use-case orchestration
- `services/`: business rules and decisions
- `domain/`: business objects and value concepts
- `data/` or `repositories/`: storage, retrieval, and mapping
- `tests/`: automated tests

If the existing codebase uses different names, follow the existing names but preserve the same separation of responsibilities.

## Result Objects

Use explicit result objects for application and service outcomes.

A blocked or failed action should include:

- `success`: `false`
- `code`: stable machine-readable reason
- `message`: readable explanation
- `context`: relevant details needed by the caller

A successful action should include:

- `success`: `true`
- Relevant domain or application data
- No vague status-only response

Avoid returning only booleans for business decisions when the caller needs to explain the outcome to a user.

Good blocked result example:

```text
Code: SUSPENDED
Message: This member is suspended until 2026-02-15.
```
