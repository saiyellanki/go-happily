import random
import streamlit as st


def init_state():
    if "history" not in st.session_state:
        st.session_state.history = []
    if "tone" not in st.session_state:
        st.session_state.tone = "Friendly"


QUOTES = [
    ("You have power over your mind — not outside events. Realize this, and you will find strength.", "Marcus Aurelius — Meditations (public domain)"),
    ("Waste no more time arguing about what a good person should be. Be one.", "Marcus Aurelius — Meditations (public domain)"),
    ("The present moment is all you ever have.", "Unknown — Traditional wisdom"),
]


def validate_message(msg):
    return f"I hear you: \"{msg}\". It's okay to feel that way."


def grounding_exercise():
    steps = [
        "Name 5 things you can see.",
        "Name 4 things you can touch.",
        "Name 3 things you can hear.",
        "Name 2 things you can smell.",
        "Name 1 thing you can taste (or imagine a taste).",
    ]
    return "Try this 5-4-3-2-1 grounding: " + " ".join(steps)


def cbt_reframe(msg):
    # very simple cognitive reframe scaffold
    reframe = (
        "Let's try a small reframe: what evidence supports this thought? "
        "What would you tell a friend in this situation? How might you test this belief?"
    )
    return reframe


def motivate(msg=None):
    lines = [
        "Small steps add up — one gentle step at a time.",
        "You are doing better than you think; progress is often quiet.",
        "Be kind to yourself today; you deserve patience and care.",
    ]
    if msg and "tired" in msg.lower():
        lines.append("Rest is productive. It's okay to pause and recharge.")
    return random.choice(lines)


def make_response(user_msg, response_type):
    if response_type == "Support":
        return f"{validate_message(user_msg)}\n\n{motivate(user_msg)}"
    if response_type == "Quote":
        q, src = random.choice(QUOTES)
        return f"\"{q}\" — {src}"
    if response_type == "Grounding":
        return grounding_exercise()
    if response_type == "Reframe":
        return cbt_reframe(user_msg)
    if response_type == "Practical Tip":
        return "Try a tiny, specific next step: what's one 5-minute action you can take now?"
    return "I'm here with you. Tell me more."


def app():
    init_state()

    st.set_page_config(page_title="Go Happily — Encouraging Friend", page_icon="🙂")
    st.title("🙂 Go Happily — Your Friendly Motivational Companion")

    st.write(
        "A gentle, positivity-focused chat assistant offering supportive words, short grounding exercises, motivational quotes (some public-domain), and simple CBT-style reframes."
    )

    with st.sidebar:
        st.header("Settings")
        st.session_state.tone = st.selectbox("Tone", ["Friendly", "Warm", "Gentle"], index=0)
        show_frameworks = st.checkbox("Show mental-health frameworks", value=True)
        if show_frameworks:
            st.markdown(
                "**Frameworks included:** validation, grounding (5-4-3-2-1), simple CBT reframes, tiny-step motivation."
            )

    # Chat input
    response_type = st.selectbox("Response Type", ["Support", "Quote", "Grounding", "Reframe", "Practical Tip"])
    user_msg = st.text_area("What's on your mind?", height=120)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Send"):
            if user_msg.strip() == "":
                st.warning("Please type a little about how you're feeling or what you need.")
            else:
                resp = make_response(user_msg, response_type)
                st.session_state.history.append(("You", user_msg))
                st.session_state.history.append(("GoHappily", resp))
    with col2:
        if st.button("Grounding Exercise"):
            resp = grounding_exercise()
            st.session_state.history.append(("GoHappily", resp))

    st.markdown("---")

    # Conversation view
    if st.session_state.history:
        for speaker, text in st.session_state.history[::-1]:
            if speaker == "You":
                st.markdown(f"**You:** {text}")
            else:
                st.markdown(f"**{speaker}:** {text}")

    col_clear, col_export = st.columns([1, 1])
    with col_clear:
        if st.button("Clear conversation"):
            st.session_state.history = []
    with col_export:
        if st.button("Download conversation"):
            data = "\n\n".join([f"{s}: {t}" for s, t in st.session_state.history])
            st.download_button("Download TXT", data=data, file_name="gohappily_conversation.txt")


if __name__ == "__main__":
    app()

