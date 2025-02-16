import chromadb
from sentence_transformers import SentenceTransformer

# โหลด embedding model ที่ต้องการใช้ (สำหรับตัวอย่างใช้ all-MiniLM-L6-v2)
embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# สร้าง client และ collection สำหรับจัดการข้อมูล
client = chromadb.Client()
collection = client.create_collection(name="green_tea_wiki")

def add_documents(docs):
    for i, doc in enumerate(docs):
        embedding = embed_model.encode(doc).tolist()
        collection.add(
            embeddings=[embedding],
            documents=[doc],
            ids=[str(i)]
        )

def query_document(query, n_results=1):
    query_embedding = embed_model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    # ตรวจสอบว่า 'documents' มีข้อมูลหรือไม่
    if len(results['documents']) > 0:
        return results['documents'][0][0]  # คืนค่า document ที่มีความคล้ายคลึงที่สุด
    else:
        return None  # ถ้าไม่พบข้อมูลใด ๆ


