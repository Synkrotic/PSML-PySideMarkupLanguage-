from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QGroupBox
from RuleSet.rulesets import elementTypes, psml_widgets
import xml.etree.ElementTree as ET



class PSMLElement:
    tag = None
    parent = None
    attributes = None
    children = None
    content = None
    widget = None

    def __init__(self, tag, parent=None, attributes=None, children=None, content=None) -> None:
        self.tag = tag
        self.parent = parent
        self.attributes = attributes if attributes else {}
        self.children = children if children else []
        self.content = content if content else ""


    def __str__(self) -> str:
        parent_tag = self.parent.tag if self.parent else "None"
        children_tags = [child.tag for child in self.children]
        return f"Tag: {self.tag}\nParent: {parent_tag}\nChildren: {children_tags}\nContent: {self.content}\nAttributes: {self.attributes}\n"


    def load(self, parent) -> None:
        if not self.tag in elementTypes: return

        if self.tag == "root":
            self.widget = QVBoxLayout()
            for child in self.children:
                child_widget = child.load(self)
                if child_widget is not None:
                    self.widget.addWidget(child_widget)
            return self.widget

        pyside_widget = psml_widgets.get(self.tag)
        if pyside_widget is None:
            raise ValueError(f"Unknown widget type: {self.tag}")
        self.widget = pyside_widget()
        
        if self.tag == "node":
            layout = QVBoxLayout()
            self.widget.setLayout(layout)
            self.layout = layout
        else:
            self.layout = None
            
        if self.content != "" and not self.content is None:
            if isinstance(self.widget, (QLabel, QPushButton)):
                self.widget.setText(self.content)
        
        self.setParent(parent)
        self.setAttributes()
        
        for child in self.children:
            child_widget = child.load(self)

        return self.widget


    def setAttributes(self):
        for attr, value in self.attributes.items():
            if "id" in attr:
                self.widget.setObjectName(value)
            elif "onclick" in attr:
                if isinstance(self.widget, QPushButton):
                    self.widget.clicked.connect(lambda: eval(value))
                else:
                    raise ValueError(f"onclick attribute is only valid for QPushButton widgets | Not for {self.tag}")
            self.widget.setProperty(attr, value)


    def setParent(self, parent):
        if hasattr(parent, 'layout') and parent.layout is not None:
            parent.layout.addWidget(self.widget)
        elif hasattr(parent.widget, 'addWidget'):
            parent.widget.addWidget(self.widget)
        else:
            raise ValueError(f"Parent {parent.tag} cannot contain child widgets")



class Transpiler:
    root: PSMLElement = None
    def __init__(self) -> None:
        pass


    def generatePSElements(self, et_element, parent: None | PSMLElement = None) -> PSMLElement:
        if not et_element.tag in elementTypes:
            raise ValueError(f"Unknown element type: {et_element.tag}")
        elem = PSMLElement(
            tag=et_element.tag,
            parent=parent,
            attributes=et_element.attrib,
            content=et_element.text or ""
        )
        for child in et_element:
            child_elem = self.generatePSElements(child, parent=elem)
            elem.children.append(child_elem)
        if elem.tag == "root":
            self.root = elem
        return elem


    def readPSML(self, filename) -> str:
        if not "templates/" in filename:
            filename = "templates/" + filename
        with open(filename, 'r') as file:
            return file.read()
        return "Unable to read file!"


    def getStringStructure(self, containerElement, indent=0) -> str:
        if containerElement is None:
            raise ValueError(f"{containerElement.tag} element is not set.")
        result = f"{"  " * indent} => {containerElement.tag}\n"
        for child in containerElement.children:
            result += self.getStringStructure(child, indent + 1)
        return result


    def run(self, filename: str):
        mainPage: str = self.readPSML(filename).strip()
        try:
            root_et = ET.fromstring(mainPage)
            if root_et.tag != "root":
                page: str = "<root>" + mainPage + "</root>"
                root_et = ET.fromstring(page)

        except ET.ParseError:
            page: str = "<root>" + mainPage + "</root>"
            root_et = ET.fromstring(page)
        self.root = root_et
        
        self.generatePSElements(self.root)
        print(self.getStringStructure(self.root))



# if __name__ == "__main__":
#     piler: Transpiler = Transpiler()
#     piler.run('main.psml')