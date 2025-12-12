# iot-13-2025
My second repo with code for lab6.
# Lab 6: Python File Manager with Decorators

This project implements a robust `FileManager` class in Python designed to handle CSV-like data operations (reading, writing, appending). The key focus of this laboratory work is to demonstrate the use of **decorators**, **custom exceptions**, and **logging**.

## 📌 Features

- **Custom Decorator (`@logged`)**:
  - Wraps methods to catch and log exceptions automatically.
  - Supports two modes: logging to `console` or saving errors to `log.txt`.
- **Automatic Sorting**:
  - The `append_sorted()` method allows adding new records (Name, Age) and immediately sorts the entire dataset by age (ascending).
- **Data Analysis**:
  - Includes a `show_average()` method to calculate and display the average age of all entries.
- **Error Handling**:
  - Uses custom exceptions: `FileNotFound` and `FileCorrupted`.

## 🚀 How it works

The script creates a file named `data.csv`. It performs the following steps:
1. Initializes the file with headers ("Ім'я", "Вік").
2. Writes initial data.
3. Appends new people to the list while maintaining the sort order by age.
4. Reads and prints the sorted list.
5. Calculates the average age.

## 🛠 Usage

To run the script, execute the following command in your terminal:

```bash
python lab6.py
