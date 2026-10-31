docker run --rm \
  --read-only \                          # no writes outside explicit mounts
  --tmpfs /tmp:rw,noexec,nosuid,size=64m \
  --cap-drop=ALL \                       # no ambient privilege
  --security-opt=no-new-privileges \     # no setuid escalation
  --pids-limit=64 \                      # no fork bomb
  --memory=512m --cpus=1.0 \             # no resource exhaustion
  --network=none \                       # no egress
  -v "$WORKDIR:/work:rw" -w /work \
  -e PATH=/usr/bin \
  sandbox-img@sha256:9f2c…              # digest, not tag
