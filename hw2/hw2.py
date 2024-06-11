import os
import tkinter as tk
from tkinter import simpledialog, PhotoImage

# GUI class for the File System Simulator
class FileSystemSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File System Simulator")

        # Initialize the File System Simulator
        self.fs = FileSystemSimulator(self.display_error)

        # Path label to show the current directory
        self.path_label = tk.Label(root, text="Current Directory: ")
        self.path_label.pack()

        # Frame for the buttons
        self.frame = tk.Frame(root)
        self.frame.pack()

        # Buttons for file and directory operations
        self.create_button = tk.Button(self.frame, text="Create File", command=self.create_file)
        self.create_button.grid(row=0, column=0)

        self.delete_button = tk.Button(self.frame, text="Delete File", command=self.delete_file)
        self.delete_button.grid(row=0, column=1)

        self.read_button = tk.Button(self.frame, text="Read File", command=self.read_file)
        self.read_button.grid(row=0, column=2)

        self.write_button = tk.Button(self.frame, text="Write to File", command=self.write_file)
        self.write_button.grid(row=0, column=3)

        self.mkdir_button = tk.Button(self.frame, text="Create Directory", command=self.create_directory)
        self.mkdir_button.grid(row=1, column=0)

        self.rmdir_button = tk.Button(self.frame, text="Delete Directory", command=self.delete_directory)
        self.rmdir_button.grid(row=1, column=1)

        self.cd_button = tk.Button(self.frame, text="Change Directory", command=self.change_directory)
        self.cd_button.grid(row=1, column=2)

        self.search_button = tk.Button(self.frame, text="Search File", command=self.search_file)
        self.search_button.grid(row=1, column=3)

        self.list_button = tk.Button(self.frame, text="List", command=self.list_directory)
        self.list_button.grid(row=2, column=0)

        # Frame to display files and directories
        self.display_frame = tk.Frame(root)
        self.display_frame.pack(pady=(10, 0))

        # Output text box for displaying messages and file contents
        self.output_text = tk.Text(root, height=5, width=60)
        self.output_text.pack(pady=(10, 0))

        # Load and resize icons
        self.folder_icon = PhotoImage(file="img/folder_icon.png").subsample(10, 10)  
        self.file_icon = PhotoImage(file="img/file_icon.png").subsample(10, 10)  
        self.left_icon = PhotoImage(file="img/left.png").subsample(10, 10)  

        self.update_display()

    # Function to display error messages
    def display_error(self, message):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, message)
        self.output_text.see(tk.END)

    # Update the path label to show the current directory
    def update_path_label(self):
        self.path_label.config(text=f"Current Directory: {self.fs.path}")

    # Update the display of files and directories
    def update_display(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()

        # Always add the left icon to go to the parent directory
        btn = tk.Button(self.display_frame, image=self.left_icon, compound="top", command=lambda: self.change_directory(".."))
        btn.grid(row=0, column=0, padx=5, pady=5)

        row, col = 0, 1

        # Get sorted directories and files
        directories = sorted([name for name, content in self.fs.current_dir.items() if isinstance(content, dict)])
        files = sorted([name for name, content in self.fs.current_dir.items() if not isinstance(content, dict)])

        # Display directories
        for name in directories:
            btn = tk.Button(self.display_frame, text=name, image=self.folder_icon, compound="top", command=lambda name=name: self.change_directory(name))
            btn.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 5:
                col = 0
                row += 1

        # Display files
        for name in files:
            btn = tk.Button(self.display_frame, text=name, image=self.file_icon, compound="top", command=lambda name=name: self.read_file(name))
            btn.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 5:
                col = 0
                row += 1

        self.update_path_label()

    # Function to create a new file
    def create_file(self):
        filename = simpledialog.askstring("Input", "Enter filename:")
        content = simpledialog.askstring("Input", "Enter file content:")
        if filename and content:
            self.fs.create(filename, content)
            self.update_display()

    # Function to delete a file
    def delete_file(self):
        filename = simpledialog.askstring("Input", "Enter filename to delete:")
        if filename:
            self.fs.delete(filename)
            self.output_text.delete(1.0, tk.END)  # Clear output box when deleting a file
            self.update_display()

    # Function to read a file
    def read_file(self, filename=None):
        if filename is None:
            filename = simpledialog.askstring("Input", "Enter filename to read:")
        if filename:
            content = self.fs.read(filename)
            self.output_text.delete(1.0, tk.END)  # Clear previous content
            self.output_text.insert(tk.END, f"Content of '{filename}': {content}\n")
            self.output_text.see(tk.END)  

    # Function to write to a file
    def write_file(self):
        filename = simpledialog.askstring("Input", "Enter filename to write:")
        content = simpledialog.askstring("Input", "Enter content to add:")
        if filename and content:
            self.fs.write(filename, content)
            self.update_display()

    # Function to create a new directory
    def create_directory(self):
        dirname = simpledialog.askstring("Input", "Enter directory name to create:")
        if dirname:
            self.fs.mkdir(dirname)
            self.update_display()

    # Function to delete a directory
    def delete_directory(self):
        dirname = simpledialog.askstring("Input", "Enter directory name to delete:")
        if dirname:
            self.fs.rmdir(dirname)
            self.update_display()

    # Function to change the current directory
    def change_directory(self, dirname=None):
        if dirname is None:
            dirname = simpledialog.askstring("Input", "Enter directory name to change to:")
        if dirname:
            self.fs.cd(dirname)
            self.output_text.delete(1.0, tk.END)  # Clear output box when changing directories
            self.update_display()

    # Function to search for a file
    def search_file(self):
        filename = simpledialog.askstring("Input", "Enter filename to search:")
        if filename:
            result = self.fs.search(filename)
            self.output_text.delete(1.0, tk.END)
            if result:
                self.output_text.insert(tk.END, "Found files:\n")
                for path in result:
                    self.output_text.insert(tk.END, f"{path}\n")
            else:
                self.output_text.insert(tk.END, "File not found.\n")
            self.output_text.see(tk.END)

    # Function to list files and directories in the current directory
    def list_directory(self):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Files and directories in current directory:\n")
        for k in sorted(self.fs.current_dir.keys()):
            self.output_text.insert(tk.END, f"{k}\n")
        self.output_text.see(tk.END)  

# Class for the File System Simulator logic
class FileSystemSimulator:
    def __init__(self, error_callback):
        self.root = {}
        self.current_dir = self.root
        self.path = "/"
        self.error_callback = error_callback

    # Function to create a file
    def create(self, filename, content):
        if filename in self.current_dir:
            if isinstance(self.current_dir[filename], dict):
                self.error_callback(f"Error: A directory named '{filename}' already exists.")
            else:
                self.error_callback(f"Error: A file named '{filename}' already exists.")
        else:
            self.current_dir[filename] = content
            print(f"File '{filename}' created.")

    # Function to delete a file
    def delete(self, filename):
        if filename in self.current_dir and not isinstance(self.current_dir[filename], dict):
            del self.current_dir[filename]
            print(f"File '{filename}' deleted.")
        else:
            self.error_callback("Error: File not found.")

    # Function to read a file
    def read(self, filename):
        if filename in self.current_dir and not isinstance(self.current_dir[filename], dict):
            return self.current_dir[filename]
        else:
            self.error_callback("Error: File not found.")
            return "File not found."

    # Function to write to a file
    def write(self, filename, content, overwrite=False):
        if filename in self.current_dir and not isinstance(self.current_dir[filename], dict):
            self.current_dir[filename] += content
            print(f"Content added to '{filename}'.")
        else:
            self.error_callback("Error: File not found.")

    # Function to create a directory
    def mkdir(self, dirname):
        if dirname in self.current_dir:
            if isinstance(self.current_dir[dirname], dict):
                self.error_callback(f"Error: A directory named '{dirname}' already exists.")
            else:
                self.error_callback(f"Error: A file named '{dirname}' already exists.")
        else:
            self.current_dir[dirname] = {}
            print(f"Directory '{dirname}' created.")

    # Function to remove a directory
    def rmdir(self, dirname):
        if dirname in self.current_dir and isinstance(self.current_dir[dirname], dict):
            if not self.current_dir[dirname]:
                del self.current_dir[dirname]
                print(f"Directory '{dirname}' removed.")
            else:
                self.error_callback("Error: Directory not empty.")
        else:
            self.error_callback("Error: Directory not found.")

    # Function to change the current directory
    def cd(self, dirname):
        if dirname == "..":
            if self.path != "/":
                self.path = os.path.dirname(self.path)
                if self.path == "/":
                    self.current_dir = self.root
                else:
                    parts = self.path.split('/')[1:]
                    self.current_dir = self.root
                    for part in parts:
                        if part in self.current_dir:
                            self.current_dir = self.current_dir[part]
                print(f"Moved to directory '{self.path}'")
            else:
                self.error_callback("Error: Already at root directory.")
        elif dirname in self.current_dir and isinstance(self.current_dir[dirname], dict):
            self.current_dir = self.current_dir[dirname]
            self.path = os.path.join(self.path, dirname)
            print(f"Moved to directory '{self.path}'")
        else:
            self.error_callback("Error: Directory not found.")

    # Update the current directory based on the path
    def _update_current_dir(self):
        self.current_dir = self.root
        parts = self.path.split('/')[1:]
        for part in parts:
            self.current_dir = self.current_dir[part]

    # Function to search for a file
    def search(self, filename):
        result = []
        self._search(self.root, filename, "", result)
        return result

    # Recursive function to search for a file
    def _search(self, current, filename, path, result):
        for k, v in current.items():
            if k == filename:
                result.append(os.path.join(path, k))
            if isinstance(v, dict):
                self._search(v, filename, os.path.join(path, k), result)

    # Function to list files and directories in the current directory
    def list(self):
        if self.current_dir:
            print("Files and directories in current directory:")
            for k in self.current_dir.keys():
                print(k)
        else:
            print("No files or directories.")

# Main function to start the GUI application
if __name__ == "__main__":
    root = tk.Tk()
    gui = FileSystemSimulatorGUI(root)
    root.mainloop()
