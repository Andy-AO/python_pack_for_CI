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
            raise ValueError(
                "Range of level should be 0~6, but current value is " + "'value'.")
        self._title_level_property = value

    def __init__(self, title_level, title, content):
        """
        构造方法

        Args:
            content: 节点本身的直辖内容，由于后续还可以向里面添加，所以实际上是用数组进行保存的，这个参数位于数组的index 0
            title: 节点的标题

                #TODO:当title_level为0的时候，title实际上应该是文件名，这个会很特殊，后续要特别注意。
            title_level: 标题的层级，需要整数，范围是0~6

        """
        self._children = OrderedDict()
        self._content = []
        self._title_level_property = None
        self._parent_property = None
        self._title_level = title_level
        self._title = title

        self.add_content(content)

    def get_content(self):
        """
        返回 Node 对象包含的具体内容

        Returns:
            内容列表
        Warns:
            是复制品，不是对象中实际数据的引用，只能用来读取内容，修改对象的数据必须通过 API。
        """
        return self._content.copy()

    def get_title(self):
        """
        返回 Node 对象的标题

        Returns:
            标题
        """
        return self._title

    def get_title_level(self):
        """
        返回 Node 对象的标题级别

        Returns:
            标题级别
        """
        return self._title_level

    def add_content(self, content):
        """
        向直辖内容数组中追加对象。

        对象生存完之后还允许修改content，是因为文件可能是逐行读取的，所以不可能一次就将数据放置完毕。

        之所以不直接拼接，就是因为要把这个计算延迟到需要的时候，到那个时候可以有更灵活的处置方式，比如说根据不同的平台来采用不同的NewLine。

        Args: 
            content: 需要添加的对象
        """
        self._content.append(content)
        pass

    def __str__(self):
        # TODO:这个是不完善的，需要好好想想到底该怎么做，很可能有个to_string方法，可以支持多种不同的字符串生成方式，而这个只是调用其中的一种，可能会进行加工

        return self._title

    def set_parent(self, new_parent):
        """
        设置 Node 的父对象

        Hint:
            如果要删除父对象，可以将new_parent设为None

        Args: 
            new_parent: 父对象
        Notes:
            通过设置父对象，让节点组织成树。
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
                old_parent.__delete_child(self)
            if not (new_parent is None):
                new_parent.__add_child(self)

    def __add_child(self, child_node):
        """
        添加子节点

        当 Node 要设置父节点时，它不仅要自己更改自己的属性，也要更改父节点的 Children，所以这个API是很必要的。

        Args:
            child_node: 需要添加的对象
        Warns:
            确保 child_node 的 parent 是当前 node，否则会抛出 ValueError 异常。
        Warns:
            添加 child 的唯一途径是用 set_parent，那是「独家代理」。
        """
        if self.had_child(child_node):
            raise ValueError('child node repeat.')
        if not (child_node.get_parent() is self):
            raise ValueError('parent of child node are not this object.')
        else:
            self._children[child_node] = 1

    def __delete_child(self, child_node, raise_exception: bool = False):
        """
        删除子节点

        当 Node 对象的 Parent 要发生更改时，除了其本身要更改之外，它现在的 Parent 的Children，也要同步的进行更改，这个方法是必要的。

        Raises:
          确保 child_node 的 parent 不是当前 node，否则会抛出 ValueError 异常。
        Warns:
            删除 child 的唯一途径是用 set_parent，那是「独家代理」。
        Args:
            child_node: 需要删除的对象
            raise_exception: 在对象不存在时是否抛出异常
        """
        if not (child_node is None):
            if child_node.get_parent() is self:
                raise ValueError(
                    'the parent of child node is still this object.')
        if self.had_child(child_node):
            self._children.pop(child_node)
        elif raise_exception:
            raise ValueError('child Node is non-existent.')

    def _get_children(self):
        """
        提供children的列表形式。
        目前这个方法不会在外部用到，即使是Node对象也是如此。
        如果要直接修改 children 不要使用这个方法，它直接提供 children 列表形式的副本而已。

        Returns: 
            children list
        """
        return list(self._children.keys())

    def had_child(self, child_node) -> bool:
        """
        看起来，query_child_index也能提供类似的功能，如果返回的值是-1，那么child是不存在的，但had_child利用HashTable，对于这个需求来说，效率应该会高很多。

        Args: 
            child_node: 需要验证存在性的对象
        Returns: 
            布尔值，表示对象存在与否
        """
        if child_node in self._children:
            return True
        else:
            return False

    def get_parent(self):
        """
        获取该对象的parent，这是对属性的简单封装。
        可以利用 Python 的布尔值自动转换，还实现对parent存在性的检查。

        Returns: 
            该对象的parent
        """
        return self._parent_property

    def query_child_index(self, child) -> int:
        """
        这主要是为getPath准备的，因为用的是链表结构，所以特定对象的index是不知道的，需要临时计算。
        这个API的运算量是不小的，所以尽量不要调用。

        Args: 
            child: 需要查询的对象
        Returns: 
            返回 int 来表示对象的 index，如果查不到，则返回 -1
        """
        try:
            index = self._get_children().index(child)
        except ValueError:
            index = -1
        return index

    def get_parents(self) -> list:
        """
        获取当前 node 的全部 parents 的 list

        Returns: 
            当前 node 的 parents 列表
        """
        current_node = self
        parents = []
        while current_node.get_parent():
            parents.append(current_node.get_parent())
            current_node = current_node.get_parent()
        return parents


pass
