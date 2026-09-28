import os, json, re

base = r'D:\bitbucket\horizon2\horizon2-ui\ClientApp\.github'
repo = r'D:\bitbucket\horizon2\horizon2-ui'
report = []

def has_bom(path):
    with open(path, 'rb') as f:
        return f.read(3) == b'\xef\xbb\xbf'

# 1. session.json hookFile references
session_path = os.path.join(base, 'hooks', 'session.json')
with open(session_path, 'r', encoding='utf-8-sig') as f:
    session = json.load(f)

report.append("=" * 60)
report.append("1. session.json hookFile references")
report.append("=" * 60)
for section, hooks in session.get('hooks', {}).items():
    for h in hooks:
        hf = h.get('hookFile', '')
        if hf:
            full = os.path.join(base, hf.lstrip('/'))
            status = '✅' if os.path.exists(full) else '❌ MISSING'
            report.append(f"  {status} {hf} (from {section}/{h['id']})")

# 2. CHARTER.md vs actual structure
report.append("")
report.append("=" * 60)
report.append("2. CHARTER.md vs actual directory structure")
report.append("=" * 60)
expected_dirs = ['agents', 'hooks', 'knowledge', 'report-templates', 'reports', 'scripts', 'skills', 'workflows']
for d in expected_dirs:
    full = os.path.join(base, d)
    report.append(f"  {'✅' if os.path.isdir(full) else '❌'} Dir: {d}/")

chart_path = os.path.join(base, 'CHARTER.md')
if os.path.exists(chart_path):
    with open(chart_path, 'r', encoding='utf-8-sig') as f:
        chart = f.read()
    charter_skills = re.findall(r'skills/(\w+)/SKILL.md', chart)
    actual_skills = [d for d in os.listdir(os.path.join(base, 'skills'))
                     if os.path.isdir(os.path.join(base, 'skills', d)) and os.path.exists(os.path.join(base, 'skills', d, 'SKILL.md'))]
    for s in charter_skills:
        ok = s in actual_skills
        report.append(f"  {'✅' if ok else '❌ MISSING'} Skill in CHARTER: skills/{s}/")
    for s in actual_skills:
        if s not in charter_skills:
            report.append(f"  ⚠️  Skill NOT in CHARTER.md: skills/{s}/")
