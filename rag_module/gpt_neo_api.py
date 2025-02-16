import requests
import re

API_TOKEN = "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"
GPTJ_API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"

def get_gptj_response(context, question, max_new_tokens=300, temperature=0.7):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    prompt = f"Answer the question briefly and concisely based on the provided context. Only provide the answer, avoid explanations. Context: {context}\nQuestion: {question}\nAnswer:"
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_new_tokens,
            "temperature": temperature,
            "stop_sequences": ["\nQ:", "\nQuestion:"],  
        },
    }
    response = requests.post(GPTJ_API_URL, headers=headers, json=payload)
    result = response.json()

    # Debug ดูผลลัพธ์ก่อน

    if isinstance(result, list) and len(result) > 0 and 'generated_text' in result[0]:
        generated_text = result[0]['generated_text']

        # เอาเฉพาะตรง 'Answer:' มาจริง ๆ ไม่เอาต่อ
        answer_start = generated_text.find("Answer:")
        if answer_start != -1:
            answer_part = generated_text[answer_start + len("Answer:"):].strip()
        else:
            answer_part = generated_text.strip()

        # ตัดตอน answer ให้หยุดที่คำถามใหม่ หรือ "Answer:" รอบถัดไป (เผื่อหลุดมา)
        answer_cleaned = re.split(r"\nQuestion:|\nAnswer:", answer_part)[0].strip()

        return answer_cleaned
    else:
        print("Unexpected response format:", result)
        return "Sorry, I couldn't process the request."
