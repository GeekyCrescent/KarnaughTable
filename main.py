import numpy as np
from Karnaugh import KarnaughTable


def main():
    # Ask the user for the number of variables
    num_variables = int(input("Enter the number of variables (1-6): "))
    truth_values = [0, 1, 1, 0, 1, 1, 1, 1]
    
    # Create an instance of KarnaughTable
    karnaugh = KarnaughTable(num_variables)

    # Input truth table values
    karnaugh.input_table_truth_from_list(truth_values)

    # Show the truth table
    karnaugh.show_truth_table()

    # Generate and show the Karnaugh map
    karnaugh.generate_karnaugh_map()
    karnaugh.show_karnaugh_map()

    # Generate groups
    non_redundant_groups = karnaugh.remove_redundant_groups()

    # Transform the gray code and get group values
    group_values = karnaugh.order_gray_code()

    # Print maxiterms
    print("Maxiterms:")
    karnaugh.maxiterm_print(group_values)


main()
