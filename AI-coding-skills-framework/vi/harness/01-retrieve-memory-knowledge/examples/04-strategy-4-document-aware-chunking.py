# Tôn trọng cấu trúc document (Markdown, HTML, Code)

def markdown_chunk(text, max_chunk_size=1000):
    """
    Chunk theo cấu trúc Markdown:
    1. Split theo headers (#, ##, ###)
    2. Nếu section quá lớn, split theo đoạn văn
    3. Giữ header như metadata cho mỗi chunk
    """
    import re
    
    # Split theo headers
    sections = re.split(r'^(#{1,3}\s+.+)$', text, flags=re.MULTILINE)
    
    chunks = []
    current_header = ""
    
    for section in sections:
        if re.match(r'^#{1,3}\s+', section):
            current_header = section.strip()
        elif section.strip():
            if len(section) <= max_chunk_size:
                chunks.append({
                    "header": current_header,
                    "content": section.strip(),
                    "metadata": {"section": current_header}
                })
            else:
                # Section quá lớn → split theo đoạn
                paragraphs = section.split('\n\n')
                current_content = ""
                for para in paragraphs:
                    if len(current_content) + len(para) <= max_chunk_size:
                        current_content += para + "\n\n"
                    else:
                        if current_content:
                            chunks.append({
                                "header": current_header,
                                "content": current_content.strip(),
                                "metadata": {"section": current_header}
                            })
                        current_content = para + "\n\n"
                if current_content:
                    chunks.append({
                        "header": current_header,
                        "content": current_content.strip(),
                        "metadata": {"section": current_header}
                    })
    
    return chunks
