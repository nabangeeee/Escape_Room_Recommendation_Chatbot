from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

# 문서 로드, 청크로 분할
loader = TextLoader("sample.txt")
docs = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# 임베딩 생성 & 벡터DB 저장 (Chroma)
embeddings = OpenAIEmbeddings()
vectordb = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")
vectordb.persist()
