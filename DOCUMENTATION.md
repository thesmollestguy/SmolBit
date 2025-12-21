# SmolBit Assembly Documentation

SmolBit is a low-level, character-based assembly language designed for a custom variable-length bitstream VM. It uses a unique memory model and a concise instruction set where single characters represent complex operations.

---

## 1. Memory Architecture
* **Pages**: The VM features 8 memory pages (Page 0–7).
* **Registers**: Each page contains 16 registers (0–f).
* **Global Register**: Register `f` is mirrored across all pages; changing it on Page 0 changes it on all others.
* **Data**: Values are stored as 16-bit unsigned integers.

---

## 2. Basic Instructions

### Page Selection
To switch the active memory page, use the corresponding character:
| Page 0 | Page 1 | Page 2 | Page 3 | Page 4 | Page 5 | Page 6 | Page 7 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `@` | `A` | `B` | `C` | `X` | `Y` | `Z` | `&` |

### Manipulation
Format: `[Instruction][Register]` (e.g., `>0` increments register 0).
* `>` : Increment register value.
* `<` : Decrement register value.
* `_` : Clear register to 0.
* `~` : Reset register to its initial value (its own address index).

### Arithmetic
Format: `[Instruction][Dest Register][Src Register]` (e.g., `+01` adds reg 1 to reg 0).
* `+` : Addition.
* `-` : Subtraction.
* `*` : Multiplication.
* `/` : Integer Division.
* `=` : Assignment (Set Dest = Src).
* `^` : Exponentiation.
* `v` : Root.
* `#` : Set Register to Immediate Byte. Format: `# [Reg] [Hex1][Hex2]` (Reads next 2 hex chars as an 8-bit value).

### Display & I/O
* `| [Reg]` : Display register as Binary.
* `% [Reg]` : Display register as Decimal.
* `h [Reg]` : Display register as Hex.
* `u [Reg]` : Display register as UTF-8 character.
* `x` : Exit program (Success).
* `E` : Exit program (Error).
* `H [Reg]` : Await Hex input from user and store in register.
* `D [Reg]` : Await Decimal input from user and store in register.

---

## 3. Control Flow (Blocks)
All blocks must be closed with the `]` character. For readability, you may add `[` at the start of a block and it will not affect compilation.

### Comparisons (`%cond`)
Used in `?` (If) and `W` (While) blocks:
* `i` : Equal (`==`).
* `j` : Less than or Equal (`<=`).
* `k` : Greater than or Equal (`>=`).
* `l` : Not Equal (`!=`).

### Control Structures
* **If**: `? [RegA] [Cond] [RegB] ... ]` - Executes block if condition is true.
* **While**: `W [RegA] [Cond] [RegB] ... ]` - Loops while condition is true.
* **Repeat**: `R [HexCount] ... ]` - Repeats block a fixed number of times (0-f).
* **For**: `L [Mode: i/j] [Reg] [Val] ... ]` - Iterator loop. If mode is `i`, `Val` is a literal hex; if `j`, `Val` is a register address.

### Functions
* **Define**: `F [HexID] ... ]` - Stores a block of code with a 4-bit identifier (0-f).
* **Call**: `S [HexID]` - Executes the previously defined function.
* **Undefine**: `U [HexID]` - Clears the function definition.

---

## 4. Syntax & Comments
* **Comments**: Anything between semicolons is ignored (e.g., `; comment ;`).
* **Literals**: Hexadecimal characters `0-f` are used for register addresses and immediate counts.
* **Formatting**: Brackets `(` and `)` can be used for visual organization but are stripped during conversion.