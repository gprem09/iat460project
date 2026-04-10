import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

def analyze_text(txt: str):
    key = os.getenv("GEMINI_API_KEY")
    if not key or key == "your_gemini_api_key_here":
        raise ValueError("GEMINI_API_KEY is missing or not configured in .env")
        
    c = genai.Client(api_key=key)
    
    prompt = f"""
    Analyze the following text and extract its core emotional data for a generative art embroidery project.
    
    Text: "{txt}"
    
    Respond STRICTLY with a JSON object containing the following keys:
    - "primary_emotion": A single word summarizing the main emotion (e.g., "melancholy", "joy", "anger").
    - "intensity_score": A float between 0.0 and 1.0 indicating how intense the emotion is.
    - "color_palette": An array of EXACTLY 7 dictionaries representing a cohesive embroidery thread color palette that perfectly matches the emotion. The palette MUST be sorted from darkest to lightest. Each dictionary MUST contain:
        - "hex": A valid 6-character hex color code (e.g., "#3A5B8C").
        - "name": A beautiful, poetic, evocative name for the thread color (e.g., "Ocean Depth Blue", "Withered Rose", "Electric Dawn").
    - "poetic_subtitle": A short, evocative phrase (maximum 10 words) that captures the mood of the text. This will be printed on the final artwork.
    
    Do not include any markdown formatting, just the raw JSON string.
    """
    
    retries = 3
    for i in range(retries):
        try:
            resp = c.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                ),
            )
            
            res = json.loads(resp.text)
            
            required_keys = ("primary_emotion", "intensity_score", "color_palette", "poetic_subtitle")
            if not all(k in res for k in required_keys):
                raise ValueError(f"Response missing required keys: {[k for k in required_keys if k not in res]}")
                
            if len(res["color_palette"]) != 7:
                raise ValueError(f"Expected 7 palette colors, got {len(res['color_palette'])}")
                
            res["intensity_score"] = float(res.get("intensity_score", 0.5))
            res["intensity_score"] = max(0.0, min(1.0, res["intensity_score"]))
                
            return res
            
        except Exception as e:
            print(f"Gemini attempt {i + 1}/{retries} failed: {e}")
            if i == retries - 1:
                return {
                    "primary_emotion": "Neutral",
                    "intensity_score": 0.5,
                    "poetic_subtitle": "Threads of quiet contemplation woven in silence.",
                    "color_palette": [
                        {"hex": "#1A1A1A", "name": "Midnight Void"},
                        {"hex": "#333333", "name": "Deep Shadow"},
                        {"hex": "#4D4D4D", "name": "Storm Cloud"},
                        {"hex": "#666666", "name": "Steel Rain"},
                        {"hex": "#808080", "name": "Stone Path"},
                        {"hex": "#999999", "name": "Morning Mist"},
                        {"hex": "#B3B3B3", "name": "Pale Ash"}
                    ]
                }

if __name__ == "__main__":
    sample = "I walked through the empty house. The silence was heavy, broken only by the ticking clock. I missed them so much."
    
    try:
        result = analyze_text(sample)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Analysis failed: {e}")
