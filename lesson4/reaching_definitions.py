#This file used set utilities while computing IN and OUT 
from set_utilities import *

# The KILL set of a block contains definitions of variables that
# are invalidated (overwritten) by definitions generated in that block.
#
# Parameters:
#   gen              : Dictionary containing the GEN set for each block.
#   reverse_mapping  : Maps each variable to all of its definitions.
#   definitions      : Dictionary containing information about each definition.
#
# Returns:
#   kill : Dictionary containing the KILL set for every block.

def kill_of_function(gen , reverse_mapping, definitions):

        kill = { }

        for  block in gen:
                kill[block] = []

                # we get the variable name using the outer loop
				#Inner loops see if the  variable def.. belong to other block
				# if yes get added to kills else skips (since it belong
				# to the current block
                for definition_name in gen[block]:
                        variable = definitions[definition_name][0]

                        # add all definition of the variable and skip  the current defintion
                        for other_definition in reverse_mapping[variable]:
                                if other_definition == definition_name:
                                        continue

                        # TO kill add only  definitions from other blocks
                                if definitions[other_definition][2] != block:
                                        if other_definition not in kill[block]:
                                                kill[block].append(other_definition)

        return kill


# Computes the GEN set for every basic block.
#
# The GEN set contains the definitions that are generated in a block
# and reach the end of the block. If a variable is defined multiple
# times within the same block, only the last definition is kept.
#
# Parameters:
#   block_of_definition : Dictionary mapping each definition to its block
#
# Returns:
#   gen : Dictionary containing the GEN set for every block.
def gen_of_function(block_of_definition):

        gen = {}

        #outer loop is used to get the block_name and variable name
		# inner loops check the definition defined and add it 
		# if it redefined it removes the same
        for definition_name, value in block_of_definition.items():
                variable = value[0]
                block_name = value[2]

                if block_name not in gen:
                        gen[block_name] = []

                #remove the older definition of the same variable
                #already present in the current block

                for old_definition in gen[block_name][:]:
                        old_variable = block_of_definition[old_definition][0]

                        if old_variable == variable:
                                gen[block_name].remove(old_definition)

                #latest definition survives
                gen[block_name].append(definition_name)

        return gen

# Computes the IN set for every basic block.
#
# The IN set of a block is the union of the OUT sets of all
# its predecessor blocks.
#
# Formula:
#     IN[B] = Union of predecessors if present
def compute_in(pred , out_data):
        in_data  = {}

        for block in  pred:

                in_data[block] = []

                #union of OUT of all predecessors
                for predecessor in pred[block]:
                        in_data[block] = union_of_sets(in_data[block] , out_data[predecessor])

        return in_data


# Computes the OUT set (definitions that reach the end of each basic block).
# Formula:
#     OUT[B] = GEN[B] ∪ (IN[B] - KILL[B])
#
#First it Remove definitions from IN that are killed in the current block.
#Then  Add definitions generated in the current block.
def compute_out(gen , kill , in_data):

        out_data = {}

        for block in gen:

                # IN[BLOCK] - KILL[BLOCK]
                temp = difference_of_sets(in_data[block] , kill[block])


                # GEN[BLOCK] UNION (IN[B] - KILL[B])
                out_data[block] = union_of_sets(gen[block], temp)

        return out_data

# Initializes the IN and OUT sets for every basic block.
#
#in_data  : Dictionary where each block's IN set is initially empty.
#out_data : Dictionary where each block's OUT set is initially empty.
def initialize_in_out(name2block):
        in_data = {}
        out_data = {}

        for block in name2block:
                in_data[block] = []
                out_data[block] = []

        return in_data , out_data


# Performs the Reaching Definitions data-flow analysis.
#
# The algorithm repeatedly computes the IN and OUT sets for every
# basic block until no OUT set changes (fixed-point iteration).
#
# Parameters:
#   name2block : Dictionary of all basic blocks.
#   pred       : Dictionary mapping each block to its predecessors.
#   gen        : Dictionary containing GEN sets for each block.
#   kill       : Dictionary containing KILL sets for each block.
#
# Returns:
#   in_data  : Final IN sets for every block.
#   out_data : Final OUT sets for every block.
def reaching_definitions(name2block , pred , gen , kill):
		#Initialized in_data , out_data sets as empty
        in_data , out_data = initialize_in_out(name2block)

        changed = True

		#Loops runs until changes are deteced  in OUT sets
        while changed:
                changed = False

                new_in = compute_in(pred ,out_data)

                new_out = compute_out(gen , kill, new_in)

                #Check whether OUT is chnanged or not
                for  block in out_data:
                        if out_data[block] != new_out[block]:
                                changed = True
                                break

				#Updates in IN and OUT for next iteration
                in_data = new_in
                out_data = new_out

        return in_data , out_data

