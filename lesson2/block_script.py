import json # to load the json library
import sys  # to read input from keyword

# used has keys to end each block of info
TERMINATORS = ('jmp', 'br', 'ret')


def form_block(body):

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
		
			continue

	# last block
	if curr_block:
		yield curr_block


def block_map(blocks):

	print("block_map\n")

	out = {}

	# to print the block name before instruction
	# if the label is present use
	# else provided the numeric block name
	for block in blocks:

		if "label" in block[0]:
			name = block[0]['label']
			block = block[1:]
		else:
			name = 'b{}'.format(len(out))

		out[name] = block

	return out


def build_cfg(name2block):

	graph = {}

	# initialize graph
	for name in name2block:
		graph[name] = []

	for name, block in name2block.items():

		# find last instruction in block
		if not block:
			continue

		last = block[-1]

		if 'op' not in last:
			continue

		op = last['op']

		# CASE 1: conditional branch
		if op == 'br':
			graph[name].append(last['labels'][0])
			graph[name].append(last['labels'][1])

		# CASE 2: jump
		elif op == 'jmp':
			graph[name].append(last['labels'][0])

		# CASE 3: return → no edges
		elif op == 'ret':
			pass

	return graph


def build_predecessors(graph):

	pred = {}

	# initialize all nodes
	for node in graph:
		pred[node] = []

	# reverse edges
	for src, dests in graph.items():

		for dst in dests:

			if dst not in pred:
				pred[dst] = []

			pred[dst].append(src)

	return pred


def print_successors(graph):

	print("\nSuccessors")

	for block, succs in graph.items():

		if succs:
			print(f"{block}: {', '.join(succs)}")
		else:
			print(f"{block}: none")


def print_predecessors(pred):

	print("\nPredecessors")

	for block, preds in pred.items():

		if preds:
			print(f"{block}: {', '.join(preds)}")
		else:
			print(f"{block}: none")


def mycfg():

	prog = json.load(sys.stdin) # stdin to read the input from pipe , json.load -> to read the json format provided has input

	for func in prog['functions']:

		name2block = block_map(form_block(func['instrs']))

		# print blocks
		for name, block in name2block.items():

			print(f"\nBlock {name}:")
			for instr in block:
				print(" ", instr)

		# build CFG
		graph = build_cfg(name2block)

		# build predecessors
		pred = build_predecessors(graph)

		# print results
		print_successors(graph)
		print_predecessors(pred)


if __name__ == "__main__":
	mycfg()
