from langchain_core.prompts import ChatPromptTemplate

RAG_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful assistant. Answer the user's question based **only** on the "
        "provided context. If the context does not contain enough information, say so. "
        "Cite sources when possible.\n\n"
        "Context:\n{context}",
    ),
    ("human", "{question}"),
])

CONCISE_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "Answer concisely using the context below. If unsure, say you don't know.\n\n"
        "Context:\n{context}",
    ),
    ("human", "{question}"),
])
