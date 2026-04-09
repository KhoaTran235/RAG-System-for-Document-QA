# RAG-System-for-Document-QA
query rewriting, summary memory + truncated chat history, structure-based chunking, hybrid retrieval.


rag_system/
│
├── app/                        # Entry point (API layer)
│   ├── main.py                # FastAPI app
│   ├── dependencies.py        # DI (inject retriever, llm,...)
│   └── routes/
│       ├── chat.py            # /chat
│       ├── ingest.py          # /ingest
│       ├── search.py          # /search
│       └── health.py
│
├── core/                      # Core logic (framework independence)
│   ├── config.py
│   ├── logging.py
│   └── constants.py
│
├── ingestion/                 # Document pipeline
│   ├── docling_loader.py      # PDF
│   ├── chunker.py
│   └── pipeline.py           # end-to-end ingest flow
│
├── retrieval/
│   ├── dense/
│   │   └── vector_store.py   # FAISS
│   ├── sparse/
│   │   └── bm25.py
│   ├── hybrid/
│   │   └── hybrid_retriever.py
│   └── reranker.py
│
├── generation/
│   ├── llm/
│   │   └── llm_client.py     # wrapper (OpenAI / local)
│   ├── prompt/
│   │   ├── qa_prompt.py
│   │   └── rewrite_prompt.py
│   └── generator.py
│
├── memory/
│   ├── chat_history.py
│   ├── summarizer.py
│   └── manager.py            # summary + truncation logic
│
├── query/
│   ├── rewrite.py
│   └── classifier.py         # optional (intent detection)
│
├── pipelines/                # orchestration (LangChain hoặc custom)
│   ├── rag_pipeline.py
│   └── ingest_pipeline.py
│
├── services/                 # business logic (API gọi vào đây)
│   ├── chat_service.py
│   ├── ingest_service.py
│   └── search_service.py
│
├── storage/
│   ├── vector_db/
│   ├── metadata_db/
│   └── cache/
│
├── utils/
│   └── text_utils.py
│
├── tests/
│
└── requirements.txt
