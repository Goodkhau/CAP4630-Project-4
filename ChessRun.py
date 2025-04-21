import chess
from tabulate import tabulate
from tkinter import *
from PIL import ImageTk, Image

def print_board(board):
    start = "\033[1;93m"
    end = "\033[0m"
    header = [' ', start + 'a' + end, start + 'b' + end, start + 'c' + end, start + 'd' + end, start + 'e' + end, start + 'f' + end, start + 'g' + end, start + 'h' + end]

    rows_info = []
    for row in range(8, 0, -1):
        row_info = [start + str(row) + end]
        for col in range(8):
            square = chess.square(col, row - 1)
            piece = board.piece_at(square)
            row_info.append(piece.symbol() if piece else ' ')
        rows_info.append(row_info)

    table = tabulate(rows_info, header, tablefmt="heavy_grid")
    print(table)

def select_piece(piece):
    square = chess.parse_square(piece)
    piece_moves = [move for move in board.legal_moves if move.from_square == square]

    if piece_moves:
        return 0
    else:
        return 1

def check_move(moveLoc, piece, prom):
    move = chess.Move.from_uci(piece + moveLoc + prom)
    if board.is_legal(move):
        return 0
    else:
        return 1

def move(moveLoc, piece, prom):
    move = chess.Move.from_uci(piece + moveLoc + prom)
    board.push(move)

def checkEP(piece, move):
    m = chess.Move.from_uci(piece + move +'')
    return board.is_en_passant(m)

def checkQCastle(piece,move):
    m = chess.Move.from_uci(piece + move +'')
    return board.is_queenside_castling(m)

def checkKCastle(piece,move):
    m = chess.Move.from_uci(piece + move +'')
    return board.is_kingside_castling(m)

def generate_all_positions():
    pass

def convert_position_matrix():
    pass

