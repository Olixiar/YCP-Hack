import argparse
from llama_index.core import VectorStoreIndex, Settings, StorageContext
from llama_index.readers.web import SimpleWebPageReader
from llama_index.vector_stores.lancedb import LanceDBVectorStore
from llama_index.llms.databricks import Databricks
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from openai import OpenAI
import streamlit as st

st.title("YCP Bot")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})



def build_RAG(
    url="https://harrypotter.fandom.com/wiki/Hogwarts_School_of_Witchcraft_and_Wizardry",
    embed_model="mixedbread-ai/mxbai-embed-large-v1",
    uri="~/tmp/lancedb_hogwart",
    force_create_embeddings=False,
    illustrate=False,
    diffuser_model="sdxl",
):
    Settings.embed_model = HuggingFaceEmbedding(model_name=embed_model)
    Settings.llm = Databricks(model="databricks-dbrx-instruct")
    documents = get_doc_from_url(url)
    vector_store = LanceDBVectorStore(uri=uri)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
    query_engine = index.as_chat_engine()

    return query_engine, model, steps

    if st.session_state.get("query_engine") is None:
        context = st.text_area(
            "Enter the link to the context",
            value="https://harrypotter.fandom.com/wiki/Hogwarts_School_of_Witchcraft_and_Wizardry",
        )
        steps = st.selectbox("Select the number of steps for diffusion", (1, 2))
        build_rag = st.button("Build RAG")
        query_engine, model = None, None
        if build_rag:
            query_engine, model, _ = build_RAG(
                context,
                "mixedbread-ai/mxbai-embed-large-v1",
                "~/tmp/lancedb_hogwarts_12",
                False,
                illustrate,
                "sdxl",
            )
            add_to_session("query_engine", query_engine)
            add_to_session("model", model)
            add_to_session("steps", steps or 1)
            print("steps", steps)
            st._experimental_rerun()
    else:
        query_engine = st.session_state["query_engine"]
        model = st.session_state["model"]
        steps = st.session_state["steps"]
        col1, col2 = st.columns(2)
        with col1:
            query = st.text_input(
                "Enter a question",
                value="What is Hogwarts?",
                label_visibility="collapsed",
            )
        with col2:
            enter = st.button("Enter")
            if enter:
                response = query_engine.chat(query)
                st.write("Response")
                st.write(response)
