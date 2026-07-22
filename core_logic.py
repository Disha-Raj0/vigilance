import google.generativeai as genai
import json

def analyze_content(input_data, mode="text"):
    # Initialize Models
    # Flash for text (speed), Pro for images (accuracy)
    model_name = "gemini-1.5-flash" if mode == "text" else "gemini-1.5-pro"
    model = genai.GenerativeModel(model_name)
    
    if mode == "text":
        prompt = "Analyze this for Digital Arrest/Scam patterns. Output JSON: {risk_score: int, verdict: str, flags: list, action: str}"
        response = model.generate_content([prompt, input_data])
    else:
        prompt = "Analyze this Indian Currency Note for counterfeiting. Check serial numbers, thread, and watermark. Output JSON: {is_genuine: bool, confidence: int, defects: list}"
        response = model.generate_content([prompt, input_data])
    
    # Clean and parse JSON
    clean_json = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(clean_json)

def get_geo_insights(map_data):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    Analyze this summary of cybercrime hotspots in India: {map_data}.
    1. Identify the top 2 dangerous 'Scam Corridors'.
    2. Suggest where Law Enforcement should increase digital patrolling.
    3. Provide a 'Threat Forecast' for the next 30 days based on these clusters.
    Keep it professional and concise for a Police Briefing.
    """
    response = model.generate_content(prompt)
    return response.text