sleep 30
curl -f https://staging.example.com/health || exit 1
npm run test:e2e -- --baseUrl=https://staging.example.com
