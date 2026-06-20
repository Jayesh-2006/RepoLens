from .chunkers.python_ast_chunker import PythonASTChunker
from .chunkers.markdown_chunker import MarkdownChunker
from .chunkers.text_chunker import TextChunker

PYTHON_AST_CHUNKER = PythonASTChunker()
MARKDOWN_CHUNKER = MarkdownChunker()
TEXT_CHUNKER = TextChunker()

def get_chunker(extension: str):

    if extension == ".py":
        return PYTHON_AST_CHUNKER

    if extension == ".md":
        return MARKDOWN_CHUNKER

    return TEXT_CHUNKER