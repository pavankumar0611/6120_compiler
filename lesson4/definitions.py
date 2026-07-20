#Function builds the all assignment/definition
#creates the def and stores block , variable name info
# Parameters:
#   name2block : Dictionary mapping block names to their instructions.
#
# Returns:
#   definitions : Dictionary mapping definition  (D1, D2, ...)
#                 to [variable, instruction, block_name].

def collect_definitions(name2block):

        definitions = {}

        count = 1

        # visit every block
        for block_name, block in name2block.items():

                # visit every instruction in the block
                for instr in block:

                        # a definition is any instruction with a destination
                        if "dest" in instr:

                                variable = instr["dest"]

                                print("D" + str(count), "defines", variable)

                                definitions["D" + str(count)] = [variable, instr , block_name]

                                count += 1

        # print all definitions
        for key, value in definitions.items():
                print(f"{key} {value}")

        return definitions


#Using definitions build by reaching defintion 
#it builds the reverse mapping
# ex : if variable a, b is passed 
#it lists of def... of passed variable
# Example:
#   a -> [D1, D5]
#   b -> [D2]
#
# Parameters:
#   definitions : Dictionary produced by collect_definitions().
#
# Returns:
#   variable_definitions : Dictionary mapping each variable
#                          to a list of its definition IDs.

def reverse_mapping(definitions):

                variable_definitions = {}

                for key , value in definitions.items():
                                if value[0] not in variable_definitions:
                                        variable_definitions[value[0]] = [key]
                                else:
                                        variable_definitions[value[0]].append(key)

                print("Reverse mapping")
                for key , value in variable_definitions.items():
                        print(F"{key}-> { value}")

                return variable_definitions
