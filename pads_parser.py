
import re
from board import (
    Board, Text, Line, Point, Piece, Via, ViaDef, ViaPad, Part,Signal, Segment, Package, Pad,
)
class PadsParser:
    SECTION_NAMES={"PCB","TEXT","LINES","VIA","PART","PARTTYPE","PARTDECAL","ROUTE","SIGNAL","POUR","TESTPOINT","MISC","REUSE","END"}
    SECTION=re.compile(r'^\*([A-Z0-9_]+)\*')
    def load(self,filename):
        print("load() 시작")

        with open(filename,"r",encoding="latin1") as f:
            lines=f.readlines()
        board=Board()

        current="HEADER"
        board.sections[current]=[]
        for line in lines:
            line=line.rstrip()
            m=self.SECTION.match(line)
            if m:
                name=m.group(1)
                if name in self.SECTION_NAMES:
                    current=name
                    board.sections.setdefault(current,[])
                    continue
            board.sections[current].append(line)
        print("parse_vias")
        self.parse_vias(board)

        print("parse_pcb")
        self.parse_pcb(board)

        print("parse_text")
        self.parse_text(board)

        print("parse_lines")
        self.parse_lines(board)

        print("parse_part")
        self.parse_part(board)

        print("parse_signal")
        self.parse_signal(board)


        self.parse_partdecal(board)
        

        print("return")

        return board

    def parse_pcb(self,board):
        for line in board.sections.get("PCB",[]):
            line=line.strip()
            if not line or line.startswith("*REMARK*"): continue
            w=line.split()
            if len(w)>=2:
                board.properties[w[0]]=w[1:]

    def parse_text(self,board):
        lines=board.sections.get("TEXT",[])
        i=0
        while i<len(lines):
            s=lines[i].strip()
            if not s:
                i+=1; continue
            w=s.split()
            if len(w)>=10:
                try:
                    t=Text()
                    t.x=int(w[0]); t.y=int(w[1]); t.rotation=float(w[2]); t.layer=int(w[3]); t.height=int(w[4]); t.width=int(w[5]); t.mirror=w[6]
                    if i+1<len(lines): t.font=lines[i+1].strip()
                    if i+2<len(lines): t.value=lines[i+2].strip()
                    board.texts.append(t)
                    i+=3
                    continue
                except Exception:
                    pass
            i+=1

    def parse_lines(self, board):
        print(">>> parse_lines() 시작")

        if "LINES" not in board.sections:
            return

        data = board.sections["LINES"]

        current_line = None
        current_piece = None
        expect_points = 0

        for raw in data:

            line = raw.strip()

            if not line:
                continue

            w = line.split()

        # -------------------------------------------------
        # Drawing 시작
        # -------------------------------------------------
            if len(w) >= 6 and w[0].startswith("DRW"):
                print("DRAWING =", w)
                current_line = Line()

                current_line.name = w[0]
                current_line.line_type = w[1]
                current_line.x = int(w[2])
                current_line.y = int(w[3])

                board.lines.append(current_line)

                current_piece = None
                expect_points = 0

                continue

        # -------------------------------------------------
        # OPEN / CLOSED
        # -------------------------------------------------
            if current_line and len(w) >= 5:
                print("LINE :", w)
                if w[0] in ("OPEN", "CLOSED"):

                    current_piece = Piece()

                    current_piece.piece_type = w[0]
                    current_piece.width = int(w[2])
                    current_piece.level = int(w[4])

                    current_line.pieces.append(current_piece)

                    expect_points = int(w[1])

                    continue

        # -------------------------------------------------
        # Point
        # -------------------------------------------------
            if current_piece and expect_points > 0:

                if len(w) >= 2:

                    try:

                        x = int(w[0])
                        y = int(w[1])

                        current_piece.points.append(Point(x, y))

                        expect_points -= 1

                    except ValueError:
                        pass

    # --------------------------
    # Debug
    # --------------------------

        print("\n========== LINES ==========")

        print("Drawings :", len(board.lines))

        if board.lines:

            d = board.lines[0]

            print("First Drawing :", d.name)

            print("Pieces :", len(d.pieces))

            if d.pieces:

                p = d.pieces[0]

                print("Piece :", p.piece_type)

                print("Points :", len(p.points))

                for pt in p.points:
                    print(pt.x, pt.y)

        print(">>> parse_lines() 종료")
        print(type(current_line))
        print(type(current_line.pieces))
        print(current_line)
        current_line.pieces.append(current_piece)

    def parse_part(self, board):

        print("\n========== PART ==========")

        if "PART" not in board.sections:
            return

        SKIP = {
            "VALUE",
            "HEIGHT",
            "LABEL",
            "TEXT",
            "ATTRIBUTE",
            "MODEL",
            "GLUE"
        }

        board.parts.clear()

        for line in board.sections["PART"]:

            line = line.strip()

            if not line:
                continue

            if line.startswith("*"):
                continue

            w = line.split()

            if len(w) < 5:
                continue

            if w[0].upper() in SKIP:
                continue

            # RefDes는 영문자로 시작해야 함
            if not w[0][0].isalpha():
                continue

            part = Part()

            part.refdes = w[0]
            part.parttype = w[1]

            try:
                part.x = int(w[2])
                part.y = int(w[3])
                part.rotation = float(w[4])
            except ValueError:
                continue

            if len(w) > 5:
                part.side = w[5]

            board.parts.append(part)

        print("PART COUNT :", len(board.parts))

        if board.parts:
            print("\nFIRST PART")
            print(board.parts[0])

    def parse_vias(self, board):

        print("\n========== VIA ==========")

        if "VIA" not in board.sections:
            return

        data = board.sections["VIA"]

        i = 0

        while i < len(data):

            line = data[i].strip()

            if line == "":
                i += 1
                continue

            if line.startswith("*"):
                i += 1
                continue

            w = line.split()

            #
            # VIA Definition
            #
            if len(w) >= 3 and w[0][0].isalpha():

                vd = ViaDef()

                vd.name = w[0]
                vd.drill = int(w[1])
                vd.stack_layers = int(w[2])

                if len(w) >= 5:
                    vd.start_layer = int(w[3])
                    vd.end_layer = int(w[4])

                i += 1

                #
                # Pad Definition
                #
                while i < len(data):

                    s = data[i].strip()

                    if s == "":
                        break

                    if s.startswith("*"):
                        break

                    p = s.split()

                    if len(p) >= 3:

                        pad = ViaPad()

                        pad.layer = int(p[0])
                        pad.diameter = int(p[1])
                        pad.shape = p[2]

                        vd.pads.append(pad)

                    i += 1

                board.via_defs.append(vd)

                continue

            i += 1

        print()

        print("VIA DEF COUNT :", len(board.via_defs))

        for v in board.via_defs:

            print("--------------------------------")

            print("Name :", v.name)

            print("Drill :", v.drill)

            print("Stack :", v.stack_layers)

            print("Layer :", v.start_layer, "~", v.end_layer)

            for p in v.pads:

                print(
                    "  ",
                    p.layer,
                    p.diameter,
                    p.shape
                )

        print("\n========== PART ==========")
        if "PART" not in board.sections:
            return
        
        SKIP_WORDS = {
            "VALUE",
            "HEIGHT",
            "GLUE",
            "LABEL",
            "TEXT",
            "ATTRIBUTE",
            "MODEL"
        }     

        data = board.sections["PART"]

        for line in data:

            line = line.strip()

            if not line:
                    continue

            if line.startswith("*"):
                    continue

            w = line.split()

                #
                # PART Header
                #
                # REFDES PARTTYPE X Y ROT ...
                #
            if len(w) < 5:
                    continue

                #
                # 첫 글자가 알파벳이 아닌 것은 제외
                #
            if not w[0][0].isalpha():
                    continue

            p = Part()

            p.refdes = w[0]

            p.parttype = w[1]

            try:

                p.x = int(w[2])

                p.y = int(w[3])

                p.rotation = float(w[4])

            except:
                    pass

                #
                # SIDE
                #
            if len(w) > 5 and w[5] in ("TOP", "BOTTOM"):
                p.side = w[5]

            board.parts.append(p)

            print()

            print("PART COUNT :", len(board.parts))

            if board.parts:

                print()

                print(board.parts[0])

                if len(board.parts) > 1:

                    print(board.parts[1])




        print("\n========== SIGNAL ==========")

        if "SIGNAL" not in board.sections:
            return

        data = board.sections["SIGNAL"]

        current = None

        for line in data:

            line = line.strip()

            if line == "":
                current = None
                continue

            w = line.split()

            #
            # Header
            #
            if len(w) == 2:

                current = Signal()

                current.start_pin = w[0]

                current.end_pin = w[1]

                board.signals.append(current)

                continue

            #
            # Segment
            #
            if current and len(w) >= 5:

                try:

                    seg = Segment()

                    seg.x = int(w[0])

                    seg.y = int(w[1])

                    seg.layer = int(w[2])

                    seg.width = int(w[3])

                    seg.flags = int(w[4])

                    if len(w) > 5:

                        for t in w[5:]:

                            if t == "THERMAL":
                                seg.thermal = True

                            elif t == "TEARDROP":
                                seg.teardrop = True

                            elif "VIA" in t:
                                seg.via = t

                    current.segments.append(seg)

                except ValueError:
                    pass

        print()

        print("SIGNAL COUNT :", len(board.signals))

        if board.signals:

            s = board.signals[0]

            print()

            print(s.start_pin)

            print(s.end_pin)

            print("Segments :", len(s.segments))

    def parse_signal(self, board):

        print("\n========== SIGNAL ==========")

        if "SIGNAL" not in board.sections:
            return

        board.signals.clear()

        current = None

        for line in board.sections["SIGNAL"]:

            line = line.strip()

            if line == "":
                current = None
                continue

            w = line.split()

            #
            # Header
            #
            if len(w) == 2:

                current = Signal()

                current.start_pin = w[0]
                current.end_pin = w[1]

                board.signals.append(current)

                continue

            #
            # Segment
            #
            if current and len(w) >= 5:

                try:

                    seg = Segment()

                    seg.x = int(w[0])
                    seg.y = int(w[1])

                    seg.layer = int(w[2])
                    seg.width = int(w[3])
                    seg.flags = int(w[4])

                    seg.raw = w

                    #
                    # 옵션
                    #
                    for token in w[5:]:

                        if token == "THERMAL":
                            seg.thermal = True

                        elif token == "TEARDROP":
                            seg.teardrop = True

                        elif token in ("P", "N"):
                            seg.polarity = token

                        elif token.endswith("VIA"):
                            seg.via = token

                    current.segments.append(seg)

                except ValueError:
                    pass

        print()

        print("SIGNAL COUNT :", len(board.signals))

        if board.signals:

            s = board.signals[0]

            print("FIRST SIGNAL")

            print(s.start_pin)

            print(s.end_pin)

            print("Segments :", len(s.segments))

            for seg in s.segments:

                print(
                    seg.layer,
                    seg.width,
                    seg.via,
                    seg.thermal,
                    seg.teardrop,
                    seg.polarity
                )


    def parse_partdecal(self, board):

        print("\n========== PARTDECAL ==========")

        if "PARTDECAL" not in board.sections:
            return

        board.packages = []

        data = board.sections["PARTDECAL"]

        current = None

        for line in data:

            line = line.strip()

            if not line:
                continue

            if line.startswith("*"):
                continue

            w = line.split()

            #
            # Footprint Header
            #
            if len(w) >= 8 and w[1] in ("M", "I"):

                current = Package()

                current.name = w[0]

                current.pads = []

                board.packages.append(current)

                continue

            #
            # PAD
            #
            if current is not None:

                if len(w) >= 3 and w[0] == "PAD":

                    continue

                #
                # PAD DATA
                #
                if len(w) >= 3:

                    try:

                        pad = Pad()

                        pad.layer = int(w[0])

                        pad.size = int(w[1])

                        pad.shape = w[2]

                        current.pads.append(pad)

                    except:

                        pass

        print()

        print("PACKAGE COUNT :", len(board.packages))

        print()

        for p in board.packages[:10]:

            print(p.name, " Pads :", len(p.pads))