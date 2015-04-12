// Rushy Panchal
// senior-focus.js
// Client-side library for my Senior Focus project

var TRANSITION_END ="transitionend webkitTransitionEnd oTransitionEnd otransitionend MSTransitionEnd";

function initializeFocus() {
	// Main function
	socket.create();
	board.create(8, 8);
	resizeGameTiles();
	}

function resizeGameTiles() {
	// Resize all of the game tiles to fit all 8 inside the board
	$board = $("#board");
	var boardWidth = $board.width();
	var tileSize = boardWidth / 8;
	$('.board-tile').css('width', tileSize).css('height', tileSize);
	$board.css('margin-left', $(window).width() / 4); // NOT WORKING: attempt to move the board to center it exactly
	}

function toggleInterface(elem) {
	// Toggle the element
	$elem = $(elem);
	if ($elem.css('display') == 'none') {
		$elem.slideDown();
		}
	else {
		$elem.slideUp();
		}
	}

var socket = {
	conn: null,
	create: function(settings) {
		// create the socket connection here
		}
	};



var board = {
	rawPieces: {
		black: document.createElement("p"),
		red: document.createElement("p"),
		blackKing: document.createElement("p"),
		redKing: document.createElement("p")
		},
	pieces: { // first index is height, second is width
		},
	workingMove: [],
	create: function(height, width) {
		// Create the game board
		var board = this;
		var gameBoard = $("#board");

		for (h = 0; h < height; h++) {
			var row = document.createElement("div");
			row.className = "board-row";
			var rowArray = board.pieces[h] = {};

			for (w = 0; w < width; w++) {
				var tile = document.createElement("div");
				tile.className = "board-tile";

				var tileData = tile.dataset;
				tileData["y"] = h;
				tileData["x"] = w;

				row.appendChild(tile);
				rowArray[w] = tile;

				(function(t) { // this has to be an explicit function or otherwise, each .click event handler is the same
					$(t).click(function() {
						var $t = $(this);
						var location = [this.dataset.y, this.dataset.x];
						var locationString = location.toString();
						if ($t.hasClass("active")) {
							// Remove the current activation if already activated
							$t.removeClass("active");
							board.workingMove.forEach(function (elem, index) {
								if (elem.toString() == locationString) { // it is easiest to match arrays as strings
									board.workingMove.splice(index, 1);
									}
								});
							}
						else { // because it's not currently active, activate the tile
							$t.addClass("active");
							board.workingMove.push(location);
							}
						});
					}(tile));
				}
			gameBoard.append(row);
			gameBoard.append(document.createElement("br"));
			}
		this.init(height, width);
		},
	init: function(height, width) {
		// Initialize the game board
		this.rawPieces.black.className = "game-piece black";
		this.rawPieces.red.className = "game-piece red";
		this.rawPieces.blackKing.className = "game-piece black king";
		this.rawPieces.redKing.className = "game-piece red king";

		var lastRow = height - 1,
			secondLastRow = height - 2,
			thirdLastRow = height - 3;

		for (h = 0; h < height; h++) {
			for (w = 0; w < height; w++) {
				var isEven = w % 2 == 0,
					toAdd = null;
				if (((h == 0 || h == 2) && ! isEven) || (h == 1 && isEven)) {
					toAdd = this.rawPieces.black;
					}
				else if (((h == thirdLastRow || h == lastRow) && isEven) || (h == secondLastRow && ! isEven)) {
					toAdd= this.rawPieces.red;
					}
				if (toAdd) {
					this.pieces[h][w].appendChild(toAdd.cloneNode());
					}
				}
			}
		},
	submit: function() {
		// Submit the game move
		$('.board-tile').removeClass("active");
		console.log(this.workingMove.toString());
		this.workingMove = [];
		},
	getTile: function(location) {
		// Get the tile at the given location
		return $(this.pieces[location[0]][location[1]]);
		},
	changePiece: function(location, callback, animate) {
		var tile = this.getTile(location);
		var piece = tile.children('.game-piece');
		if (animate != false) {
			piece.addClass("changing").on(TRANSITION_END, 
				function() {
					callback(piece);
					piece.removeClass('changing');
					});
			}
		else {
			callback(piece);
			}
		},
	upgradePiece: function(location, callback, animate) {
		// Upgrade a given piece
		return this.changePiece(location, function(piece) {
			piece.addClass("king");
			if (callback) callback(piece);
			}, animate);
		},
	killPiece: function(location, callback, animate) {
		// Kill a piece
		return this.changePiece(location, function(piece) {
			piece.remove();
			if (callback) callback(piece);
			}, animate);
		},
	movePiece: function(location, newLocation, callback, animate) {
		var board = this;
		return this.changePiece(location, function(piece) {
			piece.remove();
			board.getTile(newLocation).append(piece);
			if (callback) callback(piece);
			}, animate);
		},
	simpleMove: function(move) {
		/* Perform a simple move
		move[0] is the current location, and
		move[1] is the new location
		*/
		return this.movePiece(move[0], move[1]);
		},
	takeMove: function(move) {
		/* Perform a "take" move
		move[0] is the list of moves taken, and
		move[1] is a list of pieces taken
		*/
		var	moves = move[0],
			taken = move[1];

		this.movePiece(moves[0], moves[moves.length - 1]);

		for (index = 0; index < taken.length -1 ; index++) {
			console.log(index);
			console.log(taken[index]);
			// this.getTile(taken[index]).children('.game-piece').remove();
			this.killPiece(taken[index], null, false);
			}
		}
	}

function test() {
	board.movePiece([5, 2], [3, 2]);
	board.movePiece([6, 3], [5, 2]);
	board.takeMove([[[2, 3], [4, 1], [6, 3]], [[3, 2], [5, 2]]]);
	}

var players = {
	allPlayers: {},
	toggleDown: 'ion-ios7-arrow-thin-up',
	toggleUp: 'ion-ios7-arrow-thin-down',
	toggle: function() {
		// Toggle the list of players
		var players = this;
		$("#online-players-list").slideToggle(function() {
			$toggler = $("#player-list-toggler");
			if ($toggler.hasClass(players.toggleUp)) {
				$toggler.removeClass(players.toggleUp).addClass(players.toggleDown);
				}
			else {
				$toggler.removeClass(players.toggleDown).addClass(players.toggleUp);
				}
			});
		},
	add: function(name) {
		// Add to the list of players
		var player = document.createElement("li");
		player.innerHTML = name;
		player.className = "online-player";
		$("#online-players-list").append(player);
		this.allPlayers[name] = player;
		},
	remove: function(name) {
		// Remove from the list of players
		if (name in this.allPlayers) {
			$(this.allPlayers[name]).remove();
			delete this.allPlayers[name];
			}
		}
	};

var modal = {
	open: function(id) {
		// Open a modal
		$(id).addClass("active").on(TRANSITION_END, function() {
			$(this).css("display", "block");
			});
		},
	close: function(id) {
		// Close a modal
		$(id).removeClass("active").on(TRANSITION_END, function() {
			$(this).css("display", "none");
			});
		}
	}

$(document).ready(initializeFocus);
$(window).resize(resizeGameTiles);