import pytest

from andyao.mdspliter.tree.node import Node


class TestContent:
    def test_get_content(self):
        the_node = Node(title_level=1, title='the title', content='the content')
        # 当get_content方法获取的对象被改变时，对象不变
        the_node.get_content()[0] = 'new content'
        assert the_node.get_content() == ['the content']

    def test_add_content(self):
        the_node = Node(title_level=1, title='the title', content='the content')
        assert the_node.get_content() == ['the content']
        the_node.add_content('line 1')
        assert the_node.get_content()[1] == 'line 1'


class TestConstruction:
    def test_normal(self):
        the_node = Node(title_level=1, title='the title', content='the content')
        assert the_node.get_content() == ['the content']
        # 在这里也顺便测试了get_title()和get_content()的基本功能
        assert the_node.get_title() == 'the title'
        assert the_node.get_title_level() == 1

    def test_scope_of_title_level(self):
        with pytest.raises(ValueError):
            Node(title_level=7, title='the title', content='the content')


class TestNodeLink:
    """
    用来测试与节点之间的链接相关的内容，例如，parent的设置
    """

    @pytest.fixture(scope="class")
    def give_nodes(self, request):
        request.cls.node_1 = Node(1, 'title 1', 'content 1')
        request.cls.node_2 = Node(2, 'title 2', 'content 2')
        request.cls.node_3 = Node(2, 'title 3', 'content 3')

    def test_node(self):
        assert Node(1, 'title 1', 'content 1')

    @pytest.mark.usefixtures("give_nodes")
    class TestSetParent:
        def test_none_to_node(self):
            """
            父节点的从无到有
            """
            self.node_1.set_parent(self.node_2)
            assert not (self.node_1.get_parent() is self.node_1)
            assert self.node_1.get_parent() is self.node_2
            assert self.node_2.had_child(self.node_1)

        def test_node_to_new_node(self):
            """
            更换父节点
            """
            self.node_1.set_parent(self.node_3)
            assert self.node_1.get_parent() is self.node_3
            assert not self.node_2.had_child(self.node_1)
            assert self.node_3.had_child(self.node_1)

        def test_node_to_same_node(self):
            """
            添加相同的父节点
            """
            self.node_1.set_parent(self.node_3)
            assert self.node_1.get_parent() is self.node_3
            assert not self.node_2.had_child(self.node_1)
            assert self.node_3.had_child(self.node_1)

        def test_parent_cannot_be_themselves(self):
            """
            父节点不能是自身
            """
            with pytest.raises(ValueError):
                self.node_1.set_parent(self.node_1)

        def test_node_to_none(self):
            """
            通过将父节点设为none来删除它
            """
            self.node_1.set_parent(None)
            assert self.node_1.get_parent() is None
            assert not self.node_3.had_child(self.node_1)

        def test_circular_references_are_prohibited(self):
            """
            禁止父节点的相互依赖
            """
            self.node_2.set_parent(self.node_1)
            self.node_3.set_parent(self.node_2)
            with pytest.raises(ValueError) as ex:
                self.node_1.set_parent(self.node_3)
            assert 'circular reference.' == str(ex.value)

        pass

    @pytest.mark.usefixtures("give_nodes")
    class TestQueryChildIndex:
        """查询子节点的索引"""

        def test_none(self):
            """子节点不存在时的值是-1"""
            assert self.node_1.query_child_index(self.node_2) == -1

        def test_had(self):
            self.node_2.set_parent(self.node_1)
            assert self.node_1.query_child_index(self.node_2) == 0

    @pytest.mark.usefixtures("give_nodes")
    class TestHadChild:
        """检查节点是否拥有特定节点"""

        def test_had_child(self):
            self.node_1.set_parent(self.node_2)
            assert self.node_2.had_child(self.node_1)
            assert not self.node_2.had_child(self.node_3)
