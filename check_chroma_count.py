from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings()
vectordb = Chroma(
    persist_directory="./chroma_db",  # chroma_db 폴더가 있는 경로
    embedding_function=embeddings
)

print("저장된 문서(임베딩 청크) 수:", vectordb._collection.count())
