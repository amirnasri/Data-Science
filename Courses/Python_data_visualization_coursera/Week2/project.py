def parse_str(s, separator, quote):
    quote_pos = []
    for i in range(len(s)):
        if s[i] == quote:
            quote_pos.append(i)

    if len(quote_pos) % 2 != 0:
        raise Exception('Quoted string is malformed.')

    i = 0
    parse_output = []
    current_pos = 0
    has_qoute = True
    while current_pos < len(s):
        if i == len(quote_pos):
            has_qoute = False
            start = len(s)
            end = len(s)
        else:
            start = quote_pos[i]
            # add one for separator
            end = quote_pos[i+1] + 1
        # Get string from current_pos up to the first quote
        # The start and end of a non_quote_str must be a separator, remove those
        non_quote_str = s[current_pos:start]

        if len(non_quote_str) != 0:
            # exclude empty string in the end caused by last separator
            non_quote_str_parsed = non_quote_str.split(separator)[:-1]
            parse_output.extend([item.strip() for item in non_quote_str_parsed])

        if has_qoute:
            quote_str = s[start:end]
            parse_output.append(quote_str)
        else:
            # This is very last part (that's why there is no qoute)
            break

        i += 2
        current_pos = end + 1

    return parse_output

def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    outer_dict = {}
    
    with open(filename, 'r') as f:
        #f_data = f.read(1000)
        #return {'a' : [ord(i) for i in f_data]}
        header = f.readline()
        if header[-1] != separator:
            header = header + separator
        columns = [s.strip() for s in header.split(separator)]
        
        for line in f.readlines():
            if len(line.strip()) == 0:
                continue
            # Make sure the line ends with a separator
            # That way, we can assume each field in the line is followed by a separator
            if line[-1] != separator:
                line = line + separator
            fields = parse_str(line, separator, quote)
            inner_dict = dict(zip(columns, fields))
            key = inner_dict[keyfield]
            outer_dict[key] = inner_dict
            
    return outer_dict
            
            
             
            
def build_plot_values(gdpinfo, gdpdata):
    """
    Inputs:
      gdpinfo - GDP data information dictionary
      gdpdata - A single country's GDP stored in a dictionary whose
                keys are strings indicating a year and whose values
                are strings indicating the country's corresponding GDP
                for that year.

    Output: 
      Returns a list of tuples of the form (year, GDP) for the years
      between "min_year" and "max_year", inclusive, from gdpinfo that
      exist in gdpdata.  The year will be an integer and the GDP will
      be a float.
    """
    
    #gdp = read_csv_as_nested_dict(gdpinfo['gdpfile'], gdpinfo['country_name'], gdpinfo['separator'], gdpinfo['quote'])
    
    min_year = gdpinfo['min_year']
    max_year = gdpinfo['max_year']
    year_gdp = []

    for y, gdp in gdpdata.items():
        try:
            y_int = int(y)
            if min_year <= y_int <= max_year and gdp.strip() != '':
                year_gdp.append((y_int, float(gdp)))
        except ValueError:
            continue
            
    year_gdp = sorted(year_gdp, key=lambda x : x[0])
    return year_gdp                        
