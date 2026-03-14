from langchain.vectorstores import FAISS
from langchain.docstore.document import Document


def build_vector_store(role_data, embeddings):

    docs = []

    for role, skills in role_data.items():
        text = role + " " + " ".join(skills)
        docs.append(Document(page_content=text, metadata={"role": role}))

    vectorstore = FAISS.from_documents(docs, embeddings)

    return vectorstore