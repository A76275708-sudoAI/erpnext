# Roles — ERP v1 D5 skeleton

Map PRD roles to ERPNext **Role** records. Phase-1: create Roles + Desk shortcuts; fine-grained DocPerm can follow D6.

## Mapping

| PRD 角色 | ERPNext Role name (create) | Also grant (optional stock) | Phase-1 focus |
|----------|----------------------------|-----------------------------|---------------|
| 跟单 | `ERP v1 跟单` | Sales User (read) | exception pool, urge ship, confirm ship, assign pick |
| 仓管/拣货 | `ERP v1 仓管` | Stock User | print queue, pick, pack check, stock in/out |
| 销售 | `ERP v1 销售` | Sales User | offline SO create, stock lock, outbound confirm |
| 客服 | `ERP v1 客服` | — | return request intake, QC mark (with 仓管) |
| 运营 | `ERP v1 运营` | — | channel switches, shop auth placeholders, doc flow read |
| 财务（占位） | `ERP v1 财务` | Accounts User **read-only** where possible | menus + events only; **no posting** |
| 管理员 | `ERP v1 管理员` | System Manager (bootstrap only) | users, roles, logs, DN force-cancel path |

English aliases (optional Property / translation):

| Role name | alias |
|-----------|-------|
| ERP v1 跟单 | ERP v1 Merchandiser |
| ERP v1 仓管 | ERP v1 Warehouse |
| ERP v1 销售 | ERP v1 Sales |
| ERP v1 客服 | ERP v1 CS |
| ERP v1 运营 | ERP v1 Ops |
| ERP v1 财务 | ERP v1 Finance |
| ERP v1 管理员 | ERP v1 Admin |

## Separation of duties (account model reserved)

| Constraint | Phase-1 enforcement |
|------------|---------------------|
| 打单人 ≠ 发货人 | field/actor check stub; soft warn OK until workflow |
| 拣货人 ≠ 复核人 | same |
| 调整发起人 ≠ 审批人 | Stock Reconciliation: initiator ≠ approver fields |

Do **not** enable full Workflow engine in phase-1 (PRD out of scope).

## Permission matrix (summary → implement as DocPerm later)

| Capability | 跟单 | 仓管 | 销售 | 客服 | 运营 | 财务 | 管理员 |
|------------|------|------|------|------|------|------|--------|
| View order pool | ✓ | ✓ | own channel | ✓ | ✓ | read | ✓ |
| Print labels | — | ✓ | — | — | — | — | ✓ |
| Assign pick | ✓ | ✓ | — | — | — | — | ✓ |
| Pick / check | — | ✓ | — | — | — | — | ✓ |
| Confirm ship | ✓ | ✓ | — | — | — | — | ✓ |
| Offline SO | — | — | ✓ | — | — | — | ✓ |
| Stock in/out | — | ✓ | — | — | — | — | ✓ |
| Stock adjust | — | initiate | — | — | — | — | approve |
| Returns / QC | ✓ | QC | — | ✓ | — | — | ✓ |
| Channel switch | — | — | — | — | ✓ | — | ✓ |
| AR/AP menus | read | — | — | — | — | placeholder | ✓ |
| Users / logs | — | — | — | — | — | — | ✓ |
| DN force cancel | — | — | — | — | — | — | ✓ |

## Seed approach

1. Create seven Roles via fixture `fixtures/erp_v1/roles.json` (see that file).
2. Create seven Users in staging only (not committed with passwords).
3. Workspace / shortcuts per role can land D6 with main data.
