import streamlit as st
from pipeline import AgentPipeline
import json
import time

st.set_page_config(page_title="AI Agent System", layout="wide")

st.title("⚡ AI Agent Pipeline for Educational Content Generation")

st.markdown("""
### 🔄 Agent Pipeline Flow  
**Generator → Reviewer → (Optional Refinement)**
""")

with st.expander("🧠 How this system works"):
    st.write("""
    - Generator Agent creates structured educational content using an LLM
    - Reviewer Agent evaluates clarity, correctness, and grade appropriateness
    - If failed, system refines output using feedback-aware prompting
    """)

col1, col2, col3 = st.columns(3)

with col1:
    grade = st.slider("Grade", 1, 12, 4)

with col2:
    topic = st.text_input("Topic", "Types of angles")

with col3:
    api_key = st.text_input("Groq API Key", type="password")

generate = st.button("🚀 Generate Content")

if generate:
    if not api_key:
        st.error("Please enter API key")
    else:
        pipeline = AgentPipeline(api_key)

        # -------- Generator --------
        with st.spinner("🧠 Generator Agent is generating educational content..."):
            time.sleep(1)
            generated = pipeline.generator.generate(grade, topic)

        st.success("✅ Content Generated")
        st.divider()

        # -------- Display Generated --------
        st.subheader("📘 Explanation")
        st.write(generated.get("explanation", ""))

        st.divider()

        st.subheader("📝 MCQs")
        for mcq in generated.get("mcqs", []):
            st.write(f"**Q:** {mcq['question']}")
            for opt in mcq["options"]:
                if opt == mcq["answer"]:
                    st.success(opt)
                else:
                    st.write(opt)

        st.divider()

        # -------- Reviewer --------
        st.info("🔍 Reviewer Agent is evaluating content...")
        review = pipeline.reviewer.review(generated, grade)

        if review["status"] == "pass":
            st.success("✅ Passed Review")
            st.info("ℹ️ No refinement needed")

        else:
            st.error("❌ Failed Review")
            st.warning("⚠️ Initial output failed. Refining...")

            if review["feedback"]:
                for f in review["feedback"]:
                    st.warning(f)

            st.divider()

            # -------- Refinement --------
            with st.spinner("♻️ Generator Agent is refining content..."):
                time.sleep(1)
                refined = pipeline.generator.generate(
                    grade,
                    topic,
                    feedback=" | ".join(review["feedback"])
                )

            st.subheader("♻️ Refined Output")

            # Explanation
            st.write(refined.get("explanation", ""))

            st.divider()

            # MCQs
            for mcq in refined.get("mcqs", []):
                st.write(f"**Q:** {mcq['question']}")
                for opt in mcq["options"]:
                    if opt == mcq["answer"]:
                        st.success(opt)
                    else:
                        st.write(opt)

            st.divider()

            # -------- Final Review --------
            st.info("🔍 Reviewer Agent is re-evaluating refined content...")
            final_review = pipeline.reviewer.review(refined, grade)

            if final_review["status"] == "pass":
                st.success("✅ Refined Output Passed Review")
            else:
                st.error("❌ Refined Output Still Failing")

        # -------- Download --------
        st.download_button(
            label="📥 Download Output",
            data=json.dumps({
                "generated": generated,
                "review": review
            }, indent=2),
            file_name="output.json"
        )