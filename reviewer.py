class ReviewerAgent:
    def __init__(self):
        pass

    def review(self, content, grade):
        feedback = []

        explanation = content.get("explanation", "")
        mcqs = content.get("mcqs", [])

        # Sentence length check
        sentences = explanation.split(".")
        for i, sentence in enumerate(sentences):
            if len(sentence.split()) > 12:
                feedback.append(f"Sentence {i+1} is too long for Grade {grade}")

        # Difficult words check
        difficult_words = ["approximately", "complex", "difficult", "advanced"]
        for word in difficult_words:
            if word in explanation.lower():
                feedback.append(f"Word '{word}' is too difficult for Grade {grade}")

        # MCQ count check
        if len(mcqs) < 3:
            feedback.append("Not enough MCQs (minimum 3 required)")

        # MCQ checks
        for i, mcq in enumerate(mcqs):
            if "question" not in mcq or "options" not in mcq or "answer" not in mcq:
                feedback.append(f"MCQ {i+1} structure is incorrect")

            if len(mcq.get("options", [])) != 4:
                feedback.append(f"MCQ {i+1} does not have 4 options")

            if mcq.get("answer") not in mcq.get("options", []):
                feedback.append(f"MCQ {i+1} answer does not match options")

        status = "pass" if len(feedback) == 0 else "fail"

        return {
            "status": status,
            "feedback": feedback
        }