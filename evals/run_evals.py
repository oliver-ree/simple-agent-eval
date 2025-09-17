# import json
# import sys
# import os
# from datetime import datetime

# # Add src to path so we can import our app
# sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
# from app import EmailToneAnalyzer

# def load_test_cases(filename):
#     with open(filename, 'r') as f:
#         return json.load(f)

# def evaluate_response(actual, expected):
#     """Score a single response against expected criteria"""
#     score = 0
#     feedback = []
    
#     # Check if primary tone matches
#     if actual.get("primary_tone") == expected["primary_tone"]:
#         score += 40
#         feedback.append("✓ Correct primary tone")
#     else:
#         feedback.append(f"✗ Expected {expected['primary_tone']}, got {actual.get('primary_tone')}")
    
#     # Check confidence level
#     confidence = actual.get("confidence", 0)
#     if confidence >= expected["confidence_min"]:
#         score += 20
#         feedback.append(f"✓ Confidence adequate ({confidence})")
#     else:
#         feedback.append(f"✗ Low confidence ({confidence}, expected ≥{expected['confidence_min']})")
    
#     # Check if explanation contains expected keywords
#     explanation = actual.get("explanation", "").lower()
#     keyword_matches = sum(1 for keyword in expected["should_contain"] 
#                          if keyword in explanation)
    
#     if keyword_matches > 0:
#         score += 20 * (keyword_matches / len(expected["should_contain"]))
#         feedback.append(f"✓ Found {keyword_matches}/{len(expected['should_contain'])} expected keywords")
#     else:
#         feedback.append("✗ No expected keywords found in explanation")
    
#     # Bonus points for having suggestions
#     if actual.get("suggestions"):
#         score += 20
#         feedback.append("✓ Provided suggestions")
    
#     return min(score, 100), feedback

# def run_evaluation():
#     print("🧪 Running Email Tone Analyzer Evaluations...\n")
    
#     # Load test cases
#     test_cases = load_test_cases('evals/test_cases/tone_examples.json')
    
#     # Initialize analyzer
#     analyzer = EmailToneAnalyzer()
    
#     results = []
#     total_score = 0
    
#     for i, test_case in enumerate(test_cases, 1):
#         print(f"Running test {i}/{len(test_cases)}: {test_case['id']}")
        
#         try:
#             # Get Claude's response
#             response = analyzer.analyze_tone(test_case['email'])
            
#             # Evaluate it
#             score, feedback = evaluate_response(response, test_case['expected'])
            
#             result = {
#                 'test_id': test_case['id'],
#                 'score': score,
#                 'feedback': feedback,
#                 'response': response,
#                 'expected': test_case['expected']
#             }
            
#             results.append(result)
#             total_score += score
            
#             print(f"  Score: {score}/100")
#             for fb in feedback:
#                 print(f"    {fb}")
#             print()
            
#         except Exception as e:
#             print(f"  ❌ Error: {e}\n")
#             results.append({
#                 'test_id': test_case['id'],
#                 'score': 0,
#                 'error': str(e)
#             })
    
#     # Calculate overall performance
#     avg_score = total_score / len(test_cases)
    
#     print("=" * 50)
#     print(f"📊 EVALUATION RESULTS")
#     print(f"Average Score: {avg_score:.1f}/100")
#     print(f"Tests Passed: {sum(1 for r in results if r.get('score', 0) >= 80)}/{len(results)}")
    
#     # Save detailed results
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     results_file = f"evals/results/eval_{timestamp}.json"
    
#     with open(results_file, 'w') as f:
#         json.dump({
#             'timestamp': timestamp,
#             'average_score': avg_score,
#             'results': results
#         }, f, indent=2)
    
#     print(f"Detailed results saved to: {results_file}")
    
#     return avg_score, results

# if __name__ == "__main__":
#     run_evaluation()


import json
import sys
import os
from datetime import datetime

# --- Setup imports -------------------------------------------------------

# Add the `src` folder to Python's search path so we can import our app.py
# This makes `from app import EmailToneAnalyzer` work when running from project root
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from app import EmailToneAnalyzer

