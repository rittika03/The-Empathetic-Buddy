# 🧠 The Empathetic Buddy: State-to-Text Clinical AI
Finalist (Top 15) — OpenAImer 2026 GenAI Hackathon (Track B) at Jadavpur University

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Llama 3.1](https://img.shields.io/badge/Model-Llama_3.1_8B-orange.svg)
![Groq](https://img.shields.io/badge/Inference-Groq_LPU-black.svg)
![ChromaDB](https://img.shields.io/badge/Vector_DB-ChromaDB-purple.svg)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red.svg)

## 📌 The Problem
Standard Retrieval-Augmented Generation (RAG) systems fail in mental health and emotional support. If a user deflects with sarcasm or emotional numbness, standard LLMs take the text literally and respond with generic, templated sympathy (the "Sympathy Parrot" effect). Furthermore, standard RAG architectures suffer from context amnesia across multi-turn conversations and risk hallucinating dangerous medical advice.

## 🚀 The Solution: State-to-Text Orchestration
The Empathetic Buddy fundamentally redesigns the conversational AI pipeline. Instead of a single LLM call, this system utilizes a Dual-LLM Orchestration Pipeline that strictly decouples emotional understanding from response generation.

### ✨ Core Architectural Features
* Implicit Emotion Extraction (LLM-1): Before drafting a reply, the system forces the LLM to act as a Zero-Shot Classifier, outputting a strict JSON schema that decodes unstated distress, cognitive patterns, and underlying stressors.
* Dual-Memory Stateful Continuity: * *Short-Term:* A sliding window buffer of the last 5 messages to handle immediate context.
  * *Long-Term Profile DB:* Dynamically extracts specific user stressors (e.g., "exams", "parents") and permanently pins them to a JSON ledger, ensuring zero contradictions in multi-turn therapy.
* Deterministic Clinical Grounding (ChromaDB): Retrieves targeted psychological frameworks (CBT, DBT, Validation) mathematically mapped to the user's extracted emotional state via an Approximate Nearest Neighbor (ANN) search.
* Zero-Latency Inference & Uptime: By routing Meta's open-source Llama 3.1 8B through Groq's Language Processing Units (LPUs), the system achieves instantaneous text generation, crash-proofing the UI for live demonstrations.
* Hardcoded Safety Guardrails: Imminent harm scenarios completely bypass the generative neural network. An $O(n)$ deterministic Regex guardrail intercepts high-risk keywords at the edge, instantly triggering a local crisis UI overlay.

---

## 🏗️ System Architecture

1. Input: User submits unstructured text via the Streamlit UI.
2. Safety Check: Edge-level Regex interceptor scans for crisis keywords.
3. State Extraction: Groq API (Llama 3.1) extracts primary_state and stressors into a strict JSON payload.
4. Vector Retrieval: The local ChromaDB Native ONNX Engine bypasses PyTorch dependencies to retrieve the most mathematically relevant clinical coping strategy.
5. Generation: LLM-2 synthesizes the retrieved framework, the updated JSON memory profile, and the chat history to execute a highly targeted "Clinical Pivot."

---

## 🛠️ Technical Stack
* Generative Core & Emotion Router: Llama 3.1 8B (via Groq API)
* Vector Database: ChromaDB (Local Persistent Client using Default ONNX Engine)
* Frontend: Streamlit
* Backend Logic: Python, Regex, JSON

---

## 💻 Local Setup & Installation

This application was engineered to run locally to ensure 100% demo stability against network drops, requiring internet only for the lightweight Groq API text payloads.

### Prerequisites
* Python 3.9+
* A free [Groq API Key](https://console.groq.com/)

### Installation Steps

1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/The-Empathetic-Buddy.git](https://github.com/yourusername/The-Empathetic-Buddy.git)
   cd The-Empathetic-Buddy
