import streamlit as st

from maki import DEFAULT_TOPIC, generate_blog_post

st.title("Blog Post Generator")

topic = st.text_input("Topic", value=DEFAULT_TOPIC)

if st.button("Generate"):
    with st.spinner("Generating blog post..."):
        try:
            result = generate_blog_post(topic=topic.strip() or DEFAULT_TOPIC, verbose=True)
            st.subheader("Result")
            st.write(result)
        except Exception as exc:
            st.error(str(exc))
