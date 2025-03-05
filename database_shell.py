import os
import sys 
from database import Database

class Reader:
    def __init__(self): 
        print("Welcome to the shell!")
        self.db = Database()
        self.isOpen = True
        self.commands = {
            "FIND": self.db.search_file,
            "ADD": self.db.add_entry,
            "EXISTS": self.db.exists,
            "DEL": self.db.remove_entry,
            "FIND PERFECT": self.db.search_exact_case,
            "FIND ALL": self.db.search_all_tables,
            "FIND ALL PERFECT": self.db.search_all_exact_case,
            'CREATE TABLE': self.db.add_table,
            'DELETE TABLE': self.db.remove_table,
        }   
        self.modifiers ={
            "AND": self.checkAnd,
            "OR": self.checkOr,
            "NOT": self.db.checkNot,
            "AND OR": self.checkAndOr,
        }
        self.tables = []
        self.ids = []
        self.entries = []
        #FIND * WHERE * HAS 1140 AND 1141

    def getInput(self):
        while True:
            curr = input("Enter a command: ")
            cmd = curr.split(" ")
            for i in range(len(cmd)):
                    self.parseInput(cmd)
                    break
            
    def checkAnd(self,inp1,inp2):
        for inp in inp2:
            if inp not in inp1:
                inp1.remove(inp)
        return [inp1 + inp2]

    def checkOr(self,inp1,inp2):
        for inp in inp2:
            if inp in inp1:
                inp1.remove(inp)
        return [inp1 + inp2]

    def checkNot(self,type,inp):
        self.db.checkNot(inp,type)
        
    def checkAndOr(self,inp1,inp2):
        return [self.checkAnd(inp1,inp2) + self.checkOr(inp1,inp2)]
    
    def parseInput(self,cmd):
        fcmd = []
        cmdparam = []
        tempparam = []
        for i in range(len(cmd)): 
            if cmd[i] == "FIND" and cmd[i + 1] == "PERFECT":
                fcmd[i] = "FIND PERFECT"
            if cmd[i] == "FIND" and cmd[i + 1] == "ALL" and cmd[i + 2] == "PERFECT":
                fcmd[i] = "FIND ALL PERFECT"
            if cmd[i] == "CREATE" and cmd[i + 1] == "TABLE":
                fcmd[i] = "CREATE TABLE"
            if cmd[i] == "DELETE" and cmd[i + 1] == "TABLE":
                fcmd[i] = "DELETE TABLE"
            if cmd[i] == "IS" and cmd[i + 1] == "NOT":
                fcmd[i] = "IS NOT"
            if cmd[i] == "AND" and cmd[i + 1] == "OR":
                fcmd[i] = "AND OR"
            elif cmd[i]  not in self.modifiers.keys and cmd[i] not in self.commands.keys():
                while cmd[i] not in self.modifiers.keys and cmd[i] not in self.commands.keys():
                    tempparam += cmd[i]
                cmdparam[i] = [tempparam]
    
    def nextkeyword(self,fcmd,curr_pos):
        i = curr_pos+1
        keywords = [self.modifiers.keys(), + self.commands.keys()]
        for i in range(len(fcmd)):
            if fcmd[i] in keywords: 
                return [fcmd[i],i]
    
    def readInput(self,fcmd,cmdparam):
        cmdctr = 0
        for i in range(len(fcmd)):
            if fcmd[i] in self.commands.keys():
                cmdctr += 1 
                if fcmd[i] == "FIND" and self.nextkeyword(fcmd,i) == "IN":
                   self.commands["FIND"](cmdparam[cmdctr],cmdparam[cmdctr+1]) 
                   cmdctr += 1
                if fcmd[i] == "ADD" and self.nextkeyword(fcmd,i) == "TO":
                    self.commands["ADD"](cmdparam[cmdctr],cmdparam[cmdctr+1])
                    cmdctr += 1
                if fcmd[i] == "EXISTS" and self.nextkeyword(fcmd,i) == "IN":
                    self.commands["EXISTS"](cmdparam[cmdctr],cmdparam[cmdctr+1])
                    cmdctr += 1
                if fcmd[i] == "DEL" and self.nextkeyword(fcmd,i) == "FROM":
                    self.commands["DEL"](cmdparam[cmdctr],cmdparam[cmdctr+1]) 
                    cmdctr += 1
                if fcmd[i] == "FIND PERFECT" and self.nextkeyword(fcmd,i) == "IN":
                    self.commands["FIND PERFECT"](cmdparam[cmdctr],cmdparam[cmdctr+1])
                    cmdctr += 1
                if fcmd[i] == "FIND ALL" and self.nextkeyword(fcmd,i) == "IN":
                    self.commands["FIND ALL"](cmdparam[cmdctr],cmdparam[cmdctr+1])
                    cmdctr += 1
                if fcmd[i] == "FIND ALL PERFECT" and self.nextkeyword(fcmd,i) == "IN":
                    self.commands["FIND ALL PERFECT"](cmdparam[cmdctr],cmdparam[cmdctr+1])
                    cmdctr += 1
                if fcmd[i] == "IS" and self.nextkeyword(fcmd,i) == "IN":
                    self.commands["IS"](cmdparam[cmdctr],cmdparam[cmdctr+1])
                    cmdctr += 1
                if fcmd[i] == "IS NOT" and self.nextkeyword(fcmd,i) == "IN":
                    self.commands["IS NOT"](cmdparam[cmdctr],cmdparam[cmdctr+1])
                    cmdctr += 1
                else:
                    self.commands[fcmd[i]](cmdparam[cmdctr])


