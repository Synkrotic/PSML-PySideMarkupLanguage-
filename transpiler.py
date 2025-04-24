import xml.etree.ElementTree as ET
from RuleSet.rulesets import elementTypes



class PSMLElement:
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
    

    def load(self) -> None:
        pass


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
            raise ValueError("Root element is not set.")
        result = f"{"  " * indent} => {containerElement.tag}\n"
        for child in containerElement.children:
            result += self.getStringStructure(child, indent + 1)
        return result


    def run(self, filename: str):
        mainPage: str = self.readPSML(filename)
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



if __name__ == "__main__":
    piler: Transpiler = Transpiler()
    piler.run('main.psml')