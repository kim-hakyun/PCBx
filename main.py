from pads_parser import PadsParser
from ipc2581_writer import IPC2581Writer

def main():

    parser = PadsParser()

    board = parser.load("sample/test.asc")
    writer = IPC2581Writer()
    writer.save(board, "output.xml")


    print("=" * 60)
    print("PADS ASCII ANALYZER")
    print("=" * 60)

    print("\nSections")
    print("-" * 30)

    for name, lines in board.sections.items():
        print(f"{name:15} {len(lines)}")

    print("\nPCB Properties")
    print("-" * 30)
    print("TEXT COUNT :", len(board.texts))
    for key, value in board.properties.items():
        print(f"{key:20} {' '.join(value)}")
    print()

    print("LINES COUNT :", len(board.lines))

    print()

    if board.lines:

        first = board.lines[0]

        print("FIRST DRAWING")

        print("-------------------")

        print(first.name)

        print(first.line_type)

        print(first.x, first.y)

        print("Pieces :", len(first.pieces))
        print()

        print("PART COUNT :", len(board.parts))
        print("PACKAGE COUNT :", len(board.packages))


if __name__ == "__main__":
    main()

