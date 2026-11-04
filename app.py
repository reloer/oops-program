
import streamlit as st
import json

from core.database import (
    init_db,
    add_memory,
    get_memories,
    update_memory,
    delete_memory,
    get_stats,
    get_timeline
)

from core.documents import extract_text, split_text
from core.assistant import answer_question

st.set_page_config(
    page_title="MindVault",
    page_icon="🧠",
    layout="wide"
)

init_db()

st.markdown("""
<style>
.stApp {
    background-color: #f5f7fb;
}
.block-container {
    max-width: 1200px;
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

if "chat" not in st.session_state:
    st.session_state.chat = []

st.sidebar.title("🧠 MindVault")
st.sidebar.caption("Your Personal Digital Memory")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Add Memory",
        "Memory Library",
        "Ask MindVault",
        "Documents",
        "Settings"
    ]
)

st.title("🧠 MindVault")
st.caption("Your personal second brain")

if page == "Dashboard":

    total, categories, documents = get_stats()

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Memories", total)
    c2.metric("Categories", categories)
    c3.metric("Document Sources", documents)

    st.subheader("Recent Memories")

    memories = get_memories()

    if memories:

        for memory in memories[:8]:

            with st.container(border=True):

                st.subheader(memory["title"])

                st.write(memory["content"][:300])

                st.caption(
                    memory["category"] +
                    " | " +
                    str(memory["created_at"])
                )

    else:
        st.info("Start by adding your first memory.")

    st.subheader("Memory Activity")

    timeline = get_timeline()

    if not timeline.empty:
        st.bar_chart(
            timeline.set_index("day")["count"]
        )

elif page == "Add Memory":

    st.subheader("Save New Memory")

    with st.form("memory_form"):

        title = st.text_input("Memory Title")

        category = st.selectbox(
            "Category",
            [
                "Personal",
                "Education",
                "Projects",
                "Technology",
                "Work",
                "Ideas",
                "Other"
            ]
        )

        tags = st.text_input("Tags")

        content = st.text_area(
            "Memory Content",
            height=220
        )

        submitted = st.form_submit_button(
            "Save Memory"
        )

        if submitted:

            if title.strip() and content.strip():

                add_memory(
                    title.strip(),
                    content.strip(),
                    category,
                    tags,
                    "manual"
                )

                st.success("Memory saved successfully!")

            else:
                st.error("Enter both title and content.")

elif page == "Memory Library":

    st.subheader("Your Saved Memories")

    memories = get_memories()

    query = st.text_input("Filter memories")

    categories = sorted(
        set(m["category"] for m in memories)
    )

    category = st.selectbox(
        "Filter by category",
        ["All"] + categories
    )

    filtered = memories

    if category != "All":
        filtered = [
            m for m in filtered
            if m["category"] == category
        ]

    if query:

        filtered = [
            m for m in filtered
            if query.lower() in (
                m["title"] + " " +
                m["content"] + " " +
                m["tags"]
            ).lower()
        ]

    st.write(f"{len(filtered)} memories found")

    for memory in filtered:

        with st.expander(
            memory["title"] +
            " | " +
            memory["category"]
        ):

            title = st.text_input(
                "Title",
                value=memory["title"],
                key=f"title_{memory['id']}"
            )

            content = st.text_area(
                "Content",
                value=memory["content"],
                key=f"content_{memory['id']}"
            )

            tags = st.text_input(
                "Tags",
                value=memory["tags"] or "",
                key=f"tags_{memory['id']}"
            )

            options = [
                "Personal", "Education", "Projects",
                "Technology", "Work", "Ideas", "Other"
            ]

            current = memory["category"]

            if current not in options:
                options.append(current)

            selected = st.selectbox(
                "Category",
                options,
                index=options.index(current),
                key=f"category_{memory['id']}"
            )

            col1, col2 = st.columns(2)

            if col1.button(
                "Update",
                key=f"update_{memory['id']}"
            ):

                update_memory(
                    memory["id"],
                    title,
                    content,
                    selected,
                    tags
                )

                st.success("Memory updated!")
                st.rerun()

            if col2.button(
                "Delete",
                key=f"delete_{memory['id']}"
            ):

                delete_memory(memory["id"])
                st.rerun()

            st.caption(
                f"Source: {memory['source']} | "
                f"Created: {memory['created_at']}"
            )

elif page == "Ask MindVault":

    st.subheader("Ask Your Memories")

    st.write(
        "Ask questions about information you have saved."
    )

    for message in st.session_state.chat:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input(
        "Ask something about your memories..."
    )

    if question:

        st.session_state.chat.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):

            with st.spinner("Searching memories..."):

                answer, sources = answer_question(question)

            st.markdown(answer)

            if sources:

                with st.expander("View Sources"):

                    for source in sources:

                        st.markdown(
                            f"**{source['title']}**"
                        )

                        st.caption(
                            source["content"][:400]
                        )

        st.session_state.chat.append({
            "role": "assistant",
            "content": answer
        })

elif page == "Documents":

    st.subheader("Import Documents")

    uploaded = st.file_uploader(
        "Upload PDF or TXT",
        type=["pdf", "txt"]
    )

    if uploaded:

        if st.button("Process Document"):

            try:

                text = extract_text(
                    uploaded.name,
                    uploaded.getvalue()
                )

                chunks = split_text(text)

                if not chunks:
                    st.warning("No readable text found.")
                else:

                    for i, chunk in enumerate(chunks, 1):

                        add_memory(
                            f"{uploaded.name} - Part {i}",
                            chunk,
                            "Documents",
                            uploaded.name,
                            uploaded.name
                        )

                    st.success(
                        f"Successfully imported {len(chunks)} chunks."
                    )

            except Exception as e:

                st.error(f"Document processing failed: {e}")

elif page == "Settings":

    st.subheader("Settings and Backup")

    st.info(
        "Your memories are stored locally in "
        "database/mindvault.db."
    )

    memories = get_memories()

    export_data = json.dumps(
        memories,
        indent=4,
        ensure_ascii=False
    )

    st.download_button(
        "Export Memories as JSON",
        export_data,
        file_name="mindvault_backup.json",
        mime="application/json"
    )

    if st.button("Clear Chat History"):

        st.session_state.chat = []
        st.success("Chat history cleared.")
        st.rerun()