class guiMaker:
    g = Tk()
    g.title("Chess Game")
    g.geometry("600x455")

    c = Canvas(g,width=600,height=455)
    c.pack()

    boardImg = ImageTk.PhotoImage(Image.open('board.jpg'))
    p = Label(c, image=boardImg)
    c.create_image(300,205,image=boardImg)
    
    l = Label(g, text='')
    e = Entry(g)
    b = Button(g,text='Select',width=7)

    #PIECES STUFF
    #Images
    bBi = ImageTk.PhotoImage(Image.open("ChessPieces/blackBishop.png"))
    wBi = ImageTk.PhotoImage(Image.open("ChessPieces/whiteBishop.png"))
    bPi = ImageTk.PhotoImage(Image.open("ChessPieces/blackPawn.png"))
    wPi = ImageTk.PhotoImage(Image.open("ChessPieces/whitePawn.png"))
    bKi = ImageTk.PhotoImage(Image.open("ChessPieces/blackKing.png"))
    wKi = ImageTk.PhotoImage(Image.open("ChessPieces/whiteKing.png"))
    bRi = ImageTk.PhotoImage(Image.open("ChessPieces/blackRook.png"))
    wRi = ImageTk.PhotoImage(Image.open("ChessPieces/whiteRook.png"))
    bKni = ImageTk.PhotoImage(Image.open("ChessPieces/blackKnight.png"))
    wKni = ImageTk.PhotoImage(Image.open("ChessPieces/whiteKnight.png"))
    bQi = ImageTk.PhotoImage(Image.open("ChessPieces/blackQueen.png"))
    wQi = ImageTk.PhotoImage(Image.open("ChessPieces/whiteQueen.png"))

    #Positions
    # -1 -1 means dead
    wR1 = [0,0]
    wK1 = [1,0]
    wB1 = [2,0]
    wQ = [3,0]
    wK = [4,0]
    wB2 = [5,0]
    wK2 = [6,0]
    wR2 = [7,0]
    wP0 = [0,1]
    wP1 = [1,1]
    wP2 = [2,1]
    wP3 = [3,1]
    wP4 = [4,1]
    wP5 = [5,1]
    wP6 = [6,1]
    wP7 = [7,1]
    bR1 = [0,7]
    bK1 = [1,7]
    bB1 = [2,7]
    bQ = [3,7]
    bK = [4,7]
    bB2 = [5,7]
    bK2 = [6,7]
    bR2 = [7,7]
    bP0 = [0,6]
    bP1 = [1,6]
    bP2 = [2,6]
    bP3 = [3,6]
    bP4 = [4,6]
    bP5 = [5,6]
    bP6 = [6,6]
    bP7 = [7,6]
    #CanvasPieces
    cwP0 = None #whitepawns
    cwP1 = None
    cwP2 = None
    cwP3 = None
    cwP4 = None
    cwP5 = None
    cwP6 = None
    cwP7 = None
    cbP0 = None #blackpawns
    cbP1 = None
    cbP2 = None
    cbP3 = None
    cbP4 = None
    cbP5 = None
    cbP6 = None
    cbP7 = None
    cwR1 = None #whiterooks
    cwR2 = None
    cbR1 = None #blackrooks
    cbR2 = None
    cwKn1 = None #whiteknights
    cwKn2 = None
    cbKn1 = None #blackknights
    cbKn1 = None
    cwB1 = None #whitebishops
    cwB2 = None
    cbB1 = None #blackbishops
    cbB1 = None
    cwQ = None #whitequeen
    cbQ = None #blackqueen
    cwK = None #whiteking
    cbK = None #blackking

    #Board RelLocs
    relLocX = [0.265,0.334,0.4,0.468,0.534,0.603,0.668,0.738] #Stores relx for all piece locations
    relLocY = [0.76,0.67,0.585,0.493,0.4,0.315,0.225,0.138] #Stores rely for all piece locations

    promUnit = ''
    recentPromoteInt = 0
    wpromoted = [0,0,0,0,0,0,0,0]
    bpromoted = [0,0,0,0,0,0,0,0]
    promoted_piece = None
    piece = None
    move = None
    gameEnd = False
    f = True
    result = [0,0]

    def endfr(self):
        self.g.destroy()

    #Initializer
    def __init__(self, default=False):
        self.placePieces()
        self.statePickPiece()

    #Opens GUI
    def run(self):
        self.g.mainloop()

    #Checks whether piece selected is valid
    def checkPiece(self):
        self.piece = self.e.get()
        pCheck = select_piece(self.piece)
        if(pCheck == 1):
            self.l.config(text='Please select a VALID piece')
            pCheck = select_piece(self.piece)
        else:
            self.pieceSelect(0)

    def checkPawn(self):
        numPiece = self.convertPiece()
        if numPiece == self.wP0:
            return True
        elif numPiece == self.wP1:
            return True
        elif numPiece == self.wP2:
            return True
        elif numPiece == self.wP3:
            return True
        elif numPiece == self.wP4:
            return True
        elif numPiece == self.wP5:
            return True
        elif numPiece == self.wP6:
            return True
        elif numPiece == self.wP7:
            return True
        elif numPiece == self.bP0:
            return True
        elif numPiece == self.bP1:
            return True
        elif numPiece == self.bP2:
            return True
        elif numPiece == self.bP3:
            return True
        elif numPiece == self.bP4:
            return True
        elif numPiece == self.bP5:
            return True
        elif numPiece == self.bP6:
            return True
        elif numPiece == self.bP7:
            return True
        else:
            return False

    #Checks whether move is valid
    def checkMove(self):
        mCheck = check_move(self.move, self.piece, self.promoted_piece)
        if(mCheck == 1):
            self.l.config(text='Please select a VALID move')
            self.pieceSelect(1)
        else:
            self.moveGui()
        
    #Converts user input to arrays
    def convertPiece(self):
        first = self.piece[0]
        result = [0,0]
        result[1] = (int)(self.piece[1])-1
        match first:
            case 'a':
                result[0] = 0
                return result
            case 'b':
                result[0] = 1
                return result
            case 'c':
                result[0] = 2
                return result
            case 'd':
                result[0] = 3
                return result
            case 'e':
                result[0] = 4
                return result
            case 'f':
                result[0] = 5
                return result
            case 'g':
                result[0] = 6
                return result
            case 'h':
                result[0] = 7
                return result

    #Converts user input to arrays
    def convertMove(self):
        first = self.move[0]
        result = [0,0]
        result[1] = int(self.move[1])
        match first:
            case 'a':
                result[0] = 0
                return result
            case 'b':
                result[0] = 1
                return result
            case 'c':
                result[0] = 2
                return result
            case 'd':
                result[0] = 3
                return result
            case 'e':
                result[0] = 4
                return result
            case 'f':
                result[0] = 5
                return result
            case 'g':
                result[0] = 6
                return result
            case 'h':
                result[0] = 7
                return result
  
    #Deletes killed units from the canvas
    def deletePiece(self, m):
        if(self.wR1 == m):
            self.wR1 = [-1,-1]
            self.c.delete(self.cwR1)
        elif(self.wK1 == m):
            self.wK1 = [-1,-1]
            self.c.delete(self.cwKn1)
        elif(self.wB1 == m):
            self.wB1 = [-1,-1]
            self.c.delete(self.cwB1)
        elif(self.wQ == m):
            self.wQ = [-1,-1]
            self.c.delete(self.cwQ)
        elif(self.wK == m):
            self.wK = [-1,-1]
            self.c.delete(self.cwK)
        elif(self.wB2 == m):
            self.wB2 = [-1,-1]
            self.c.delete(self.cwB2)
        elif(self.wK2 == m):
            self.wK2 = [-1,-1]
            self.c.delete(self.cwKn2)
        elif(self.wR2 == m):
            self.wR2 = [-1,-1]
            self.c.delete(self.cwR2)
        elif(self.wP0 == m):
            self.wP0 = [-1,-1]
            self.c.delete(self.cwP0)
        elif(self.wP1 == m):
            self.wP1 = [-1,-1]
            self.c.delete(self.cwP1)
        elif(self.wP2 == m):
            self.wP2 = [-1,-1]
            self.c.delete(self.cwP2)
        elif(self.wP3 == m):
            self.wP3 = [-1,-1]
            self.c.delete(self.cwP3)
        elif(self.wP4 == m):
            self.wP4 = [-1,-1]
            self.c.delete(self.cwP4)
        elif(self.wP5 == m):
            self.wP5 = [-1,-1]
            self.c.delete(self.cwP5)
        elif(self.wP6 == m):
            self.wP6 = [-1,-1]
            self.c.delete(self.cwP6)
        elif(self.wP7 == m):
            self.wP7 = [-1,-1]
            self.c.delete(self.cwP7)
        elif(self.bR1 == m):
            self.bR1 = [-1,-1]
            self.c.delete(self.cbR1)
        elif(self.bK1 == m):
            self.bK1 = [-1,-1]
            self.c.delete(self.cbKn1)
        elif(self.bB1 == m):
            self.bB1 = [-1,-1]
            self.c.delete(self.cbB1)
        elif(self.bQ == m):
            self.bQ = [-1,-1]
            self.c.delete(self.cbQ)
        elif(self.bK == m):
            self.bK = [-1,-1]
            self.c.delete(self.cbK)
        elif(self.bB2 == m):
            self.bB2 = [-1,-1]
            self.c.delete(self.cbB2)
        elif(self.bK2 == m):
            self.bK2 = [-1,-1]
            self.c.delete(self.cbKn2)
        elif(self.bR2 == m):
            self.bR2 = [-1,-1]
            self.c.delete(self.cbR2)
        elif(self.bP0 == m):
            self.bP0 = [-1,-1]
            self.c.delete(self.cbP0)
        elif(self.bP1 == m):
            self.bP1 = [-1,-1]
            self.c.delete(self.cbP1)
        elif(self.bP2 == m):
            self.bP2 = [-1,-1]
            self.c.delete(self.cbP2)
        elif(self.bP3 == m):
            self.bP3 = [-1,-1]
            self.c.delete(self.cbP3)
        elif(self.bP4 == m):
            self.bP4 = [-1,-1]
            self.c.delete(self.cbP4)
        elif(self.bP5 == m):
            self.bP5 = [-1,-1]
            self.c.delete(self.cbP5)
        elif(self.bP6 == m):
            self.bP6 = [-1,-1]
            self.c.delete(self.cbP6)
        elif(self.bP7 == m):
            self.bP7 = [-1,-1]
            self.c.delete(self.cbP7)

    #Moves the images on the canvas
    def movePiece(self,newMove):
        self.piece = self.convertPiece()
        if(self.wR1 == self.piece):
            self.wR1 = newMove
            self.c.coords(self.cwR1, (self.relLocX[self.wR1[0]])*600 ,(self.relLocY[self.wR1[1]])*455)
        elif(self.wK1 == self.piece):
            self.wK1 = newMove
            self.c.coords(self.cwKn1, (self.relLocX[self.wK1[0]])*600 ,(self.relLocY[self.wK1[1]])*455)
        elif(self.wB1 == self.piece):
            self.wB1 = newMove
            self.c.coords(self.cwB1, (self.relLocX[self.wB1[0]])*600 ,(self.relLocY[self.wB1[1]])*455)
        elif(self.wQ == self.piece):
            self.wQ = newMove
            self.c.coords(self.cwQ, (self.relLocX[self.wQ[0]])*600 ,(self.relLocY[self.wQ[1]])*455)
        elif(self.wK == self.piece):
            self.wK = newMove
            self.c.coords(self.cwK, (self.relLocX[self.wK[0]])*600 ,(self.relLocY[self.wK[1]])*455)
        elif(self.wB2 == self.piece):
            self.wB2 = newMove
            self.c.coords(self.cwB2, (self.relLocX[self.wB2[0]])*600 ,(self.relLocY[self.wB2[1]])*455)
        elif(self.wK2 == self.piece):
            self.wK2 = newMove
            self.c.coords(self.cwKn2, (self.relLocX[self.wK2[0]])*600 ,(self.relLocY[self.wK2[1]])*455)
        elif(self.wR2 == self.piece):
            self.wR2 = newMove
            self.c.coords(self.cwR2, (self.relLocX[self.wR2[0]])*600 ,(self.relLocY[self.wR2[1]])*455)
        elif(self.wP0 == self.piece):
            self.wP0 = newMove
            self.c.coords(self.cwP0, (self.relLocX[self.wP0[0]])*600 ,(self.relLocY[self.wP0[1]])*455)
        elif(self.wP1 == self.piece):
            self.wP1 = newMove
            self.c.coords(self.cwP1, (self.relLocX[self.wP1[0]])*600 ,(self.relLocY[self.wP1[1]])*455)
        elif(self.wP2 == self.piece):
            self.wP2 = newMove
            self.c.coords(self.cwP2, (self.relLocX[self.wP2[0]])*600 ,(self.relLocY[self.wP2[1]])*455)
        elif(self.wP3 == self.piece):
            self.wP3 = newMove
            self.c.coords(self.cwP3, (self.relLocX[self.wP3[0]])*600 ,(self.relLocY[self.wP3[1]])*455)
        elif(self.wP4 == self.piece):
            self.wP4 = newMove
            self.c.coords(self.cwP4, (self.relLocX[self.wP4[0]])*600 ,(self.relLocY[self.wP4[1]])*455)
        elif(self.wP5 == self.piece):
            self.wP5 = newMove
            self.c.coords(self.cwP5, (self.relLocX[self.wP5[0]])*600 ,(self.relLocY[self.wP5[1]])*455)
        elif(self.wP6 == self.piece):
            self.wP6 = newMove
            self.c.coords(self.cwP6, (self.relLocX[self.wP6[0]])*600 ,(self.relLocY[self.wP6[1]])*455)
        elif(self.wP7 == self.piece):
            self.wP7 = newMove
            self.c.coords(self.cwP7, (self.relLocX[self.wP7[0]])*600 ,(self.relLocY[self.wP7[1]])*455)
        elif(self.bR1 == self.piece):
            self.bR1 = newMove
            self.c.coords(self.cbR1, (self.relLocX[self.bR1[0]])*600 ,(self.relLocY[self.bR1[1]])*455)
        elif(self.bK1 == self.piece):
            self.bK1 = newMove
            self.c.coords(self.cbKn1, (self.relLocX[self.bK1[0]])*600 ,(self.relLocY[self.bK1[1]])*455)
        elif(self.bB1 == self.piece):
            self.bB1 = newMove
            self.c.coords(self.cbB1, (self.relLocX[self.bB1[0]])*600 ,(self.relLocY[self.bB1[1]])*455)
        elif(self.bQ == self.piece):
            self.bQ = newMove
            self.c.coords(self.cbQ, (self.relLocX[self.bQ[0]])*600 ,(self.relLocY[self.bQ[1]])*455)
        elif(self.bK == self.piece):
            self.bK = newMove
            self.c.coords(self.cbK, (self.relLocX[self.bK[0]])*600 ,(self.relLocY[self.bK[1]])*455)
        elif(self.bB2 == self.piece):
            self.bB2 = newMove
            self.c.coords(self.cbB2, (self.relLocX[self.bB2[0]])*600 ,(self.relLocY[self.bB2[1]])*455)
        elif(self.bK2 == self.piece):
            self.bK2 = newMove
            self.c.coords(self.cbKn2, (self.relLocX[self.bK2[0]])*600 ,(self.relLocY[self.bK2[1]])*455)
        elif(self.bR2 == self.piece):
            self.bR2 = newMove
            self.c.coords(self.cbR2, (self.relLocX[self.bR2[0]])*600 ,(self.relLocY[self.bR2[1]])*455)
        elif(self.bP0 == self.piece):
            self.bP0 = newMove
            self.c.coords(self.cbP0, (self.relLocX[self.bP0[0]])*600 ,(self.relLocY[self.bP0[1]])*455)
        elif(self.bP1 == self.piece):
            self.bP1 = newMove
            self.c.coords(self.cbP1, (self.relLocX[self.bP1[0]])*600 ,(self.relLocY[self.bP1[1]])*455)
        elif(self.bP2 == self.piece):
            self.bP2 = newMove
            self.c.coords(self.cbP2, (self.relLocX[self.bP2[0]])*600 ,(self.relLocY[self.bP2[1]])*455)
        elif(self.bP3 == self.piece):
            self.bP3 = newMove
            self.c.coords(self.cbP3, (self.relLocX[self.bP3[0]])*600 ,(self.relLocY[self.bP3[1]])*455)
        elif(self.bP4 == self.piece):
            self.bP4 = newMove
            self.c.coords(self.cbP4, (self.relLocX[self.bP4[0]])*600 ,(self.relLocY[self.bP4[1]])*455)
        elif(self.bP5 == self.piece):
            self.bP5 = newMove
            self.c.coords(self.cbP5, (self.relLocX[self.bP5[0]])*600 ,(self.relLocY[self.bP5[1]])*455)
        elif(self.bP6 == self.piece):
            self.bP6 = newMove
            self.c.coords(self.cbP6, (self.relLocX[self.bP6[0]])*600 ,(self.relLocY[self.bP6[1]])*455)
        elif(self.bP7 == self.piece):
            self.bP7 = newMove
            self.c.coords(self.cbP7, (self.relLocX[self.bP7[0]])*600 ,(self.relLocY[self.bP7[1]])*455)

    def promImage(self,new):
        p = self.convertPiece()
        if(self.wP0 == p):
            if(new == 'n'):
                self.c.itemconfig(self.cwP0, image = self.wKni)
            elif(new == 'q'):
                self.c.itemconfig(self.cwP0, image = self.wQi)
            elif(new == 'b'):
                self.c.itemconfig(self.cwP0, image = self.wBi)
            else:
                self.c.itemconfig(self.cwP0, image = self.wRi)
        elif(self.wP1 == p):
            if(new == 'n'):
                self.c.itemconfig(self.cwP1, image = self.wKni)
            elif(new == 'q'):
                self.c.itemconfig(self.cwP1, image = self.wQi)
            elif(new == 'b'):
                self.c.itemconfig(self.cwP1, image = self.wBi)
            else:
                self.c.itemconfig(self.cwP1, image = self.wRi)
        elif(self.wP2 == p):
            if(new == 'n'):
                self.c.itemconfig(self.cwP2, image = self.wKni)
            elif(new == 'q'):
                self.c.itemconfig(self.cwP2, image = self.wQi)
            elif(new == 'b'):
                self.c.itemconfig(self.cwP2, image = self.wBi)
            else:
                self.c.itemconfig(self.cwP2, image = self.wRi)
        elif(self.wP3 == p):
            if(new == 'n'):
                self.c.itemconfig(self.cwP3, image = self.wKni)
            elif(new == 'q'):
                self.c.itemconfig(self.cwP3, image = self.wQi)
            elif(new == 'b'):
                self.c.itemconfig(self.cwP3, image = self.wBi)
            else:
                self.c.itemconfig(self.cwP3, image = self.wRi)
        elif(self.wP4 == p):
            if(new == 'n'):
                self.c.itemconfig(self.cwP4, image = self.wKni)
            elif(new == 'q'):
                self.c.itemconfig(self.cwP4, image = self.wQi)
            elif(new == 'b'):
                self.c.itemconfig(self.cwP4, image = self.wBi)
            else:
                self.c.itemconfig(self.cwP4, image = self.wRi)
        elif(self.wP5 == p):
            if(new == 'n'):
                self.c.itemconfig(self.cwP5, image = self.wKni)
            elif(new == 'q'):
                self.c.itemconfig(self.cwP5, image = self.wQi)
            elif(new == 'b'):
                self.c.itemconfig(self.cwP5, image = self.wBi)
            else:
                self.c.itemconfig(self.cwP5, image = self.wRi)
        elif(self.wP6 == p):
            if(new == 'n'):
                self.c.itemconfig(self.cwP6, image = self.wKni)
            elif(new == 'q'):
                self.c.itemconfig(self.cwP6, image = self.wQi)
            elif(new == 'b'):
                self.c.itemconfig(self.cwP6, image = self.wBi)
            else:
                self.c.itemconfig(self.cwP6, image = self.wRi)
        elif(self.wP7 == p):
            if(new == 'n'):
                self.c.itemconfig(self.cwP7, image = self.wKni)
            elif(new == 'q'):
                self.c.itemconfig(self.cwP7, image = self.wQi)
            elif(new == 'b'):
                self.c.itemconfig(self.cwP7, image = self.wBi)
            else:
                self.c.itemconfig(self.cwP7, image = self.wRi)
        elif(self.bP0 == p):
            if(new == 'n'):
                self.c.itemconfig(self.cbP0, image = self.bKni)
            elif(new == 'q'):
                self.c.itemconfig(self.cbP0, image = self.bQi)
            elif(new == 'b'):
                self.c.itemconfig(self.cbP0, image = self.bBi)
            else:
                self.c.itemconfig(self.cbP0, image = self.bRi)
        elif(self.bP1 == p):
            if(new == 'n'):
                self.c.itemconfig(self.cbP1, image = self.bKni)
            elif(new == 'q'):
                self.c.itemconfig(self.cbP1, image = self.bQi)
            elif(new == 'b'):
                self.c.itemconfig(self.cbP1, image = self.bBi)
            else:
                self.c.itemconfig(self.cbP1, image = self.bRi)
        elif(self.bP2 == p):
            if(new == 'n'):
                self.c.itemconfig(self.cbP2, image = self.bKni)
            elif(new == 'q'):
                self.c.itemconfig(self.cbP2, image = self.bQi)
            elif(new == 'b'):
                self.c.itemconfig(self.cbP2, image = self.bBi)
            else:
                self.c.itemconfig(self.cbP2, image = self.bRi)
        elif(self.bP3 == p):
            if(new == 'n'):
                self.c.itemconfig(self.cbP3, image = self.bKni)
            elif(new == 'q'):
                self.c.itemconfig(self.cbP3, image = self.bQi)
            elif(new == 'b'):
                self.c.itemconfig(self.cbP3, image = self.bBi)
            else:
                self.c.itemconfig(self.cbP3, image = self.bRi)
        elif(self.bP4 == p):
            if(new == 'n'):
                self.c.itemconfig(self.cbP4, image = self.bKni)
            elif(new == 'q'):
                self.c.itemconfig(self.cbP4, image = self.bQi)
            elif(new == 'b'):
                self.c.itemconfig(self.cbP4, image = self.bBi)
            else:
                self.c.itemconfig(self.cbP4, image = self.bRi)
        elif(self.bP5 == p):
            if(new == 'n'):
                self.c.itemconfig(self.cbP5, image = self.bKni)
            elif(new == 'q'):
                self.c.itemconfig(self.cbP5, image = self.bQi)
            elif(new == 'b'):
                self.c.itemconfig(self.cbP5, image = self.bBi)
            else:
                self.c.itemconfig(self.cbP5, image = self.bRi)
        elif(self.bP6 == p):
            if(new == 'n'):
                self.c.itemconfig(self.cbP6, image = self.bKni)
            elif(new == 'q'):
                self.c.itemconfig(self.cbP6, image = self.bQi)
            elif(new == 'b'):
                self.c.itemconfig(self.cbP6, image = self.bBi)
            else:
                self.c.itemconfig(self.cbP6, image = self.bRi)
        elif(self.bP7 == p):
            if(new == 'n'):
                self.c.itemconfig(self.cbP7, image = self.bKni)
            elif(new == 'q'):
                self.c.itemconfig(self.cbP7, image = self.bQi)
            elif(new == 'b'):
                self.c.itemconfig(self.cbP7, image = self.bBi)
            else:
                self.c.itemconfig(self.cbP7, image = self.bRi)
        
    def checkEnpassant(self, m,p):
        b = checkEP(p,m)
        if(b):
            if board.turn == chess.WHITE:
                self.killUnitUnder()
            else:
                self.killUnitAbove()

    def killUnitAbove(self): #kills white units enpassant
        newMove = self.convertMove()
        if newMove == self.wP0:
            self.wP0 = [-1,-1]
            self.c.delete(self.cwP0)
        elif newMove == self.wP1:
            self.wP1 = [-1,-1]
            self.c.delete(self.cwP1)
        elif newMove == self.wP2:
            self.wP2 = [-1,-1]
            self.c.delete(self.cwP2)
        elif newMove == self.wP3:
            self.wP3 = [-1,-1]
            self.c.delete(self.cwP3)
        elif newMove == self.wP4:
            self.wP4 = [-1,-1]
            self.c.delete(self.cwP4)
        elif newMove == self.wP5:
            self.wP5 = [-1,-1]
            self.c.delete(self.cwP5)
        elif newMove == self.wP6:
            self.wP6 = [-1,-1]
            self.c.delete(self.cwP6)
        elif newMove == self.wP7:
            self.wP7 = [-1,-1]
            self.c.delete(self.cwP7)

    def killUnitUnder(self): #kills black units enpassant
        newMove = self.convertMove()
        newMove[1] -=2
        if newMove == self.bP0:
            self.bP0 = [-1,-1]
            self.c.delete(self.cbP0)
        elif newMove == self.bP1:
            self.bP1 = [-1,-1]
            self.c.delete(self.cbP1)
        elif newMove == self.bP2:
            self.bP2 = [-1,-1]
            self.c.delete(self.cbP2)
        elif newMove == self.bP3:
            self.bP3 = [-1,-1]
            self.c.delete(self.cbP3)
        elif newMove == self.bP4:
            self.bP4 = [-1,-1]
            self.c.delete(self.cbP4)
        elif newMove == self.bP5:
            self.bP5 = [-1,-1]
            self.c.delete(self.cbP5)
        elif newMove == self.bP6:
            self.bP6 = [-1,-1]
            self.c.delete(self.cbP6)
        elif newMove == self.bP7:
            self.bP7 = [-1,-1]
            self.c.delete(self.cbP7)

    #Graphical move for Kingside Castle on White
    def wKCastleMove(self,newMove):
        self.wR2 = [5,0]
        self.c.coords(self.cwR2, (self.relLocX[self.wR2[0]])*600 ,(self.relLocY[self.wR2[1]])*455)

    #Graphical move for Queenside Castle on White
    def wQCastleMove(self,newMove):
        self.wR1 = [3,0]
        self.c.coords(self.cwR1, (self.relLocX[self.wR1[0]])*600 ,(self.relLocY[self.wR1[1]])*455)

    #Graphical move for Kingside Castle on Black
    def bKCastleMove(self,newMove):
        self.bR2 = [5,7]
        self.c.coords(self.cbR2, (self.relLocX[self.bR2[0]])*600 ,(self.relLocY[self.bR2[1]])*455)
    
    #Graphical move for Queenside Castle on Black
    def bQCastleMove(self,newMove):
        self.bR1 = [3,7]
        self.c.coords(self.cbR1, (self.relLocX[self.bR1[0]])*600 ,(self.relLocY[self.bR1[1]])*455)

    #Checks if the given move is a castle
    def checkCastle(self, m, p): #1 if king, 2 if queen, 0 if none
        q = checkQCastle(p,m)
        k = checkKCastle(p,m)
        if(q):
            return 2
        elif(k):
            return 1
        else:
            return 0

    #Instruction list once move is confirmed
    def moveGui(self):
        if(board.turn == chess.WHITE):
            t = 1
        else:
            t = 2
        newMove = self.convertMove()
        newMove[1] -= 1
        self.deletePiece(newMove)
        self.checkEnpassant(self.move,self.piece)
        c = self.checkCastle(self.move,self.piece)
        move(self.move, self.piece, self.promoted_piece)
        if(c == 0):
            self.movePiece(newMove)
        elif(c == 1):
            if(t == 1):
                self.wKCastleMove(newMove)
                self.movePiece(newMove)
            else:
                self.bKCastleMove(newMove)
                self.movePiece(newMove)
        else:
            if(t == 1):
                self.wQCastleMove(newMove)
                self.movePiece(newMove)
            else:
                self.bQCastleMove(newMove)
                self.movePiece(newMove)
        if board.turn == chess.WHITE:
            self.statePickPiece()
        else:
            self.BLACKstatePickPiece()

    #Gets index of given pawn
    def getPawnNum(self):
        p = self.convertPiece()
        if (p == self.wP0) or (p == self.bP0):
            return 0
        elif (p == self.wP1) or (p == self.bP1):
            return 1
        elif (p == self.wP2) or (p == self.bP2):
            return 2
        elif (p == self.wP3) or (p == self.bP3):
            return 3
        elif (p == self.wP4) or (p == self.bP4):
            return 4
        elif (p == self.wP4) or (p == self.bP4):
            return 4
        elif (p == self.wP5) or (p == self.bP5):
            return 5
        elif (p == self.wP6) or (p == self.bP6):
            return 6
        elif (p == self.wP7) or (p == self.bP7):
            return 7

    #Promotion prompt
    def promote(self):
        self.promoted_piece = ''
        rank = int(self.move[1])
        pNum = self.getPawnNum()
        self.recentPromoteInt = pNum
        if (rank == 1 or rank == 8):
            if board.turn == chess.WHITE:
                if(self.wpromoted[pNum] == False):
                    self.wpromoted[pNum] = True
                    self.l.config(text='Which type to promote to? (b/n/r/q)')
                    self.e.delete(0,'end')
                    self.b.config(text='Select',width=7, command=self.promoteCheck)
                else:
                    self.checkMove()
            else:
                if(self.bpromoted[pNum] == False):
                    self.bpromoted[pNum] = True
                    self.l.config(text='Which type to promote to? (b/n/r/q)')
                    self.e.delete(0,'end')
                    self.b.config(text='Select',width=7, command=self.promoteCheck)
                else:
                    self.checkMove()
        else:
            self.checkMove()

    #Checks if correct letter is entered for promotion
    def promoteCheck(self):
        check = self.e.get()
        if(check != 'b') and (check != 'n') and (check != 'r') and (check != 'q'):
            self.l.config(text='Please select a VALID type. (b/n/r/q)')
            self.promote()
        else:
            self.promoted_piece = self.e.get()
            self.promImage(check)
            self.checkMove()

    #Black turn start
    def BLACKstatePickPiece(self):
        res = board.result()
        if res != '*':
            self.gameEnd = True
        if (self.gameEnd == True):
            self.end()
        else:
            self.promoted_piece=''
            self.l.config(text='BLACK TURN: Which piece to move? Please enter the code (d1, c4, etc.)')
            self.e.delete(0,'end')
            self.b.config(text='Select',width=7, command=self.checkPiece)

    #Starts promotion prompt if pawn
    def checkMoveList(self):
        self.move = self.e.get()
        p = self.checkPawn()
        if(p):
            self.promote()
        else:
            self.checkMove()

    def undoPromote(self):
        if board.turn == chess.WHITE:
            match self.recentPromoteInt:
                case 0:
                    self.c.itemconfig(self.cwP0, image = self.wPi)
                    return
                case 1:
                    self.c.itemconfig(self.cwP1, image = self.wPi)
                    return
                case 2:
                    self.c.itemconfig(self.cwP2, image = self.wPi)
                    return
                case 3:
                    self.c.itemconfig(self.cwP3, image = self.wPi)
                    return
                case 4:
                    self.c.itemconfig(self.cwP4, image = self.wPi)
                    return
                case 5:
                    self.c.itemconfig(self.cwP5, image = self.wPi)
                    return
                case 6:
                    self.c.itemconfig(self.cwP6, image = self.wPi)
                    return
                case 7:
                    self.c.itemconfig(self.cwP7, image = self.wPi)
                    return
        else:
            match self.recentPromoteInt:
                case 0:
                    self.c.itemconfig(self.cbP0, image = self.bPi)
                    return
                case 1:
                    self.c.itemconfig(self.cbP1, image = self.bPi)
                    return
                case 2:
                    self.c.itemconfig(self.cbP2, image = self.bPi)
                    return
                case 3:
                    self.c.itemconfig(self.cbP3, image = self.bPi)
                    return
                case 4:
                    self.c.itemconfig(self.cbP4, image = self.bPi)
                    return
                case 5:
                    self.c.itemconfig(self.cbP5, image = self.bPi)
                    return
                case 6:
                    self.c.itemconfig(self.cbP6, image = self.bPi)
                    return
                case 7:
                    self.c.itemconfig(self.cbP7, image = self.bPi)
                    return

    #Requests where to move piece
    def pieceSelect(self, val):
        if val==1:
            self.l.config(text='Promotion reverted. Please select a valid movement.')
            self.undoPromote()
        else:
            self.l.config(text='Where to move it? Please enter the code (d1, c4, etc.)')
        self.e.delete(0,'end')
        self.b.config(text='Select',width=7, command=self.checkMoveList)

    #Initializes all pieces
    def placePieces(self):
        #White
        #Pawns
        self.cwP0 = self.c.create_image((self.relLocX[self.wP0[0]])*600,(self.relLocY[self.wP0[1]])*455,image=self.wPi)
        self.cwP1 = self.c.create_image((self.relLocX[self.wP1[0]])*600,(self.relLocY[self.wP1[1]])*455,image=self.wPi)
        self.cwP2 = self.c.create_image((self.relLocX[self.wP2[0]])*600,(self.relLocY[self.wP2[1]])*455,image=self.wPi)
        self.cwP3 = self.c.create_image((self.relLocX[self.wP3[0]])*600,(self.relLocY[self.wP3[1]])*455,image=self.wPi)
        self.cwP4 = self.c.create_image((self.relLocX[self.wP4[0]])*600,(self.relLocY[self.wP4[1]])*455,image=self.wPi)
        self.cwP5 = self.c.create_image((self.relLocX[self.wP5[0]])*600,(self.relLocY[self.wP5[1]])*455,image=self.wPi)
        self.cwP6 = self.c.create_image((self.relLocX[self.wP6[0]])*600,(self.relLocY[self.wP6[1]])*455,image=self.wPi)
        self.cwP7 = self.c.create_image((self.relLocX[self.wP7[0]])*600,(self.relLocY[self.wP7[1]])*455,image=self.wPi)
        #Rooks
        self.cwR1 = self.c.create_image((self.relLocX[self.wR1[0]])*600,(self.relLocY[self.wR1[1]])*455,image=self.wRi)
        self.cwR2 = self.c.create_image((self.relLocX[self.wR2[0]])*600,(self.relLocY[self.wR2[1]])*455,image=self.wRi)
        #Bishops
        self.cwB1 = self.c.create_image((self.relLocX[self.wB1[0]])*600,(self.relLocY[self.wB1[1]])*455,image=self.wBi)
        self.cwB2 = self.c.create_image((self.relLocX[self.wB2[0]])*600,(self.relLocY[self.wB2[1]])*455,image=self.wBi)
        #Knights
        self.cwKn1 = self.c.create_image((self.relLocX[self.wK1[0]])*600,(self.relLocY[self.wK1[1]])*455,image=self.wKni)
        self.cwKn2 = self.c.create_image((self.relLocX[self.wK2[0]])*600,(self.relLocY[self.wK2[1]])*455,image=self.wKni)
        #Queen
        self.cwQ = self.c.create_image((self.relLocX[self.wQ[0]])*600,(self.relLocY[self.wQ[1]])*455,image=self.wQi)
        #King
        self.cwK = self.c.create_image((self.relLocX[self.wK[0]])*600,(self.relLocY[self.wK[1]])*455,image=self.wKi)

        #Black
        #Pawns
        self.cbP0 = self.c.create_image((self.relLocX[self.bP0[0]])*600,(self.relLocY[self.bP0[1]])*455,image=self.bPi)
        self.cbP1 = self.c.create_image((self.relLocX[self.bP1[0]])*600,(self.relLocY[self.bP1[1]])*455,image=self.bPi)
        self.cbP2 = self.c.create_image((self.relLocX[self.bP2[0]])*600,(self.relLocY[self.bP2[1]])*455,image=self.bPi)
        self.cbP3 = self.c.create_image((self.relLocX[self.bP3[0]])*600,(self.relLocY[self.bP3[1]])*455,image=self.bPi)
        self.cbP4 = self.c.create_image((self.relLocX[self.bP4[0]])*600,(self.relLocY[self.bP4[1]])*455,image=self.bPi)
        self.cbP5 = self.c.create_image((self.relLocX[self.bP5[0]])*600,(self.relLocY[self.bP5[1]])*455,image=self.bPi)
        self.cbP6 = self.c.create_image((self.relLocX[self.bP6[0]])*600,(self.relLocY[self.bP6[1]])*455,image=self.bPi)
        self.cbP7 = self.c.create_image((self.relLocX[self.bP7[0]])*600,(self.relLocY[self.bP7[1]])*455,image=self.bPi)
        #Rooks
        self.cbR1 = self.c.create_image((self.relLocX[self.bR1[0]])*600,(self.relLocY[self.bR1[1]])*455,image=self.bRi)
        self.cbR2 = self.c.create_image((self.relLocX[self.bR2[0]])*600,(self.relLocY[self.bR2[1]])*455,image=self.bRi)
        #Bishops
        self.cbB1 = self.c.create_image((self.relLocX[self.bB1[0]])*600,(self.relLocY[self.bB1[1]])*455,image=self.bBi)
        self.cbB2 = self.c.create_image((self.relLocX[self.bB2[0]])*600,(self.relLocY[self.bB2[1]])*455,image=self.bBi)
        #Knights
        self.cbKn1 = self.c.create_image((self.relLocX[self.bK1[0]])*600,(self.relLocY[self.bK1[1]])*455,image=self.bKni)
        self.cbKn2 = self.c.create_image((self.relLocX[self.bK2[0]])*600,(self.relLocY[self.bK2[1]])*455,image=self.bKni)
        #Queen
        self.cbQ = self.c.create_image((self.relLocX[self.bQ[0]])*600,(self.relLocY[self.bQ[1]])*455,image=self.bQi)
        #King
        self.cbK = self.c.create_image((self.relLocX[self.bK[0]])*600,(self.relLocY[self.bK[1]])*455,image=self.bKi)

    def end(self):
        self.l.config(text='Checkmate. Press End to close the game')
        self.e.destroy()
        self.b.config(text='End',width=7, command=self.endfr)
        self.b.place(relx=.5, rely=0.95,anchor='center')

    #White turn start
    def statePickPiece(self):
        res = board.result()
        if res != '*':
            self.gameEnd = True
        if (self.gameEnd == True):
            self.end()
        else:
            self.promoted_piece=''
            self.l.config(text='WHITE TURN: Which piece to move? Please enter the code (d1, c4, etc.)')
            self.e.delete(0,'end')
            self.b.config(text='Select',width=7, command=self.checkPiece)
            self.l.place(relx=0.5,rely=0.89,anchor='center')
            self.e.place(relx=0.4,rely=0.955, anchor='center')
            self.b.place(relx=0.67,rely=0.95, anchor='center')
            if(self.f == True):
                self.f = False
                self.run()

board = chess.Board()
g = guiMaker(True)