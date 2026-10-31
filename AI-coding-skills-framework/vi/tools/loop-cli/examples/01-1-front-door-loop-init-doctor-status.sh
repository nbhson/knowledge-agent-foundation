# Scaffold + chẩn đoán + trạng thái (khuyên dùng: một binary cho cả ba)
npx @cobusgreyling/loop init . --pattern daily-triage --tool grok
npx @cobusgreyling/loop doctor .
npx @cobusgreyling/loop status .

# Tương đương cũ (forks không cần đổi)
npx @cobusgreyling/loop-init .

# Tuỳ chọn: scaffold thêm versioned harness
npx @cobusgreyling/loop init . --with-foundry
