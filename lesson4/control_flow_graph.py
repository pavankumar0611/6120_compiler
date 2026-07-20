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

        # preserve block order
        block_names = list(name2block.keys())

        for i, name in enumerate(block_names):

                block = name2block[name]

                # next block for fallthrough
                next_block = None
                if i + 1 < len(block_names):
                        next_block = block_names[i + 1]

                # empty block falls through
                                # b0 :
                                # b1 :
                                #       print x;
                if not block:
                        if next_block:
                                graph[name].append(next_block)
                        continue

                last = block[-1]

                # no op => fallthrough
                if 'op' not in last:
                        if next_block:
                                graph[name].append(next_block)
                        continue

                op = last['op']

                # branch
                if op == 'br':
                        graph[name].append(last['labels'][0])
                        graph[name].append(last['labels'][1])

                # jump
                elif op == 'jmp':
                        graph[name].append(last['labels'][0])

                # return
                elif op == 'ret':
                        pass

                # fallthrough
                else:
                        if next_block:
                                graph[name].append(next_block)

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


def printing_the_block(block_of_info):

        for key , value in block_of_info.items():
                print(key , "->" , value)

