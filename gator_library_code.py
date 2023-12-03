import sys
import time

class Book:
    def __init__(self, book_id, book_name, author_name, availability_status, borrowed_by, reservation_heap):
     # Initialize a Node representing a book in the library with its attributes and status.
        self.book_id = book_id
        self.book_name = book_name
        self.author_name = author_name
        self.availability_status = availability_status
        self.borrowed_by = borrowed_by
        self.reservation_heap = reservation_heap
        self.color = 'black'
        self.parent = None
        self.left = None
        self.right = None

    
    def __repr__(self):
    # Provide a string representation of the node, detailing its key attributes.
        if self.book_id is None:
            return "NIL Node"
        return (f"Node(book_id={self.book_id}, book_name='{self.book_name}', "
                f"author_name='{self.author_name}', availability_status={self.availability_status}, "
                f"borrowed_by={self.borrowed_by}, reservations={list(self.reservation_heap.heap)})")
class Minimum_Heap:
    def __init__(self):
        # Initialize an empty heap.
        self.heap = []

    def insert(self, a):
         # Insert an element into the heap and maintain the min-heap property.
        self.heap.append(a)
        self._bubble_up(len(self.heap) - 1)

    def extractMinimum(self):
        # Remove and return the smallest element from the heap.
        if not self.heap:
            raise IndexError("Extracting from an empty heap is not allowed.")
        min_val = self.heap[0]
        if len(self.heap) > 1:
            self.heap[0] = self.heap.pop()
            self._min_heapify(0)
        else:
            self.heap.pop()
        return min_val

    def Heapify(self, index):
        # Helper method to maintain the min-heap property from a given index downwards.
        smallest = index
        left_child = 2 * index + 1
        right_child = 2 * index + 2

        if left_child < len(self.heap) and self.heap[left_child] < self.heap[smallest]:
            smallest = left_child

        if right_child < len(self.heap) and self.heap[right_child] < self.heap[smallest]:
            smallest = right_child

        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._min_heapify(smallest)

    def BubbleUp(self, index):
        # Helper method to adjust the heap upwards, maintaining the min-heap property.
        parent_index = (index - 1) // 2
        if index > 0 and self.heap[index] < self.heap[parent_index]:
            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
            self._bubble_up(parent_index)

