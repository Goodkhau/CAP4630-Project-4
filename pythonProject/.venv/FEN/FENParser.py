class FENParser:
    def __init__(self, rows):
        self.rows = rows.split("/")

    def ToTensor(self):
        return self.rows

    def Parse(self):
        parsed_rows = []
        for row in self.rows:
            parsed_row = []
            ## Get each character in the row and translate
            for i in range(len(row)):
                character = row[i]
                if (character.isdigit()):
                    for j in range(int(character)):
                        parsed_row.append(0)
                else:
                    parsed_row.append(self.GetPieceEncoding(character))
            parsed_rows.append(parsed_row)
        self.rows = parsed_rows

    def GetPieceEncoding(self, character):
        match character:
            ## White Pieces
            case 'P':
                return 1
            case 'N':
                return 2
            case 'B':
                return 3
            case 'R':
                return 4
            case 'Q':
                return 5
            case 'K':
                return 6
            ## Black Pieces
            case 'p':
                return -1
            case 'n':
                return -2
            case 'b':
                return -3
            case 'r':
                return -4
            case 'q':
                return -5
            case 'k':
                return -6
