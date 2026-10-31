engine.add_stage("extract",  extract_stage,  checkpoint=True)
engine.add_stage("validate", validate_stage, on_error="fail", timeout_s=300)
engine.add_stage("load",     load_stage,     checkpoint=True)
# on fail → status "rolled_back" to nearest checkpoint, else "failed"
