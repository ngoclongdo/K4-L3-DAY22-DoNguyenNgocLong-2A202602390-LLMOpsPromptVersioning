"""
Tiện ích để tải và xử lý dữ liệu cho RAG pipeline.

Cách dùng:
    from utils.data_loader import load_knowledge_base, split_text, build_vectorstore

    text        = load_knowledge_base()
    chunks      = split_text(text, chunk_size=500, chunk_overlap=50)
    vectorstore = build_vectorstore(chunks, embeddings)
"""
from pathlib import Path


def load_knowledge_base(path: str = None) -> str:
    """
    Đọc file knowledge base và trả về nội dung dạng chuỗi.

    Args:
        path: đường dẫn tới file text.
              Mặc định: data/knowledge_base.txt (thư mục gốc của project)

    Returns:
        Nội dung file dưới dạng str
    """
    if path is None:
        path = Path(__file__).parent.parent.parent / "data" / "knowledge_base.txt"
    return Path(path).read_text(encoding="utf-8")


def split_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list:
    """
    Chia văn bản thành các đoạn nhỏ (chunks) để index.

    Dùng RecursiveCharacterTextSplitter — tách ưu tiên theo đoạn văn, câu, rồi ký tự.

    Args:
        text         : văn bản cần chia
        chunk_size   : số ký tự tối đa mỗi chunk (mặc định: 500)
        chunk_overlap: số ký tự chồng lên nhau giữa 2 chunks liên tiếp (mặc định: 50)

    Returns:
        list[str] — danh sách các chuỗi chunk
    """
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_text(text)


def build_vectorstore(chunks: list, embeddings):
    """
    Tạo FAISS vectorstore từ danh sách chunks và embeddings.

    Args:
        chunks    : list[str] — danh sách text chunks đã chia
        embeddings: Embeddings instance (từ get_embeddings())

    Returns:
        FAISS vectorstore đã được index và sẵn sàng dùng để retrieve
    """
    from langchain_community.vectorstores import FAISS
    from pathlib import Path
    import time

    cache_path = Path(__file__).parent.parent.parent / "data" / "faiss_index"
    if cache_path.exists():
        try:
            print("📦 Tìm thấy FAISS index đã lưu trong data/faiss_index, đang tải...")
            return FAISS.load_local(str(cache_path), embeddings, allow_dangerous_deserialization=True)
        except Exception as e:
            print(f"⚠️ Không thể tải cache FAISS: {e}. Đang tạo lại...")

    print(f"🔨 Đang tạo FAISS index từ {len(chunks)} chunks ...")

    batch_size = 50
    vectorstore = None
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        print(f"   Đang xử lý chunk {i + 1} - {min(i + batch_size, len(chunks))} / {len(chunks)}...")

        max_retries = 3
        for attempt in range(max_retries):
            try:
                if vectorstore is None:
                    vectorstore = FAISS.from_texts(batch, embeddings)
                else:
                    vectorstore.add_texts(batch)
                break
            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    print(f"   ⏳ Gặp giới hạn RPM của Gemini (429), đợi 35s trước khi thử lại (lần {attempt + 1}/{max_retries})...")
                    time.sleep(35)
                else:
                    raise e

        if i + batch_size < len(chunks):
            time.sleep(10)

    try:
        vectorstore.save_local(str(cache_path))
        print("💾 Đã lưu FAISS index vào data/faiss_index để tái sử dụng.")
    except Exception:
        pass

    print("✅ FAISS vectorstore đã sẵn sàng.")
    return vectorstore
