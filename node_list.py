from manim import *

class NodeElement(VGroup):
    def __init__(self, value, next_element=None, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        self.next_element = next_element
        self.node = Square()
        self.text = Text(str(value)).move_to(self.node.get_center())
        self.arrow = None
        self.add(self.node, self.text)
        self.update_arrow()

    def update_arrow(self):
        if self.next_element:
            if self.arrow:
                self.remove(self.arrow)
            self.arrow = Arrow(self.node.get_right(), self.next_element.node.get_left())
            self.add(self.arrow)
        else:
            if self.arrow:
                self.remove(self.arrow)
            self.arrow = Arrow(self.node.get_bottom(), self.node.get_bottom() + DOWN)
            self.add(self.arrow)

class NodeElementList(VGroup):
    def __init__(self, values, **kwargs):
        super().__init__(**kwargs)
        self.node_list = []
        for i, value in enumerate(values):
            node_element = NodeElement(value)
            if i > 0:
                self.node_list[-1].next_element = node_element
                self.node_list[-1].update_arrow()
            node_element.move_to(2 * i * RIGHT)
            self.node_list.append(node_element)
            self.add(node_element)

class NodeElementListAnimation(Scene):
    def construct(self):
        node_list = NodeElementList([1, 2, 3, 4, 5])
        self.play(Create(node_list))
        self.wait(1)

        self.play(node_list.node_list[0].animate.shift(UP))
        self.wait(1)

        self.play(node_list.node_list[1].animate.shift(UP))
        self.wait(1)

        self.play(node_list.node_list[2].animate.shift(UP))
        self.wait(1)

        self.play(node_list.node_list[3].animate.shift(UP))
        self.wait(1)

        self.play(node_list.node_list[4].animate.shift(UP))
        self.wait(1)

        self.play(FadeOut(node_list))
        self.wait(1)