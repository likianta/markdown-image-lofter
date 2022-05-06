"""
the dirty hack method to get boundary position from image tokens.

warning:
    this is a workaround, cause i didn't know how to make a proper way to get
    boundary info from `markdown_it_py : token`.
    i've checked the source code of `markdown_it_py` and found that
    `~/site-packages/markdown_it/rules_inline/image.py : def image` is
    responsible for matching image pattern.
    so i planted a "global" dict to store the boundary info (tuple[int start,
    int end]) for my purpose.

note: we have to modify the source code of 'image.py':
    # for markdown_it_py v2.1.0
    # the 149th line: insert below
    __dirty_hack.store_image_boundary(oldPos, pos)
the `__dirty_hack` doesn't need any import, because i've planted it into
`builtins` in this module.
"""
from __future__ import annotations

import builtins


class DirtyHack:
    _index = -1
    _boundary = []
    
    def store_image_boundary(self, start: int, end: int):
        print('set', (start, end), ':pvis')
        self._boundary.append((start, end))
    
    def get_image_boundary(self) -> tuple[int, int]:
        self._index += 1
        if self._index == 0: print(':i0')
        print('get', self._boundary[self._index], ':vis')
        return self._boundary[self._index]


dirty_hack = DirtyHack()
setattr(builtins, '__dirty_hack', dirty_hack)
