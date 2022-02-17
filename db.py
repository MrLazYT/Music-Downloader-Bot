import sqlite3

def connect(db_name):
    return sqlite3.connect(f".\data\{db_name}")

def create_table(table_name, columns, db):
    sql = db.cursor()
    
    sql.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    {columns}
                )
                """)
    
    db.commit()

def generate_id(table_name, db):
    sql = db.cursor()
    
    id = 0
    
    for i in sql.execute(f"""SELECT id FROM {table_name}"""):
        id = i[0] + 1
    
    return id

def insert_into_table(table_name, values, values_num, db):
    sql = db.cursor()
    
    id = generate_id(table_name, db)
    
    if id == 0:
        sql.execute(f"""
                    INSERT INTO {table_name} VALUES ({id}, {values})
                    """)
        
        db.commit()
        
        print("[INFO] Values added successfuly!")
    else:
        insert = True
        
        for value in sql.execute(f"""SELECT * FROM {table_name}"""):
            for i in range(0, values_num):
                if value[i + 1] in values:
                    print(f"[INFO] Cant to add this value: {value[i + 1]} because it was added!")
                    insert = False
        if insert:
            sql.execute(f"""
                INSERT INTO {table_name} VALUES ({id}, {values})
                """)
            
            db.commit()
            
            print("[INFO] Values added successfully!")

def select_all_from_table(table_name, column_num, db):
    sql = db.cursor()
    
    for values in sql.execute(f"""SELECT * FROM {table_name}"""):
        print("| ", end="")
        
        for column in range(0, column_num + 1):
            if column < column_num:
                print(values[column], end=" | ")
            else:
                print(values[column] + " |")

def select_from_table(table_name, column_name, db):
    sql = db.cursor()
    
    for value in sql.execute(f"""SELECT {column_name} FROM {table_name}"""):
        print(value[0])

def select_from_table_where_smtg(table_name, columns_name, condition, db):
    sql = db.cursor()
    
    find = False
    
    for value in sql.execute(f"""SELECT {columns_name} FROM {table_name} WHERE {condition}"""):
        print(value[0])
        find = True
    
    if find == False:
        print(f"[INFO] Cant find value with this condition: \"{condition}\"!")

def update_table(table_name, column_name, value, condition, db):
    sql = db.cursor()
    
    sql.execute(f"""
                UPDATE {table_name} SET {column_name} == {value} WHERE {condition}
                """)
    
    db.commit()
    
    print("[INFO] value updated successfully!")

def delete_table(table_name, db):
    sql = db.cursor()
    
    sql.execute(f"""
                DROP TABLE {table_name}
                """)
    
    db.commit()
    
    print(f"[INFO] Table: \"{table_name}\" deleted successfully!")