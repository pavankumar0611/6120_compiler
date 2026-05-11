import sys
import json

data = json.load(sys.stdin)

table = []
temporary_state = {}   # var -> canonical var
expr_table = {}        # expression -> canonical var
const_values = {}      # var -> actual constant value

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
                const_values[var] = value

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

            # replace args with duplicate  variables if present
			# using get for safe purpose .. get ( key , default )
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

                updated_args = []

                # copy propagation logic
                # before adding the row check add/sub arguments are int( add a , b)
                # then check for folding the expr, if folding is true add the new column
                # then do the compile time work and save has const value in table
                # before adding const value check if it exist , yes means reuse
                #else calculate
                for a in new_args:
                   if a in const_values:
                       updated_args.append(const_values[a])
                   else:
                       updated_args.append(a)

                new_args = updated_args 
            folded = False
            result = None

            # all is built int function that check for all args in new one by one
            # isinstance( x, int( checks whether value is integer
            # all() function collects these result and returns true if all arguments are int
            # else false
            if all(isinstance(x, int) for x in new_args):
             # using all to check if both parameters in add/sub are int
                if op == "add":
                    result = new_args[0] + new_args[1]
                elif op == "mul":
                    result = new_args[0] * new_args[1]
                elif op == "sub":
                    result = new_args[0] - new_args[1]
                elif op == "div":
                    result = new_args[0] // new_args[1]
                else:
                    result = None

                if result is not None:
                    folded = True

                    key = ("const", result)


                    if key in expr_table:
                        existing_var = expr_table[key]
                        temporary_state[var] = existing_var
                    else:
                        expr_table[key] = var
                        const_values[var] = result
                        temporary_state[var] = var

                        table.append((sl_no, result, "const", var))
                        sl_no += 1

                continue

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
