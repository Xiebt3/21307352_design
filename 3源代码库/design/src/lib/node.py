"""
软件设计
    1.Composite模式 Node同时是中间节点和叶子节点。
    2.Template模式 Node的render是Composite模式中的业务（operation）方法，同时也是Template模式中的整体（play）方法
    3.继承：由多个类共同实现基类、各种xxxNode子类，持有node（Node），实现基类方法重用
"""
from abc import abstractmethod
from typing import Dict, List, Iterator


class Node:
    def __init__(self, name: str, level: int, is_last: bool, children: List['Node']):
        self._name: str = name  # 中间节点name为key，叶子节点name为key
        self._level: int = level  # 缩进级别
        self._is_last: bool = is_last  # 是否是最后一个（兄弟）节点
        self.__children: List['Node'] = children  # 初始为空列表 中间节点的children, Composite模式

    def render(self, prefix: str, icon_family: Dict[str, str]) -> str:
        return self._render(prefix, icon_family)

    def _render(self, prefix: str, icon_family: Dict[str, str]) -> str:
        leaf_icon: str = icon_family.get("leaf")
        container_icon: str = icon_family.get("container")
        if self._is_leaf():
            return self.__render_leaf(prefix, leaf_icon)
        else:
            return self.__render_container(prefix, container_icon, icon_family)

    """
    @设计模式 Composite
    python有继承，实现复用
    """

    def __render_leaf(self, prefix: str, icon: str) -> str:
        return self._render_node_line(prefix, icon)

    def __render_container(self, prefix: str, container_icon: str, icon_family: Dict[str, str]) -> str:
        node_line: str = self._render_node_line(prefix, container_icon)

        child_prefix: str = self._get_child_prefix(prefix)
        children_str = "".join(child._render(child_prefix, icon_family) for child in self.__children_iter())
        return node_line + children_str

    # prefix+level,prefix是祖先层级的指示线，形如"│  "
    def _render_node_line(self, prefix: str, icon: str) -> str:
        if self._is_root():
            return ""  # 根节点不输出
        else:
            return str("{}{}\n".format(prefix, self._get_label(icon)))

    @abstractmethod
    def _get_label(self, icon: str) -> str:
        raise NotImplementedError("Node是抽象类，不应该被直接使用，参考：TreeStyleNode icon:{}".format(icon))

    # @设计模式Template模式，部分方法
    # @继承，抽象方法，xxxNode子类必须覆盖实现
    @abstractmethod
    def _get_child_prefix(self, prefix: str) -> str:
        raise NotImplementedError("Node是抽象类，不应该被直接使用，参考：TreeStyleNode prefix:{}".format(prefix))

    def _is_root(self) -> bool:
        return self._level == 0

    def _is_leaf(self) -> bool:
        return len(self.__children) == 0

    def __children_iter(self) -> Iterator['Node']:
        return iter(self.__children)
