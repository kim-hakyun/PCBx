from pads_parser import PadsParser
from ipc2581_writer import IPC2581Writer


parser = PadsParser()

board = parser.load("sample/test.asc")

writer = IPC2581Writer()

writer.save(board, "output/output.xml")