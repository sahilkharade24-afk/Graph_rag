import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class Generator:
    def __init__(self, model_name="gemini-1.5-flash"):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("Warning: GOOGLE_API_KEY not found in environment. Answer generation will fail.")
        genai.configure(api_key=api_key)
        self.model_name = model_name
        self._initialize_model()

    def _initialize_model(self):
        try:
            self.model = genai.GenerativeModel(self.model_name)
        except Exception:
            self._discover_and_fallback()

    def _discover_and_fallback(self):
        print(f"Model {self.model_name} initialization issue. Discovering available models...")
        try:
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            # Prioritize models
            priorities = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-pro"]
            for priority in priorities:
                for available in available_models:
                    if priority in available:
                        print(f"Found suitable model: {available}. Using it as fallback.")
                        self.model_name = available
                        self.model = genai.GenerativeModel(self.model_name)
                        return
            
            if available_models:
                print(f"No preferred model found. Using first available: {available_models[0]}")
                self.model_name = available_models[0]
                self.model = genai.GenerativeModel(self.model_name)
            else:
                print("No models supporting generateContent found.")
        except Exception as e:
            print(f"Failed to discover models: {e}")

    def generate_answer(self, query, context_chunks):
        """
        Generates an answer to the query using the provided context chunks.
        """
        context_text = "\n---\n".join(context_chunks)
        prompt = f"""
You are a helpful assistant. Use the following pieces of retrieved context to answer the question. 
If you don't know the answer based on the context, just say that you don't know, don't try to make up an answer.

Context:
{context_text}

Question: {query}

Answer:
"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            if "404" in str(e):
                print(f"Model {self.model_name} returned 404 during generation. Attempting discovery...")
                self._discover_and_fallback()
                # Retry once if we found a new model
                return self.model.generate_content(prompt).text
            else:
                raise e

def get_answer(query, context_chunks):
    generator = Generator()
    return generator.generate_answer(query, context_chunks)
