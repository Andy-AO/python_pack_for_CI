"""
放置树状类数据结构以及相关内容。
data包是其下游。

"""
from collections import OrderedDict


class Node:
    """
    树的原子，即「节点」。
    单个对象看就是节点，连同Node对象的子对象来看就称为树，树干是两个Node之间的关系。

    """

    @property
    def _title_level(self):
        return self._title_level_property

    @_title_level.setter
    def _title_level(self, value):
        if value > 6 or value < 0:
            raise ValueError("Range of level should be 0~6, but current value is " + "'value'.")
        self._title_level_property = value

    def __init__(self, title_level, title, content):
        """
        构造方法

        :param content: 节点本身的直辖内容，由于后续还可以向里面添加，所以实际上是用数组进行保存的，这个参数位于数组的index 0
        :param title: 节点的标题
        :param title_level:标题的层级，需要整数，范围是0~6
        
        """
        self._children = OrderedDict()
        self._content = []
        self._title_level_property = None
        self._parent_property = None
        self._title_level = title_level
        self._title = title

        self.add_content(content)

    def add_content(self, content):
        """
        向直辖内容数组中追加对象。

        对象生存完之后还允许修改content，是因为文件可能是逐行读取的，所以不可能一次就将数据放置完毕。

        之所以不直接拼接，就是因为要把这个计算延迟到需要的时候，到那个时候可以有更灵活的处置方式，比如说根据不同的平台来采用不同的NewLine。

        :param content: 需要添加的对象
        """
        self._content.append(content)
        pass

    def __str__(self):
        return self._title

    def set_parent(self, new_parent):
        """
        只有通过设置父对象，才能够把这些节点组织成树状结构。
        如果要删除父对象，可以将new_parent设为None

        :param new_parent: 目标父对象
        """
        old_parent = self._parent_property
        if not (old_parent is new_parent):
            if new_parent is self:
                raise ValueError('The parent node cannot be itself.')
            if not (new_parent is None):
                if self in new_parent.get_parents():
                    raise ValueError('circular reference.')
            self._parent_property = new_parent
            if old_parent:
                old_parent.delete_child(self)
            if not (new_parent is None):
                new_parent.add_child(self)

    def add_child(self, child_node):
        """
        当Node要设置父节点时，他不仅要自己更改自己的属性，也要更改父节点的Children，所以这个API是很必要的。
        要注意的是这个调用 API 时，需要先检查对应的节点的 parent 是否正确，如果不正确的话是不予添加的。
        所以添加 child 的唯一途径是用 set_parent 而不是用这个方法。

        :param child_node: 需要添加的对象
        """
        if self.had_child(child_node):
            raise ValueError('child node repeat.')
        if not (child_node.get_parent() is self):
            raise ValueError('parent of child node are not this object.')
        else:
            self._children[child_node] = 1

    def _get_children(self):
        """
        提供children的列表形式。
        目前这个方法不会在外部用到，即使是Node对象也是如此。
        如果要直接修改 children 不要使用这个方法，它直接提供 children 列表形式的副本而已。
        
        :return: children list
        """
        return list(self._children.keys())

    def delete_child(self, child_node, raise_exception: bool = False):
        """
        当Node对象的Parent要发生更改时，除了其本身要更改之外，它现在的Parent的Children，也要同步的进行更改，所以提供这个API是必要的。
        不能删除 child parent 为当前对象的 node。

        :param child_node: 需要删除的对象
        :param raise_exception: 在对象不存在时是否抛出异常
        """
        if not (child_node is None):
            if child_node.get_parent() is self:
                raise ValueError('the parent of child node is still this object.')
        if self.had_child(child_node):
            self._children.pop(child_node)
        elif raise_exception:
            raise ValueError('child Node is non-existent.')

    def had_child(self, child_node) -> bool:
        """
        看起来，query_child_index也能提供类似的功能，如果返回的值是-1，那么child是不存在的，但had_child利用HashTable，对于这个需求来说，效率应该会高很多。

        :param child_node: 需要验证存在性的对象
        :return: 布尔值，表示对象存在与否
        """
        if child_node in self._children:
            return True
        else:
            return False

    def get_parent(self):
        """
        获取该对象的parent，这是对属性的简单封装。
        可以利用 Python 的布尔值自动转换，还实现对parent存在性的检查。

        :return: 该对象的parent
        """
        return self._parent_property

    def query_child_index(self, child) -> int:
        """
        这主要是为getPath准备的，因为用的是链表结构，所以特定对象的index是不知道的，需要临时计算。
        这个API的运算量是不小的，所以尽量不要调用。

        :param child: 需要查询的对象
        :return: 返回 int 来表示对象的 index，如果查不到，则返回 -1
        """
        try:
            index = self._get_children().index(child)
        except ValueError:
            index = -1
        return index

    def get_parents(self) -> list:
        """
        获取当前 node 的全部 parents 的 list

        :return: 当前 node 的 parents 列表
        """
        current_node = self
        parents = []
        while current_node.get_parent():
            parents.append(current_node.get_parent())
            current_node = current_node.get_parent()
        return parents


pass
