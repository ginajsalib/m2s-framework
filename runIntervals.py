import ConfigParser
import subprocess
import csv
from datetime import datetime

#l2_values = [256, 512, 1024, 2048]
#l3_values = [4, 8, 12, 16]
l2_values = [256, 512] 
l3_values = [4]


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
        'Commit.Total',
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
    keys_l2 = [ 'Accesses', 'HitRatio', 'Evictions', 'Hits'] 
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
   rows = [] 
   for l2 in l2_values:
       for l3 in l3_values:
         max_inst = 500000
         end = 338500000
         step = 500000 
         while max_inst <= end:
        # Generate the filename based on the current l2 and l3 values
           filename = '/scripts/mem-config-{0}-{1}.txt'.format(l2, l3)
           out_x86_filename = '/scripts/mm_x86_Report-{0}-{1}.txt'.format(l2, l3)
           out_mem_filename = '/scripts/mm_Memory_Report-{0}-{1}.txt'.format(l2, l3)
           # Define the command you want to run, using the filename
           command = [' /usr/local/bin/m2s',' --x86-sim',' detailed',' --mem-config ', filename, ' --x86-config', ' /scripts/x86-config.txt', '--x86-report', out_x86_filename, '--mem-report', out_mem_filename,'--x86-max-inst',str(max_inst), ' /multi2sim/m2s-bench-parsec-3.0-src/blackscholes/blackscholes',' 1',' /multi2sim/m2s-bench-parsec-3.0/blackscholes/data-small/in_4K.txt',' prices.txt']
        
           # Print the command to be executed (optional)
           print('Running command:', ' '.join(command))
        
           # Execute the command
           try:
               return_code = subprocess.call(' '.join(command), shell=True)
 
               #subprocess.check_call(command)
           except subprocess.CalledProcessError as e:
               print('Error running command:', e) 
           ini_file_path = out_x86_filename  # Path to your INI file
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
           merged_dict['max_inst'] = max_inst
           merged_dict["l2"] = l2
           merged_dict["l3"] = l3
           max_inst += step
           print(merged_dict)
           rows.append(merged_dict)
   if rows:
        headers = rows[0].keys()
        # Generate a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Construct the filename with the timestamp
        out_filename = "output_{}.csv".format(timestamp)

        with open(out_filename, 'wb') as csvfile:
           writer = csv.writer(csvfile)
           writer.writerow(headers)
           for row in rows:
               writer.writerow([row.get(header, '') for header in headers])
 



      
