import os

new_lines = [
    " * @copyright\n",
    " * Copyright (c) 2018-2023 COMPANY A SAS\n",
    " * Copyright (c) 2024 COMPANY B SA - All Rights Reserved\n",
    " * \n",
    " * This file is part of PROJECT.\n",
    " * \n",
    " * Use of this source code is governed by an MIT-style\n",
    " * license that can be found in the LICENSE file or at\n",
    " * https://opensource.org/licenses/MIT.\n",
    " * \n"
]

file_counter = 0

def get_line_idx_range(lines_list, fp):
    # return a list of 2 elements: the index of the copyright line,
    # and the index of the author line.
    # fp = filepath parameter only if there is an error.
    index_range = []
    for index, line in enumerate(lines_list):
        if "@copyright" in line:
            index_range.append(index)
        if "@author" in line:
            index_range.append(index)
            break
    if len(index_range) != 2:
        print(f"warning: len(index_range) = {len(index_range)} != 2 in file {fp} : skip!")
    return index_range

def remove_elements_by_index_range(lines, index_range):
    # Create a set of indexes to remove for O(1) lookup time
    index_set = set(index_range)
    # Use list comprehension to filter lines based on index_set
    filtered_lines = [line for index, line in enumerate(lines) if index not in index_set]
    return filtered_lines
    
def insert_lines_at_idx(ln_ls, new_lns, idx):
    ln_ls[idx:idx] = new_lns
    return ln_ls

if __name__ == "__main__":
    directory = "." #work in the current directory.
    for dirpath, _, filenames in os.walk(directory): # get all filenames recursively
        for filename in filenames:
            if filename.endswith('.c') or filename.endswith('.h'): # only source files
                file_path = os.path.join(dirpath, filename) # work with file_path.

                # read the file & get list of lines
                with open(file_path, 'r') as file: 
                    lines = file.readlines()

                # Find lines index range to remove
                index_range = get_line_idx_range(lines, file_path)
                # check if we didnt find a header (index_range len is < 2)
                if len(index_range) != 2:
                    continue # skip to next file.
                else:
                    # remove lines within range (between copyright and author)
                    lines_deleted = remove_elements_by_index_range(lines,
                                        range(index_range[0], index_range[-1]))

                    # insert the new header lines in place
                    lines_upd = insert_lines_at_idx(lines_deleted, new_lines, index_range[0])

                    # save the new lines on the file path (overwrite)
                    with open(file_path, 'w') as output_file:
                        output_file.writelines(lines_upd)

                    file_counter += 1
                    print(f"{file_counter}: Updated {file_path}")

