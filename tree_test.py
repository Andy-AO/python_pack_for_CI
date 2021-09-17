import pytest

from tree import Node


def test_get_content():
    the_node = Node(title_level=1, title='the title', content='the content')
    # 当get_content方法获取的对象被改变时，对象不变
    the_node.get_content()[0] = 'new content'
    assert the_node.get_content() == ['the content']


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
