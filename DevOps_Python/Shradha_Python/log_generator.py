def read_log_lines(file_path="logs.txt"):

    if not isinstance(file_path,str):
        raise TypeError("FilePath must be a string")
    if not file_path:
        raise ValueError("FilePath cannot be an empty string")
    

    with open(file_path,'r') as file:

        for line in file:

            stripline = line.strip()

            if not stripline or stripline.startswith('#'):
                continue

            yield stripline

for line in read_log_lines():
    print(line)















    


