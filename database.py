import sqlite3


DATABASE_NAME = "home_inventory.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_tables():

    connection = get_connection()

    cursor = connection.cursor()

    # -------------------------
    # HOUSEHOLD ITEMS
    # -------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT,
            description TEXT
        )
        """
    )

    # -------------------------
    # REMINDER LISTS
    # -------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS lists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        """
    )

    # -------------------------
    # REMINDER LIST ITEMS
    # -------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS list_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            list_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            position INTEGER NOT NULL,
            FOREIGN KEY (list_id) REFERENCES lists(id)
            ON DELETE CASCADE
        )
        """
    )

    connection.commit()

    connection.close()


def add_item(name, location="", description=""):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO items (name, location, description)
        VALUES (?, ?, ?)
        """,
        (
            name,
            location,
            description,
        ),
    )

    connection.commit()

    item_id = cursor.lastrowid

    connection.close()

    return item_id


def get_items():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, name, location, description
        FROM items
        ORDER BY id DESC
        """
    )

    items = cursor.fetchall()

    connection.close()

    return items









def search_items(search_text=""):

    connection = get_connection()

    cursor = connection.cursor()

    if search_text.strip():

        cursor.execute(
            """
            SELECT id, name, location, description
            FROM items
            WHERE name LIKE ?
            ORDER BY id DESC
            """,
            (
                f"%{search_text.strip()}%",
            ),
        )

    else:

        cursor.execute(
            """
            SELECT id, name, location, description
            FROM items
            ORDER BY id DESC
            """
        )

    items = cursor.fetchall()

    connection.close()

    return items







def update_item(item_id, name, location="", description=""):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE items
        SET name = ?, location = ?, description = ?
        WHERE id = ?
        """,
        (
            name,
            location,
            description,
            item_id,
        )
    )

    connection.commit()
    connection.close()





def delete_item(item_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM items
        WHERE id = ?
        """,
        (item_id,)
    )

    connection.commit()
    connection.close()




def add_list_item(list_id, name, position):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO list_items (list_id, name, position)
        VALUES (?, ?, ?)
        """,
        (
            list_id,
            name,
            position,
        )
    )

    connection.commit()

    connection.close()




def create_list(name):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO lists (name)
        VALUES (?)
        """,
        (name,)
    )

    connection.commit()

    list_id = cursor.lastrowid

    connection.close()

    return list_id







def get_lists():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, name
        FROM lists
        ORDER BY id DESC
        """
    )

    lists = cursor.fetchall()

    connection.close()

    return lists







def get_list_items(list_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, name, position
        FROM list_items
        WHERE list_id = ?
        ORDER BY position ASC
        """,
        (list_id,)
    )

    items = cursor.fetchall()

    connection.close()

    return items




def delete_list_item(item_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM list_items
        WHERE id = ?
        """,
        (item_id,)
    )

    connection.commit()

    connection.close()



def update_list_item(item_id, new_name):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE list_items
        SET name = ?
        WHERE id = ?
        """,
        (new_name, item_id)
    )

    connection.commit()

    connection.close()


def delete_list(list_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM lists
        WHERE id = ?
        """,
        (list_id,)
    )

    connection.commit()

    connection.close()


def rename_list(list_id, new_name):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE lists
        SET name = ?
        WHERE id = ?
        """,
        (new_name, list_id)
    )

    connection.commit()

    connection.close()