import sys
import json

data = json.load(sys.stdin)

table = []
temporary_state = {}   # var -> canonical var
expr_table = {}        # expression -> canonical var

sl_no = 1

for func in data["functions"]:
    for instr in func["instrs"]:

        op = instr.get("op")

        # logic to deal with CONST arguments
        if op == "const":
            var = instr["dest"]
            value = instr["value"]

            key = ("const", value)

            if key in expr_table:
                #if its is already present in the table  reuse existing constant
                temporary_state[var] = expr_table[key]
            else:
                expr_table[key] = var
                temporary_state[var] = var

                table.append((sl_no, value, "const", var))
                sl_no += 1

        # for print variable we just need to skip because we are using no need to maintain any info in table
        elif op == "print":
            continue

        elif op == "id":
           var = instr["dest"]
           args = instr["args"][0]

           id_value = temporary_state.get(args , args)
           temporary_state[var] = id_value

           table.append((sl_no, id_value , op , var))
           sl_no += 1
        # to maintain binary operation(add, mul,sub , div  etc.)
        elif "args" in instr:
            var = instr["dest"]
            args = instr["args"]

            #  replace args with duplicate  variables if present
			#  using get for safe purpose .. get ( key , default )
			# if the key is present return the value from the table else return default
			# example : int a = 5 , b = 5   then b will point to a since same value
            new_args =  [temporary_state.get(a, a) for a in args]

            # for commutative we sort things ex : a * b is same has b * a ...
            if op in ["add", "mul"]:
                key = (op, tuple(sorted(new_args)))
            else:
                key = (op, tuple(new_args))

            if key in expr_table:
                # if the expr is present reuse the same expression
                existing_var = expr_table[key]
                temporary_state[var] = existing_var

            else:
                expr_table[key] = var
                temporary_state[var] = var

                table.append((sl_no, "".join(new_args), op, var))
                sl_no += 1

        else:
            continue


# for printing the table with format
print("\nLVN Table:\n")
print("{:<6} {:<15} {:<15} {:<10}".format("SL No", "Value", "Meaning", "Variable"))

for row in table:
    print("{:<6} {:<15} {:<15} {:<10}".format(*row))


# PRINT FINAL MAPPING
print("Final Variable Mapping for understading\n")
for key, value in temporary_state.items():
    print(f"{key} -> {value}")
