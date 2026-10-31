sections = re.split(r'^(#{1,3}\s+.+)$', text, flags=re.MULTILINE)
for section in sections:
    if re.match(r'^#{1,3}\s+', section):
        current_header = section.strip()      # the heading becomes metadata
    elif section.strip():
        for para in section.split('\n\n'):   # too big → split by paragraph
            chunks.append({"content": para.strip(),
                           "metadata": {"section": current_header}})
