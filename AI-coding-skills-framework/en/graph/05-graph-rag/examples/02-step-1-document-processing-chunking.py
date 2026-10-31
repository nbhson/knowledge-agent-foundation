from pathlib import Path

class DocumentProcessor:
    def __init__(self, chunk_size=1000, overlap=100):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk(self, text: str) -> list[str]:
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunks.append(text[start:end])
            start = end - self.overlap
        return chunks
    
    def process_directory(self, dir_path: str) -> list[dict]:
        all_chunks = []
        for file in Path(dir_path).glob("*.md"):
            text = file.read_text(encoding="utf-8")
            for i, chunk in enumerate(self.chunk(text)):
                all_chunks.append({
                    "id": f"{file.name}#{i}",
                    "text": chunk,
                    "source": str(file),
                })
        return all_chunks
