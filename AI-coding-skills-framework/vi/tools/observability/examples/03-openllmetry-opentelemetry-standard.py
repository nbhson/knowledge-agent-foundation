# OpenTelemetry-compatible — trace chuẩn OTLP
from traceloop.sdk import Traceloop

Traceloop.init(app_name="my_harness")

# Mọi framework (LangChain, LlamaIndex, OpenAI SDK...) tự động trace
# → Export sang Jaeger, Grafana, Datadog, ...
