import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
class BinaryFileComparer:
    def __init__(self, root):
        self.root = root
        self.root.title("Binary File Comparer")

        self.label_font = ('Helvetica', 10)
        self.entry_font = ('Helvetica', 10)
        self.button_font = ('Helvetica', 10, 'bold')
        self.button_normal_bg = '#2196F3'  
        self.button_disabled_bg = '#CCCCCC' 
        self.button_active_bg = '#1E88E5'  
        self.error_bg = '#FF6347' 
        self.success_bg = '#32CD32' 

        self.original_file = ".\\237036CA3A_237109HE2B-20240707-201748 hamad  ecu 2020 2m ecu altima.bin"
        self.edited_file = ".\\237036CA3A_237109HE2B-20240713-213414 100% shutter off.bin"
        
        self.third_file = ""
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Third Binary File:", font=self.label_font).grid(row=2, column=0, padx=10, pady=5, sticky='w')
    
        self.third_entry = tk.Entry(self.root, width=50, font=self.entry_font, state='readonly')
        self.third_entry.grid(row=2, column=1, padx=10, pady=5)
      
        self.third_button = tk.Button(self.root, text="Add File", font=self.button_font, bg=self.button_normal_bg, command=self.select_third)
        self.third_button.grid(row=2, column=2, padx=10, pady=5)
        self.compare_button = tk.Button(self.root, text="Compare and Generate", font=self.button_font, bg=self.button_disabled_bg, state='disabled', command=self.compare_and_generate)
        self.compare_button.grid(row=3, column=1, padx=10, pady=10)
        
    def select_original(self):
        self.original_file = filedialog.askopenfilename(filetypes=[("Binary Files", "*.bin")])
        if self.original_file:
            self.original_entry.config(state='normal', bg='white')
            self.original_entry.delete(0, tk.END)
            self.original_entry.insert(0, self.original_file)
            self.original_entry.config(state='readonly')
            self.original_button.config(bg=self.button_active_bg)
            self.check_all_files_selected()

    def select_edited(self):
        self.edited_file = filedialog.askopenfilename(filetypes=[("Binary Files", "*.bin")])
        if self.edited_file:
            self.edited_entry.config(state='normal', bg='white')
            self.edited_entry.delete(0, tk.END)
            self.edited_entry.insert(0, self.edited_file)
            self.edited_entry.config(state='readonly')
            self.edited_button.config(bg=self.button_active_bg)
            self.check_all_files_selected()

    def select_third(self):
        self.third_file = filedialog.askopenfilename(filetypes=[("Binary Files", "*.bin")])
        if self.third_file:
            self.third_entry.config(state='normal', bg='white')
            self.third_entry.delete(0, tk.END)
            self.third_entry.insert(0, self.third_file)
            self.third_entry.config(state='readonly')
            self.third_button.config(bg=self.button_active_bg)
            self.check_all_files_selected()

    def check_all_files_selected(self):
        if self.original_file and self.edited_file and self.third_file:
            self.compare_button.config(state='normal', bg=self.button_normal_bg)

    def compare_and_generate(self):
        if self.original_file == "" or self.edited_file == "" or self.third_file == "":
            messagebox.showerror("Error", "Please select all three binary files.", parent=self.root)
            return

        try:
            temp_third_file = self.third_file + "_temp"

            with open(self.original_file, 'rb') as f_original, open(self.edited_file, 'rb') as f_edited, open(temp_third_file, 'wb') as f_third:
                original_data = f_original.read()
                edited_data = f_edited.read()

                if len(original_data) != len(edited_data):
                    raise ValueError("Files must be of the same length.")

                third_data = bytearray(original_data)

                row_size = 16 
                total_rows = len(original_data) // row_size

                for row in range(total_rows):
                    for col in range(row_size):
                        index = row * row_size + col
                        if original_data[index] != edited_data[index]:
                            third_data[index] = edited_data[index]

                f_third.write(third_data)

            save_path = filedialog.asksaveasfilename(filetypes=[("Binary Files", "*.bin")], initialfile=self.third_file.split("/")[-1])
            if save_path:
                shutil.move(temp_third_file, save_path)  
                messagebox.showinfo("Success", f"Comparison and generation completed successfully. Third file saved as {save_path}.", parent=self.root)
            else:
                messagebox.showwarning("Warning", "Save operation canceled. The temporary file remains.", parent=self.root)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}", parent=self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = BinaryFileComparer(root)
    root.mainloop()
