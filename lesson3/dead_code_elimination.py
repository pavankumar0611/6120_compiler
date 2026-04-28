import json
import sys

TERMINATORS = ('jmp', 'br', 'ret')

#To diff part of instructions falling into each block
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


#to keep track on no of instructions in individual block
def count_instrs(prog):
    total = 0

    for func in prog['functions']:
        total = total + len(func['instrs'])

    return total

#Function to deduce the code to improve speed
def optimize_func(prog):
    prev_count = -1

	# Loop run till the instruction can be reduced further
    while True:
        mark_used_2(prog)
        delete_unused(prog)

		# To track the instructions to remove after opt
		# if the last count is equal to curr count exit
		#else run the loop for futher deduction
        curr_count = count_instrs(prog)

        if curr_count == prev_count:
            break

        prev_count = curr_count


# Function to mark  variable are used
#Used backwards to keep track of variable is used or not after defing
def mark_used_2(prog):
    for func in prog['functions']:

        live = set()

        for instr in reversed(func['instrs']):

            # If it is print we are using the variable , makr it has used and add to live
            if instr.get('op') == 'print':
                instr['used'] = True
                live.update(instr['args'])

            # For assignment variables , mark it has used and add to live
            elif 'dest' in instr:

                dest = instr['dest']

                if dest in live:
                    instr['used'] = True
                    live.remove(dest)
                    if 'args' in instr:
                        live.update(instr['args'])
                else:
                    instr['used'] = False


#Function to delete the instruction mark has not used 
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

        last_def = {}   # var -> instruction index
        to_delete = set()

        instrs = func['instrs']

        for i, instr in enumerate(instrs):		# Enumeration to keep track of instr and index to access it

            # CASE 1: variable is 'used' delete that instr from last_def
            if 'args' in instr:
                for var in instr['args']:
                    if var in last_def:
                        del last_def[var]

            # CASE 2: variable is DEFINED
            if 'dest' in instr:
                var = instr['dest']

                # if already re-defined then  → mark old last_def for delete
                if var in last_def:
                    to_delete.add(last_def[var])

                # update last definition to keep track of the actual instruction pointing
                last_def[var] = i

        # Loop to  delete instructions
        func['instrs'] = [
            instr for i, instr in enumerate(instrs)
            if i not in to_delete
        ]

if __name__ == "__main__":
    mycfg()
