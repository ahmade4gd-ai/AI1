import json, os

class Architect:
    def __init__(self):
        self.memory_file = "memory_db.json"
        self.memory = self.load_memory()

    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f: return json.load(f)
        return {"sessions": [], "global_knowledge": 1.0}

    def process(self, user_query):
        # تحليل السياق من الذاكرة
        context = self.memory["sessions"][-3:] if self.memory["sessions"] else "لا يوجد سياق سابق."
        print(f"[*] العقل المدبر: يفكك الطلب بناءً على سياق: {context}")
        
        # تحويل الطلب للوكيل الثاني (المبرمج)
        task_payload = {
            "task": user_query,
            "context": context,
            "instruction": "Convert this to optimized code using DeepSeek logic."
        }
        return task_payload

    def save_chat(self, user_msg, ai_res):
        self.memory["sessions"].append({"q": user_msg, "a": ai_res})
        with open(self.memory_file, 'w') as f: json.dump(self.memory, f)
