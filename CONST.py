POSITIONS = [
                        (0, 5),
                    (1, 4), (1, 6),
                (2, 3), (2, 5), (2, 7),
            (3, 2), (3, 4), (3, 6), (3, 8),
        (4, 1), (4, 3), (4, 5), (4, 7), (4, 9),
    (5, 0), (5, 2), (5, 4), (5, 6), (5, 8), (5, 10),
        (6, 1), (6, 3), (6, 5), (6, 7), (6, 9),
    (7, 0), (7, 2), (7, 4), (7, 6), (7, 8), (7, 10),
        (8, 1), (8, 3), (8, 5), (8, 7), (8, 9),
    (9, 0), (9, 2), (9, 4), (9, 6), (9, 8), (9, 10),
        (10, 1), (10, 3), (10, 5), (10, 7), (10, 9),
    (11, 0), (11, 2), (11, 4), (11, 6), (11, 8), (11, 10),
        (12, 1), (12, 3), (12, 5), (12, 7), (12, 9),
    (13, 0), (13, 2), (13, 4), (13, 6), (13, 8), (13, 10),
        (14, 1), (14, 3), (14, 5), (14, 7), (14, 9),
    (15, 0), (15, 2), (15, 4), (15, 6), (15, 8), (15, 10),
        (16, 1), (16, 3), (16, 5), (16, 7), (16, 9), 
            (17, 2), (17, 4), (17, 6), (17, 8),
                (18, 3), (18, 5), (18, 7), 
                    (19, 4), (19, 6),
                        (20, 5)
]

POS_IDX = {pos: idx for idx, pos in enumerate(POSITIONS)}

PAWN_PROMOTION_HEXAGONS = [(5,0), (4,1), (3,2), (2,3), (1,4), (0,5), (1,6),
                         (2,7), (3,8), (4,9), (5,10),
                         (15,0), (16,1), (17,2), (18,3), (19,4), (20,5), (19,6),
                         (18,7), (17,8), (16,9), (15,10)]
                                        
DEPTH = 0
MOVE_LIMIT = 20
