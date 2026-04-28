import json
import sys

TERMINATORS = ('jmp', 'br', 'ret')

def form_block(body):
    print("form_map\n")
    curr_block = []

    for instr in body:

        # CASE 1: label → start new block
        if 'label' in instr:
            if curr_block:
                yield curr_block
            curr_block = [instr]
            continue

        # CASE 2: normal instruction
        curr_block.append(instr)

        # CASE 3: terminator → end block
        if 'op' in instr and instr['op'] in TERMINATORS:
            yield curr_block
            curr_block = []

    # last block
    if curr_block:
        yield curr_block

def block_map(blocks):
  print("block_map\n")
  out = {}

  for block in blocks:
       print("block_map loop\n")
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

    for func in prog['functions']:
        name2block = block_map(form_block(func['instrs']))

        for name, block in name2block.items():
            print(f"\n===== Block {name} =====")

            for i, instr in enumerate(block):
                op = instr.get("op", "")
                dest = instr.get("dest", "")
                args = instr.get("args", [])
                used = instr.get("used", "")

                print(f"{i}: op={op}, dest={dest}, args={args}, used={used}")




def count_instrs(prog):
    total = 0

    for func in prog['functions']:
        total = total + len(func['instrs'])

    return total

def find_reassigned_vars(prog):
    reassigned = set()

    for func in prog['functions']:

        prev_dest = None

        for instr in func['instrs']:

            if 'dest' not in instr:
                prev_dest = None
                continue

            curr = instr['dest']

            # currently only for deleting the consecutive variable present
            if curr == prev_dest:
                reassigned.add(curr)

            prev_dest = curr

    return reassigned

def optimize_func(prog):
    print("optimized block\n")

    prev_count = -1

    while True:
        reassigned = find_reassigned_vars(prog)
        mark_used(prog)
        delete_unused(prog)

        curr_count = count_instrs(prog)

        if curr_count == prev_count:
	        break

        prev_count = curr_count

    print(reassigned)

#function to mark instruction used or not
def mark_used(prog):
    for func in prog['functions']:
        used_vars = set()
        reassigned = find_reassigned_vars(prog)

        last_seen = set()

        # collect used variables
        for instr in func['instrs']:
            if 'args' in instr:
                used_vars.update(instr['args'])

        for instr in func['instrs']:

            if instr.get('op') == 'print':
                instr['used'] = True
                continue

            if 'dest' in instr:

                d = instr['dest']

                # for handling  consecutive reassignment
                if d in reassigned:
                    if d in last_seen:
                        instr['used'] = False   # first occurrence → delete
                    else:
                        instr['used'] = True    # second occurrence → keep
                        last_seen.add(d)

                # normal rule for deleting the unused variable
                elif d in used_vars:
                    instr['used'] = True
                else:
                    instr['used'] = False

            else:
                instr['used'] = False

#Functions to delete unused insturction
def delete_unused(prog):
    for func in prog['functions']:
        func['instrs'] = [
            instr for instr in func['instrs']
            if instr['used']]


if __name__ == "__main__":
    mycfg()