class Red_Black_Tree:
    def __init__(self):
        # Initialize the Red-Black Tree with a NIL node as the root and set its color to black.
        self.NIL = Book(None, None, None, None, None, Minimum_Heap())
        self.NIL.color = 'black'
        self.NIL.left = self.NIL
        self.NIL.right = self.NIL
        self.NIL.parent = self.NIL
        self.root = self.NIL
        self.insert_helper_count = 0
        
    def minimum_value(self, node):
        # Find the node with the minimum value in the subtree rooted at the given node.
            while node.left != self.NIL:
                node = node.left
            return node
        
    
    def transplant_value(self, a, b):
        if a.parent == None:
            self.root = b
        elif a == a.parent.left:
            a.parent.left = b
        else:
            a.parent.right = b
        b.parent = a.parent
    
    def delete(self, z):
        # Delete a node z from the Red-Black Tree and maintain its properties.
        
            if z is None or z == self.NIL:
                return  # Ensure we're not trying to delete a None or NIL node
            
            y = z
            y_original_color = y.color
            if z.left == self.NIL:
                x = z.right
                if x != self.NIL:  # Check if x is not NIL before transplant
                    self.transplant_value(z, z.right)
            elif z.right == self.NIL:
                x = z.left
                if x != self.NIL:  # Check if x is not NIL before transplant
                    self.transplant_value(z, z.left)
            else:
                y = self.minimum_value(z.right)
                y_original_color = y.color
                x = y.right
                if y.parent == z:
                    x.parent = y
                else:
                    self.transplant_value(y, y.right)
                    y.right = z.right
                    y.right.parent = y
                self.transplant_value(z, y)
                y.left = z.left
                y.left.parent = y
                y.color = z.color
                if x != self.NIL:  # Check if x is not NIL before setting parent
                    x.parent = y
            if y_original_color == 'black':
                self.delete_helper(x if x != self.NIL else self.root)
        
    
    
    def delete_helper(self, x):
        # Adjust the tree after deletion to maintain Red-Black Tree properties.
        
            while x != self.root and x.color == 'black':
                if x == x.parent.left:
                    w = x.parent.right
                    if w and w.color == 'red':
                        # Perform color flips and rotations to rebalance the tree.
                        self.flip_color(w)  # Color flip
                        self.flip_color(x.parent)  # Color flip
                        self.insert_helper_count += 3
                        self.rotate_left(x.parent)
                        w = x.parent.right
                    if w and w.left.color == 'black' and w.right.color == 'black':
                        self.flip_color(w)
                        self.insert_helper_count += 3
                        x = x.parent
                    else:
                        if w.right.color == 'black':
                            self.flip_color(w.left)
                            self.flip_color(w)
                            self.insert_helper_count += 2
                            self.rotate_right(w)
                            w = x.parent.right
                        self.flip_color(w)
                        w.color = x.parent.color
                        self.flip_color(x.parent)  # Color flip
                        self.flip_color(w.right)  # Color flip
                        self.insert_helper_count += 3  # Increment for each flip
                        self.rotate_left(x.parent)
                        x = self.root
                else:
                    w = x.parent.left
                    if w.color == 'red':
                        self.flip_color(w)
                        self.flip_color(x.parent)
                        self.insert_helper_count += 3
                        self.rotate_right(x.parent)
                        w = x.parent.left

                    if w.right.color == 'black' and w.left.color == 'black':
                        self.flip_color(w)
                        self.insert_helper_count += 2
                        x = x.parent
                    else:
                        if w.left.color == 'black':
                            self.flip_color(w.right)
                            self.flip_color(w)
                            self.insert_helper_count += 3
                            self.rotate_left(w)
                            w = x.parent.left

                        self.flip_color(w)
                        w.color = x.parent.color
                        self.flip_color(x.parent)
                        self.flip_color(w.left)
                        self.insert_helper_count += 2
                        self.rotate_right(x.parent)
                        x = self.root
        
            self.flip_color(x)  # Final color flip to ensure black root
            self.insert_helper_count += 1
        
    
    def flip_color(self, node):
        
        if node is not None and node != self.NIL:
            original_color = node.color
            node.color = 'black' if node.color == 'red' else 'red'
        


    def insert(self, node):
        # Insert a node into the Red-Black Tree and fix the tree to maintain its properties.
            y = None
            x = self.root
            while x != self.NIL:
                y = x
                if node.book_id < x.book_id:
                    x = x.left
                else:
                    x = x.right
            node.parent = y
            if y is None:
                self.root = node
            elif node.book_id < y.book_id:
                y.left = node
            else:
                y.right = node
            node.left = self.NIL
            node.right = self.NIL
            node.color = 'red'
            self.fix_insert(node)
        

    def _insert_helper(self, node):
        # Fix the tree after insertion to maintain Red-Black Tree properties.
            while node != self.root and node.parent.color == 'red':
                if node.parent == node.parent.parent.left:
                    uncle = node.parent.parent.right
                    if uncle.color == 'red':
                        # Flipping colors of parent, uncle, and grandparent
                        self.flip_color(node.parent)
                        self.flip_color(uncle)
                        self.flip_color(node.parent.parent)
                        self.insert_helper_count += 3  # Count this set of flips
                        node = node.parent.parent
                    else:
                        if node == node.parent.right:
                            node = node.parent
                            self.rotate_left(node)
                        self.flip_color(node.parent)  # Color flip
                        self.flip_color(node.parent.parent)  # Color flip
                        self.insert_helper_count += 2  # Increment for each flip
                        self.rotate_right(node.parent.parent)
                else:
                    uncle = node.parent.parent.left
                    if uncle.color == 'red':
                        # Flipping colors of parent, uncle, and grandparent
                        self.flip_color(node.parent)
                        self.flip_color(uncle)
                        self.flip_color(node.parent.parent)
                        self.insert_helper_count += 3
                        node = node.parent.parent
                    else:
                        if node == node.parent.left:
                            node = node.parent
                            self.rotate_right(node)
                        self.flip_color(node.parent)  # Color flip
                        self.flip_color(node.parent.parent)  # Color flip
                        self.insert_helper_count += 2
                        self.rotate_left(node.parent.parent)
            
    

    def rotate_left(self, x):
        # Perform a left rotation around a given node.
            if x is None or x.right is None:
                return "Error: 'None' node encountered in rotate_left"

            y = x.right
            x.right = y.left
            if y.left is not None:
                y.left.parent = x

            y.parent = x.parent
            if x.parent is None:
                self.root = y
            elif x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y

            y.left = x
            x.parent = y
            return "rotate_left executed successfully"
        

    def rotate_right(self, y):
        # Perform a right rotation around a given node.

            if y is None or y.left is None:
                return "Error: 'None' node encountered in rotate_right"

            x = y.left
            y.left = x.right
            if x.right is not None:
                x.right.parent = y

            x.parent = y.parent
            if y.parent is None:
                self.root = x
            elif y == y.parent.right:
                y.parent.right = x
            else:
                y.parent.left = x

            x.right = y
            y.parent = x
            return "rotate_right executed successfully"
        

    
    def print_books_range(self, book_id1, book_id2):
        # Print the details of books in a specified range of IDs.
        book_details_list = []
        self._print_books_range(self.root, book_id1, book_id2, book_details_list)
        return book_details_list
    
    def _print_books_range(self, node, book_id1, book_id2, book_details_list):
        # Helper method to traverse the tree and collect book details in the specified range.

            if node is not None and node != self.NIL:
                if book_id1 < node.book_id:
                    self._print_books_range(node.left, book_id1, book_id2, book_details_list)
                if book_id1 <= node.book_id <= book_id2:
                    # Extract only the patron IDs from the reservations heap
                    reservations = [str(res[2]) for res in node.reservation_heap.heap] if node.reservation_heap.heap else []
                    # Format the book details as a multi-line string
                    book_details = (
                        f"BookID = {node.book_id}\n"
                        f"Title = \"{node.book_name}\"\n"
                        f"Author = \"{node.author_name}\"\n"
                        f"Availability = {'Yes' if node.availability_status else 'No'}\n"
                        f"BorrowedBy = {node.borrowed_by if node.borrowed_by else 'None'}\n"
                        f"Reservations = [{', '.join(reservations)}]\n"
                    )
                    book_details_list.append(book_details)
                if book_id2 > node.book_id:
                    self._print_books_range(node.right, book_id1, book_id2, book_details_list)
        


    def search(self, node, book_id):
         # Search for a book by its ID in the tree.
            if node is None or node == self.NIL or book_id == node.book_id:
                return node
            if book_id < node.book_id:
                return self.search(node.left, book_id)
            else:
                return self.search(node.right, book_id)
        


