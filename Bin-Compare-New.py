import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os
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
      
        self.third_button = tk.Button(self.root, text="Select Third", font=self.button_font, bg=self.button_normal_bg, command=self.select_third)
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
            # Make a temporary copy of the third file to work with
            temp_third_file = self.third_file + "_temp"
            shutil.copy(self.third_file, temp_third_file)
            
            # Compare original and edited files
            with open(self.original_file, 'rb') as f_original, open(self.edited_file, 'rb') as f_edited:
                original_data = f_original.read()
                edited_data = f_edited.read()

                if len(original_data) != len(edited_data):
                    raise ValueError("Files must be of the same length.")

                # Modify the temporary third file based on the comparison
                with open(temp_third_file, 'rb+') as f_third:
                    third_data = bytearray(f_third.read())
                    count = 0
                    for i in range(len(original_data)):
                        if original_data[i] != edited_data[i]:
                            third_data[i] = edited_data[i]
                            count += 1
                    f_third.seek(0)
                    f_third.write(third_data)
                    f_third.truncate()

            # Save the modified third file to a new location
            save_path = filedialog.asksaveasfilename(filetypes=[("Binary Files", "*.bin")], initialfile=self.third_file.split("/")[-1])
            if save_path:
                shutil.copy(temp_third_file, save_path)
                messagebox.showinfo("Success", f"Comparison and generation completed successfully. {count} changes. Third file saved as {save_path}.", parent=self.root)
            else:
                messagebox.showwarning("Warning", "Save operation canceled. The temporary file remains.", parent=self.root)

            # Cleanup: Delete the temporary file
            if os.path.exists(temp_third_file):
                os.remove(temp_third_file)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}", parent=self.root)


if __name__ == "__main__":
    root = tk.Tk()
    app = BinaryFileComparer(root)
    root.mainloop()
