#It check and add the variable defined two sets
#and creates the new set containg all the elements 
#that are present in two block
def union_of_sets(set1 , set2):
        result = []

		# Add all unique elements from the first set
        for value in set1:
                if value not in result:
                        result.append(value)

		# Adds elements from the second set that are not present
        for value in set2:
                if  value not in result:
                        result.append(value)

        return result

#It creates the defintions that are present/common 
#in the two sets
def intersection_of_sets(set1 , set2):
        result = []

		  # Check every element in the first set
        for value_1 in set1:
                Found = False
                for value_2 in set2:
                        if value_1 == value_2:
                                Found = True
                                break

				 # Add the element if it exists in both sets
                if Found is True:
                        if value_1 not in result:
                                result.append(value_1)

        return result


# The resulting list contains elements that are present in
# set1 but not in set2.
def difference_of_sets(set1 , set2):
        result = []

        for value_1 in set1:
                Found = False
				# Determine whether the element exists in the second set
                for value_2 in set2:
                        if value_1 == value_2:
                                Found = True
                                break

				# Keep only elements that are not present in set2
                if Found is False:
                        if value_1 not in result:
                                result.append(value_1)

        return result