class GatorLibraryUFL:

    def __init__(self):
        # Initialize the library with a Red-Black Tree to store book data and a counter for color flips.
        self.rb_tree = Red_Black_Tree()
        self.color_flip_count = 0  # To keep track of color flip counts during insertions
    
        
    def read_commands_from_file(self, input_filename):
         # Read and return a list of commands from the specified input file.
            with open(input_filename, 'r') as file:
                commands = file.readlines()
            return commands


    def write_output_to_file(self, output_filename, output_lines):
        # Write given output lines to the specified output file.
        with open(output_filename, 'w') as file:
            for line in output_lines:
                file.write(line + '\n')

    def insert_book(self, book_id, book_name, author_name, availability_status):
        
            # Insert book into the Red-Black Tree
            new_book = Book(book_id, book_name, author_name, availability_status, None, Minimum_Heap())
            self.rb_tree.insert(new_book)
            self.color_flip_count += self.rb_tree.insert_helper_count  # Update color flip count
            self.rb_tree.insert_helper_count = 0  # Reset the fix-up count after the operation
            return ""
        
    

    def print_book(self, book_id):
            # Print details of the book with the given book_id
            node = self.rb_tree.search(self.rb_tree.root, book_id)
            if node and node != self.rb_tree.NIL:
                reservations = [str(reservation[2]) for reservation in node.reservation_heap.heap]  # Extract patron IDs
                formatted_reservations = f"[{', '.join(reservations)}]" if reservations else "[]"
                book_details = [
                    f"BookID = {node.book_id}",
                    f"Title = \"{node.book_name}\"",
                    f"Author = \"{node.author_name}\"",
                    f"Availability = {'Yes' if node.availability_status else 'No'}",
                    f"BorrowedBy = {node.borrowed_by if node.borrowed_by else 'None'}",
                    f"Reservations = {formatted_reservations}\n"  # Use the adjusted reservations list
                ]
                return '\n'.join(book_details)
            else:
                return "BookID not found in the Library\n"
       
        
    def print_books(self, book_id1, book_id2):
        # This method will call a method on the RBTree to print the details
        # of all books within the given range.
        if book_id1 > book_id2:
            return "Invalid range: Starting ID is greater than ending ID.\n"

        # Call the helper function on the RBTree with the provided range
        book_details_list = self.rb_tree.print_books_range(book_id1, book_id2)

        # Convert the list of book details into a formatted string
        output_str = "\n".join(book_details_list)
        return output_str


    def borrow_book(self, patron_id, book_id, patron_priority):
        node = self.rb_tree.search(self.rb_tree.root, book_id)
        if not node:
            return "BookID not found in the Library\n"

        # Check if the book is already borrowed by the same patron
        if node.borrowed_by == patron_id:
            return f"Book {book_id} Already Borrowed by Patron {patron_id}\n"

        # Check if the book is available for borrowing
        if node.availability_status:
            node.availability_status = False
            node.borrowed_by = patron_id
            self.color_flip_count += self.rb_tree.insert_helper_count
            self.rb_tree.insert_helper_count = 0 
            return f"Book {book_id} Borrowed by Patron {patron_id}\n"

        # Check reservation limit
        if len(node.reservation_heap.heap) >= 20:
            return f"Unable to reserve book {book_id} for Patron {patron_id}; reservation limit reached.\n"

        # Add patron to the reservation heap
        timestamp = time.time()  # Use timestamp for FIFO order among same-priority reservations
        node.reservation_heap.insert((patron_priority, timestamp, patron_id))
        return f"Book {book_id} Reserved by Patron {patron_id}\n"
        

    def return_book(self, patron_id, book_id):
        node = self.rb_tree.search(self.rb_tree.root, book_id)
        if not node or node == self.rb_tree.NIL:
            return "BookID not found in the Library\n"

        # Check if the book is currently borrowed by the given patron
        if not node.availability_status and node.borrowed_by == patron_id:
            # Process the next reservation, if any
            if node.reservation_heap.heap:
                next_patron_info = node.reservation_heap.extractMinimum()
                next_patron = next_patron_info[2]
                node.borrowed_by = next_patron
                return f"Book {book_id} returned by Patron {patron_id}\nBook {book_id} allotted to Patron {next_patron}\n"
            else:
                # Make the book available if there are no reservations
                self.color_flip_count += self.rb_tree.insert_helper_count  # Update color flip count
                self.rb_tree.insert_helper_count = 0  # Reset the fix-up count after the operation

                node.availability_status = True
                node.borrowed_by = None
                return f"Book {book_id} returned by Patron {patron_id}\n"
              
        else:
            return "Return operation failed. Either the book is not borrowed or it is borrowed by another patron.\n"
        

            
    def find_closest_book(self, target_id):
        closest_books = self._find_closest_book(self.rb_tree.root, target_id, [])
        if closest_books:
            closest_books.sort(key=lambda book: book.book_id)
            return "\n".join([self.print_book(book.book_id) for book in closest_books])
        else:
            return "No books available in the library\n"
        

    def _find_closest_book(self, node, target_id, closest_books):
        
        if node is None or node == self.rb_tree.NIL:
            return closest_books

        if not closest_books:
            closest_books.append(node)
        else:
            current_distance = abs(target_id - node.book_id)
            closest_distance = abs(target_id - closest_books[0].book_id)

            if current_distance < closest_distance:
                closest_books = [node]
            elif current_distance == closest_distance:
                closest_books.append(node)

        if node.book_id < target_id:
            # Check right subtree
            closest_books = self._find_closest_book(node.right, target_id, closest_books)
        else:
            # Check left subtree
            closest_books = self._find_closest_book(node.left, target_id, closest_books)

        return closest_books

    
    
    def delete_book(self, book_id):
        node = self.rb_tree.search(self.rb_tree.root, book_id)
        if node is not None and node != self.rb_tree.NIL:
            # Notify patrons if there are active reservations
            if node.reservation_heap.heap:
                patrons_to_notify = [str(heap_node[2]) for heap_node in node.reservation_heap.heap]
                node.reservation_heap.heap = []  # Clear reservations
                self.rb_tree.delete(node)
                self.color_flip_count += self.rb_tree.insert_helper_count
                self.rb_tree.insert_helper_count = 0  # Reset the fix-up count
                return f"Book {book_id} is no longer available. Reservations made by Patrons {','.join(patrons_to_notify)} have been cancelled!\n"
            
            else:
                # Delete the book if there are no reservations
                self.rb_tree.delete(node)
                self.color_flip_count += self.rb_tree.insert_helper_count
                self.rb_tree.insert_helper_count = 0 
                return f"Book {book_id} is no longer available.\n"
        else:
            return "BookID not found in the Library.\n"

    def operation(self, command):
         # Parse and execute a given command string, handling various library operations.
        
        try:
            parts = command.strip().replace(')', '(').split('(')
            operation_ = parts[0].strip()
            args = [arg.strip().strip('"') for arg in parts[1].split(',') if arg]

            if operation_ == 'InsertBook':
                args = parts[1].split(',', 3) 
                args = [arg.strip().strip('"') for arg in args]
                try:
                    book_id = int(args[0])
                    book_name = args[1]
                    author_name = args[2]
                    availability_status = args[3] == 'Yes'
                except (ValueError, IndexError) as e:
                    return f"Error in InsertBook arguments: {e}", True
                return self.insert_book(book_id, book_name, author_name, availability_status), True

            elif operation_ == 'PrintBook':
                book_id = int(args[0])
                return self.print_book(book_id), True
            
            elif operation_ == 'BorrowBook':
                patron_id = int(args[0])
                book_id = int(args[1])
                patron_priority = int(args[2])
                return self.borrow_book(patron_id, book_id, patron_priority), True
            
            elif operation_ == 'PrintBooks':
                # Assuming parts[0] is something like 'PrintBooks(1' and parts[1] is something like ' 2)'
                book_id1 = int(args[0].strip())
                book_id2 = int(args[1].strip())
                return self.print_books(book_id1, book_id2), True

            elif operation_ == 'ReturnBook':
                # Ensure the command is split correctly
                args = [arg.strip().strip('"') for arg in parts[1].split(',')]
                if len(args) < 2:
                    return "Error: Not enough arguments for ReturnBook", True
                try:
                    patron_id = int(args[0].strip())
                    book_id = int(args[1].strip())
                except ValueError as e:
                    return f"Error in ReturnBook arguments: {e}", True
                return self.return_book(patron_id, book_id), True
                
            elif operation_ == 'FindClosestBook':
                target_id_str = command.split('(')[1].split(')')[0].strip()
                # Check if the '(' and ')' are present and properly formatted
                try:
                    # Extract the number within the parentheses
                    target_id = int(target_id_str)
                    # Attempt to convert the string to an integer
                    target_id = int(target_id_str)
                except (ValueError, IndexError) as e:
                    return f"Error parsing target ID for FindClosestBook: {e}", True

                return self.find_closest_book(target_id), True
                
            elif operation_ == 'DeleteBook':
                book_id = int(args[0])
                # return book_id
                return self.delete_book(book_id), True
                
            elif operation_ == 'ColorFlipCount':
                return f"Colour Flip Count: {self.color_flip_count}", True
                
            elif operation_ == 'Quit':
                return "Program Terminated!!", False  # Signal to stop command execution
            else:
                return f"Unknown command: {operation_}", True  # Continue command execution with result
        
        except Exception as e:
            return f"", True  # Continue command execution with error message
    


    def read_commands_from_file(self, input_filename):
        try:
            with open(input_filename, 'r', encoding='utf-8') as file:
                commands = file.readlines()
            return commands
        except IOError as e:
            return []

    def write_output_to_file(self, output_filename, output_lines):
        with open(output_filename, 'w') as file:
            for line in output_lines:
                file.write(line + '\n')


if __name__ == "__main__":
    import sys

    # Check if the correct number of arguments is given
    if len(sys.argv) != 2:
        print("Usage: python gator_library_code.py <input_filename>")
        sys.exit(1)

    # Get the input filename from command line argument
    input_filename = sys.argv[1]
    # Determine the output filename based on the input filename
    output_filename = input_filename.split('.')[0] + "_output_file.txt"
    
    # Instantiate the library system
    library_system = GatorLibraryUFL()

    # Read commands from the input file
    commands = library_system.read_commands_from_file(input_filename)
    output_lines = []

    # Execute each command and collect the results
    for command in commands:
        result, continue_execution = library_system.operation(command.strip())
        if not continue_execution:
            output_lines.append(result)
            break
        output_lines.append(result)

    # Write the results to the output file
    library_system.write_output_to_file(output_filename, output_lines)

