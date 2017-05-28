from PIL import Image
import os

#PyChess
#A PNG based python engine for everyone.
#Developed by EncloCreations


class Chess:
    def __init__(self):
        self.imageObjects = {'bb': Image.open("Assets/bb.png").convert('RGBA')
            , 'bk': Image.open("Assets/bk.png").convert('RGBA')
            , 'bn': Image.open("Assets/bn.png").convert('RGBA')
            , 'bp': Image.open("Assets/bp.png").convert('RGBA')
            , 'bq': Image.open("Assets/bq.png").convert('RGBA')
            , 'br': Image.open("Assets/br.png").convert('RGBA')
            , 'wb': Image.open("Assets/wb.png").convert('RGBA')
            , 'wk': Image.open("Assets/wk.png").convert('RGBA')
            , 'wn': Image.open("Assets/wn.png").convert('RGBA')
            , 'wp': Image.open("Assets/wp.png").convert('RGBA')
            , 'wq': Image.open("Assets/wq.png").convert('RGBA')
            , 'wr': Image.open("Assets/wr.png").convert('RGBA')}

    def new_game(self, dir):
        return Game(self, self.imageObjects, dir)


class Game:
    def __init__(self, ctct, imo, directory):
        self.positions = {'br1': 'A8', 'bn1': 'B8', 'bb1': 'C8', 'bk': 'D8', 'bq': 'E8', 'bb2': 'F8', 'bn2': 'G8'
            , 'br2': 'H8', 'bp1': 'A7', 'bp2': 'B7', 'bp3': 'C7', 'bp4': 'D7', 'bp5': 'E7', 'bp6': 'F7', 'bp7': 'G7'
            , 'bp8': 'H7', 'wr1': 'H1', 'wn1': 'G1', 'wb1': 'F1', 'wk': 'E1', 'wq': 'D1', 'wb2': 'C1', 'wn2': 'B1'
            , 'wr2': 'A1', 'wp1': 'H2', 'wp2': 'G2', 'wp3': 'F2', 'wp4': 'E2', 'wp5': 'D2', 'wp6': 'C2', 'wp7': 'B2'
            ,'wp8': 'A2'}

        self.pieces = ['br1', 'bn1', 'bb1', 'bk', 'bq', 'bb2', 'bn2', 'br2', 'bp1', 'bp2', 'bp3', 'bp4', 'bp5', 'bp6'
            ,'bp7', 'bp8', 'wr1', 'wn1', 'wb1', 'wk', 'wq', 'wb2', 'wn2', 'wr2', 'wp1', 'wp2', 'wp3', 'wp4', 'wp5'
            ,'wp6', 'wp7', 'wp8']

        self.exactPositions = self.get_exact_positions()
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.dir = directory
        self.imo = imo
        self.ctct = ctct
        self.currentMove = 0
        self.raw = []
        self.rawType = []
        self.rawPieceType = []
        self.turn = 1
        self.cturn = "w"

    def get_exact_positions(self):
        letter_values = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8}
        return_statement = {}
        for i in self.pieces:
            return_statement[i] = ((letter_values[self.positions[i][0]] - 1) * 89 + 48, abs(int(self.positions[i][1]) - 8) * 89 + 49)
        return return_statement

    def get_raw(self):
        self.raw = []
        for i in self.pieces:
            self.raw.append(self.positions[i])
            self.rawType.append(i[0])
            self.rawPieceType.append(self.pieces[1])

    def render(self):
        bkg = Image.open("Assets/Chessboard.png").convert('RGBA')
        for i in self.pieces:
            fg = self.imo[i[0] + i[1]]
            bkg.paste(fg, (self.exactPositions[i][0], self.exactPositions[i][1]), fg)
        bkg.save(self.dir + str(self.currentMove) + ".png")

    def move(self, move):
        rp = 'null'
        sp = 0
        check = self.val(move)
        if check.startswith("Valid"):
            for n, i in self.positions.items():
                if i == move[0] + move[1]:
                    sp = n
                if i == move[3] + move[4]:
                    rp = n
            if rp == 'null':
                self.positions[sp] = move[3] + move[4]
            elif rp != 'null':
                self.positions.pop(rp)
                self.pieces.pop(self.pieces.index(rp))
                self.positions[sp] = move[3] + move[4]
            self.currentMove += 1
            self.exactPositions = self.get_exact_positions()
            self.render()
            return check
        elif check.startswith("Invalid"):
            return check
        self.turn *= -1
        if self.turn == 1:
            self.cturn = "w"
        else:
            self.cturn = "b"

    def val(self, move):
        if self.get_type(move[0] + move[1]) != "null":
            return "Valid"
        else:
            return "Invalid: No piece in square " + move[0] + move[1]

    def get_type(self, coords):
        types = {"r": "Rook", "n": "Knight", "b": "Bishop", "k": "King", "q": "Queen", "p": "Pawn"}
        for n, i in self.positions.items():
            if i == coords:
                return types[n[1]]
        return "null"

    def get_cp(self, i, i2, sp):
        l = ("A", "B", "C", "D", "E", "F", "G", "H")
        cp = None
        if i == 0:
            cp = sp[0] + str(int(sp[1]) + i2)
        elif i == 1:
            cp = str(l.index(sp[0]) + i2) + str(int(sp[1]) + i2)
        elif i == 2:
            cp = str(l.index(sp[0]) + i2) + sp[1]
        elif i == 3:
            cp = str(l.index(sp[0]) + i2) + str(int(sp[1]) - i2)
        elif i == 4:
            cp = sp[0] + str(int(sp[1]) - i2)
        elif i == 5:
            cp = str(l.index(sp[0]) - i2) + str(int(sp[1]) - i2)
        elif i == 6:
            cp = str(l.index(sp[0]) - i2) + sp[1]
        elif i == 7:
            cp = str(l.index(sp[0]) - i2) + str(int(sp[1]) + i2)
        return cp

    def get_cp_k(self, i, sp):
        cp = None
        l = ("A", "B", "C", "D", "E", "F", "G", "H")
        if i == 1:
            cp = str(l.index(sp[0]) - 1) + str(int(sp[1]) + 2)
        elif i == 2:
            cp = str(l.index(sp[0]) + 1) + str(int(sp[1]) + 2)
        elif i == 3:
            cp = str(l.index(sp[0]) + 2) + str(int(sp[1]) + 1)
        elif i == 4:
            cp = str(l.index(sp[0]) + 2) + str(int(sp[1]) - 1)
        elif i == 5:
            cp = str(l.index(sp[0]) + 1) + str(int(sp[1]) - 2)
        elif i == 6:
            cp = str(l.index(sp[0]) - 1) + str(int(sp[1]) - 2)
        elif i == 7:
            cp = str(l.index(sp[0]) - 2) + str(int(sp[1]) - 1)
        elif i == 8:
            cp = str(l.index(sp[0]) - 2) + str(int(sp[1]) + 1)
        return cp

    def in_check(self, kp):
        for i in range(0, 7):
            for i2 in range(0, 7):
                cp = self.get_cp(i, i2, kp)
                if i % 2 == 0:
                    chk = ("q", "b")
                else:
                    chk = ("q", "r")
                if self.rawPieceType[self.raw.index(cp)] in chk:
                    return [True, self.raw.index(cp)]
        for i in range(0, 8):
            cp = self.get_cp_k(i, kp)
            if self.rawPieceType[self.raw.index(cp)] == "n":
                return [True, self.raw.index(cp)]
        return [False]

    def validate_move(self, ptype, sp, kp, move):
        vd = self.in_check(kp)
        if vd[0]:
            self.get_raw()
            ma = []
            s = False
            tm = {"Rook": (7, 0, 7, 0, 7, 0, 7, 0), "Knight": ((2, 1), 0, (2, 1), 0, (2, 1), 0, (2, 1)),
                             "Bishop": (0, 7, 0, 7, 0, 7, 0, 7), "King": (1, 1, 1, 1, 1, 1, 1, 1)
            ,"Queen": (7, 7, 7, 7, 7, 7, 7, 7), "Pawn": (1, 0, 0, 0, 0, 0, 0, 0, 0)}
            if ptype != "Knight":
                for i in range(0, 7):
                    for i2 in range(0, tm[ptype][i]):
                        cp = self.get_cp(i, i2, sp)
                        if cp in self.raw:
                            if self.rawType[self.raw.index(cp)] == self.cturn:
                                break
                            elif self.rawType[self.raw.index(cp)] != self.cturn:
                                ma.append(cp)
                                break
                        else:
                            ma.append(cp)
            else:
                for i in range(0, 8):
                    cp = self.get_cp_k(i, sp)
                    if cp in self.raw:
                        if self.rawType[self.raw.index(cp)] != self.cturn:
                            ma.append(cp)
                    else:
                        ma.append(cp)

            if move[3] + move[4] not in ma:
                return ["Invalid", "there's already a friendly piece at " + move[3] + move[4]]

            for i in range(0, 7):
                for i2 in range(0, 7):
                    cp = self.get_cp(i, i2, kp)
                    if cp != sp and not s:
                        break
                    elif s:
                        if i % 2 == 0:
                            chk = ("q", "b")
                        else:
                            chk = ("q", "r")
                        if self.rawPieceType[self.raw.index(cp)] in chk:
                            return ["Invalid", move + " puts self in check"]
                    else:
                        s = True
            return ["Valid"]
        else:
            pass


class Certificate:
    def __init__(self, validator, reason, end_game_move, end_reason, alert, game_finished):
        self.Validator = validator
        self.Alert = alert
        self.Reason = reason
        self.EndGameMove = end_game_move
        self.EndReason = end_reason
        self.GameFinished = game_finished

    def get_validator(self):
        if not self.Validator:
            return {"Validator": self.Validator, "Reason": self.Reason}
        else:
            return {"Validator": self.Validator, "Alert": self.Alert}

    def get_game_status_validator(self):
        if self.EndGameMove:
             return {"Validator": self.EndGameMove, "Reason": self.EndReason, "GameFinished": self.GameFinished}
        else:
            return {"Validator": False}

    def close(self):
        self.close()

myObject = Chess()
x = myObject.new_game("game1/")
print(x.move("A4 B4"))
