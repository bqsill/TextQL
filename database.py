import random 
import getopt
import sys

class Database():
    def __init__(self):
        self.path = "" # Place the file to your data.txt here
        self.file = open(self.path, "w+")
        self.data = self.file.read()
        self.tables = []
        self.chunkinized_data = []

    
        
    #FORMAT LLLLXX(250T)
    def generate_entry(self,entry,table):
        return str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9))+ table + entry + ("0" * (250-len(entry)))
    
    def add_entry(self,entry,table):
        self.file.write(self.generate_entry(entry,table))
    
    def search_file(self, search_term, table=None):
        chunk_list = []
        self.file.seek(0)
        
        # Search in chunks of 256 characters
        chunk_size = 256
        results = []
        processed_positions = set()  # To avoid processing the same position multiple times
        
        while True:
            current_position = self.file.tell()
            
            # If we've already processed this position, break to avoid infinite loop
            if current_position in processed_positions:
                break
                
            processed_positions.add(current_position)
            
            chunk = self.file.read(chunk_size)
            if not chunk:
                break
                
            # Check if search term in current chunk
            if search_term in chunk:
                # Store the chunk for processing
                chunk_list.append((chunk, current_position))
        
        # Process all chunks with matches after reading file
        for chunk_data, chunk_pos in chunk_list:
            # Split chunk into lines
            lines = chunk_data.split('\n')
            for line in lines:
                if not line:  # Skip empty lines
                    continue
                    
                # Check if search term in line and table matches (if specified)
                if search_term in line and (table is None or (len(line) > 5 and line[4:6] == table)):
                    if line not in results:  # Avoid duplicates
                        results.append(line)
        
        return results

    def search_exact_case(self, search_term, table=None):
        chunk_list = []
        self.file.seek(0)
        
        # Search in chunks of 256 characters
        chunk_size = 256
        results = []
        processed_positions = set()
        
        while True:
            current_position = self.file.tell()
            
            # Prevent infinite loop
            if current_position in processed_positions:
                break
                
            processed_positions.add(current_position)
            
            chunk = self.file.read(chunk_size)
            if not chunk:
                break
                
            # Check if search term in current chunk
            if search_term in chunk:
                chunk_list.append((chunk, current_position))
        
        # Process all chunks with matches
        for chunk_data, chunk_pos in chunk_list:
            lines = chunk_data.split('\n')
            for line in lines:
                if not line:
                    continue
                # Check table code if specified
                if table is not None and (len(line) < 6 or line[4:6] != table):
                    continue
                # Get content part (after LLLLTT format)
                content = line[6:] if len(line) > 6 else ''
                # Split into words and look for exact match
                words = content.strip('0').split()
                if search_term in words:
                    if line not in results:
                        results.append(line)
        return results
    
    def search_all_tables(self,entry):
        chunk_size = 256
        self.tables = []
        results = []
        self.file.seek(0)
 
        num_chunks = len(self.data) / chunk_size
        for i in range(int(num_chunks)):
            chunk = self.file.read(chunk_size)
            if not chunk:
                break
            if entry in chunk:
                self.tables.append(chunk[4]+chunk[5])
         
        for table in self.tables:
            results.append(self.search_file(entry,table))
        return results

    def add_table(self,table):
        self.tables.append(table)
        print("Table added")
    
    def remove_table(self,table):
        self.tables.remove(table)
        for tables in self.tables:
            if tables == table:
                for chunk in self.file:
                    if chunk[4:6] == table:
                        chunk = ""
                        print("Table removed")
                        return
        print("Table not found")
    
    def remove_entry(self,entry):
        id = self.search_exact_case(entry)[0:4]
        for chunk in self.file:
            if chunk[0:4] == id:
                chunk = ""
                print("Entry removed")
                return
        print("Entry not found")
            
    def exists(self,entry,table):
        for chunk in self.file:
            if chunk[4:6] == table and chunk[6:] == entry:
                return True
        return False
    
    def checkNot(self,entry,type):
        if type == "TABLE":
            return [i for i in self.data if i[0:4] != entry]
        if type == "ID":
            return [i for i in self.data if i[4:6] != entry]
        return [i for i in entry if i[6:] != entry]

    def chunk_data(self):
        chunk_size = 256
        num_chunks = int(len(self.data) / chunk_size)
        for i in range(num_chunks):
            chunk = self.file.read(chunk_size)
            self.chunkinized_data += [chunk]

    def getTables(self):
        self.chunk_data()
        for chunk in self.chunkinized_data:
            self.tables.append(chunk[4:6])

    def search_all_exact_case(self,entry):
        for table in self.tables:
            self.search_exact_case(entry)