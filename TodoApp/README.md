# SQLite Terminal Usage

## Introduction

This documentation provides a step-by-step guide on how to use SQLite in the terminal. SQLite is a lightweight, file-based database management system that is widely used for small-scale applications.

## Prerequisites

Before getting started, ensure that you have SQLite installed on your system. You can download SQLite from the official website and follow the installation instructions specific to your operating system.

## Initiating SQLite

To initiate SQLite in the terminal, follow these steps:

1. Open your terminal or command prompt.
2. Navigate to the directory where your SQLite database file is located.
3. Run the following command to start the SQLite terminal:

3.1. To initiate the db
```
$ sqlite3 to-dos.db
```


3.2. To check the tables 
```
sqlite3> .schema
```

4. isert the data into the table:

```sql
-- Insert sample data
INSERT INTO todos (id, title, description, priority, complete) 
VALUES 
    (1, 'Example Todo 1', 'Description for Todo 1', 1, false),
    (2, 'Example Todo 2', 'Description for Todo 2', 2, true),
    (3, 'Example Todo 3', 'Description for Todo 3', 3, false);

```
5. Then, run the Query below, to see the data added:

```sql
select * from todo;
```

5.1. For better visualization use:
```
$ .mode box
```
