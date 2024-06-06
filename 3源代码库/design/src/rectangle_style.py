from typing import List, Dict

from lib.factory import AbstractFactory
from lib.node import Node


class RectangleStyleFactory(AbstractFactory):
    def __init__(self):
        super().__init__()

    def _create_node(self, name: str, level: int, is_last: bool, children: List[Node]) -> 'RectangleStyleNode':
        return RectangleStyleNode(name, level, is_last, children)


class RectangleStyleNode(Node):
    def __init__(self, name: str, level: int, is_last: bool, children: List[Node]):
        super().__init__(name, level, is_last, children)

    """
        @设计模式 Template模式：部分方法（具体实现）
        输出矩形（rectangle）
    """

    def _get_label(self, icon: str) -> str:
        symbol: str = '└─' if self._is_last and self._is_leaf() else '├─'
        return "{}{}{}".format(symbol, icon, self._name)

    def _get_child_prefix(self, prefix: str) -> str:
        return prefix + ("" if self._level == 0 else "│ ")

    def _render_node_line(self, prefix: str, icon: str) -> str:
        label: str = self._get_label(icon)
        suffix: str = '─' * (40 - len(prefix) - len(label))
        return "{}{}{}─┤\n".format(prefix, label, suffix)

    # 修正res
    def render(self, prefix: str, icon_family: Dict[str, str]) -> str:
        res: str = self._render(prefix, icon_family)
        lines = res.split('\n')
        lines = lines[:-1]  # 每行都有\n，所以最后一个lines为空
        if self._is_root():
            if lines:
                # 1)最后一行超出的symbol "│ " "─┤"置换为"└─" "─┘"
                lines[-1] = lines[-1].replace("│ ", "└─").replace("─┤", "─┘")
                # 2)第一行超出的symbol "├─" "─┤"置换为"┌─" "─┐"
                lines[0] = lines[0].replace("├─", "┌─").replace("─┤", "─┐")
                # 3)中间行将"└─"置换为"├─"
                for i in range(1, len(lines) - 1):
                    lines[i] = lines[i].replace("└─", "├─")
                lines.append("")
            return "\n".join(lines)
        else:
            return res
