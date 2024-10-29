import numpy as np

class KarnaughTable:
    # Constructor
    def __init__(self, num_variables):
        self.num_variables = num_variables
        self.table_truth = []
        self.map = np.zeros((2 ** (num_variables // 2), 2 ** (num_variables - num_variables // 2)), dtype=int)
        self.gray_code = []
    
        # Function to transform the binary to numbers to gray code
    # [000, 001, 010, 011, 100, 101, 110, 111] to [00, 01, 11, 10]
    def generate_gray_code(self):
        gray_code = [f'{i ^ (i >> 1):0{self.num_variables}b}' for i in range(2 ** self.num_variables)]
        return gray_code
    
    # Input values into the table truth
    def input_table_truth(self):
        num_boxes = 2 ** self.num_variables
        for i in range(num_boxes):
            box = int(input(f'Value for {bin(i)[2:].zfill(self.num_variables)}: '))
            self.table_truth.append(box)

    def input_table_truth_from_list(self, values):
        if len(values) != 2 ** self.num_variables:
            raise ValueError(f"Expected {2 ** self.num_variables} values for a truth table with {self.num_variables} variables.")
        
        self.table_truth = values  # Replace the table with the new list
    
    # Function to show the truth table. With a maximum of 10 variables
    def show_truth_table(self):
        num_boxes = 2 ** self.num_variables
        possible_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'] # Can be modified for more
        print("TRUTH TABLE")
        print(f"{''.join(possible_letters[:self.num_variables])}\t|\tS") # Print the variable letter
        print('-' * 13)
        for i in range(num_boxes):
            print(f'{bin(i)[2:].zfill(self.num_variables)}\t|\t{self.table_truth[i]}') # Fills with zeros before the number
        print('\n')


    # Function to show the Karnaugh Map, must be under 6 variables
    def show_karnaugh_map(self):
        if self.num_variables > 6:  # Can be changed, but it is not actually readable
            print("Too big to make it visual")
        else:
            self.gray_code = self.generate_gray_code()
            num_rows = 2 ** (self.num_variables // 2)
            num_cols = 2 ** (self.num_variables - self.num_variables // 2)
            column_variables = []
            row_variables = []
            print('KARNAUGH MAP')
            print('\t|', end='')
            # Print every column and append the significant bits to the column variables
            for i in range(num_cols):
                variable_column = self.gray_code[i][int(-np.log2(num_cols)):]  # Format it taking the necessary bits
                column_variables.append(variable_column)
                print(f"{variable_column} | ", end='')
            print()  # End line
            # Print every row
            for row in range(num_rows):
                variable_row = self.gray_code[row][int(-np.log2(num_rows)):]  # Taking the necessary bits
                row_variables.append(variable_row)
                print(f"{variable_row}\t|", end='')
                # Print all the row values
                for col in range(num_cols):
                    # Combine the row values with the column values
                    # Example:      "0" + "00"
                    combination = row_variables[row] + column_variables[col]
                    combination = int(combination, 2)  # Transform it from binary to decimal
                    # Check each index of the truth table
                    # Formar for bigger number of variables
                    if self.table_truth[combination] == 1 and self.num_variables < 5: 
                        print(" 1 | ", end='')
                    elif self.table_truth[combination] == 1 and self.num_variables >= 5:
                        print(" 1  | ", end='')
                    elif self.table_truth[combination] == 0 and self.num_variables >= 5:
                        print("    | ", end='')
                    else:
                        print("   | ", end='')
                print()
    
      # Function that inserts the values of the karnaugh map into a matrix
    def generate_karnaugh_map(self):
        self.gray_code = self.generate_gray_code()
        num_rows = 2 ** (self.num_variables // 2)
        num_cols = 2 ** (self.num_variables - self.num_variables // 2)
        column_variables = []
        row_variables = []
        # Same functionality as in the printing, but inserting in the map variable
        for i in range(num_cols):
            variable_column = self.gray_code[i][int(-np.log2(num_cols)):]  # Format that takes the necessary bits
            column_variables.append(variable_column)
        for row in range(num_rows):
            variable_row = self.gray_code[row][int(-np.log2(num_rows)):] # Take necessary bits
            row_variables.append(variable_row)
            for col in range(num_cols):
                combination = row_variables[row] + column_variables[col]
                combination = int(combination, 2)
                if self.table_truth[combination] == 1:  # Addas a 1 if the combination in the truth table is a one
                    self.map[row][col] = 1
                else:
                    self.map[row][col] = 0  # Adds a zero otherwise

    # Function to define if the value being accessed is a one or in the limits of the matrix
    def is_safe(self, i, j):
        if (i < 0 or i >= self.map.shape[0]): # Checks limits in x
            return False
        elif (j < 0 or j >= self.map.shape[1]): # Checks limits in y
              return False
        elif self.map[i][j] == 0:  # Checks if the value is 0
            return False
        else:
            return True
        
    # Function that check if the value to the right is safe.
    def is_right_safe(self, w, h, i, j):
        for k in range(h):  # Checks for each height
            if not self.is_safe(i + w, j + k):
                return False
        return True

   # Function to create all possible groups
    def create_groups(self):
        groups = []

        for i in range(self.map.shape[0]):  # Iterate through rows
            for j in range(self.map.shape[1]):  # Iterate through columns
                if (not self.is_safe(i, j)):  # Check if position is safe
                    continue
                groups.append(self.make_groups_dict(i, j, i, j))  # Add single-cell group
                w = 1 
                h = 1 
                while self.is_safe(i, j + h - 1):  # Check for vertical expansion
                    if (np.log2(h) % 1 != 0):
                        h += 1  # Increase height
                        continue
                    w = 1  # Reset width
                    while True:  # Check for horizontal expansion
                        if (not self.is_right_safe(w, h, i, j)):
                            if (np.log2(w) % 1 == 0):
                                groups.append(self.make_groups_dict(i, j, i + w - 1, j + h - 1))
                                break
                            else:
                                new_w = w
                                while np.log2(new_w) % 1 != 0:
                                    new_w -= 1  # Adjust width to the nearest power of 2
                                groups.append(self.make_groups_dict(i, j, i + new_w - 1, j + h - 1))
                                break
                        w += 1  # Increase width

                    h += 1  # Increase height

        groups.sort(key=lambda a: a['area'], reverse=True)  # Sort groups by area
        return groups 
    
    # Function to check for envolving groups ---------------------------------------------------------------------------------------

    # Transform the values to a dict format
    def make_groups_dict(self, x1, y1, x2, y2):
        return {'start': {'x': x1, 'y': y1}, 
                'end': {'x': x2, 'y': y2}, 
                'area': (x2-x1+1)*(y2-y1+1)};   

    # Function to remove the redundant groups
    def remove_redundant_groups(self):
        groups = self.create_groups()  # Get all possible groups
        non_redundant_groups = []  # List to store groups that are not redundant

        # Sort groups by area in descending order
        groups.sort(key=lambda x: x['area'], reverse=True)

        for current_group in groups:
            is_redundant = False  # Flag to track redundancy

            # Compare current group with already added non-redundant groups
            for other_group in non_redundant_groups:
                # Check if the current group is contained within another group and is smaller or equal in area
                if (current_group['area'] <= other_group['area'] and 
                        self.is_contained(current_group, other_group)):
                    is_redundant = True  # Mark as redundant
                    break  # Exit the loop since redundancy is confirmed

            if not is_redundant:
                non_redundant_groups.append(current_group)  # Add to non-redundant groups

        return non_redundant_groups  # Return the list of non-redundant groups



    # Check if a whole group is inside another group
    def is_contained(self, group_a, group_b):
        return (group_a['start']['x'] >= group_b['start']['x'] and 
                group_a['end']['x'] <= group_b['end']['x'] and 
                group_a['start']['y'] >= group_b['start']['y'] and 
                group_a['end']['y'] <= group_b['end']['y'])
    
    # Function to transform the gray code into a binary code and 
    def order_gray_code(self):
        non_redundant_groups = self.remove_redundant_groups()  # Get non-redundant groups

        separator = 2 ** (self.num_variables // 2)  # Calculate separator for splitting
        parts = np.array_split(self.gray_code, separator)  # Split gray code into parts
        ordered_gray_code = []  # List to hold the ordered gray code
        
        # Reverse every second part to maintain the Gray code order
        for idx, part in enumerate(parts):
            if idx % 2 == 1:
                part = part[::-1]  # Reverse the part if the index is odd
            ordered_gray_code.extend(part)  # Extend the ordered list with the current part 

        # Reshape the ordered gray code array
        ordered_gray_code = np.array(ordered_gray_code).reshape(
            2 ** (self.num_variables // 2), 
            2 ** (self.num_variables - self.num_variables // 2)
        )

        group_values = []  # List to store values of each group

        # Extract values from the ordered gray code for each non-redundant group
        for group in non_redundant_groups:
            current_group_values = []  # List to hold current group's values
            for i in range(group['start']['x'], group['end']['x'] + 1):
                for j in range(group['start']['y'], group['end']['y'] + 1):
                    current_group_values.append(ordered_gray_code[i, j])  # Append the value
            group_values.append(current_group_values)  # Add current group values to the main list
        
        return group_values  # Return the list of group values

    # Function that prints the maxiterm form of the expression
    def maxiterm_print(self, group_values):
        possible_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        var_letter = ''.join(possible_letters[:self.num_variables])  # Get variable letters based on the number of variables

        string_maxiterm = ""  # Initialize the string for maxiterms

        for i in group_values:
            transposed_bits = list(zip(*i))  # Transpose the group values for easier access

            # Identify unchanged indices (where all values in the column are the same)
            unchanged_indices = [i for i, column in enumerate(transposed_bits) if len(set(column)) == 1]
            
            if len(unchanged_indices) == 0:
                print(1)  # Print '1' if no unchanged indices are found
            else:
                unchanged_info = []
                for index in unchanged_indices:
                    unchanged_value = i[0][index]  # Get the value from the first list in the group
                    unchanged_info.append((var_letter[index], unchanged_value))  # Store variable and its value

                string_and = ""
                for var, value in unchanged_info:
                    if value == '1':
                        string_and += var  # Append variable name for '1'
                    else:
                        string_and += '!' + var  # Append negated variable for '0'

                string_maxiterm += '(' + string_and + ')' + ' + '  # Add the current maxiterm to the string

        # Remove the trailing ' + ' if string_maxiterm is not empty
        if string_maxiterm:
            string_maxiterm = string_maxiterm.rstrip(' + ')

        print(string_maxiterm)  # Print the final maxiterm string

