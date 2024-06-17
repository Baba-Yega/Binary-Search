import tkinter as tk
from tkinter import messagebox
from anytree import Node, RenderTree, AnyNode
from anytree.exporter import DotExporter
from anytree.search import findall_by_attr
from subprocess import check_call
from PIL import Image, ImageTk
import io

class BST:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    # function to add input to BST
    def add(self, value):
        if value < self.value:
            if self.left is None:
                self.left = BST(value)
            else:
                self.left.add(value)
        else:
            if self.right is None:
                self.right = BST(value)
            else:
                self.right.add(value)

    # function to search for value in BST
    def search(self, value):
        if self.value == value:
            return True
        elif value < self.value:
            if self.left is None:
                return False
            else:
                return self.left.search(value)
        else:
            if self.right is None:
                return False
            else:
                return self.right.search(value)
    
    # function to delete value from BST
    def delete(self, value):
        if self.value == value:
            if self.left is None and self.right is None:
                return None
            elif self.left is None:
                return self.right
            elif self.right is None:
                return self.left
            else:
                min_right = self.right.find_min()
                self.value = min_right.value
                self.right = self.right.delete(min_right.value)
        elif value < self.value:
            self.left = self.left.delete(value)
        else:
            self.right = self.right.delete(value)
        return self

    def find_min(self):
        if self.left is None:
            return self
        else:
            return self.left.find_min()

    # function to perform preorder traversal
    def preorder(self):
        res = []
        res.append(self.value)
        if self.left is not None:
            res += self.left.preorder()
        if self.right is not None:
            res += self.right.preorder()
        return res
    
    # function to perform inorder traversal
    def inorder(self):
        res = []
        if self.left is not None:
            res += self.left.inorder()
        res.append(self.value)
        if self.right is not None:
            res += self.right.inorder()
        return res
    
    # function to perform posorder traversal
    def postorder(self):
        res = []
        if self.left is not None:
            res += self.left.postorder()
        if self.right is not None:
            res += self.right.postorder()
        res.append(self.value)
        return res

# class to create custom dialog box
class BinaryTreeViewDialog:
    def __init__(self, parent, image_data):
        self.top = tk.Toplevel(parent)
        self.top.title("Binary Tree View")
        self.top.geometry("400x400")
        self.image_data = image_data

        img = Image.open(io.BytesIO(self.image_data))
        tk_image = ImageTk.PhotoImage(img)
        image_label = tk.Label(self.top, image=tk_image)
        image_label.image = tk_image
        image_label.pack()

    def show(self):
        self.top.grab_set()
        self.top.wait_window()

# GUI class
class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Form 1")
        self.master.geometry("500x400")
        self.bst = None

        # ADD Section
        self.add_button = tk.Button(self.master, text="Add new Item", font=('bold', 14), command=self.add_button_clicked, width=15)
        self.add_button.grid(row=0, column=0, padx=10, pady= 20)
        self.entry_field = tk.Entry(self.master, width=25)
        self.entry_field.grid(row = 0, column= 1 ,pady= 20)
        
        # SEARCH SECTION
        self.search_button = tk.Button(self.master, text="Search Item", font=('bold', 14), command=self.search_button_clicked, width=15)
        self.search_button.grid(row=1, column=0)
        self.entry_search = tk.Entry(self.master, width=25)
        self.entry_search.grid(row = 1, column= 1, pady= 20)

        # DELETE SECTION
        self.delete_button = tk.Button(self.master, text="Delete Item",font=('bold', 14),  command=self.delete_button_clicked, width=15)
        self.delete_button.grid(row=2, column=0)
        self.entry_delete = tk.Entry(self.master, width=25)
        self.entry_delete.grid(row=2, column=1, pady=20 )

        # VIEW SECTION
        self.view_button = tk.Button(self.master, text='View Binary Tree', font=('bold', 14), command=self.view_button_clicked)
        self.view_button.grid(row=3, column=1, pady=20)
        
        # PREORDER SECTION
        self.preorder_button = tk.Button(self.master, text="Preorder\nTraversal", font=('bold', 14), height=2, width=10, command=self.preorder_button_clicked)
        self.preorder_button.grid(row=4, column=0, pady=20)

        # INORDER SECTION
        self.inorder_button = tk.Button(self.master, text="In-order\nTraversal", font=('bold', 14),  height=2, width=10, command=self.inorder_button_clicked)
        self.inorder_button.grid(row=4, column=1)
        
        # POSTORDER SECTION
        self.postorder_button = tk.Button(self.master, text="Postorder\nTraversal", font=('bold', 14), height=2, width=10, command=self.postorder_button_clicked)
        self.postorder_button.grid(row=4, column=2)

    # function called when new items added
    def add_button_clicked(self):
        values = self.entry_field.get().lower()
        values = values.split(',')
        self.bst = BST(values[0])
        for value in values[1:]:
            self.bst.add(value)
        messagebox.showinfo("Info", f"{values} added to the BST.")

    # function called when an entry is searched for
    def search_button_clicked(self):
        search_item = self.entry_search.get().lower()
        found = self.bst.search(search_item)
        if found:
            messagebox.showinfo("Info", f"{search_item} found in the BST.")
        else:
            messagebox.showinfo("Info", f"{search_item} not found in the BST.")
    
    # function called when an entry is deleted
    def delete_button_clicked(self):
        delete_item = self.entry_delete.get().lower()
        self.bst = self.bst.delete(delete_item)
        messagebox.showinfo("Info", f"{delete_item} deleted from the BST.")
    
    # function to view binary tree
    def view_button_clicked(self):
        if self.bst is None:
            messagebox.showerror("Error", "BST is empty.")
        else:
            root = AnyNode(name=str(self.bst.value))
            self._add_nodes(root, self.bst)
            DotExporter(root).to_dotfile("bst.dot")
            check_call(["dot", "-Tpng", "bst.dot", "-o", "bst.png"])
            with open("bst.png", "rb") as img:
                img_data = img.read()
                dialog = BinaryTreeViewDialog(self.master, img_data)
                dialog.show()

    def _add_nodes(self, parent, bst_node):
        if bst_node.left is not None:
            left_node = AnyNode(name=str(bst_node.left.value), parent=parent)
            self._add_nodes(left_node, bst_node.left)
        if bst_node.right is not None:
            right_node = AnyNode(name=str(bst_node.right.value), parent=parent)
            self._add_nodes(right_node, bst_node.right)

    def preorder_button_clicked(self):
        if self.bst is None:
            messagebox.showerror("Error", "BST is empty.")
        else:
            res = self.bst.preorder()
            # result = " ".join(map(str, self.bst.preorder()))
            messagebox.showinfo("Preorder Traversal", str(res))

    def inorder_button_clicked(self):
        if self.bst is None:
            messagebox.showerror("Error", "BST is empty.")
        else:
            res = self.bst.inorder()
            messagebox.showinfo("Inorder Traversal", str(res))

    def postorder_button_clicked(self):
        if self.bst is None:
            messagebox.showerror("Error", "BST is empty.")
        else:
            res = self.bst.postorder()
            messagebox.showinfo("Postorder Traversal", str(res))

root = tk.Tk()
gui = GUI(root)
root.mainloop()
# 15 12 7 14 27 20 23 88 