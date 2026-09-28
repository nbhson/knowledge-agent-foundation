---
name: rum-activity-tracking
description: Guidelines for implementing user activity tracking (Elastic APM RUM) via rum-* template attributes and RumEventService, covering page visits, tab changes, user interactions, and section context in the Horizon 2 UI project.
---

# RUM Activity Tracking

**Tracking is declarative**: add `rum-*` attributes to templates. Only tab changes need a TypeScript call. Never touch the APM SDK from feature code.

[RumEventService](../../../src/shared/rum/rum-event.service.ts) listens globally for `click` / `submit` / `change` / `keydown` and resolves attributes with `target.closest('[attr]')` — so **context attributes are inherited from ancestors**. Reference implementations: Maintenance Support and Contracts trackers.

---

## 1. Attributes

| Attribute | Label | Put it on | Form |
| :--- | :--- | :--- | :--- |
| `rum-action-name` | `action_name` | the interactive element | static if literal, `[attr.]` otherwise |
| `rum-active-tab` | `active_tab` | tab content root (+ every overlay — §4) | `[attr.]` (enum) |
| `rum-active-section` | `active_section` | section wrapper on detail pages | `[attr.]` (`item.name`) |
| `rum-action-required` | — | same element as `rum-action-name` | **bare, never bound** |
| `rum-display-pattern` | `action_pattern` | same element as `rum-action-name` | static (`pageName-actionName`) |

Missing value → `'None'`.

### Static vs binding

- Constant string → **static**: `rum-action-name="Apply Changes Filter"`
- Enum / property / expression → **binding**: `[attr.rum-action-name]="column.columnHeaderName"`
- **Never** `[rum-action-name]="..."` — no such DOM property, renders nothing, `closest()` finds nothing. 0 occurrences today; keep it that way.
- Don't wrap a plain literal in a binding. Three legacy cases remain (maintenance header `'Create New Request'`, maintenance table `'Set Priority'`, admin configuration header `'Add Category'`) — align them when touching those files.
- `rum-action-required` is a **presence** check (`closest('[rum-action-required]') != null`). Angular removes an attribute only for `null`/`undefined`, so `[attr.rum-action-required]="false"` renders `="false"` — still present, still tracked. Keep it unconditional.

### What `rum-action-required` does

Without it the labels ride Angular's managed `user-interaction` transaction, which may be dropped. With it a second **unmanaged** transaction is started so the event always ships:

- custom transaction → `action_type: 'custom'` + the real labels
- original → `action_type: 'superseded'`, tab/section reset to `'None'`

Seeing both in Kibana is expected. **Any action that matters to a report must carry it.**

---

## 2. Page visit — route config only

Read automatically on every `NavigationEnd`; no component code.

| Route data | Label |
| :--- | :--- |
| `title` | `page_name` + transaction name |
| `isDetails: true` | `page_details` |
| `parent: PageTitle.X` | `page_tracker` — **required** on detail routes, else the tracker rollup breaks |
| `isExternal` | `page_external` |

---

## 3. Tab change — the only TS call

**a. Declare the enum triple** — id (URL param + `autoId`), label (UI text + RUM grouping key), and the map:

```ts
export enum MaintenanceSupportTabId { SUPPORT_OVERSIGHT = 'supportOversight' /* ... */ }
export enum MaintenanceSupportTabLabel { SUPPORT_OVERSIGHT = 'Support Oversight' /* ... */ }
export const MAINTENANCE_SUPPORT_TAB_LABELS: Record<MaintenanceSupportTabId, MaintenanceSupportTabLabel> = { /* ... */ };
```

Ids live in URLs and automation selectors; labels are what users and reports see — renaming a label must not break deep links. The map exists because a deep link gives RUM only `?tab=<id>`: without it, page-load would report a different `active_tab` than a user click.

**b. Register in [`PANEL_ITEMS`](../../../src/constants/menu-panel.ts)** — add `tabs` + `defaultTab` to the tracker's existing entry. `getTrackerTabInfo()` matches on `subTooltip`, so it must equal the route `title`/`parent`.

**c. Call it:**

```ts
onTabChange(tabIndex: number): void {
  if (this.isSyncingTabFromQueryParams) { this.isSyncingTabFromQueryParams = false; return; }
  this.selectedTab = this.tabMapping[tabIndex] ?? /* default */;
  this._rumEventService.trackTabChange(this.tabLabelMapping[this.selectedTab]);
}
```

- Pass the **label**, never the id.
- Skip programmatic / query-param sync — that is not user activity.
- The default tab is already covered by page-load; `trackTabChange(label, isDefaultTab)` returns early when `true`.
- **Top-level tracker tabs only.** Nested tab groups (e.g. Contracts/Budget Lifecycle inside Contracts Oversight) are deliberately not tracked as tab changes.

---

## 4. Overlays — the `closest()` trap

CDK overlays (`mat-dialog`, `mat-menu`, side panels) render **outside** the tab's DOM, so `closest()` finds no `rum-active-tab` and it degrades to `'None'`. Pass the label in and re-declare it:

```ts
SiteListDialogComponent.open(this._dialog, this.autoId, element.sites, title,
  MaintenanceSupportTabLabel.SUPPORT_OVERSIGHT);
```

```html
<div class="site-list-dialog" [attr.rum-active-tab]="dialogData.activeTab">
```

`mat-menu` items do the same per item.

---

## 5. Examples

```html
<!-- header button: static name, tab re-declared -->
<button rum-action-name="Create New Request" [attr.rum-active-tab]="...TRACKER" rum-action-required>

<!-- table link: name it after the column -->
<a [routerLink]="..." [attr.rum-action-name]="column.columnHeaderName" rum-action-required>

<!-- detail page: one attribute on the section wrapper, children inherit it -->
<div *ngFor="let item of sectionItemsDisplay" [id]="item.id" [attr.rum-active-section]="item.name">

<!-- cross-module navigation -->
<button rum-action-name="Sponsor Module" rum-display-pattern="pageName-actionName" rum-action-required>
```

`autoId` and `rum-*` are separate contracts: on a row-action menu button, `autoId` uses the **value** enum while `rum-action-name` uses the **display** enum.

---

## 6. Testing & verification

Mock it in the container spec — `{ provide: RumEventService, useValue: { trackTabChange: jest.fn() } }` — and assert both branches: called on a user click, **not** called when syncing from query params.

Manual: set `apmConfig.rum` → `active: true`, `logLevel: "debug"`, log in (nothing reports before `setUserContext`), then read `console.debug('RUM Event: ', ...)` and watch for unexpected `'None'`.

---

## 7. Checklist

- [ ] Route has `title`; detail routes have `isDetails` + `parent`.
- [ ] Enum triple declared; `PANEL_ITEMS` has `tabs` + `defaultTab`.
- [ ] `trackTabChange` passes the label and skips programmatic syncs.
- [ ] Each tab content root has `[attr.rum-active-tab]`.
- [ ] Every report-worthy action has `rum-action-name` **and** `rum-action-required`.
- [ ] Names come from enums / constants / column headers, not stray literals.
- [ ] Overlays and menu items re-declare `rum-active-tab`.
- [ ] Form matches the value source; `rum-action-required` is bare; no property binding.
- [ ] Container spec mocks `RumEventService`.
