---
categories:
    - Coding
---
# Bingo With Bitmasking

## What is bitmasking?

Bitmasking is a technique where you use bits and bitwise operations to efficiently store and manipulate sets of boolean (on/off, true/false) values. In the context of bingo, you can represent the state of the entire board (which cells are marked) as a single integer, where each bit corresponds to a cell on the board.

For example, in a 5x5 bingo board, you have 25 cells, so you can use a 25-bit integer. If a cell is marked, its corresponding bit is set to 1; otherwise, it's 0. This allows you to quickly check for completed rows, columns, or diagonals using bitwise operations.

**Advantages:**

- Fast checks for bingo lines (using AND, OR, etc.)
- Compact storage (just one integer for the whole board)
- Easy to manipulate and update

## How it works in bingo context?

We add bit to every cell of bingo board

```code
┏━━━┳━━━┳━━━┳━━━┳━━━┓
┃ 1 ┃ 0 ┃ 0 ┃ 0 ┃ 0 ┃
┣━━━╂━━━╂━━━╂━━━╂━━━┫
┃ 1 ┃ 1 ┃ 1 ┃ 0 ┃ 0 ┃
┣━━━╂━━━╂━━━╂━━━╂━━━┫
┃ 0 ┃ 0 ┃ 1 ┃ 0 ┃ 0 ┃
┣━━━╂━━━╂━━━╂━━━╂━━━┫
┃ 0 ┃ 0 ┃ 0 ┃ 1 ┃ 0 ┃
┣━━━╂━━━╂━━━╂━━━╂━━━┫
┃ 0 ┃ 0 ┃ 0 ┃ 0 ┃ 1 ┃
┗━━━┻━━━┻━━━┻━━━┻━━━┛
```

this way we can get 25 bits long binary
`1000011100001000001000001` or 17698881 in decimal.

If we want to check for example cell in [0,0] and check if it is part of any full bingo lines and in which direction, we can give the cell different bitmasks to check.

Let's have an example: Let's check if cell [0,0] is part of full horizontal line. Full horizontal line means that every bit in the first row is 1. So in binary format it is `1111100000000000000000000` or 32505856 in decimal. Let's use previous game state here. Let's check with bitwise AND (&) if there is a full horizontal line.

```javascript
(17698881 & 32505856) === 32505856
> false
```

Seems like it isn't. Let's update the game to other state.

```code
┏━━━┳━━━┳━━━┳━━━┳━━━┓
┃ 1 ┃ 1 ┃ 1 ┃ 1 ┃ 1 ┃
┣━━━╂━━━╂━━━╂━━━╂━━━┫
┃ 1 ┃ 1 ┃ 1 ┃ 0 ┃ 0 ┃
┣━━━╂━━━╂━━━╂━━━╂━━━┫
┃ 0 ┃ 0 ┃ 1 ┃ 0 ┃ 0 ┃
┣━━━╂━━━╂━━━╂━━━╂━━━┫
┃ 0 ┃ 0 ┃ 0 ┃ 1 ┃ 0 ┃
┣━━━╂━━━╂━━━╂━━━╂━━━┫
┃ 0 ┃ 0 ┃ 0 ┃ 0 ┃ 1 ┃
┗━━━┻━━━┻━━━┻━━━┻━━━┛
```

It is now `1111111100001000001000001` or 33427521.

```javascript
(33427521 & 32505856) === 32505856
> true
```

Now we know that there is full horizontal line. But hey! There's also diagonal line from [0,0] to [5,5]. Let's check that too. So just the diagonal line would be

```code
┏━━━┳━━━┳━━━┳━━━┳━━━┓
┃ 1 ┃ 0 ┃ 0 ┃ 0 ┃ 0 ┃
┣━━━╂━━━╂━━━╂━━━╂━━━┫
┃ 0 ┃ 1 ┃ 0 ┃ 0 ┃ 0 ┃
┣━━━╂━━━╂━━━╂━━━╂━━━┫
┃ 0 ┃ 0 ┃ 1 ┃ 0 ┃ 0 ┃
┣━━━╂━━━╂━━━╂━━━╂━━━┫
┃ 0 ┃ 0 ┃ 0 ┃ 1 ┃ 0 ┃
┣━━━╂━━━╂━━━╂━━━╂━━━┫
┃ 0 ┃ 0 ┃ 0 ┃ 0 ┃ 1 ┃
┗━━━┻━━━┻━━━┻━━━┻━━━┛
```

or `1000001000001000001000001` or 17043521.

The previous game state was 33427521.

```javascript
(33427521 & 17043521) === 17043521
> true
```

Wohoo! We can check the diagonal line too. Now we can implement the game. We give every cell information about the potential winning lines it can be part of. For the cell [0,0] that would be [horizontal, vertical, diagonal] or [32505856, 17318416, 17043521]. When we check the game state against these values, we can determine if there is a bingo.
