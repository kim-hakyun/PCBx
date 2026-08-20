from geometry import normalize_polygon
import xml.etree.ElementTree as ET

class IPC2581Writer:

    def save(self, board, filename):

        root = ET.Element("IPC-2581")

        root.set("revision", "B")

        root.set("xmlns", "http://webstds.ipc.org/2581")
        root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        root.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")

        root.set(
        "xsi:schemaLocation",
        "http://webstds.ipc.org/2581 "
        "http://webstds.ipc.org/2581/IPC-2581B1.xsd"
    )

        content = ET.SubElement(root,"Content")
        content.set("roleRef", "OWNER")

        function = ET.SubElement(content, "FunctionMode")

        function.set("mode", "USERDEF")
        function.set("level", "1")


        ET.SubElement(content,"FunctionMode").text = "USERDEF"

        logistic = ET.SubElement(root,"LogisticHeader")
        logistic.set("owner", "PCBX")
        logistic.set("sender", "PCBX")

        history = ET.SubElement(root,"HistoryRecord")
        history.set("number", "1")

        ecad = ET.SubElement(root,"Ecad")
        ecad.set("name", "MAIN")


        #
        # CadHeader
        #

        cad_header = ET.SubElement(ecad, "CadHeader")

        cad_header.set("units", "MILLIMETER")

        cad_data = ET.SubElement(ecad, "CadData")
        #
        # Layers
        #
        layers = int(board.properties.get("MAXIMUMLAYER", ["2"])[0])

        for i in range(1, layers + 1):

            layer = ET.SubElement(cad_data, "Layer")

            layer.set("name", f"L{i}")

        #
        # Layer Function
        #
        if i == 1:

            layer.set("layerFunction", "SIGNAL")

            layer.set("side", "TOP")

        elif i == layers:

            layer.set("layerFunction", "SIGNAL")

            layer.set("side", "BOTTOM")

        else:

            layer.set("layerFunction", "SIGNAL")

            layer.set("side", "INNER")

        layer.set("polarity", "POSITIVE")

        #
        # Stackup
        #
        stackup = ET.SubElement(cad_data, "Stackup")

        stackup.set("name", "PRIMARY")
        stackup.set("overallThickness", "1.600")
        stackup.set("tolPlus", "0.150")
        stackup.set("tolMinus", "0.150")

        header = ET.SubElement(root, "CadHeader")

        header.set("units", "MM")

        group = ET.SubElement(stackup, "StackupGroup")

        group.set("name", "DEFAULT")
        group.set("thickness", "1.600")
        group.set("tolPlus", "0.150")
        group.set("tolMinus", "0.150")


    for i in range(1, layers + 1):

        ref = ET.SubElement(group, "StackupLayer")

        ref.set("layerOrGroupRef", f"L{i}")
        #
        # CadData
        #
        cad = ET.SubElement(root, "CadData")

        #
        # LayerStack
        #
        stack = ET.SubElement(cad, "LayerStack")

        layers = int(board.properties.get("MAXIMUMLAYER", ["2"])[0])

        for i in range(1, layers + 1):

            layer = ET.SubElement(stack, "Layer")

            layer.set("name", "L" + str(i))

        #
        # STEP
        #
        step = ET.SubElement(cad_data, "Step")

        step.set("name", "BOARD")

        datum = ET.SubElement(step, "Datum")

        datum.set("x", "0.0")
        datum.set("y", "0.0")

        profile = ET.SubElement(step, "Profile")

        #
        # Components
        #
        for part in board.parts:

            c = ET.SubElement(step, "Component")

            c.set("refDes", part.refdes)

            c.set("packageRef", part.parttype)

            c.set("layerRef", "L1")

            c.set("mountType", "SMT")

        #
        # Logical Nets
        #
        nets = ET.SubElement(step, "LogicalNets")

        for sig in board.signals:

            net = ET.SubElement(nets, "Net")

            net.set("from", sig.start_pin)

            net.set("to", sig.end_pin)

            for seg in sig.segments:

                s = ET.SubElement(net, "Segment")

                s.set("x", str(seg.x))

                s.set("y", str(seg.y))

                s.set("layer", str(seg.layer))

                s.set("width", str(seg.width))

                if seg.via:

                    s.set("via", seg.via)

        tree = ET.ElementTree(root)

        ET.indent(tree)

        tree.write(
            filename,
            encoding="utf-8",
            xml_declaration=True
        )

        print()

        print("Commit0012 Export Complete")