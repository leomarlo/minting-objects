def remove_comments(filename="../frontend/frontend.conf", output="../frontend/frontend_uncommented.conf"):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Filtering out lines that start with a comment
    cleaned_lines = [line for line in lines if not line.strip().startswith("#")]

    # Overwriting the file with cleaned content
    with open(output, 'w') as file:
        file.writelines(cleaned_lines)

if __name__ == "__main__":
    # change directory to the one containing this script
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    remove_comments()
