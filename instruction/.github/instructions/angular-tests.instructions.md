---
name: 'Angular unit tests (Jest)'
description: 'Use when creating or editing Jest spec files.'
applyTo: '**/*.spec.ts'
---

# Unit tests (Jest)

- Spec beside source (`*.spec.ts`); HTTP/transport mocks in the owning API folder as `*.mock.ts`, never inside the spec. Pure utils get `*.util.spec.ts` beside the util.
- `TestBed.configureTestingModule`; mock deps (`HttpClientTestingModule`, `jest.spyOn`, `provideMockStore` for NgRx).
- Prefer `autoId` selectors (`querySelector('[autoId=\"...\"]')`) over fragile CSS/text. Fail-first (red) then green.
- Always add/update `autoId` on touched interactive/viewable template elements (see `.github/skills/ui-autoid/SKILL.md`).
- Details: `.github/skills/unit-test/SKILL.md`.
