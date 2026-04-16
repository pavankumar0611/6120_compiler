# Bril CFG Block-by-Block Printer

This project contains a Python script that reads Bril programs (in JSON form) and prints their information **block by block**. It is useful for understanding control flow structure and basic blocks in a Bril program.

---

## 📌 Description

The script processes Bril input (converted to JSON using `bril2json`) and:

- Splits the program into **basic blocks**
- Prints each block separately
- Displays instructions inside each block in a structured way

This helps in:
- Control Flow Graph (CFG) construction
- Program analysis
- Debugging compiler passes

---

## ⚙️ Requirements

Make sure you have:

- Python 3 installed
- `bril2json` tool available (from the Bril toolchain)

---

## ▶️ How to Run

Use the following commands to run the script:

```bash
bril2json < combo.bril | python3 mycfg_3.py


FUNCTION form_block(body):

    curr_block = []

    FOR each instr in body:

        IF instr has 'label':
            IF curr_block is not empty:
                OUTPUT curr_block
            curr_block = [instr]
            CONTINUE

        ADD instr to curr_block

        IF instr has 'op' AND instr['op'] in (jmp, br, ret):
            OUTPUT curr_block
            curr_block = []

    IF curr_block is not empty:
        OUTPUT curr_block
```

