# Simple Agent Eval

A simple evaluation framework for AI agents, demonstrated with an email tone analyzer powered by Claude.

## Overview

This project showcases how to build and evaluate AI agents using a practical example - an email tone analysis system that achieves **92% accuracy** across multiple test scenarios.

## Features

- **Email Tone Analysis**: Identifies 6 tone categories (professional, casual, urgent, friendly, aggressive, apologetic)
- **High Accuracy**: 92% average score on comprehensive evaluations
- **Robust Evaluation Framework**: Systematic testing with confidence scoring and keyword matching
- **Detailed Feedback**: Provides explanations and suggestions for tone improvement
- **Error Handling**: Robust JSON parsing with fallback error reporting

## Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up your Anthropic API key:**
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

3. **Run a single analysis:**
```bash
python src/app.py
```

4. **Run the full evaluation suite:**
```bash
python evals/run_evals.py
```

## Project Structure

```
simple-agent-eval/
├── src/
│   ├── app.py           # EmailToneAnalyzer class with Claude integration
│   └── prompts.py       # Optimized prompts for tone analysis
├── evals/
│   ├── run_evals.py     # Evaluation framework
│   ├── test_cases/
│   │   └── tone_examples.json  # Test scenarios
│   └── results/         # Timestamped evaluation results
├── requirements.txt     # Python dependencies
└── README.md
```

## Evaluation Results

The system achieves excellent performance across diverse email scenarios:

- **Average Score**: 92.0/100
- **Test Coverage**: 5 scenarios (urgent, professional, friendly, apologetic, mixed tone)
- **All Tests Passing**: 100% success rate with proper JSON parsing
- **High Confidence**: Consistent 9/10 confidence scores

### Sample Test Cases

| Scenario | Email Type | Expected Tone | Score |
|----------|------------|---------------|-------|
| `professional_001` | Business partnership | Professional | 100% |
| `mixed_001` | Urgent + apologetic | Urgent | 93.3% |
| `friendly_001` | Casual check-in | Friendly | 90% |
| `apologetic_001` | Delay notification | Apologetic | 90% |
| `urgent_001` | Report request | Urgent | 86.7% |

## Key Implementation Details

### Robust JSON Parsing
The system includes sophisticated error handling for LLM responses:
- Parses JSON responses from Claude
- Provides fallback error reporting with raw response data
- Handles edge cases in model output formatting

### Evaluation Framework
- **Scoring System**: Multi-faceted evaluation (tone accuracy, confidence, keyword matching, suggestions)
- **Keyword Matching**: Validates explanations contain expected terminology
- **Confidence Thresholds**: Ensures model certainty meets test requirements
- **Timestamped Results**: Tracks performance over time

### Prompt Engineering
The prompts have been optimized to:
- Ensure JSON-only responses (no extra commentary)
- Provide clear tone categorization guidelines
- Include confidence rating instructions
- Generate actionable improvement suggestions

## Usage Examples

### Analyzing Email Tone
```python
from src.app import EmailToneAnalyzer

analyzer = EmailToneAnalyzer()
result = analyzer.analyze_tone("Hi John, I need the report ASAP...")

print(result)
# {
#   "primary_tone": "urgent",
#   "confidence": 9,
#   "explanation": "Phrases like 'ASAP' signal time pressure...",
#   "suggestions": "Consider adding context about urgency..."
# }
```

### Running Custom Evaluations
```python
from evals.run_evals import run_evaluation

avg_score, results = run_evaluation()
print(f"Average performance: {avg_score}%")
```

## Contributing

This framework can be extended for other AI agent evaluation scenarios:

1. **Add New Test Cases**: Extend `tone_examples.json` with additional scenarios
2. **Custom Evaluation Metrics**: Modify the scoring system in `run_evals.py`
3. **Different AI Tasks**: Adapt the framework for other Claude-powered applications

## License

MIT License - feel free to use this as a template for your own agent evaluation projects.

---

*This project demonstrates practical AI agent development with comprehensive testing - perfect for learning prompt engineering, evaluation frameworks, and working with Claude's API.*
