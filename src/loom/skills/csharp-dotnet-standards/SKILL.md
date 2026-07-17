---
name: csharp-dotnet-standards
description: >-
  Enforces .NET 9 / C# 13 conventions including clean architecture layering,
  nullable reference types, async/await patterns, DI lifetimes, and xUnit
  testing. Use when generating, reviewing, or refactoring C# (.cs) code or
  .NET project files.
license: MIT
compatibility: .NET 9+, C# 13
metadata:
  author: Shariq Khan
  version: "1.0.0"
---

# C# / .NET Standards

## Core rules
1. Clean Architecture: Domain / Application / Infrastructure / Presentation.
2. Nullable reference types ON at project level.
3. Async everywhere: `Task<T>`, `ConfigureAwait(false)` in library code.
4. DI lifetimes: Scoped for per-request, Singleton for stateless services.
5. Records for DTOs, sealed classes by default.
6. Structured logging via `ILogger<T>`. No `Console.WriteLine`.
7. xUnit + FluentAssertions + NSubstitute. AAA pattern.

## When to load references
- New project layout → `references/clean-architecture-layout.md`
- Async questions → `references/async-antipatterns.md`
- Style setup → copy `scripts/.editorconfig` and `scripts/Directory.Build.props`

## Definition of done
- Build passes with 0 warnings
- Tests for every public method on Application layer services