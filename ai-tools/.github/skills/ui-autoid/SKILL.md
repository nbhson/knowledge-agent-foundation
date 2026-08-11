---
name: ui-autoid
description: Guidelines for adding autoId attributes to HTML elements to support UI automation testing (clickable and viewable elements) in the Horizon 2 UI project.
---

# UI Automation autoId Attribute

This skill enforces consistent `autoId` attributes on HTML elements to support UI automation testing (Playwright, Selenium, Cypress). Every interactive or viewable element must expose a stable `autoId` that automation can target instead of brittle CSS/text selectors.

---

## 1. When to Add `autoId`

Add `autoId` to:

- **Clickable / Interactive**: buttons, icon buttons, hyperlinks, navbar items, tabs, breadcrumbs, dropdowns, selects, checkboxes, radios, pagination controls, elements with `(click)` handler or router link.
- **Viewable / Assertable**: page titles/headings, labels, table headers, toast/messages, empty/loading/error states.

Do **not** add to purely decorative elements.

---

## 2. Naming Convention

```
<pageName>-<contextLevel1>-<contextLevel2>-...-<elementId>
```

The middle context levels are **flexible** — mirror the actual UI/DOM hierarchy. There is **no fixed number of levels**: use as many (or as few) as needed to uniquely and clearly locate the element (e.g., `tab → section → form → element`).

| Segment | Description | Example |
| :--- | :--- | :--- |
| `pageName` | Page/screen name (camelCase) | `studyLandingPage` |
| `contextLevelN` | One or more context levels mirroring the page structure: tab, section, panel, form, toolbar, header, position, etc. (camelCase) | `toolbar`, `header`, `filtersPanel`, `detailsTab`, `profileSection`, `editForm` |
| `elementId` | Short descriptive identifier (camelCase) | `downLoadBtn`, `searchInput` |

**Element suffix table** (for `elementId`):

| Element Type | Suffix | Example |
| :--- | :--- | :--- |
| Button | `Btn` | `downLoadBtn`, `saveBtn` |
| Input / Text field | `Input` | `searchInput` |
| Link / Anchor | `Link` | `viewAllLink` |
| Dropdown / Select | `Dropdown` / `Select` | `statusDropdown` |
| Checkbox | `Checkbox` | `agreeCheckbox` |
| Radio | `Radio` | `priorityRadio` |
| Title / Heading | `Title` | `pageTitle` |
| Label | `Label` | `userNameLabel` |
| Table header | `Header` | `totalAmountHeader` |
| Toast / Message | `Message` | `saveSuccessMessage` |
| Tab | `Tab` | `overviewTab` |
| Pagination | `Pagination` | `paginationBar`, `nextPageBtn` |
| Navbar / Menu item | `Item` | `profileMenuItem` |
| Icon button | `IconBtn` | `settingsIconBtn` |

**Examples**:

| Element | autoId |
| :--- | :--- |
| Download button (study landing toolbar) | `studyLandingPage-toolbar-downLoadBtn` |
| Search input (reports filters panel) | `reportsPage-filtersPanel-searchInput` |
| Page title (admin dashboard header) | `adminDashboard-header-pageTitle` |
| Save button (budget request form footer) | `budgetRequestPage-formFooter-saveBtn` |
| Next page button (tracker pagination) | `trackerPage-pagination-nextPageBtn` |
| Username label (profile sidebar) | `profilePage-sidebar-userNameLabel` |
| First name input (admin, user details tab, edit profile section, edit form) | `adminPage-userDetailsTab-editProfileSection-editForm-firstNameInput` |
| Cancel button (purchase order, approval tab, budget check panel, reject dialog) | `purchaseOrderPage-approvalTab-budgetCheckPanel-rejectDialog-cancelBtn` |

---

## 3. How to Apply in Angular 15 Templates

Use `autoId="..."` (static) or `[attr.autoId]="'...'"` (dynamic). Never use `[autoId]` (property binding — no native `autoId` DOM property).

```html
<!-- Static -->
<button autoId="studyLandingPage-toolbar-downLoadBtn" (click)="download()">Download</button>

<!-- Dynamic (in loop) - suffix with index/key -->
<button *ngFor="let item of items; let i = index; trackBy: trackById"
        [attr.autoId]="'trackerPage-dataTable-rowActionBtn-' + i"
        (click)="onAction(item)">Action</button>

<!-- Router link / navbar -->
<a autoId="studyLandingPage-navbar-studyNavItem" routerLink="/study" routerLinkActive="active">Study</a>

<!-- Title / label -->
<h1 autoId="studyLandingPage-header-pageTitle">Study Landing</h1>
<span autoId="profilePage-sidebar-userNameLabel">{{ userName }}</span>

<!-- Form control (multi-level context: tab → section → form) -->
<input autoId="adminPage-userDetailsTab-editProfileSection-editForm-firstNameInput"
       formControlName="firstName" type="text" />
<mat-select autoId="reportsPage-filtersPanel-statusDropdown" formControlName="status">...</mat-select>
```

---

## 4. Rules & Best Practices

1. **Uniqueness**: Each `autoId` must be unique within its page.
2. **Stability**: `autoId` values are part of the automation contract — treat like public API. Do not rename casually.
3. **Readability**: Use meaning names, not `btn-1`.
4. **No random values**: Never use random/timestamp values (loop index is acceptable, deterministic).
5. **Attributes only**: Use `autoId="..."` or `[attr.autoId]="'...'"`, never `[autoId]`.
6. **Context levels mirror the UI hierarchy**: Include only context levels that meaningfully help locate the element (tab, section, panel, form, toolbar...). Do not pad with unnecessary levels; do not omit necessary ones. The goal is a clear, deterministic path from page → element.
7. **Shared components**: Expose optional `@Input() autoId?: string` and bind `[attr.autoId]="autoId"` inside the template so callers can pass page-specific IDs (including multi-level context).
8. **Manual check**: Verify rendered DOM contains expected `autoId` values (dev tools / `npm run startdev`).

---

## 5. Relation to Other Skills

- **Feature Delivery / Refactor / Unit Test**: Always add/update `autoId` for any touched template with interactive or viewable elements.
- **Unit Test**: Use `autoId` as primary selector (`fixture.nativeElement.querySelector('[autoId="..."]')`) instead of fragile CSS/text selectors.
- **Code Review / Pre-PR**: Verify new/modified templates comply with the naming convention; no accidental renames.
- **Angular Architecture**: Presenter components accept `autoId` via `@Input()` and bind with `[attr.autoId]`.
- **Styling Standards**: `autoId` does not affect styling; keep using SCSS classes for presentation.

---

## 6. Verification Checklist

- [ ] Every clickable element (button, link, navbar, dropdown, checkbox, radio, pagination) has an `autoId`.
- [ ] Every viewable element tests may assert (title, label, message, table header) has an `autoId`.
- [ ] All `autoId` values follow `<pageName>-<contextLevel...>-<elementId>` (camelCase) — context levels flexibly mirror the page hierarchy.
- [ ] No duplicate `autoId` values within the same page.
- [ ] Context levels are meaningful (not padded, not omitted).
- [ ] Set via `autoId="..."` or `[attr.autoId]="'...'"`, never `[autoId]`.
- [ ] Shared components expose `@Input() autoId?: string`.
- [ ] Existing automation tests still target the same `autoId` values.