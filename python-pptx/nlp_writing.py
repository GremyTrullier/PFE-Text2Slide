def replace_sentence(input_file, output_file, isentence, osentence):
    """
    Function that copies a file and changes a line into another. It doesn't replace the line in the file (unless input and output files are the same.
    Parameters:
        - input_file: path of the file to be read (and replaced)
        - output_file: path of the file to be written
        - isentence: sentence you want to remove from the file
        - osentence: sentence you want to add to the file
    """
    with open(input_file, "r", encoding = "utf-8") as ifile:
        fcontent = ifile.read()

    lines = fcontent.split("\n")

    for i, line in enumerate(lines):
        if (isentence in line):
            if (line[len(line)-1] == ','):
                lines[i] = osentence+','
                print(f"Changed {isentence}\n into {lines[i]}.")
                continue
            lines[i] = osentence
            print(f"Changed {isentence}\n into {lines[i]}.")
            
    fcontent = "\n".join(lines)

    with open(output_file, "w", encoding = "utf-8") as ofile:
        ofile.write(fcontent)
        ofile.flush()