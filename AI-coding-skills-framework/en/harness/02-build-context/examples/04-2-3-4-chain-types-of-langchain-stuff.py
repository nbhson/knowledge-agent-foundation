qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vector_store.as_retriever(),
    chain_type="map_reduce"  # ← map each chunk, then reduce
)
