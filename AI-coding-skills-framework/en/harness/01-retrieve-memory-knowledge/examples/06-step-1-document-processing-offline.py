"""
Step 1: Document processing — Build the knowledge base

Process:
Document → Clean → Chunk → Embed → Store

Input:  PDF, HTML, TXT, Markdown...
Output: Vector DB with embedded chunks
"""

from pathlib import Path

class DocumentProcessor:
    def __init__(self, chunk_size=500, chunk_overlap=50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def load_document(self, file_path):
        """Load and extract text from many formats"""
        path = Path(file_path)

        if path.suffix == ".pdf":
            return self._load_pdf(path)
        elif path.suffix == ".md":
            return self._load_markdown(path)
        elif path.suffix == ".txt":
            return path.read_text(encoding="utf-8")
        elif path.suffix in [".html", ".htm"]:
            return self._load_html(path)
        else:
            raise ValueError(f"Unsupported format: {path.suffix}")

    def chunk_document(self, text, metadata=None):
        """Split the document into chunks"""
        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start:end]

            chunk = {
                "text": chunk_text,
                "metadata": {
                    **(metadata or {}),
                    "start_char": start,
                    "end_char": end,
                }
            }
            chunks.append(chunk)
            start = end - self.chunk_overlap

        return chunks

    def process_directory(self, dir_path):
        """Process an entire directory"""
        all_chunks = []
        for file in Path(dir_path).glob("*"):
            if file.suffix in [".pdf", ".md", ".txt", ".html"]:
                text = self.load_document(file)
                chunks = self.chunk_document(text, {
                    "source": str(file),
                    "filename": file.name,
                })
                all_chunks.extend(chunks)

        print(f"Processed {len(list(Path(dir_path).glob('*')))} files")
        print(f"Created {len(all_chunks)} chunks")
        return all_chunks


# Usage
processor = DocumentProcessor(chunk_size=500, chunk_overlap=50)
chunks = processor.process_directory("./documents")
