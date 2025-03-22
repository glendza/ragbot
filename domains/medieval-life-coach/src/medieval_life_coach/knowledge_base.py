from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

MAX_CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
MARKDOWN_SEPARATORS = [
    "\n#{1,6} ",
    "```\n",
    "\n\\*\\*\\*+\n",
    "\n---+\n",
    "\n___+\n",
    "\n\n",
    "\n",
    " ",
    "",
]


def get_knowledge_base() -> list[str]:
    knowledge_locations = [
        Path(__file__).parent
        / "data/Malleus_maleficarum,_translated_to_English_by_the_Rev._Montague_Summers,_1928,_1948,_from_the_Internet_Archive_-_b31349717.pdf",
        Path(__file__).parent / "data/divinecomedyofda671dant.pdf",
    ]
    text_chunks = [
        chunk for knowledge_location in knowledge_locations for chunk in load_and_preprocess(knowledge_location)
    ]
    return text_chunks


def load_and_preprocess(file_path: Path) -> list[str]:
    loader = PyPDFLoader(str(file_path))

    docs = loader.load()

    # Text preprocessing:
    text_content = "\n".join([doc.page_content for doc in docs])
    text_content = text_content.replace("\f", " ")  # Remove page breaks
    text_content = text_content.strip()

    # Split text into chunks:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=MAX_CHUNK_SIZE,  # Maximum size of each chunk (in characters)
        chunk_overlap=CHUNK_OVERLAP,  # Overlapping characters between chunks to preserve context
        add_start_index=True,  # Adds start index metadata to each chunk for reference
        strip_whitespace=True,  # Removes leading and trailing whitespace from chunks
        separators=MARKDOWN_SEPARATORS,  # Defines custom separators for splitting text
    )

    return splitter.split_text(text_content)
