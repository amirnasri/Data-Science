import os
email_path = './beck-s'

def read_email_files(path):
    email_files = []
    new_line = '\n'
    for root, dirnames, filenames in os.walk(email_path):
        email_files.extend([os.path.join(root, f) for f in filenames])
    
    for email_file in email_files:
        with open(email_file) as f:
            lines = f.readlines()
            try:
                body_start = lines.index(new_line)
            except ValueError:
                continue
            body = ''.join(lines[body_start + 1:])
            yield email_file, body
                
                
for a, b in read_email_files(email_path):
    print "{" + a + b + "}"        
