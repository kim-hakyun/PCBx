from dataclasses import dataclass, field


@dataclass
class Board:

    properties: dict = field(default_factory=dict)

    sections: dict = field(default_factory=dict)

    texts: list = field(default_factory=list)

    lines: list = field(default_factory=list)

    vias: list = field(default_factory=list)

    via_defs: list = field(default_factory=list)
    
    parts: list = field(default_factory=list)

    signals: list = field(default_factory=list)

    packages: list = field(default_factory=list)
    


@dataclass
class Via:

    x: int = 0

    y: int = 0

    drill: str = ""

    padstack: str = ""

    net: str = ""

    start_layer: int = 0

    end_layer: int = 0

    

@dataclass
class Text:

    x: int = 0
    y: int = 0

    rotation: float = 0.0

    layer: int = 0

    height: int = 0
    width: int = 0

    mirror: str = "N"

    font: str = ""

    value: str = ""


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Line:

    name: str = ""

    line_type: str = ""

    x: int = 0

    y: int = 0

    pieces: list = field(default_factory=list)

    text: int = 0

    points: list = field(default_factory=list)

@dataclass
class Piece:
    piece_type: str = ""
    width: int = 0
    level: int = 0
    points: list = field(default_factory=list)

@dataclass
class ViaDef:

    name: str = ""

    drill: int = 0

    stack_layers: int = 0

    start_layer: int = 0

    end_layer: int = 0

    pads: list = field(default_factory=list)

@dataclass
class ViaPad:

    layer: int = 0
    diameter: int = 0
    shape: str = ""


@dataclass
class Part:

    refdes: str = ""

    parttype: str = ""

    decal: str = ""

    x: int = 0

    y: int = 0

    rotation: float = 0.0

    side: str = ""

    glued: bool = False



@dataclass
class Segment:

    x: int = 0
    y: int = 0

    layer: int = 0

    width: int = 0

    flags: int = 0

    via: str = ""

    thermal: bool = False

    teardrop: bool = False

    polarity: str = ""

    raw: list = field(default_factory=list)


@dataclass
class Signal:

    start_pin : str = ""

    end_pin : str = ""

    segments :list =  field(default_factory=list)

@dataclass
class Pad:

    name: str = ""

    layer: int = 0

    x: int = 0

    y: int = 0

    size: int = 0

    rotation: float = 0.0

    shape: str = "R"

    pin_number: int = 0

@dataclass
class Package:

    name: str = ""

    pads: list = field(default_factory=list)

    outlines: list = field(default_factory=list)

    texts: list = field(default_factory=list)

    pins: list = field(default_factory=list)



@dataclass
class Pin:

    number: int = 0

    x: int = 0

    y: int = 0

@dataclass
class Outline:

    kind: str = ""          # OPEN CLOSED CIRCLE

    width: int = 0

    layer: int = 0

    points: list = field(default_factory=list)