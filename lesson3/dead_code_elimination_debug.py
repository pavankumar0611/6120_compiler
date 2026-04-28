import json
import sys

TERMINATORS = ('jmp', 'br', 'ret')

def form_block(body):
    curr_block = []

    for instr in body:

        if 'label' in instr:
            if curr_block:
                yield curr_block
            curr_block = [instr]
            continue

        curr_block.append(instr)

        if 'op' in instr and instr['op'] in TERMINATORS:
            yield curr_block
            curr_block = []

    if curr_block:
        yield curr_block


def block_map(blocks):
    out = {}

    for block in blocks:
        if "label" in block[0]:
            name = block[0]['label']
            block = block[1:]
        else:
            name = 'b{}'.format(len(out))

        out[name] = block

    return out


def mycfg():
    prog = json.load(sys.stdin)

    optimize_func(prog)
    remove_reassigned(prog)
    # Function to print in bril format 
    print_bril(prog)


def count_instrs(prog):
    total = 0

    for func in prog['functions']:
        total = total + len(func['instrs'])

    return total


def optimize_func(prog):
    prev_count = -1

    while True:
        mark_used(prog)
        delete_unused(prog)

        curr_count = count_instrs(prog)

        if curr_count == prev_count:
            break

        prev_count = curr_count


# Function to mark variable has used or not in per block
def mark_used(prog):
    for func in prog['functions']:

        live = set()

        for instr in reversed(func['instrs']):

            # PRINT: its args are live
            if instr.get('op') == 'print':
                instr['used'] = True
                live.update(instr['args'])

            # ASSIGNMENT
            elif 'dest' in instr:

                dest = instr['dest']

                if dest in live:
                    instr['used'] = True
                    live.remove(dest)
                    if 'args' in instr:
                        live.update(instr['args'])
                else:
                    instr['used'] = False

def delete_unused(prog):
    for func in prog['functions']:
        func['instrs'] = [
            instr for instr in func['instrs']
            if instr['used']
        ]


# for printing in bril format 
def print_bril(prog):
    for func in prog['functions']:
        print(f"@{func['name']} {{")

        for instr in func['instrs']:

            if 'label' in instr:
                print(f"{instr['label']}:")
                continue

            op = instr.get('op')

            if op == 'print':
                args = " ".join(instr.get('args', []))
                print(f"  print {args};")
                continue

            dest = instr.get('dest')
            typ = instr.get('type')
            args = " ".join(instr.get('args', []))
            value = instr.get('value')

            if op == 'const':
                print(f"  {dest}: {typ} = const {value};")
            else:
                print(f"  {dest}: {typ} = {op} {args};")

        print("}")

# for removing the reassigned variables 
def remove_reassigned(prog):
    for func in prog['functions']:

        print("\n=== NEW FUNCTION ===")

        last_def = {}   # var -> instruction index
        to_delete = set()

        instrs = func['instrs']

        for i, instr in enumerate(instrs):

            print(f"\nProcessing instr {i}: {instr}")
            print(f"Current last_def: {last_def}")

            # CASE 1: checking for variable is used 
            if 'args' in instr:
                for var in instr['args']:
                    if var in last_def:
                        print(f"  USE of {var} → removing from last_def")
                        del last_def[var]

            # CASE 2: variable is defined
            if 'dest' in instr:
                var = instr['dest']

                print(f"  DEF of {var}")

                # if already defined and not used → delete old one
                if var in last_def:
                    print(f"  {var} redefined → marking old instr {last_def[var]} for deletion")
                    to_delete.add(last_def[var])

                # update last definition to keep track to delete the proper instr and point to new one
                last_def[var] = i
                print(f"  Updating last_def[{var}] = {i}")

            print(f"Updated last_def: {last_def}")

        print(f"\nInstructions to delete: {to_delete}")

        # delete instructions
        func['instrs'] = [
            instr for i, instr in enumerate(instrs)
            if i not in to_delete
        ]

        print("\nAfter deletion:")
        for instr in func['instrs']:
            print(instr)

if __name__ == "__main__":
    mycfg()
