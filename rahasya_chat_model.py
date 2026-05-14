# RUN THIS ON PORT 5001 FOR THE AI CHAT & MODELS TAB
import sys
import re
import time
from collections import defaultdict
from typing import Dict, List, Optional

try:
    from flask import Flask, request, jsonify
    from flask_cors import CORS
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    print("[!] Missing required packages. Please run: pip install flask flask-cors scikit-learn")
    sys.exit(1)

class EnterpriseKnowledgeBase:
    """Retrieval-Augmented Generation (RAG) Database Simulator"""
    def __init__(self):
        self.documents = {
            "zero_knowledge_proofs": {
                "keywords": ["zero-knowledge", "zkp", "crypto", "proof", "privacy"],
                "content": "Zero-Knowledge Proofs (ZKPs) allow a prover to prove to a verifier that a statement is true without revealing the data itself. Essential for enterprise identity verification without passing passwords."
            },
            "soc2_compliance": {
                "keywords": ["soc2", "compliance", "audit", "security", "iso27001", "policy"],
                "content": "SOC2 Type II requires strict access controls (RBAC), end-to-end encryption, and automated audit trails. Microservices must validate service-to-service communication via mTLS."
            },
            "react_performance": {
                "keywords": ["react", "render", "hook", "usememo", "usecallback", "performance"],
                "content": "React performance heavily relies on preventing unnecessary re-renders. Use `React.memo` for pure components, `useMemo` for expensive calculations, and `useCallback` for stable function references."
            }
        }
        self.vector_index = TfidfVectorizer(stop_words='english')
        self.doc_keys = list(self.documents.keys())
        doc_texts = [" ".join(d["keywords"]) + " " + d["content"] for d in self.documents.values()]
        self.tfidf_matrix = self.vector_index.fit_transform(doc_texts)

    def retrieve(self, query: str) -> Optional[str]:
        query_vec = self.vector_index.transform([query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix)[0]
        best_idx = similarities.argmax()
        if similarities[best_idx] > 0.15: 
            return self.documents[self.doc_keys[best_idx]]["content"]
        return None

class AdvancedConversationalAI:
    """
    Advanced conversational AI foundation model simulator.
    Capable of long-context reasoning, tool-augmented simulation, and multi-domain handling.
    """
    def __init__(self):
        self.kb = EnterpriseKnowledgeBase()
        self.sessions = defaultdict(list)
        print("[SYS] Booting Advanced Conversational Intelligence Engine...")
        print("[SYS] Conversational AI Router Online on Port 5001.")

    def generate_response(self, prompt: str, model_type: str, history: List[dict]) -> str:
        prompt_lower = prompt.lower().strip()
        is_pro = "pro" in model_type.lower() or "llama" in model_type.lower()
        
        # 1. Check Enterprise Knowledge Base (RAG)
        retrieved_data = self.kb.retrieve(prompt)
        base_context = f"*[Retrieved Internal Knowledge]*\n{retrieved_data}\n\n" if retrieved_data else ""

        # 2. General Greetings
        if re.match(r'^(hi|hello|hey|greetings|good morning|good afternoon|sup|howdy)[\s\!\.\?]*$', prompt_lower) or prompt_lower in ['hi', 'hello', 'hey']:
            return f"Hello! I am Rahasya AI ({model_type}), your secure enterprise intelligence assistant. I am capable of multi-domain reasoning, coding, and strategic analysis. How can I assist your workflows today?"

        # 3. Identity Questions
        if "who are you" in prompt_lower or "what are you" in prompt_lower or "your name" in prompt_lower:
            return f"I am Rahasya AI ({model_type}), an advanced sovereign conversational model. I am designed to operate in isolated enterprise environments, ensuring your data remains completely private while delivering high-performance reasoning."

        # 4. Coding & Debugging Domain
        if any(word in prompt_lower for word in ["code", "python", "javascript", "react", "html", "debug", "sql", "memory leak"]):
            resp = base_context + f"As your technical copilot, I can certainly help with that request. Here is an optimized, enterprise-grade approach:\n\n"
            if is_pro:
                resp += "```python\n# Secure Implementation Example\ndef process_secure_data(payload):\n    '''Validates and processes isolated data'''\n    try:\n        result = sanitize(payload)\n        return result\n    except Exception as e:\n        log_error(e)\n        return None\n```\n\nWould you like me to tailor this code to a specific framework or language, or analyze runtime complexity?"
            else:
                resp += "I recommend implementing strict validation functions and memory-safe loops. Let me know if you need the exact syntax snippet."
            return resp

        # 5. Math & Logic Domain
        if "calculate" in prompt_lower or "math" in prompt_lower or "derivative" in prompt_lower or "+" in prompt_lower:
            resp = base_context
            if is_pro:
                resp += "Processing mathematical computation...\n\n1. Let f(x) = u(x)v(x)\n2. Apply the product rule: f'(x) = u'(x)v(x) + u(x)v'(x)\n\nThe logic evaluates accurately. Let me know if you need to derive specific variables."
            else:
                resp += "Math analysis complete. The derivative requires the product rule. Would you like the final output?"
            return resp

        # 6. Enterprise / Business Domain
        if "enterprise" in prompt_lower or "business" in prompt_lower or "workflow" in prompt_lower or "deploy" in prompt_lower or "brainstorm" in prompt_lower:
            resp = base_context
            resp += "Strategic orchestration mode active. Here is a high-level approach for the enterprise requirement:\n\n"
            resp += "1. **Phase 1:** Core Infrastructure Isolation (Zero-Trust).\n2. **Phase 2:** Data Ingestion & Vector Indexing.\n3. **Phase 3:** Autonomous Multi-Agent Deployment.\n\nWhich phase would you like me to expand on step-by-step?"
            return resp

        # 7. General Fallback (Intelligent Mirroring)
        resp = base_context
        if is_pro:
            resp += f"I have processed your query regarding '{prompt[:40]}...'. As an advanced analytical model, I can break this down further. Could you clarify the specific constraints or formats needed for this task to ensure a highly accurate response?"
        else:
            resp += "I understand. I am processing this request locally. How would you like the output structured?"
        return resp

    def chat(self, session_id: str, prompt: str, model_type: str = "Rahasya-Pro") -> Dict:
        """Main entry point for AI Chat interactions"""
        
        # Retrieve Conversation Context
        history = self.sessions[session_id]
        
        # Simulate processing speed based on model size
        time.sleep(0.5 if "Flash" in model_type else 1.2) 
        
        # Generate Intelligent Response
        response_text = self.generate_response(prompt, model_type, history)
        
        # Memory Persistence
        self.sessions[session_id].append({"role": "user", "content": prompt})
        self.sessions[session_id].append({"role": "assistant", "content": response_text})
        if len(self.sessions[session_id]) > 20:  # Context window limit
            self.sessions[session_id] = self.sessions[session_id][-20:]

        return {
            "response": response_text,
            "security_flagged": False,
            "model_used": model_type,
            "context_length": len(self.sessions[session_id])
        }

app = Flask(__name__)
CORS(app)

chat_model = AdvancedConversationalAI()

@app.route('/api/chat', methods=['POST'])
def chat_ai():
    """Endpoint for AI Chat & Models (Conversational Engine)"""
    data = request.json
    if not data or 'prompt' not in data:
        return jsonify({"error": "No prompt provided"}), 400
        
    prompt = data['prompt']
    model_type = data.get('model', 'Rahasya-Pro')
    session_id = data.get('session_id', 'user_session_1')
    
    try:
        result = chat_model.chat(session_id, prompt, model_type)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("[SYS] Waiting for Chat Frontend connections on http://127.0.0.1:5001 ...")
    app.run(port=5001, debug=False)