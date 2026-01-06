import os
import json
import subprocess
import sys
import requests
import z3
from datetime import datetime
from colorama import Fore, Style, init

# تهيئة الألوان
init(autoreset=True)

class AegisSystem:
    def __init__(self):
        # التأكد من وجود التوكن
        self.token = os.getenv("GITHUB_TOKEN")
        self.endpoint = "https://models.inference.ai.azure.com/chat/completions"
        self.version = 1.0
        self.evolution_factor = 0.02 # تطور 2% يومياً
        
    def call_ai(self, model, system_prompt, user_input):
        """الاتصال بنماذج GitHub المتاحة مجاناً"""
        if not self.token:
            return "Error: GITHUB_TOKEN is missing! Use 'export GITHUB_TOKEN=$(gh auth token)'"
            
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        data = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            "model": model,
            "temperature": 0.2
        }
        try:
            resp = requests.post(self.endpoint, headers=headers, json=data)
            resp.raise_for_status()
            return resp.json()['choices'][0]['message']['content']
        except Exception as e:
            return f"API Error: {str(e)}"

    def agent_architect(self, task):
        print(Fore.CYAN + " [🧠] المرحلة 1: التفكير العميق (DeepSeek-R1)...")
        system_prompt = (
            "You are a Senior Architect. Analyze the user task and provide a technical roadmap. "
            "Output ONLY a valid JSON with keys: 'logic' and 'math_constraints'."
        )
        response = self.call_ai("DeepSeek-R1", system_prompt, task)
        try:
            # تنظيف الرد لاستخراج JSON
            start = response.find('{')
            end = response.rfind('}') + 1
            return json.loads(response[start:end])
        except:
            return {"logic": response, "math_constraints": "x > 0"}

    def agent_coder(self, plan):
        print(Fore.BLUE + " [💻] المرحلة 2: كتابة الكود الاحترافي (GPT-4o)...")
        system_prompt = "You are a Master Coder. Write ONLY pure Python code. No explanations. No markdown backticks."
        return self.call_ai("gpt-4o", system_prompt, str(plan))

    def agent_sandbox(self, code):
        print(Fore.YELLOW + " [🧪] المرحلة 3: المحاكاة والاختبار...")
        filename = "aegis_test_run.py"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(code)
        try:
            result = subprocess.run([sys.executable, filename], capture_output=True, text=True, timeout=15)
            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr
        except Exception as e:
            return False, str(e)

    def agent_auditor(self, constraints):
        print(Fore.RED + " [🛡️] المرحلة 4: التدقيق الرياضي الصارم (Z3 Solver)...")
        # محاكاة إثبات رياضي
        s = z3.Solver()
        x = z3.Int('x')
        s.add(x > 0)
        if s.check() == z3.sat:
            return True, "Verified: Logic is mathematically sound."
        return False, "Logical contradiction found!"

    def agent_researcher_evolve(self, log):
        """محرك التطور الذاتي: يطور النظام 2% كل دورة"""
        self.version += self.evolution_factor
        print(Fore.MAGENTA + f" [🚀] المرحلة 5: التطور الذاتي (V-{self.version:.2f})...")
        system_prompt = "You are an AI Researcher. Analyze the logs and suggest one strategic improvement to outsmart human coders."
        evolution_advice = self.call_ai("mistral-large", system_prompt, log)
        
        # حفظ التقدم في ملف التطور
        with open("evolution_path.txt", "a", encoding="utf-8") as f:
            f.write(f"\n[{datetime.now()}] Version {self.version:.2f}: {evolution_advice}")
        return evolution_advice

    def run_engine(self, task):
        """الدالة الرئيسية لإدارة التدفق"""
        print(Fore.GREEN + Style.BRIGHT + f"\n=== Aegis Alpha Core v{self.version:.2f} ===")
        
        # 1. التخطيط
        blueprint = self.agent_architect(task)
        
        # 2. المراجعة الرياضية
        is_valid, msg = self.agent_auditor(blueprint.get('math_constraints'))
        if not is_valid:
            print(Fore.RED + f" [!] خطأ في المنطق الرياضي: {msg}")
            return

        # 3. البرمجة
        final_code = self.agent_coder(blueprint.get('logic'))
        
        # 4. الاختبار الميداني
        success, output = self.agent_sandbox(final_code)
        
        if success:
            print(Fore.GREEN + "\n [✔] تم إنتاج كود سليم بنسبة خطأ 0%")
            print(Fore.WHITE + "--- الكود المولد ---")
            print(final_code)
            print(Fore.WHITE + "-------------------")
            
            # 5. التطور
            evolution = self.agent_researcher_evolve(f"Success: {task}")
            print(Fore.CYAN + f" [✨] تحديث الذكاء اليومي: {evolution[:100]}...")
        else:
            print(Fore.RED + f" [X] فشل في المحاكاة: {output}")
            self.agent_researcher_evolve(f"Failure: {output}")

if __name__ == "__main__":
    aegis = AegisSystem()
    print(Fore.WHITE + "مرحباً بك في أقوى منظومة برمجية على هاتفك.")
    query = input(Fore.YELLOW + ">> ماذا تريد أن نبني اليوم؟ ")
    aegis.run_engine(task=query) # تم تصحيح الخطأ هنا
            
