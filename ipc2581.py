import xml.etree.ElementTree as ET


class IPC2581Writer:

    def save(self, board, filename):

        root = ET.Element("IPC-2581")

        #
        # Header
        #
        header = ET.SubElement(root, "Header")

        ET.SubElement(header, "Units").text = str(
            board.properties.get("UNITS", ["1"])[0]
        )

        #
        # Board
        #
        board_node = ET.SubElement(root, "Board")

        #
        # Components
        #
        comp_node = ET.SubElement(board_node, "Components")

        for part in board.parts:

            c = ET.SubElement(comp_node, "Component")

            c.set("RefDes", part.refdes)
            c.set("PartType", part.parttype)

            c.set("X", str(part.x))
            c.set("Y", str(part.y))

            c.set("Rotation", str(part.rotation))

        #
        # Nets
        #
        net_node = ET.SubElement(board_node, "Nets")

        for sig in board.signals:

            net = ET.SubElement(net_node, "Net")

            net.set("From", sig.start_pin)

            net.set("To", sig.end_pin)

            for seg in sig.segments:

                s = ET.SubElement(net, "Segment")

                s.set("X", str(seg.x))
                s.set("Y", str(seg.y))
                s.set("Layer", str(seg.layer))
                s.set("Width", str(seg.width))

                if seg.via:
                    s.set("Via", seg.via)

        tree = ET.ElementTree(root)

        ET.indent(tree)

        tree.write(
            filename,
            encoding="utf-8",
            xml_declaration=True
        )

        print()

        print("IPC2581 Saved")

        print(filename)