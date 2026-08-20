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

        # -----------------------------
        # Root
        # -----------------------------
        root = ET.Element("IPC-2581")

        root.set("revision", "A")

        # -----------------------------
        # Content
        # -----------------------------
        ET.SubElement(root, "Content")

        # -----------------------------
        # LogisticHeader
        # -----------------------------
        ET.SubElement(root, "LogisticHeader")

        # -----------------------------
        # HistoryRecord
        # -----------------------------
        ET.SubElement(root, "HistoryRecord")

        # -----------------------------
        # Ecad
        # -----------------------------
        ecad = ET.SubElement(root, "Ecad")

        # -----------------------------
        # CadHeader
        # -----------------------------
        header = ET.SubElement(ecad, "CadHeader")

        header.set("units", "MILLIMETER")

        # -----------------------------
        # CadData
        # -----------------------------
        cad = ET.SubElement(ecad, "CadData")

        # -----------------------------
        # Layer
        # -----------------------------
        max_layer = 2

        try:
            if "MAXIMUMLAYER" in board.properties:
                max_layer = int(board.properties["MAXIMUMLAYER"][0])
        except Exception:
            pass

        for i in range(1, max_layer + 1):

            layer = ET.SubElement(cad, "Layer")

            layer.set("name", f"L{i}")

        # -----------------------------
        # Step
        # -----------------------------
        step = ET.SubElement(cad, "Step")

        step.set("name", "BOARD")

        ET.SubElement(step, "Profile")

        # -----------------------------
        # Components
        # -----------------------------
        for part in getattr(board, "parts", []):

            comp = ET.SubElement(step, "Component")

            comp.set("refdes", getattr(part, "refdes", ""))

            comp.set("package", getattr(part, "parttype", ""))

            comp.set("x", str(getattr(part, "x", 0)))

            comp.set("y", str(getattr(part, "y", 0)))

            comp.set("rotation", str(getattr(part, "rotation", 0)))

        # -----------------------------
        # Save
        # -----------------------------
        tree = ET.ElementTree(root)

        try:
            ET.indent(tree, space="    ")
        except AttributeError:
            # Python < 3.9 호환
            pass
        os.makedirs(os.path.dirname(filename), exist_ok=True )
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