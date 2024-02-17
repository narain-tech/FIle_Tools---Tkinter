import os
import filecmp
import tkinter as tk
from tkinter import filedialog, messagebox

class FileToolsApp:
    def __init__(self, master):
        self.master = master
        master.title("File Tools")

        # Original File Finder Section
        self.original_file_label = tk.Label(master, text="Original File:")
        self.original_file_label.grid(row=0, column=0, sticky="w")

        self.original_file_entry = tk.Entry(master, width=50)
        self.original_file_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

        self.browse_button = tk.Button(master, text="Browse", command=self.browse_original_file)
        self.browse_button.grid(row=0, column=3, padx=5, pady=5)

        # Directory Section
        self.directory_label = tk.Label(master, text="Directory:")
        self.directory_label.grid(row=1, column=0, sticky="w")

        self.directory_entry = tk.Entry(master, width=50)
        self.directory_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        self.browse_dir_button = tk.Button(master, text="Browse", command=self.browse_directory)
        self.browse_dir_button.grid(row=1, column=3, padx=5, pady=5)

        # Find Copies Section
        self.find_button = tk.Button(master, text="Find Copies", command=self.find_copies)
        self.find_button.grid(row=2, column=1, columnspan=2, pady=10)

        # Scan Directory Section
        self.scan_button = tk.Button(master, text="Scan Directory", command=self.scan_directory)
        self.scan_button.grid(row=3, column=1, columnspan=2, pady=10)

        # Delete Copies Section
        self.delete_button = tk.Button(master, text="Delete Copies", command=self.delete_copies)
        self.delete_button.grid(row=4, column=1, columnspan=2, pady=10)

        # Results Section
        self.result_label = tk.Label(master, text="Results:")
        self.result_label.grid(row=5, column=0, sticky="w")

        self.result_text = tk.Text(master, height=10, width=60)
        self.result_text.grid(row=6, column=0, columnspan=4, padx=5, pady=5)

    def browse_original_file(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select Original File")
        self.original_file_entry.delete(0, tk.END)
        self.original_file_entry.insert(0, filename)

    def browse_directory(self):
        directory = filedialog.askdirectory(initialdir="/", title="Select Directory")
        self.directory_entry.delete(0, tk.END)
        self.directory_entry.insert(0, directory)

    def find_copies(self):
        original_file = self.original_file_entry.get()
        directory = self.directory_entry.get()

        if not original_file or not directory:
            messagebox.showerror("Error", "Please select the original file and the directory.")
            return

        if not os.path.exists(original_file):
            messagebox.showerror("Error", f"The original file '{original_file}' does not exist.")
            return

        copies = self.search_copies(original_file, directory)

        if copies:
            self.result_text.delete(1.0, tk.END)
            for copy in copies:
                self.result_text.insert(tk.END, copy + '\n')
        else:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "No potential copies found.")

    def search_copies(self, original_file, directory):
        copies = []

        for dirpath, _, filenames in os.walk(directory):
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)

                if filecmp.cmp(original_file, full_path):
                    copies.append(full_path)

        return copies

    def scan_directory(self):
        directory = self.directory_entry.get()

        if not directory:
            messagebox.showerror("Error", "Please select a directory.")
            return

        self.result_text.delete(1.0, tk.END)

        self.scan_directory_recursive(directory)

    def scan_directory_recursive(self, directory):
        for dirpath, _, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                self.result_text.insert(tk.END, f"File: {file_path}\n")

                # Determine file type
                file_type = self.get_file_type(filename)
                self.result_text.insert(tk.END, f"Type: {file_type}\n\n")

    def get_file_type(self, filename):
        name, extension = os.path.splitext(filename)
        return extension

    def delete_copies(self):
        original_file = self.original_file_entry.get()
        directory = self.directory_entry.get()

        if not original_file or not directory:
            messagebox.showerror("Error", "Please select the original file and the directory.")
            return

        if not os.path.exists(original_file):
            messagebox.showerror("Error", f"The original file '{original_file}' does not exist.")
            return

        deleted_files = self.delete_copies_recursive(original_file, directory)

        if deleted_files:
            self.result_text.delete(1.0, tk.END)
            for deleted_file in deleted_files:
                self.result_text.insert(tk.END, f"Deleted: {deleted_file}\n")
        else:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "No copies found or deleted.")

    def delete_copies_recursive(self, original_file, directory):
        deleted_files = []

        for dirpath, _, filenames in os.walk(directory):
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)

                if filecmp.cmp(original_file, full_path):
                    try:
                        os.remove(full_path)
                        deleted_files.append(full_path)
                    except Exception as e:
                        print(f"Error deleting file {full_path}: {e}")

        return deleted_files

def main():
    root = tk.Tk()
    app = FileToolsApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