# --- Helper functions ---------------------------------------------------

def load_test_cases(filename):
    """Load test cases (emails + expected results) from a JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)

def evaluate_response(actual, expected):
    """
    Compare the model's response (actual) against expected criteria.
    Return a score (0–100) and a list of feedback messages.
    """
    score = 0
    feedback = []
    
    # 1. Check if primary tone matches exactly
    if actual.get("primary_tone") == expected["primary_tone"]:
        score += 40
        feedback.append("✓ Correct primary tone")
    else:
        feedback.append(f"✗ Expected {expected['primary_tone']}, got {actual.get('primary_tone')}")
    
    # 2. Check if model confidence is at least the minimum required
    confidence = actual.get("confidence", 0)
    if confidence >= expected["confidence_min"]:
        score += 20
        feedback.append(f"✓ Confidence adequate ({confidence})")
    else:
        feedback.append(f"✗ Low confidence ({confidence}, expected ≥{expected['confidence_min']})")
    
    # 3. Check if explanation contains at least one expected keyword
    explanation = actual.get("explanation", "").lower()
    keyword_matches = sum(1 for keyword in expected["should_contain"] 
                         if keyword in explanation)
    
    if keyword_matches > 0:
        # Partial credit based on how many keywords were matched
        score += 20 * (keyword_matches / len(expected["should_contain"]))
        feedback.append(f"✓ Found {keyword_matches}/{len(expected['should_contain'])} expected keywords")
    else:
        feedback.append("✗ No expected keywords found in explanation")
    
    # 4. Bonus points if suggestions were provided
    if actual.get("suggestions"):
        score += 20
        feedback.append("✓ Provided suggestions")
    
    # Cap the score at 100
    return min(score, 100), feedback

# --- Main evaluation loop ------------------------------------------------

def run_evaluation():
    print("🧪 Running Email Tone Analyzer Evaluations...\n")
    
    # Load all test cases (list of {id, email, expected})
    test_cases = load_test_cases('evals/test_cases/tone_examples.json')
    
    # Initialize the tone analyzer (Claude client)
    analyzer = EmailToneAnalyzer()
    
    results = []     # store results of each test
    total_score = 0  # keep track of average
    
    # Loop through each test case
    for i, test_case in enumerate(test_cases, 1):
        print(f"Running test {i}/{len(test_cases)}: {test_case['id']}")
        
        try:
            # Send the email text to the analyzer (calls Claude)
            response = analyzer.analyze_tone(test_case['email'])
            
            # Compare model response with expected output
            score, feedback = evaluate_response(response, test_case['expected'])
            
            # Record the result
            result = {
                'test_id': test_case['id'],
                'score': score,
                'feedback': feedback,
                'response': response,
                'expected': test_case['expected']
            }
            
            results.append(result)
            total_score += score
            
            # Print a summary to console
            print(f"  Score: {score}/100")
            for fb in feedback:
                print(f"    {fb}")
            print()
            
        except Exception as e:
            # Catch errors so one broken test doesn't crash everything
            print(f"  ❌ Error: {e}\n")
            results.append({
                'test_id': test_case['id'],
                'score': 0,
                'error': str(e)
            })
    
    # --- Final summary ---------------------------------------------------
    
    avg_score = total_score / len(test_cases)
    
    print("=" * 50)
    print(f"📊 EVALUATION RESULTS")
    print(f"Average Score: {avg_score:.1f}/100")
    print(f"Tests Passed: {sum(1 for r in results if r.get('score', 0) >= 80)}/{len(test_cases)}")
    
    # Save results to a timestamped JSON file under evals/results/
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"evals/results/eval_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        json.dump({
            'timestamp': timestamp,
            'average_score': avg_score,
            'results': results
        }, f, indent=2)
    
    print(f"Detailed results saved to: {results_file}")
    
    return avg_score, results

# --- Script entrypoint ---------------------------------------------------

if __name__ == "__main__":
    # Only run evaluations if script is executed directly
    run_evaluation()