if __name__ == "__main__":
    print("="*60)
    print("DATABASE SHELL DEMONSTRATION")
    print("="*60)
    
    # Initialize the Reader
    r = Reader()
    db = r.db
    
    # Sample data for demonstration
    print("\n[1] Creating sample tables...")
    tables = ["CU", "PR", "OR", "SU"]
    for table in tables:
        db.add_table(table)
    print(f"Created {len(tables)} tables: {', '.join(tables)}")
    
    # Add sample entries to tables
    print("\n[2] Adding sample entries to tables...")
    entries = [
        ("John Smith customer record", "CU"),
        ("Jane Doe premium customer", "CU"),
        ("Laptop product 15-inch", "PR"),
        ("Smartphone product with 5G", "PR"),
        ("Order #12345 for John Smith", "OR"),
        ("Order #67890 for Jane Doe", "OR"),
        ("Support ticket for John Smith", "SU"),
        ("Support ticket for product issue", "SU")
    ]
    
    for entry, table in entries:
        db.add_entry(entry, table)
        print(f"✓ Added to {table}: {entry}")
    
    # Force file to be written
    db.file.flush()
    
    # Search for entries
    print("\n[3] Searching for 'John Smith'...")
    results = db.search_file("John Smith", None)
    print(f"Found {len(results)} results:")
    for i, result in enumerate(results, 1):
        table_code = result[4:6] if len(result) > 6 else "??"
        content = result[6:50] + "..." if len(result) > 50 else result[6:]
        print(f"  {i}. [Table {table_code}] {content}")
    
    # Search in specific table
    print("\n[4] Searching for 'customer' in 'CU' table...")
    results = db.search_file("customer", "CU")
    print(f"Found {len(results)} results in CU table:")
    for i, result in enumerate(results, 1):
        content = result[6:50] + "..." if len(result) > 50 else result[6:]
        print(f"  {i}. {content}")
    
    # Exact search
    print("\n[5] Exact search for 'product'...")
    results = db.search_exact_case("product", None)
    print(f"Found {len(results)} exact matches:")
    for i, result in enumerate(results, 1):
        table_code = result[4:6] if len(result) > 6 else "??"
        content = result[6:50] + "..." if len(result) > 50 else result[6:]
        print(f"  {i}. [Table {table_code}] {content}")
    
    # Search across all tables
    print("\n[6] Searching for 'Jane' across all tables...")
    results = db.search_all_tables("Jane")
    print(f"Found {len(results)} results across all tables:")
    for i, result in enumerate(results, 1):
        table_code = result[4:6] if len(result) > 6 else "??"
        content = result[6:50] + "..." if len(result) > 50 else result[6:]
        print(f"  {i}. [Table {table_code}] {content}")
    
    # Check if entry exists
    print("\n[7] Checking if entries exist...")
    check_entries = [
        ("John Smith", "CU"),
        ("nonexistent", "CU")
    ]
    
    for entry, table in check_entries:
        exists = db.exists(entry, table)
        status = "✓ EXISTS" if exists else "✗ DOES NOT EXIST"
        print(f"  '{entry}' in table '{table}': {status}")
    
    # Remove an entry and verify
    print("\n[8] Removing an entry...")
    entry_to_remove = "Jane Doe"
    print(f"Before removal - searching for '{entry_to_remove}':")
    before_results = db.search_file(entry_to_remove, None)
    print(f"  Found {len(before_results)} entries")
    
    # Remove the entry
    db.remove_entry(entry_to_remove)
    
    print(f"After removal - searching for '{entry_to_remove}':")
    after_results = db.search_file(entry_to_remove, None)
    print(f"  Found {len(after_results)} entries")
    
    # Display all tables
    print("\n[9] Current tables:")
    all_tables = db.getTables()
    for i, table in enumerate(db.tables, 1):
        print(f"  {i}. {table}")
    
    # Clean up and exit
    print("\n[10] Cleaning up...")
    db.file.close()
    print("Database file closed")
    
    print("\n" + "="*60)
    print("DEMONSTRATION COMPLETE")
    print("="*60)
    
    # Now start the interactive shell
    print("\nStarting interactive shell...")
    r.getInput()





