## Summary

> Brief description of the changes made and why.

## Ticket

- **Jira**: `SP0168-<ticket number>`
- **Commit prefix**: `SP0168-<ticket number>: <short summary>`

## Type of Change

- [ ] Bug Fix
- [ ] Feature Delivery
- [ ] Refactor
- [ ] Unit Test
- [ ] Documentation / Framework

## Files Modified

| File | Change |
| :--- | :--- |
| `src/...` | _What changed and why_ |

## Validation Evidence

- [ ] `npm run lint` — passed
- [ ] `npm run format` — passed
- [ ] `npm run test` — passed (attach summary)
- [ ] `npm run build` — passed

<details>
<summary>Test output</summary>

```
Paste test output here
```

</details>

## Checklist

- [ ] No `any` types introduced; interfaces/models reused from `src/models/`
- [ ] No duplicate logic — existing services/constants/components reused
- [ ] No unused imports, variables, or commented-out code
- [ ] No credentials, keys, or tokens committed
- [ ] Follows Angular 15 module patterns (no standalone components)
- [ ] SCSS follows `@import` at top + design system variables
- [ ] Services imported via `@services/*` specific path (no barrel/relative)
- [ ] Report artifact `*.ctx.md` saved to `.github/reports/`

## Risk Assessment

- **Backward Compatibility**: [Yes / No — explain]
- **Risks & Mitigation**: [describe]

## References

- Report: `/.github/reports/<report-file>.ctx.md`
- Related PRs/commits (if any)