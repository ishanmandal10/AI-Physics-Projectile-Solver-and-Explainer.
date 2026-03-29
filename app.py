import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from groq import Groq
import time

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Physics Applet", layout="wide")

#  API key
client = Groq(api_key="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")

g = 9.8

# ---------------- TITLE ----------------
st.title("🚀 AI Physics Applet")
st.markdown("Projectile Motion + AI Tutor + Numerical Solver")

# ---------------- INPUT + GRAPH ----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎛️ Controls")

    velocity = st.slider("Velocity (m/s)", 1, 100, 20)
    angle_deg = st.slider("Angle (degrees)", 0, 90, 45)

    angle = np.radians(angle_deg)

    time_of_flight = (2 * velocity * np.sin(angle)) / g
    range_ = (velocity**2 * np.sin(2 * angle)) / g
    height = (velocity**2 * (np.sin(angle))**2) / (2 * g)

    st.subheader("📊 Results")
    st.metric("Time of Flight", f"{time_of_flight:.2f} s")
    st.metric("Range", f"{range_:.2f} m")
    st.metric("Max Height", f"{height:.2f} m")

with col2:
    st.subheader("📈 Trajectory")

    t = np.linspace(0, time_of_flight, 100)
    x = velocity * np.cos(angle) * t
    y = velocity * np.sin(angle) * t - 0.5 * g * t**2

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Height (m)")
    st.pyplot(fig)

# ---------------- ANIMATION ----------------
st.subheader("🎥 Animation")

if st.button("▶️ Play Animation", key="btn_animation"):
    plot_placeholder = st.empty()

    for i in range(len(t)):
        fig, ax = plt.subplots()

        ax.plot(x, y, linestyle="dashed", alpha=0.5)
        ax.scatter(x[i], y[i], s=100)

        ax.set_xlim(0, max(x)*1.1)
        ax.set_ylim(0, max(y)*1.2)

        ax.set_xlabel("Distance (m)")
        ax.set_ylabel("Height (m)")

        plot_placeholder.pyplot(fig)
        time.sleep(0.02)

# ==============================
# 🤖 AI EXPLANATION
# ==============================

st.divider()
st.subheader("🤖 Ask AI")

question = st.text_input("Type your physics question here", key="input_question")

if st.button("Explain Concept 🤖", key="btn_explain"):
    if question.strip() == "":
        st.warning("Please enter a question")
    else:
        try:
            prompt = f"""
            You are a physics teacher.

            Explain this clearly with intuition and examples:

            {question}
            """

            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
            )

            st.success("Explanation:")
            st.write(response.choices[0].message.content)

        except Exception as e:
            st.error(f"Error: {e}")

# ==============================
# 🧠 NUMERICAL SOLVER
# ==============================

st.divider()
st.subheader("🧠 AI Numerical Solver")

problem = st.text_area("Enter your physics problem here", key="input_problem")

if st.button("Solve Numerical 🧠", key="btn_solver"):
    if problem.strip() == "":
        st.warning("Please enter a problem")
    else:
        try:
            prompt = f"""
            Solve this physics problem step by step:

            {problem}

            Provide:
            1. Known values
            2. Formula used
            3. Step-by-step solution
            4. Final answer (with units)

            Keep it simple and clear.
            """

            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
            )

            st.success("Solution:")
            st.write(response.choices[0].message.content)

        except Exception as e:
            st.error(f"Error: {e}")