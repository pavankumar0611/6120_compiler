import sys
import json

data = json.load(sys.stdin)

temporary_state = {} # temporary to check and add to list if does 
expr_table = {} # expr table to keep track of variable

#If the variable is read
# create a key like hash 
# if key exists use the same thing
# else add to expr_table and add to temporary
# return the new instr ( optimized function instr block )
for func in data["functions"]:
    new_instrs = []

    for instr in func["instrs"]:
        op = instr.get("op")

        if op == "const":
            var = instr["dest"]
            value = instr["value"]

            key = ("const", value) # to store the info in hash format 

			# if the variable/ expr exists in expr_table 
			# make use of it 
			# else add to tbale and use the same key return to store in expr_table
            if key in expr_table:
                temporary_state[var] = expr_table[key]
                continue
            else:
                expr_table[key] = var
                temporary_state[var] = var
                new_instrs.append(instr)


        elif op == "id":
           var = instr["dest"]
           args =  instr["args"][0]
           id_value = temporary_state.get(args , args)
           temporary_state[var] = id_value

           instr["args"] = id_value
           new_instrs.append(instr)


        elif op == "print":
            instr["args"] = [temporary_state.get(a, a) for a in instr["args"]]
            new_instrs.append(instr)

		# to handle the assignment variables
        elif "args" in instr:
            var = instr["dest"]
            args = instr["args"]

			# using get function 
			# if it exists use it else add the new element later
            new_args = [temporary_state.get(a, a) for a in args]

            if op in ["add", "mul"]:
                key = (op, tuple(sorted(new_args))) # if we sort then we are achieving commutative property for add , mul operation
                instr["args"] = list(key[1])
            else:
                key = (op, tuple(new_args))
                instr["args"] = new_args

            if key in expr_table:
                temporary_state[var] = expr_table[key]
                continue
            else:
                expr_table[key] = var
                temporary_state[var] = var
                new_instrs.append(instr)

    func["instrs"] = new_instrs


def print_bril(data):
    for func in data["functions"]:
        print(f"@{func.get('name', 'main')} {{")
        for instr in func["instrs"]:
            if instr["op"] == "const":
                print(f"  {instr['dest']}: int = const {instr['value']};")
            elif instr["op"] == "print":
                print(f"  print {' '.join(instr['args'])};")
            else:
                print(f"  {instr['dest']}: int = {instr['op']} {' '.join(instr['args'])};")
        print("}")

print_bril(data)
