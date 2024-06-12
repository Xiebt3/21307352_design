from typing import List

from lib.node import Node
from lib.factory import AbstractFactory


class TreeStyleFactory(AbstractFactory):
    def __init__(self):
        super().__init__()

    def _create_node(self, name: str, level: int, is_last: bool, children: List[Node]) -> 'TreeStyleNode':
        return TreeStyleNode(name, level, is_last, children)


class TreeStyleNode(Node):
    def __init__(self, name: str, level: int, is_last: bool, children: List[Node]):
        super().__init__(name, level, is_last, children)

    def _get_label(self, icon: str) -> str:
        symbol: str = '└─' if self._is_last else '├─'
        return "{}{}{}".format(symbol, icon, self._name)
        # return super().get_label(icon)

    """
        @设计模式 Template模式：部分方法（具体实现）
        输出树形（tree），形如：
        ├─ oranges
        │  └─ mandarin
        │     ├─ clementine
        │     └─ tangerine: cheap & juicy!
        └─ apples
           ├─ gala //叶节点
           └─ pink lady
        每一行的prefix是由上一行的prefix决定的，如果是最后一个（兄弟）节点，那么prefix是“  ”否则是“│ ”
    """

    def _get_child_prefix(self, prefix: str) -> str:
        if self._is_root():
            return prefix + ""
        elif self._is_last:
            return prefix + "  "
        else:
            return prefix + "│ "
