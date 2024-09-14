import ConfigParser

def read_x86_ini_file(file_path):
    # Create a ConfigParser object
    config = ConfigParser.ConfigParser()
    
    # Read the INI file
    config.read(file_path)
    
    # Debug: Print the sections to check if 'Global' is present
    print("Sections found:", config.sections())
    
    # Check if 'Global' section exists
    if not config.has_section(' Global '):
        raise ValueError("Section ' Global ' not found in the INI file")

    # Define the keys we're interested in
    keys = [
        'Commit.Integer',
        'Commit.FloatingPoint',
        'Commit.Ctrl',
        'Commit.Memory',
        'Commit.PredAcc'
    ]

    # Create a dictionary to store the values
    values_dict = {}

    # Loop through the keys and fetch their values
    for key in keys:
        if config.has_option(' Global ', key):
            values_dict[key] = config.get(' Global ', key)
        else:
            raise ValueError("Key '{0}' not found in the 'Global' section".format(key))
    
    return values_dict

def read_mem_ini_file(file_path):
    config = ConfigParser.ConfigParser()
    config.read(file_path)
    section_l1 = ' mod-l1-0 '
    keys_l1 = ['Accesses']
    section_l2 = ' mod-l2-0 '
    keys_l2 = [ 'Accesses', 'HitRatio', 'Evictions'] 
    # accesses needs to be max over all l2 caches 
    section_l3 = ' mod-l3-0 '
    keys_l3 = ['Accesses']
    sections = { section_l1: keys_l1, section_l2: keys_l2, section_l3: keys_l3}
    mem_values = {} 
    for key,value in sections.iteritems():
        if not config.has_section(key):
            raise ValueError("Section '{0} ' not found in the INI file".format(key))
        for item in value: 
            if config.has_option(key, item):
                mem_values[item] = config.get(key, item)
            else:
                raise ValueError("Key '{0}' not found in the '{1}' section".format(item, key))
    return mem_values

# Example usage
if __name__ == "__main__":
    ini_file_path = 'mm_x86_Report'  # Path to your INI file
    try:
        result = read_x86_ini_file(ini_file_path)
        print(result)
    except Exception as e:
        print("Error: {}".format(e))
    mem_file_path = 'mm_MemoryReport'
    try:
        mem_result = read_mem_ini_file(mem_file_path)
        print(mem_result)
    except Exception as e:
        print("Error: {}".format(e))
    merged_dict = result.copy()

    for key, value in mem_result.items():
        merged_dict[key] = value

    print(merged_dict)






      
