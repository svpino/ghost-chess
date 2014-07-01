import sys, json

PIECE_PAWN = 0
PIECE_KING = 1
PIECE_BISHOP = 2
PIECE_ROOK = 3
PIECE_KNIGHT = 4
PIECE_QUEEN = 5

answers = []
board = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]

pieces = []

pieces.append({  
	"id": PIECE_PAWN,
	"movement": [[1, 1], [-1, 1], [-1, -1], [1, -1]],
	"ifNoDiscard": [PIECE_QUEEN, PIECE_KING, PIECE_BISHOP],
	"ifYesDiscard": [PIECE_KNIGHT]
});

pieces.append({  
	"id": PIECE_KING,
	"movement": [[1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1], [1, 0]],
	"ifNoDiscard": [PIECE_QUEEN],
	"ifYesDiscard": [PIECE_KNIGHT, PIECE_PAWN]
});

pieces.append({  
	"id": PIECE_BISHOP,
	"movement": [[1, 1], [-1, 1], [-1, -1], [1, -1], [2, 2], [-2, 2], [-2, -2], [2, -2], [3, 3], [-3, 3], [-3, -3], [3, -3], [4, 4], [-4, 4], [-4, -4], [4, -4], [5, 5], [-5, 5], [-5, -5], [5, -5], [6, 6], [-6, 6], [-6, -6], [6, -6], [7, 7], [-7, 7], [-7, -7], [7, -7]],
	"ifNoDiscard": [PIECE_QUEEN],
	"ifYesDiscard": [PIECE_KNIGHT, PIECE_PAWN]
});

pieces.append({  
	"id": PIECE_ROOK,
	"movement": [[0, 1], [-1, 0], [0, -1], [1, 0], [0, 2], [-2, 0], [0, -2], [2, 0], [0, 3], [-3, 0], [0, -3], [3, 0], [0, 4], [-4, 0], [0, -4], [4, 0], [0, 5], [-5, 0], [0, -5], [5, 0], [0, 6], [-6, 0], [0, -6], [6, 0], [0, 7], [-7, 0], [0, -7], [7, 0]],
	"ifNoDiscard": [PIECE_QUEEN],
	"ifYesDiscard": [PIECE_KNIGHT]
});

pieces.append({  
	"id": PIECE_KNIGHT,
	"movement": [[2, 1], [1, 2], [-1, 2], [-2, 1], [-2, -1], [-1, -2], [1, -2], [2, -1]],
	"ifNoDiscard": [],
	"ifYesDiscard": [PIECE_PAWN, PIECE_KING, PIECE_BISHOP, PIECE_ROOK, PIECE_QUEEN]
});

pieces.append({  
	"id": PIECE_QUEEN,
	"movement": [[1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1], [1, 0], [2, 2], [0, 2], [-2, 2], [-2, 0], [-2, -2], [0, -2], [2, -2], [2, 0], [3, 3], [0, 3], [-3, 3], [-3, 0], [-3, -3], [0, -3], [3, -3], [3, 0], [4, 4], [0, 4], [-4, 4], [-4, 0], [-4, -4], [0, -4], [4, -4], [4, 0], [5, 5], [0, 5], [-5, 5], [-5, 0], [-5, -5], [0, -5], [5, -5], [5, 0], [6, 6], [0, 6], [-6, 6], [-6, 0], [-6, -6], [0, -6], [6, -6], [6, 0], [7, 7], [0, 7], [-7, 7], [-7, 0], [-7, -7], [0, -7], [7, -7], [7, 0]],
	"ifNoDiscard": [],
	"ifYesDiscard": [PIECE_KNIGHT, PIECE_KING]
});

jsonData = json.loads(open(sys.argv[1]).read()) 
numberOfQueries = 0

def isAttacking(position, movement):
	row = (position - 1) / 8 + 1
	col = (position - 1) % 8 + 1

	newRow = row + movement[0]
	newCol = col + movement[1]

	if newRow >= 1 and newRow <= 8 and newCol >= 1 and newCol <= 8:
		item = query((newRow - 1) * 8 + newCol)
		if item != "X":
			return False

	return True	

def findOutWhatIsThisPiece(position):
	possiblePieces = [True, True, True, True, True, True]

	for piece in pieces:
		if possiblePieces[piece["id"]]:
			movementCount = 1
			totalMovements = len(piece["movement"])
			
			isThisPieceStillAPossibility = True
			while totalMovements - movementCount >= 0:
				movement = piece["movement"][movementCount - 1]
				if not isAttacking(position, movement):
					isThisPieceStillAPossibility = False
					break
				movementCount += 1

			if isThisPieceStillAPossibility:
				for i in piece["ifYesDiscard"]:
					possiblePieces[i] = False
			else:
				possiblePieces[piece["id"]] = False
				for i in piece["ifNoDiscard"]:
					possiblePieces[i] = False

	result = ""			
	if possiblePieces[0]:
		result = "Pawn"			
	elif possiblePieces[1]:	
		result = "King"
	elif possiblePieces[2]:	
		result = "Bishop"
	elif possiblePieces[3]:	
		result = "Rook"
	elif possiblePieces[4]:	
		result = "Knight"
	else:	
		result = "Queen"

	return {
		"position": position,
		"piece": result
	};		

def query(position):
	if board[position - 1] is None:
		board[position - 1] = jsonData["content"][position - 1]["value"]
		global numberOfQueries
		numberOfQueries += 1

	return board[position - 1]	

def start():
	totalPieces = jsonData["pieces"]
	position = 1;
	while len(answers) < totalPieces:
		board[position - 1] = jsonData["content"][position - 1]["value"]
		if board[position - 1] == "P":
			answers.append(findOutWhatIsThisPiece(position))

		position+=1


	print numberOfQueries, answers	


start()