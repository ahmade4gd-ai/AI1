/* Aegis Alpha System - Node.js Edition
   The Self-Evolving AI Programmer
*/

const express = require('express');
const fs = require('fs');
const ModelClient = require("@azure-rest/ai-inference").default;
const { AzureKeyCredential } = require("@azure/core-auth");
const { isUnexpected } = require("@azure-rest/ai-inference");

const app = express();
app.use(express.json());
app.use(express.static('public'));

// --- إعدادات النماذج ---
const GITHUB_TOKEN = "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"; // ⚠️ غير هذا المفتاح بمفتاح جديد لاحقاً للأمان
const ENDPOINT = "https://models.github.ai/inference";

const CLIENT = ModelClient(ENDPOINT, new AzureKeyCredential(GITHUB_TOKEN));

// تعريف النماذج حسب الأدوار
const AGENTS = {
    architect: "deepseek/DeepSeek-R1-0528",  // التفكير
    coder: "xai/grok-3",                     // البرمجة
    sandbox: "openai/gpt-4.1-nano",          // المحاكاة
    auditor: "microsoft/MAI-DS-R1",          // التدقيق
    evolver: "meta/Llama-4-Scout-17B-16E-Instruct" // التطور
};

// --- دالة الاتصال الموحدة بالذكاء الاصطناعي ---
async function askAI(role, prompt, temp = 1.0) {
    const modelName = AGENTS[role];
    console.log(`[🤖] ${role.toUpperCase()} using ${modelName}...`);

    try {
        const response = await CLIENT.path("/chat/completions").post({
            body: {
                messages: [
                    { role: "system", content: "You are an expert AI agent part of the Aegis System." },
                    { role: "user", content: prompt }
                ],
                temperature: temp,
                top_p: 1,
                max_tokens: 4096,
                model: modelName
            }
        });

        if (isUnexpected(response)) {
            throw response.body.error;
        }

        return response.body.choices[0].message.content;
    } catch (err) {
        console.error(`Error calling ${role}:`, err);
        return `Error: ${err.message}`;
    }
}

// --- الوظائف الأساسية للنظام ---

// 1. الوكيل الخامس: التطور الذاتي (يعدل الكود نفسه!)
async function evolveSystem(feedback) {
    console.log(" [🧬] الوكيل الخامس يبدأ عملية التطور...");
    
    // قراءة الكود الحالي
    const currentCode = fs.readFileSync(__filename, 'utf8');
    
    const evolutionPrompt = `
    أنت مطور أنظمة ذكي جداً (Llama-4).
    لديك صلاحية الوصول للكود المصدري لهذا النظام.
    الهدف: تحسين النظام ليصبح أقوى في البرمجة.
    الملاحظات الأخيرة: ${feedback}
    
    مهمتك:
    1. اقترح تحسيناً واحداً صغيراً وفعالاً للكود (مثلاً تحسين البرومبت، إضافة وظيفة جديدة).
    2. لا تقم بتغيير الأجزاء الأساسية (مثل التوكن).
    3. أعطني الكود المعدل فقط.
    `;

    // ملاحظة: في النسخة الحقيقية، سنجعله يكتب الملف، هنا سنكتفي بطباعة التحديث للأمان
    const suggestion = await askAI("evolver", evolutionPrompt, 0.7);
    
    // تسجيل التطور في ملف خارجي
    fs.appendFileSync('evolution_log.txt', `\n--- ${new Date().toISOString()} ---\n${suggestion}\n`);
    return suggestion;
}

// --- مسارات السيرفر (API Endpoints) ---

app.post('/api/start', async (req, res) => {
    const userTask = req.body.task;
    let logs = [];

    try {
        // المرحلة 1: التخطيط (DeepSeek)
        const plan = await askAI("architect", `حلل هذا الطلب برمجياً وضع خطة دقيقة جداً: ${userTask}`);
        logs.push({ agent: "Architect (DeepSeek)", content: plan });

        // المرحلة 2: البرمجة (Grok-3)
        const code = await askAI("coder", `بناءً على هذه الخطة، اكتب كود Node.js كامل واحترافي: ${plan}`);
        logs.push({ agent: "Coder (Grok-3)", content: code });

        // المرحلة 3: التدقيق (Microsoft MAI)
        const audit = await askAI("auditor", `راجع هذا الكود واكتشف أي أخطاء منطقية أو أمنية:\n${code}`);
        logs.push({ agent: "Auditor (Microsoft)", content: audit });

        // المرحلة 4: المحاكاة السريعة (GPT Nano)
        const test = await askAI("sandbox", `تخيل أنك تشغل هذا الكود، ماذا ستكون المخرجات المتوقعة؟ وهل سينجح؟\n${code}`);
        logs.push({ agent: "Sandbox (GPT Nano)", content: test });

        // المرحلة 5: التطور (Llama-4 Scout)
        // يتم استدعاء التطور في الخلفية
        evolveSystem(`User Task: ${userTask}, Result: Success`).then(adv => console.log("System Evolved!"));

        res.json({ status: "success", logs: logs, finalCode: code });

    } catch (error) {
        res.status(500).json({ status: "error", message: error.message });
    }
});

// تشغيل السيرفر
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`\n🛡️ Aegis System Online.`);
    console.log(`🚀 افتح المتصفح على: http://localhost:${PORT}`);
});
