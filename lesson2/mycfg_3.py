import json # to load the json library
import sys  # to read input from keyword

#used has keys to  end the each block of info
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
            yield curr_block	# To print the curr_block
            curr_block = []

    # last block
    if curr_block:
        yield curr_block

def block_map(blocks):
  print("block_map\n")
  out = {}

# to print the block name before instruction
# if the label is present use
# else provided the numberic block name
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
	prog = json.load(sys.stdin) # stdin to read the input from pipe , json.load -> to read the json format provided has input
	for func in prog['functions']:
		name2block =  block_map(form_block(func ['instrs']))
		for name, block  in name2block.items():
			print(f" Block {name}: ")
			for instrs in block:
			    print(" ", instrs)
			print()

if __name__ == "__main__": # optional even directly call the functions you want to run
    mycfg()
