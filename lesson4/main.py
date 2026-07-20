import json # to load the json library
import sys  # to read input from keyword


from control_flow_graph  import *
from set_utilities import *
from definitions import *
from reaching_definitions import *

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


                                # collect all definitions from every block
                definitions = collect_definitions(name2block)

                # build reverse mapping
                reverse_mapped_list = reverse_mapping(definitions)

                print("\nprinting of gen of a block")
                gen = gen_of_function(definitions)
                printing_the_block(gen)


                print("\nprinting of kill of the block")
                kill = kill_of_function(gen , reverse_mapped_list , definitions)
                printing_the_block(kill)


                print("\n final answer\n")
                in_data , out_data = reaching_definitions(name2block , pred , gen , kill)

                print("\nFinal IN")
                for block , value in in_data.items():
                    print(block , "->" , value)

                print("\nFinal OUT")
                for block, value in out_data.items():
                    print(block , "->" , value)



if __name__ == "__main__":
        mycfg()
