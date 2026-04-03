from generator import GeneratorAgent
from reviewer import ReviewerAgent


class AgentPipeline:
    def __init__(self, api_key):
        self.generator = GeneratorAgent(api_key)
        self.reviewer = ReviewerAgent()

    def run(self, grade, topic):
        generated = self.generator.generate(grade, topic)

        if "error" in generated:
            return {
                "generated": generated,
                "review": {"status": "fail", "feedback": ["Invalid JSON from generator"]},
                "refined": None
            }

        review = self.reviewer.review(generated, grade)

        refined_output = None

        if review["status"] == "fail":
            feedback_text = " | ".join(review["feedback"])
            refined_output = self.generator.generate(grade, topic, feedback=feedback_text)

        return {
            "generated": generated,
            "review": review,
            "refined": refined_output
        }