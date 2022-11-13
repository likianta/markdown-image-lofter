from typing import Iterator

from .text_scanner import PRESET_RULES
from .text_scanner import PairRule
from .text_scanner import Scanner

scanner = Scanner(
    pair_rules=(
        PRESET_RULES.BASE_RULES['pair_aa.backtick'],
        # PRESET_RULES.BASE_RULES['pair_ab.parentheses'],
        # PRESET_RULES.BASE_RULES['pair_ab.brackets'],
        PRESET_RULES.BASE_RULES['pair_ab.braces'],
        PRESET_RULES.BASE_RULES['block_aa.backtick'],
        (('<!--', '-->'), PairRule.BLOCK_AB),
        (('![', ')'), PairRule.PAIR_AB),  # img pattern
    )
)


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
        ), ...
        
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
    from re import compile
    img_pattern = compile(r'!\[(.*?)]\((.*?)(?: *"(.*?)")? *\)')
    
    for seg in scanner.scan(doc):
        # print(seg.span.start_rowx, seg.text, seg.type)
        if seg.type == 'PAIR_AB':
            if seg.pair == ('![', ')'):
                target = seg
            elif seg.pair == ('[', ']'):
                if len(seg.children) == 1 \
                        and seg.children[0].pair == ('![', ')'):
                    target = seg.children[0]
                else:
                    continue
            else:
                continue
            
            assert target
            
            print(':v', target.text, img_pattern.match(target.text))
            if match := img_pattern.match(target.text):
                alt, src, title = (x or '' for x in match.groups())
                print(':lv2i', target.text, alt, src, title)
                yield (
                    (target.span.start_rowx, target.span.end_rowx),
                    (target.span.start_colx, target.span.end_colx),
                    (src, alt, title),
                )
            else:
                print(':v3i', target.text)
