def retrieve_role(vectorstore, role):

    docs = vectorstore.similarity_search(role, k=1)

    return docs[0].page_content