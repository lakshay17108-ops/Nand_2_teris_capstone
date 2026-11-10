// Box.asm
// Capstone - Nand to Tetris I (ETCCNT301)
// Name: Lakshay    Roll No: 2501730367    K = 67
//
// Box size for my K:
//   starts at row K = 0
//   20 rows tall
//   width = 16 * ((K mod 4) + 1) = 16 * 1 = 16 pixels (1 word) from the left edge
//
// While any key is pressed the box is black, when the key is
// released the box is cleared (white).
//
// Row r starts at SCREEN + 32*r, so for K = 0 the first word is SCREEN itself.

(START)
    @color
    M=0             // default colour = white (no key)
    @KBD
    D=M
    @DRAW
    D;JEQ           // KBD = 0 -> no key, keep white
    @color
    M=-1            // key pressed -> black (all 16 bits set)

(DRAW)
    @SCREEN
    D=A
    @addr
    M=D             // addr = first word of row 0
    @20
    D=A
    @count
    M=D             // 20 rows to paint

(ROW)
    @color
    D=M
    @addr
    A=M
    M=D             // paint one word = 16 pixels of this row
    @32
    D=A
    @addr
    M=D+M           // move to the next row (+32 words)
    @count
    MD=M-1
    @ROW
    D;JGT           // more rows left?
    @START
    0;JMP           // check the keyboard again
