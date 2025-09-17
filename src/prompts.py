#THIS WAS THE OLD PROMPT

# TONE_ANALYSIS_PROMPT = """
# Analyze the tone of this email and provide a structured response.

# Email to analyze:
# {email_content}

# Respond with exactly this JSON format:
# {{
#     "primary_tone": "one of: professional, casual, urgent, friendly, aggressive, apologetic",
#     "confidence": "number from 1-10",
#     "explanation": "brief explanation of why you chose this tone",
#     "suggestions": "brief suggestion for improvement if needed"
# }}
# """


#THIS IS AN IMPROVED PROMPT
TONE_ANALYSIS_PROMPT = """
You are an expert at analyzing email communication tone. Analyze the tone of this email carefully.

Email to analyze:
{email_content}

Consider these factors:
- Word choice (formal vs casual language)
- Urgency indicators (deadlines, "ASAP", etc.)
- Emotional markers (apologies, enthusiasm, frustration)
- Greeting and closing formality

Rate your confidence from 1-10 where:
- 8-10: Very clear tone indicators
- 5-7: Some ambiguity but clear primary tone
- 1-4: Mixed or unclear signals

CRITICAL: Respond with ONLY the JSON below. Do not add any additional text, commentary, or explanation outside of the JSON structure.

{{
    "primary_tone": "one of: professional, casual, urgent, friendly, aggressive, apologetic",
    "confidence": number from 1-10,
    "explanation": "explain specific words/phrases that indicate this tone",
    "suggestions": "brief suggestion for improvement if tone could be better"
}}
"""

