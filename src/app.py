# import os
# import json
# from anthropic import Anthropic
# from dotenv import load_dotenv
# from prompts import TONE_ANALYSIS_PROMPT

# load_dotenv()

# class EmailToneAnalyzer:
#     def __init__(self):
#         self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
#     def analyze_tone(self, email_content):
#         prompt = TONE_ANALYSIS_PROMPT.format(email_content=email_content)
        

        
#         response = self.client.messages.create(
#             model="claude-3-5-haiku-latest",
#             max_tokens=300,
#             messages=[{"role": "user", "content": prompt}]
#         )
        
#         try:
#             # Parse the JSON response
#             result = json.loads(response.content[0].text)
#             return result
#         except json.JSONDecodeError:
#             return {"error": "Failed to parse response", "raw": response.content[0].text}

# # Test it out
# if __name__ == "__main__":
#     analyzer = EmailToneAnalyzer()
    
#     test_email = """
#     Hi John,
    
#     I need the quarterly report ASAP. The board meeting is tomorrow and I don't have the numbers yet.
    
#     Thanks,
#     Sarah
#     """
    
#     result = analyzer.analyze_tone(test_email)
#     print(json.dumps(result, indent=2))




# Import built-in and external libraries
import os               # for accessing environment variables like your API key
import json             # for parsing the model's JSON output into Python dicts
from anthropic import Anthropic   # official Anthropic SDK client
from dotenv import load_dotenv    # loads variables from a .env file into environment
from prompts import TONE_ANALYSIS_PROMPT  # custom prompt template from prompts.py

# Load environment variables from the .env file (so ANTHROPIC_API_KEY is available)
load_dotenv()

class EmailToneAnalyzer:
    """
    A small helper class that uses Anthropic's API to analyze the tone of emails.
    """

    def __init__(self):
        # Initialize the Anthropic client with your API key
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    def analyze_tone(self, email_content):
        """
        Take an email's text, inject it into the prompt, send it to the model,
        and return the model's JSON-formatted analysis.
        """

        # Insert the actual email content into the prompt template
        prompt = TONE_ANALYSIS_PROMPT.format(email_content=email_content)
        
        # Call the Anthropic Messages API with the prepared prompt
        response = self.client.messages.create(
            model="claude-3-5-haiku-latest",   # model version to use
            max_tokens=300,                    # limit on how many tokens the model can return
            messages=[{"role": "user", "content": prompt}]  # send the prompt as a user message
        )
        
        try:
            # The model response comes back as text. Parse the first content block as JSON.
            result = json.loads(response.content[0].text)
            return result
        except json.JSONDecodeError:
            # If parsing fails (e.g. model output wasn’t valid JSON), return the raw text
            return {"error": "Failed to parse response", "raw": response.content[0].text}

# Test the class if this file is run directly (not imported as a module)
if __name__ == "__main__":
    analyzer = EmailToneAnalyzer()  # create an analyzer instance
    
    # A sample email to analyze
    test_email = """
    Hi Hannah! How are you mate?
    
    Just wondering where you are at with the report? 
    Cheers friendo.

    """
    
    # Analyze the tone of the test email
    result = analyzer.analyze_tone(test_email)

    # Pretty-print the JSON result
    print(json.dumps(result, indent=2))