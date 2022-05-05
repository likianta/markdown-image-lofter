from typing import Iterator

from markdown_it import MarkdownIt
from urllib.parse import unquote

from ._dirty_hack import dirty_hack

_md_processor = MarkdownIt()


def extract_image_urls(doc: str) -> Iterator[
    tuple[
        tuple[int, int],
        tuple[int, int],
        tuple[str, str, str],
    ]
]:
    """
    args:
        doc: markdown document.
        
    yield:
        (
            (int row_start, int row_end),
            (int col_start, int col_end),
            (str src, str alt, str title)
        )
        
        details:
            row_start: int, counts from 0.
            row_end: int. usually it is `row_start + 1`.
            col_start: int, counts from 0.
            col_end: int. it is `col_start + len(raw_text)`.
            src, alt, title: `![alt](src "title")`
    
    ps:
        it seems that MarkdownIt's tokens don't recognize `alt` as
        Token.attrs['alt']. we have to use `Token.children[0].content` instead.
    """
    for token in _md_processor.parse(doc):
        if token.type == 'inline':
            # print('[1856]', token.as_dict(), ':lv')
            row_span = tuple(token.map)  # e.g. [7, 8] -> (7, 8)
            
            for child_token in token.children:
                if child_token.type == 'image':
                    # print('[1857]', child_token.as_dict(), ':lv')
                    alt = child_token.content
                    src = unquote(child_token.attrs['src'], encoding='utf-8')
                    title = child_token.attrs.get('title', '')
                    
                    # see `dirty_hack : docstring`.
                    col_span = dirty_hack.get_image_boundary()
                    
                    yield (
                        row_span, col_span,
                        (src, alt, title),
                    )
