import os
import xml.etree.ElementTree as ET


class IPC2581Writer:
    """
    Minimal IPC2581 Writer
    Commit100 Base Version

    목적:
        - main.py가 정상 실행될 것
        - output.xml 생성될 것
        - 이후 Commit에서 기능 추가
    """

    def __init__(self):
        pass

    def save(self, board, filename):

        root = ET.Element("IPC-2581")
        root.set("revision", "A")

        ET.SubElement(root, "Content")
        ET.SubElement(root, "LogisticHeader")
        ET.SubElement(root, "HistoryRecord")

        ecad = ET.SubElement(root, "Ecad")

        header = ET.SubElement(ecad, "CadHeader")
        header.set("units", "MILLIMETER")

        cad = ET.SubElement(ecad, "CadData")

        max_layer = 2

        try:
            if "MAXIMUMLAYER" in board.properties:
                max_layer = int(board.properties["MAXIMUMLAYER"][0])
        except Exception:
            pass

        for i in range(1, max_layer + 1):
            layer = ET.SubElement(cad, "Layer")
            layer.set("name", f"L{i}")

        step = ET.SubElement(cad, "Step")
        step.set("name", "BOARD")

        ET.SubElement(step, "Profile")

        #
        # Commit0102
        #
        self.write_packages(step, board)

        #
        # Components
        #
        for part in getattr(board, "parts", []):

            comp = ET.SubElement(step, "Component")

            comp.set("refdes", getattr(part, "refdes", ""))
            comp.set("package", getattr(part, "parttype", ""))
            comp.set("x", str(getattr(part, "x", 0)))
            comp.set("y", str(getattr(part, "y", 0)))
            comp.set("rotation", str(getattr(part, "rotation", 0)))

        tree = ET.ElementTree(root)

        try:
            ET.indent(tree, space="    ")
        except AttributeError:
            pass

        folder = os.path.dirname(filename)

        if folder:
            os.makedirs(folder, exist_ok=True)

        tree.write(
            filename,
            encoding="utf-8",
            xml_declaration=True,
        )

        print()
        print("====================================")
        print(" IPC2581 Export Complete")
        print(" Output :", filename)
        print(" Layers :", max_layer)
        print(" Parts  :", len(getattr(board, "parts", [])))
        print("====================================")
        print(type(board.packages))
        print(type(board.packages[0]))
        print(board.packages[:5])

    def write_packages(self, step, board):
        """
        Commit0102
        Package Name Export
        """

        package_list = ET.SubElement(step, "PackageList")

        count = 0

        for pkg in getattr(board, "packages", []):

            package = ET.SubElement(package_list, "Package")

            #
            # 현재는 문자열 리스트
            #
            package.set("name", str(pkg))

            count += 1

        print("Packages :", count)