import google.generativeai as genai
import threading
import time
import os

# ==========================================
# CENTRALIZED AI GATEKEEPER
# ==========================================
# This module prevents 'Key Stomping' by ensuring only ONE 
# thread interacts with the global Gemini library at a time.

class AIGatekeeper:
    _lock = threading.Lock()
    
    # New Multi-Project Keys
    KEYS = {
        "Vault": "AIzaSyDKIs5LJqP5GW8BAJZbkXEDPtAOseI5IUo",
        "Chat": "AIzaSyDKIs5LJqP5GW8BAJZbkXEDPtAOseI5IUo",
        "Tracker": "AIzaSyDKIs5LJqP5GW8BAJZbkXEDPtAOseI5IUo"
    }

    @classmethod
    def call(cls, role, prompt, image=None, safety_settings=None, **kwargs):
        """
        Perform an ATOMIC AI call. Locks the library, configures the key,
        generates content, and releases.
        """
        api_key = cls.KEYS.get(role, cls.KEYS["Vault"])
        
        # MODEL TIERING:
        # 1. gemini-1.5-flash-8b (Highly efficient, higher rate limits in some tiers)
        # 2. gemini-flash-latest (Reliable 1.5-flash)
        # 3. gemini-2.0-flash-lite (Fastest/New)
        candidates = ['gemini-1.5-flash-8b', 'gemini-flash-latest', 'gemini-2.0-flash-lite']
        
        # Priority logic: If role is "Tracker" (Scraper), it should yield if Vault is busy
        # For now, we use a simple lock, but we can add more nuanced yield logic here.
        
        with cls._lock:
            print(f"🔒 [AI-SYNC] Locking for role: {role}")
            genai.configure(api_key=api_key)
            
            errors = []
            for model_name in candidates:
                try:
                    print(f"📡 [AI-SYNC] Probing {model_name} for {role}...")
                    model = genai.GenerativeModel(model_name)
                    
                    if image:
                        response = model.generate_content([prompt, image], safety_settings=safety_settings, **kwargs)
                    else:
                        response = model.generate_content(prompt, safety_settings=safety_settings, **kwargs)
                    
                    print(f"✅ [AI-SYNC] Success with {model_name}")
                    return response
                except Exception as e:
                    error_str = str(e)
                    print(f"⚠️ [AI-SYNC] {model_name} failed: {error_str[:100]}")
                    
                    # If it's a 429 (Rate Limit):
                    if "429" in error_str or "quota" in error_str.lower():
                        if role == "Tracker":
                            print(f"⏳ [AI-SYNC] Scraper hit rate limit. Cooling down for 10s...")
                            time.sleep(10) # Scraper yields longer
                        continue # Try next model
                    
                    if "404" in error_str or "not found" in error_str.lower():
                        continue # Try next model
                        
                    errors.append(f"{model_name}: {error_str[:40]}")
                    continue

            print(f"❌ [AI-SYNC] All models exhausted for {role}.")
            raise Exception(f"AI exhaustion for {role}. Failures: {' | '.join(errors)}")

# Global helper for easy access
def ai_dispatch(role, prompt, image=None, **kwargs):
    return AIGatekeeper.call(role, prompt, image=image, **kwargs)
