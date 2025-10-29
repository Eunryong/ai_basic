# linkedlist.py

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
    
    def insert(self, data, position=None):
        new_node = Node(data)
        
        if self.head is None or position == 0:
            new_node.next = self.head
            self.head = new_node
            return
        
        if position is None:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
            return
        
        current = self.head
        for i in range(position - 1):
            if current.next is None:
                break
            current = current.next
        
        new_node.next = current.next
        current.next = new_node
    
    def delete(self, data):
        if self.head is None:
            return False
        
        if self.head.data == data:
            self.head = self.head.next
            return True
        
        current = self.head
        while current.next is not None:
            if current.next.data == data:
                current.next = current.next.next
                return True
            current = current.next
        
        return False
    
    def display(self):
        if self.head is None:
            return
        
        current = self.head
        index = 0
        while current is not None:
            print(f"{current.data}")
            current = current.next
    
    def is_empty(self):
        return self.head is None
    
    def clear(self):
        self.head = None

def main():
    linkedlist = LinkedList()
    linkedlist.insert("Blue Valentine")
    linkedlist.insert("Good Goodbye")
    linkedlist.insert("Golden", 1)
    linkedlist.display()
    print()
    linkedlist.delete("Good Goodbye")
    linkedlist.display()
    print()
    linkedlist.clear()
    linkedlist.display()
    print()

if __name__ == "__main__":
    main()
