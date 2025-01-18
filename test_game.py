import pytest
from Player import Player
from Board import Board

def test_player():
    p = Player("TestPlayer")
    assert p.name == "TestPlayer"
    assert p.score == 0
    p.add_score(10)
    assert p.get_score() == 10
    p.add_score(5)
    assert p.get_score() == 15

def test_board():
    board = Board(10, 4)

    with pytest.raises(ValueError, match='Only positive integers'):
        Board(0, 4)
    with pytest.raises(ValueError, match='Only positive integers'):
        Board(10, 0)

    assert board.layoutSize == 10;
    assert board.treasureNumber == 4;

def test_place_treasures():
    b = Board(10, 4)

    treasures = []
    for row in b.board:
        for item in row:
            if item != '_':
                treasures.append(item)

    assert len(set(treasures)) == 4, "Not all treasures are placed correctly"

    assert len(treasures) == sum(range(1, 5)), "Incorrect number of treasures placed"

def test_pick_treasure():
    b = Board(10, 4)

    with pytest.raises(IndexError, match='Invalid Points, Does not exists'):
        b.pick(-1, 0)
    with pytest.raises(IndexError, match='Invalid Points, Does not exists'):
        b.pick(0, 11)

    assert b.pick(0, 0) is None;  # Assuming (0,0) is initially empty


