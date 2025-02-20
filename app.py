from flask import Flask, render_template, request, jsonify
from rag_module.wiki_retrieval import get_wiki_page
from rag_module.vector_store import add_documents, query_document
from rag_module.gpt_neo_api import get_gptj_response

app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")

# ดึงข้อมูล Wikipedia และบันทึกลง Vector Store
try:
    green_tea_text = get_wiki_page("Green_tea")
except ValueError as e:
    print(e)
    green_tea_text = ""

def split_into_chunks(text, chunk_size=300):
    words = text.split()
    return [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

chunks = split_into_chunks(green_tea_text)
add_documents(chunks)  # เพิ่มข้อมูลลงฐาน Vector Store

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_question = request.json.get("message", "")
    retrieved_context = query_document(user_question)
    response = get_gptj_response(retrieved_context, user_question)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
