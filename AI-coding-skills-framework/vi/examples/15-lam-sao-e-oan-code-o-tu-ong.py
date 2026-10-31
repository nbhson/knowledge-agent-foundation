from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

# Load vector DB đã có sẵn
vector_store = Chroma(
    embedding_function=OllamaEmbeddings(model="nomic-embed-text"),
    persist_directory="./chroma_db"
)

# Tạo chain: tự động retrieve + augment + generate
qa_chain = RetrievalQA.from_chain_type(
    llm=Ollama(model="gemma3:12b"),
    retriever=vector_store.as_retriever(),
    chain_type="stuff"  # stuff = nhồi context vào prompt
)

# Dùng: tự động chạy retrieve → augment → LLM
result = qa_chain.invoke("BHYT có chi trả bệnh tim không?")
print(result)
