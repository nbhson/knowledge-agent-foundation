# Front door (khuyên dùng) — một binary cho init + doctor + status
npx @cobusgreyling/loop init . --pattern daily-triage --tool grok
npx @cobusgreyling/loop doctor .

# Tương đương cũ (vẫn hỗ trợ — forks không cần đổi)
npx @cobusgreyling/loop-init .

# Tuỳ chọn: scaffold thêm versioned harness (harness-foundry)
npx @cobusgreyling/loop init . --with-foundry
