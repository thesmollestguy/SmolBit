# SmolBit Assembly Documentation

SmolBit is a low-level, character-based assembly language designed for a custom variable-length bitstream VM. It uses a unique memory model and a concise instruction set where single characters represent complex operations.

---

## 1. Memory Architecture
* **Pages**: The VM features 8 memory pages (Page 0–7).
* **Registers**: Each page contains 16 registers (0–f).
* **Global Register**: Register `f` is mirrored across all pages; changing it on Page 0 changes it on all others.
* **Data**: Values are stored as 32-bit unsigned integers.

---

## 2. Basic Instructions

### Page Selection
To switch the active memory page, use the corresponding character:
| Page 0 | Page 1 | Page 2 | Page 3 | Page 4 | Page 5 | Page 6 | Page 7 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `PG1` | `PG2` | `PG3` | `PG4` | `PG5` | `PG6` | `PG7` | `PG8` |

### Manipulation
Format: `[Instruction][Register]` (e.g., `INC 0` increments register 0).
* `INC` : Increment register value.
* `DEC` : Decrement register value.
* `CLZ` : Clear register to 0.
* `CLI` : Reset register to its initial value (its own address index).

### Arithmetic
Format: `[Instruction][Dest Register][Src Register]` (e.g., `ADD 1 0` adds reg 1 to reg 0).
* `ADD` : Addition.
* `SUB` : Subtraction.
* `MUL` : Multiplication.
* `DIV` : Integer Division.
* `SET` : Assignment (Set Dest = Src).
* `POW` : Exponentiation.
* `ROT` : Root.
* `LDI` : Set Register to Immediate Byte. Format: `LDI [Reg] [Hex1][Hex2]` (Reads next 2 hex chars as an 8-bit value).

### Display & I/O
* `DPU [Reg]` : Display register as UTF-8 character.
* `DPD [Reg]` : Display register as Decimal.
* `DPH [Reg]` : Display register as Hex.
* `DPI [Byte]` : Display byte as UTF-8 character. (Also `DPI "[Text]"` for longer strings)
* `EXO` : Exit program (Success).
* `ERR` : Exit program (Error).
* `INH [Reg]` : Await Hex input from user and store in register.
* `IND [Reg]` : Await Decimal input from user and store in register.

---

## 3. Control Flow (Blocks)
All blocks must be closed with the `]` character. For readability, you may add `[` at the start of a block and it will not affect compilation.

### Comparisons (`%cond`)
Used in `IF` (If) and `WHL` (While) blocks:
* `=` : Equal (`==`).
* `<` : Less than or Equal (`<=`).
* `>` : Greater than or Equal (`>=`).
* `!` : Not Equal (`!=`).

### Control Structures
* **If**: `IF [RegA] [Cond] [RegB] ... ]` - Executes block if condition is true.
* **While**: `WHL [RegA] [Cond] [RegB] ... ]` - Loops while condition is true.
* **Repeat**: `REP [HexCount] ... ]` - Repeats block a fixed number of times (0-f).
* **For**: `FOR [Reg] [Byte] ... ]` - Repeats Byte times, each iteration stores iteration number (starting at 0) in Reg
* **For**: `VFR [Reg] [Reg] ... ]` - Repeats Reg times, each iteration stores iteration number (starting at 0) in Reg

### Functions
* **Define**: `DEF [HexID] ... ]` - Stores a block of code with a 4-bit identifier (0-f).
* **Call**: `CLL [HexID]` - Executes the previously defined function.
* **Undefine**: `UDF [HexID]` - Clears the function definition.

---

## 4. Syntax & Comments
* **Comments**: Anything between semicolons is ignored (e.g., `; comment ;`).
* **Literals**: Hexadecimal characters `0-f` are used for register addresses and immediate counts.
* **Formatting**: Brackets `(` and `)` can be used for visual organization but are stripped before compilation. `[`, `{`, and `}` will also be stripped before compilation.