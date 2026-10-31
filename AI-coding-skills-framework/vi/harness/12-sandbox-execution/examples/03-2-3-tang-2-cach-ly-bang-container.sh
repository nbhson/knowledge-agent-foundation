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
