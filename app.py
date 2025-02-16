from rag_module.wiki_retrieval import get_wiki_page
from rag_module.vector_store import add_documents, query_document
from rag_module.gpt_neo_api import get_gptj_response

# 1. ดึงข้อมูลหน้า Wikipedia "Green tea"
try:
    green_tea_text = get_wiki_page("Green_tea")
except ValueError as e:
    print(e)
    green_tea_text = ""

# 2. แบ่งข้อความเป็นชิ้นเล็ก ๆ (chunking) - ตัวอย่างง่าย ๆ ด้วยการแบ่งด้วยตัวแบ่งบรรทัดหรือความยาว
def split_into_chunks(text, chunk_size=300):
    words = text.split()
    return [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

chunks = split_into_chunks(green_tea_text)

# 3. เพิ่ม chunks ลงใน Vector Store (ChromaDB)
add_documents(chunks)

user_question = input("Enter your question: ")

retrieved_context = query_document(user_question)

response = get_gptj_response(retrieved_context, user_question)

print(f"Question: {user_question}")
print(f"Answer: {response}")
