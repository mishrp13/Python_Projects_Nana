def read_config_file(filepath):

    with open(filepath,'r') as file:
        for line in file:
            yield line


def filter_config_lines(lines):
    for line in lines:
        stripped_line= line.strip()
        if stripped_line and not stripped_line.startswith('#'):
            yield stripped_line

def parse_config_lines(lines):

    current_section= None

    for line in lines:

        if line.startswith('[') and line.endswith(']'):

            current_section= line[1:-1]
            continue


        elif '=' in line:
            key ,value= line.split('=',1)
            yield(current_section,key.strip(),value.strip())



lines = read_config_file("config.txt")
filtered = filter_config_lines(lines)
parsed = parse_config_lines(filtered)

for item in parsed:
    print(item)