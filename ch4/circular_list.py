
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = None    
    
    def insert(self, data, position=None):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            new_node.next = new_node
            return
        
        current = self.head
        
        if position == 0:
            while current.next != self.head:
                current = current.next
            current.next = new_node
            new_node.next = self.head
            self.head = new_node
            return
        
        if position == None:
            while current.next != self.head:
                current = current.next
            current.next = new_node
            new_node.next = self.head
            return
        
        count = 0
        while count < position - 1 and current.next != self.head:
            current = current.next
            count += 1
        
        new_node.next = current.next
        current.next = new_node
        
    def delete(self, data):

        if self.head is None:
            return False

        if self.head.next == self.head and self.head.data == data:
            self.head = None
            return True
        
        if self.head.data == data:
            current = self.head
            while current.next != self.head:
                current = current.next
            
            current.next = self.head.next
            self.head = self.head.next
            return True

        current = self.head
        while current.next != self.head:
            if current.next.data == data:
                current.next = current.next.next
                return True
            current = current.next
        
        return False
    
    def display(self):

        if self.head is None:
            return
        
        current = self.head
        while True:
            print(f"[{current.data}]")
            
            current = current.next
    
            if current == self.head:
                break
        
    def is_empty(self):
        return self.head is None
    
    def clear(self):
        self.head = None

    def get_next(self, data):
        if self.head is None:
            return None
        
        current = self.head
        while True:
            if current.data == data:
                return current.next.data
            
            current = current.next
            if current == self.head:
                break
        
        return None

def main():
    circularlist = CircularLinkedList()
    circularlist.insert("Dynamite - BTS")
    circularlist.insert("APT. - 로제")
    circularlist.insert("Supernova - aespa")
    circularlist.insert("Love wins all - 아이유")

    circularlist.display()

    # 특정 곡의 다음 곡 확인
    print("🎵 다음 곡 확인:")
    current = "Dynamite - BTS"
    print(f"'{current}'의 다음 곡: {circularlist.get_next(current)}")

    current = "Love wins all - 아이유"
    print(f"'{current}'의 다음 곡: {circularlist.get_next(current)}")
    print()

if __name__ == "__main__":
    main()