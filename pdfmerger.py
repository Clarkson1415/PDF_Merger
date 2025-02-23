import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger
import threading

def add_pdfs():
    files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    for file in files:
        pdf_listbox.insert(tk.END, file)

def remove_selected():
    selected = pdf_listbox.curselection()
    for index in reversed(selected):  # Remove from bottom up to avoid index shift
        pdf_listbox.delete(index)

def move_up():
    selected = pdf_listbox.curselection()
    for i in selected:
        if i > 0:
            text = pdf_listbox.get(i)
            pdf_listbox.delete(i)
            pdf_listbox.insert(i - 1, text)
            pdf_listbox.selection_set(i - 1)

def move_down():
    selected = pdf_listbox.curselection()
    for i in reversed(selected):
        if i < pdf_listbox.size() - 1:
            text = pdf_listbox.get(i)
            pdf_listbox.delete(i)
            pdf_listbox.insert(i + 1, text)
            pdf_listbox.selection_set(i + 1)

def merge_pdfs():
    pdf_files = pdf_listbox.get(0, tk.END)
    if not pdf_files:
        messagebox.showerror("Error", "No PDFs selected!")
        return

    output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not output_path:
        return

    # Create a loading popup window
    loading_popup = tk.Toplevel(root)
    loading_popup.title("Merging PDFs...")
    tk.Label(loading_popup, text="Merging PDFs, please wait...").pack(padx=20, pady=20)
    loading_popup.geometry("300x100")
    loading_popup.transient(root)
    loading_popup.grab_set()
    loading_popup.update()

    def merge_thread():
        try:
            merger = PdfMerger()
            for pdf in pdf_files:
                merger.append(pdf)
            merger.write(output_path)
            merger.close()
            success = True
            error = ""
        except Exception as e:
            success = False
            error = str(e)
        # Schedule finishing function on main thread
        root.after(0, finish_merge, success, error)

    def finish_merge(success, error):
        loading_popup.destroy()
        if success:
            messagebox.showinfo("Success", f"PDFs merged successfully!\nSaved to: {output_path}")
        else:
            messagebox.showerror("Error", f"An error occurred:\n{error}")

    # Start merging in a separate thread
    threading.Thread(target=merge_thread).start()

# Create main window
root = tk.Tk()
root.title("PDF Combiner with Ordering")

# Listbox to display selected PDFs
pdf_listbox = tk.Listbox(root, selectmode=tk.SINGLE)
pdf_listbox.pack(pady=10, fill=tk.X, expand=True)

# Buttons for PDF actions
btn_frame = tk.Frame(root)
btn_frame.pack()

btn_add = tk.Button(btn_frame, text="Add PDFs", command=add_pdfs)
btn_add.grid(row=0, column=0, padx=5)

btn_remove = tk.Button(btn_frame, text="Remove Selected", command=remove_selected)
btn_remove.grid(row=0, column=1, padx=5)

btn_up = tk.Button(btn_frame, text="Move Up", command=move_up)
btn_up.grid(row=0, column=2, padx=5)

btn_down = tk.Button(btn_frame, text="Move Down", command=move_down)
btn_down.grid(row=0, column=3, padx=5)

btn_merge = tk.Button(root, text="Merge PDFs", command=merge_pdfs)
btn_merge.pack(pady=10)

root.mainloop()
