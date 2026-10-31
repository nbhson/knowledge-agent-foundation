# OpenTelemetry-compatible — standard OTLP tracing
from traceloop.sdk import Traceloop

Traceloop.init(app_name="my_harness")

# Every framework (LangChain, LlamaIndex, OpenAI SDK...) traces automatically
# → Export to Jaeger, Grafana, Datadog, ...
