# Karnaugh Map Solver

This Python package provides a `KarnaughTable` class that generates and manipulates Karnaugh maps, which are used in Boolean algebra to simplify logic expressions. It is designed to support truth table input, Karnaugh map visualization, group creation, redundant group removal, and output of expressions in maxiterm form. 

## Features

- **Gray Code Generation**: Transforms binary numbers to Gray code format for Karnaugh map layout.
- **Truth Table Input**: Supports truth table input via direct input or list.
- **Truth Table and Map Visualization**: Displays truth table and Karnaugh map (up to 6 variables for readability).
- **Group Creation and Redundancy Removal**: Creates groups in the Karnaugh map and removes redundant groups to optimize the map.
- **Maxiterm Form Output**: Outputs the minimized Boolean expression in maxiterm form.

## Installation

Ensure you have Python installed, and then install NumPy:

```bash
pip install numpy
```

## Usage

### 1. Import the Class and Create an Instance
```python
from karnaugh import KarnaughTable

kt = KarnaughTable(num_variables=4)  # Set the number of variables for the map
```

### 2. Generate Gray Code

```python
gray_code = kt.generate_gray_code()
```

### 3. Input Truth Table Values
```python
# Direct input
kt.input_table_truth_from_list([0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0])

# Display Truth Table
kt.show_truth_table()
```

### 4. Show Karnaugh Map
```python
kt.show_karnaugh_map()
```

### 5. Generate and Remove Redundant Groups
```python
kt.generate_karnaugh_map()
groups = kt.create_groups()
non_redundant_groups = kt.remove_redundant_groups()
```

### 6. Output Maxiterm Expression
```python
group_values = kt.order_gray_code()
kt.maxiterm_print(group_values)
```

## Example

Here's an example of a 3-variable Karnaugh map and the corresponding truth table input.

```python
kt = KarnaughTable(num_variables=3)
kt.input_table_truth_from_list([1, 0, 0, 1, 1, 0, 1, 0])
kt.show_truth_table()
kt.show_karnaugh_map()
kt.generate_karnaugh_map()
kt.remove_redundant_groups()
kt.maxiterm_print(kt.order_gray_code())
```

## License

This project is open-source. Feel free to modify and extend.
