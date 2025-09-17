# htmlnode.py

class HTMLNode(): 
    def __init__(self, tag=None, value=None, children=None, props=None): 
        self.tag = tag
        self.value = value
        self.children = children 
        self.props = props

    def to_html(self): 
        raise NotImplementedError

    def props_to_html(self): 
        if self.props is None: 
            return ""
        html_string = ""
        for k, v in self.props.items(): 
            html_string += f' {k}="{v}"'
        return html_string
    
    def __eq__(self, other): 
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props
                )

    def __repr__(self): 
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode): 
    def __init__(self, value, tag=None, props=None): 
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self): 
        if self.value is None: 
            raise ValueError("LeafNode must have a value")
        if self.tag is None: 
            return f"{self.value}"
        if self.props is None: 
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode): 
    def __init__(self, tag, children, props=None): 
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self): 
        if self.tag is None: 
            raise ValueError("ParentNode must have a tag")
        if self.children is None: 
            raise ValueError("ParentNode must have at least one child")
        html_string = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children: 
            html_string += child.to_html()
        html_string += f"</{self.tag}>"
        return html_string
