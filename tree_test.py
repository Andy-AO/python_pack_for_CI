import pytest

from tree import Node


class TestConstruction:
    def test_normal(self):
        the_node = Node(title_level=1, title='the title', content='the content')
        assert the_node.get_content() == ['the content']
        assert the_node.get_title() == 'the title'
        assert the_node.get_title_level() == 1

    def test_scope_of_title_level(self):
        with pytest.raises(ValueError):
            Node(title_level=7, title='the title', content='the content')
