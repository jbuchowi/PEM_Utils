import pem
import os, errno
import argparse
import tkinter as tk
from tkinter import filedialog, messagebox

def main():
    is_command_line = True
    app_description = 'This app splits PEM chain file into root and intermediate file'
    arg_parser = argparse.ArgumentParser(description=app_description,
                                         usage='use "python %(prog)s --help" for more information', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    arg_parser.add_argument('-f', '--pem_file', help='a full path to input file', required=False)
    args = arg_parser.parse_args()
    if args.pem_file is None:
        is_command_line = False
        root = tk.Tk()
        root.withdraw()
        file_type = [("PEM files", '*.pem')]
        pem_file_full = filedialog.askopenfilename(title="Select chain PEM file", initialfile="*chain*.pem", filetype=file_type)
    else:
        pem_file_full = args.pem_file

    if pem_file_full == '':
        if is_command_line:
            print("PEM Chain file not selected")
        else:
            messagebox.showerror("Error", "PEM Chain file not selected")
        exit(errno.ENOENT)

    #pem_file_full = "C:/Users/jbuchowi/Downloads/May14-3dx-dev01_certs/551986_3dx-dev01.plm.celestica.com_chain.pem"
    file_name = os.path.basename(pem_file_full)
    path = os.path.dirname(pem_file_full)
    root_pem_name = file_name.replace("chain", "root")
    root_pem_file = os.path.join(path, root_pem_name)
    intermediate_pem_name = file_name.replace("chain", "intermediate")
    intermediate_pem_file = os.path.join(path, intermediate_pem_name)
    certs = pem.parse_file(pem_file_full)

    root_pem = certs[1]
    intermediate_pem = certs[0]

    pem_out = open(root_pem_file, "w", newline='\n')
    pem_out.write(str(root_pem))

    pem_out = open(intermediate_pem_file, "w", newline='\n')
    pem_out.write(str(intermediate_pem))

    if is_command_line:
        print(f"root pem file saved in: {root_pem_file}")
        print(f"intermediate pem file saved in: {intermediate_pem_file}")
    else:
        messagebox.showinfo("PEM Split Successful", f"root pem file saved in: {root_pem_file}\n\nintermediate pem file saved in: {intermediate_pem_file}")


if __name__ == '__main__':
    main()
