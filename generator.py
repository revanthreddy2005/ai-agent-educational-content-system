from groq import Groq
import json


class GeneratorAgent:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)

    def generate(self, grade, topic, feedback=None):
        prompt = f"""
You are an educational content generator.

Generate content for:
Grade: {grade}
Topic: {topic}

Rules:
- Use very simple language suitable for the grade
- Keep sentences short and clear
- First give a short explanation
- Then create 3 MCQs
- Questions should not repeat or be too trivial
- Questions must test understanding of the topic

Each MCQ must have:
- question
- 4 options labeled A, B, C, D
- correct answer must EXACTLY match one option text

Return ONLY in JSON format:
{{
  "explanation": "...",
  "mcqs": [
    {{
      "question": "...",
      "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
      "answer": "A. ..."
    }}
  ]
}}
"""

        if feedback:
            prompt += f"""
IMPORTANT:
You MUST improve the previous response using this feedback:
{feedback}

- Simplify sentences further
- Fix all mentioned issues
- Ensure it passes review
"""

        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        output_text = response.choices[0].message.content

        try:
            return json.loads(output_text)
        except:
            return {
                "error": "Invalid JSON output",
                "raw": output_text
            }