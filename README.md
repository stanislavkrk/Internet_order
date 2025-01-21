Order Management System

This project implements an order management system with hash tables to efficiently manage and search client orders. The system supports adding, searching, and deleting orders while improving performance and usability through the use of hash-based data structures.

Features

Order Creation:
        Allows users to create new orders with details such as name, surname, item, quantity, and date.
        Automatically assigns a unique order number to each entry.

 Efficient Search:
        Implements hash tables for quick lookups across key fields:
            Order number
            Client's name and surname
            Item name
            Quantity
            Date of order
        Returns precise search results instead of ambiguous matches.

Order Deletion:
        Removes orders efficiently, updating all associated hash tables.
        Ensures data consistency by deleting references from every hash table.

Abstract Design:
        Uses an abstract base class (AbstrDict) as an interface for other classes, promoting modularity and code reusability.

User-Friendly Interface:
        Console-based menu for navigating the system.
        Input validation ensures a smooth user experience.
