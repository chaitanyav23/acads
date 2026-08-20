// #include<iostream>
// #include<vector>
// #include<unordered_map>
// #include<string>
// #include<ctime>
// using namespace std;

// class Book {
// public:
//     int id;
//     string title;
//     string author;
//     bool isIssued;

//     Book(int id, string title, string author) {
//         this->id = id;
//         this->title = title;
//         this->author = author;
//         this->isIssued = false;
//     }
// };

// class Library {
// private:
//     vector<Book> books;
//     unordered_map<int, bool> issuedBooks;

// public:
//     void addBook(int id, string title, string author) {
//         books.push_back(Book(id, title, author));
//         issuedBooks[id] = false;
//         cout << "Book added successfully!" << endl;
//     }

//     void displayBooks() {
//         if (books.empty()) {
//             cout << "No books available in the library." << endl;
//             return;
//         }
//         cout << "Available Books in the Library:\n";
//         for (const auto &book : books) {
//             cout << "ID: " << book.id << ", Title: " << book.title << ", Author: " << book.author;
//             cout << (book.isIssued ? " (Issued)" : " (Available)") << endl;
//         }
//     }

//     bool issueBook(int id) {
//         for (auto &book : books) {
//             if (book.id == id) {
//                 if (!book.isIssued) {
//                     book.isIssued = true;
//                     issuedBooks[id] = true;
//                     return true; // Successfully issued
//                 } else {
//                     return false; // Already issued
//                 }
//             }
//         }
//         return false; // Book ID not found
//     }

//     bool returnBook(int id) {
//         for (auto &book : books) {
//             if (book.id == id) {
//                 if (book.isIssued) {
//                     book.isIssued = false;
//                     issuedBooks[id] = false;
//                     return true; // Successfully returned
//                 } else {
//                     return false; // Not issued
//                 }
//             }
//         }
//         return false; // Book ID not found
//     }

//     bool isBookIssued(int id) {
//         return issuedBooks[id];
//     }
// };

// class User {
// protected:
//     string id;
//     Library &library;

// public:
//     User(string id, Library &lib) : id(id), library(lib) {}
//     virtual void display_menu() = 0; // Pure virtual function
// };

// class Student : public User {
// public:
//     Student(string id, Library &lib) : User(id, lib) {}

//     void display_menu() override {
//         while (true) {
//             cout << "\nStudent Menu:\n1. See All Books\n2. Issue Book\n3. Return Book\n4. Logout\nEnter choice: ";
//             int choice;
//             cin >> choice;

//             if (choice == 1) {
//                 library.displayBooks();
//             } else if (choice == 2) {
//                 int book_id;
//                 cout << "Enter Book ID to issue: ";
//                 cin >> book_id;
//                 issue_book(book_id);
//             } else if (choice == 3) {
//                 int book_id;
//                 cout << "Enter Book ID to return: ";
//                 cin >> book_id;
//                 return_book(book_id);
//             } else if (choice == 4) {
//                 cout << "Logging out..." << endl;
//                 break;
//             } else {
//                 cout << "Invalid choice. Try again." << endl;
//             }
//         }
//     }

//     void issue_book(int book_id) {
//         static int issuedCount = 0;
//         if (issuedCount >= 3) {
//             cout << "You have reached the maximum issue limit (3 books)." << endl;
//             return;
//         }

//         if (library.issueBook(book_id)) {
//             cout << "Book issued successfully." << endl;
//             issuedCount++;
//         } else {
//             cout << "Book cannot be issued (Either not found or already issued)." << endl;
//         }
//     }

//     void return_book(int book_id) {
//         if (library.returnBook(book_id)) {
//             cout << "Book returned successfully." << endl;
//         } else {
//             cout << "Invalid Book ID or book was not issued." << endl;
//         }
//     }
// };

// class Faculty : public User {
// public:
//     Faculty(string id, Library &lib) : User(id, lib) {}

//     void display_menu() override {
//         while (true) {
//             cout << "\nFaculty Menu:\n1. See All Books\n2. Issue Book\n3. Return Book\n4. Logout\nEnter choice: ";
//             int choice;
//             cin >> choice;

//             if (choice == 1) {
//                 library.displayBooks();
//             } else if (choice == 2) {
//                 int book_id;
//                 cout << "Enter Book ID to issue: ";
//                 cin >> book_id;
//                 issue_book(book_id);
//             } else if (choice == 3) {
//                 int book_id;
//                 cout << "Enter Book ID to return: ";
//                 cin >> book_id;
//                 return_book(book_id);
//             } else if (choice == 4) {
//                 cout << "Logging out..." << endl;
//                 break;
//             } else {
//                 cout << "Invalid choice. Try again." << endl;
//             }
//         }
//     }

//     void issue_book(int book_id) {
//         static int issuedCount = 0;
//         if (issuedCount >= 5) {
//             cout << "You have reached the maximum issue limit (5 books)." << endl;
//             return;
//         }

//         if (library.issueBook(book_id)) {
//             cout << "Book issued successfully." << endl;
//             issuedCount++;
//         } else {
//             cout << "Book cannot be issued (Either not found or already issued)." << endl;
//         }
//     }

//     void return_book(int book_id) {
//         if (library.returnBook(book_id)) {
//             cout << "Book returned successfully." << endl;
//         } else {
//             cout << "Invalid Book ID or book was not issued." << endl;
//         }
//     }
// };

// class Librarian : public User {
// public:
//     Librarian(string id, Library &lib) : User(id, lib) {}

//     void display_menu() override {
//         while (true) {
//             cout << "\nLibrarian Menu:\n1. Add Book\n2. See All Books\n3. Logout\nEnter choice: ";
//             int choice;
//             cin >> choice;

//             if (choice == 1) {
//                 int id;
//                 string title, author;
//                 cout << "Enter Book ID: "; cin >> id;
//                 cout << "Enter Title: "; cin >> title;
//                 cout << "Enter Author: "; cin >> author;
//                 library.addBook(id, title, author);
//             } else if (choice == 2) {
//                 library.displayBooks();
//             } else if (choice == 3) {
//                 cout << "Logging out..." << endl;
//                 break;
//             } else {
//                 cout << "Invalid choice. Try again." << endl;
//             }
//         }
//     }
// };

// int main() {
//     Library library;
//     library.addBook(101, "C++ Programming", "Bjarne Stroustrup");
//     library.addBook(102, "Data Structures", "Mark Weiss");

//     Librarian librarian("LIB001", library);
//     librarian.display_menu();

//     return 0;
// }



// #include <iostream>
// #include <vector>
// #include <unordered_map>
// #include <fstream>
// #include <ctime>
// using namespace std;

// class Student : public User {
//     private:
//         vector<int> borrowedBooks;
//         int maxBorrowLimit = 3;
//         Library &library;  // Use a reference instead of a pointer
    
//     public:
//         Student(Library &lib) : library(lib) {}  // Initialize reference
    
//         void borrowBook(int book_id) override {
//             if (borrowedBooks.size() >= maxBorrowLimit) {
//                 cout << "Borrow limit reached! Return a book before borrowing a new one." << endl;
//                 return;
//             }
//             if (library.issueBook(book_id)) {  // ✅ Use dot (.)
//                 borrowedBooks.push_back(book_id);
//                 cout << "Book borrowed successfully!" << endl;
//             } else {
//                 cout << "Book is either unavailable or already issued." << endl;
//             }
//         }
    
//         void returnBook(int book_id) override {
//             auto it = std::find(borrowedBooks.begin(), borrowedBooks.end(), book_id);
//             if (it != borrowedBooks.end()) {
//                 borrowedBooks.erase(it);
//                 library.returnBook(book_id);  // ✅ Use dot (.)
//                 cout << "Book returned successfully!" << endl;
//             } else {
//                 cout << "You haven't borrowed this book." << endl;
//             }
//         }
//     };
    
// class Book {
// public:
//     int id;
//     string title;
//     string author;
//     bool isIssued;
//     time_t issueDate;
    
//     Book(int id, string title, string author)
//         : id(id), title(title), author(author), isIssued(false), issueDate(0) {}
// };

// class Library {
// private:
//     vector<Book> books;
//     unordered_map<int, time_t> issuedBooks;

// public:
//     void addBook(int id, string title, string author) {
//         books.push_back(Book(id, title, author));
//         issuedBooks[id] = 0;
//     }

//     void displayBooks() {
//         if (books.empty()) {
//             cout << "No books available in the library.\n";
//             return;
//         }
//         cout << "\nAvailable Books:\n";
//         for (const auto &book : books) {
//             cout << "ID: " << book.id << ", Title: " << book.title
//                  << ", Author: " << book.author
//                  << (book.isIssued ? " (Issued)" : " (Available)") << endl;
//         }
//     }

//     bool issueBook(int id, time_t &borrowDate) {
//         for (auto &book : books) {
//             if (book.id == id && !book.isIssued) {
//                 book.isIssued = true;
//                 book.issueDate = time(nullptr);
//                 issuedBooks[id] = book.issueDate;
//                 borrowDate = book.issueDate;
//                 return true;
//             }
//         }
//         return false;
//     }

//     bool returnBook(int id, time_t &borrowDate) {
//         for (auto &book : books) {
//             if (book.id == id && book.isIssued) {
//                 book.isIssued = false;
//                 borrowDate = issuedBooks[id];
//                 issuedBooks[id] = 0;
//                 return true;
//             }
//         }
//         return false;
//     }
// };

// class User {
// protected:
//     string id;
//     string userType;
//     Library &library;
//     vector<int> borrowedBooks;
//     unordered_map<int, time_t> borrowHistory;

// public:
//     User(string id, string userType, Library &lib) : id(id), userType(userType), library(lib) {}
//     virtual void borrowBook(int book_id) = 0;
//     virtual void returnBook(int book_id) = 0;
//     virtual void displayMenu() = 0;
// };

// class Student : public User {
// private:
//     static const int MAX_BORROW = 3;
//     static const int MAX_DAYS = 15;
//     static const int FINE_PER_DAY = 10;

// public:
//     Student(string id, Library &lib) : User(id, "Student", lib) {}
    
//     void borrowBook(int book_id) override {
//         if (borrowedBooks.size() >= MAX_BORROW) {
//             cout << "You have reached the borrowing limit (3 books).\n";
//             return;
//         }
//         time_t borrowDate;
//         if (library.issueBook(book_id, borrowDate)) {
//             borrowedBooks.push_back(book_id);
//             borrowHistory[book_id] = borrowDate;
//             cout << "Book issued successfully.\n";
//         } else {
//             cout << "Book cannot be issued.\n";
//         }
//     }
    
//     void returnBook(int book_id) override {
//         time_t borrowDate;
//         if (library.returnBook(book_id, borrowDate)) {
//             borrowedBooks.erase(remove(borrowedBooks.begin(), borrowedBooks.end(), book_id), borrowedBooks.end());
//             time_t currentTime = time(nullptr);
//             int daysBorrowed = (currentTime - borrowDate) / 86400;
//             if (daysBorrowed > MAX_DAYS) {
//                 int fine = (daysBorrowed - MAX_DAYS) * FINE_PER_DAY;
//                 cout << "You have exceeded the borrowing limit. Your fine is: Rs." << fine << "\n";
//             } else {
//                 cout << "Book returned successfully.\n";
//             }
//         } else {
//             cout << "Invalid Book ID or book was not issued.\n";
//         }
//     }
    
//     void displayMenu() override {
//         while (true) {
//             cout << "\nStudent Menu:\n1. See All Books\n2. Issue Book\n3. Return Book\n4. Logout\nEnter choice: ";
//             int choice;
//             cin >> choice;
//             if (choice == 1) library.displayBooks();
//             else if (choice == 2) {
//                 int book_id;
//                 cout << "Enter Book ID to issue: ";
//                 cin >> book_id;
//                 borrowBook(book_id);
//             } else if (choice == 3) {
//                 int book_id;
//                 cout << "Enter Book ID to return: ";
//                 cin >> book_id;
//                 returnBook(book_id);
//             } else if (choice == 4) {
//                 cout << "Logging out...\n";
//                 break;
//             } else {
//                 cout << "Invalid choice. Try again.\n";
//             }
//         }
//     }
// };

// int main() {
//     Library library;
//     library.addBook(101, "C++ Programming", "Bjarne Stroustrup");
//     library.addBook(102, "Data Structures", "Mark Weiss");
//     library.addBook(103, "Algorithms", "CLRS");
//     library.addBook(104, "Operating Systems", "Silberschatz");
//     library.addBook(105, "Database Systems", "Navathe");

//     Student student("STU123", library);
//     student.displayMenu();
//     return 0;
// }

// #include <bits/stdc++.h>
// using namespace std;

// vector<vector<string>> content;

// // File handling functions
// void readfile(string fname);
// void writefile(vector<vector<string>> par, string fname);
// void writefileappend(vector<string> par, string fname);

// // Base class: User
// class User {
// protected:
//     string password;
// public:
//     string name;
//     string id;
//     int role;

//     virtual void display_menu() = 0; // Pure virtual function
//     void login();
//     void see_all_books();
//     void see_issued_books();
//     virtual void issue_book(string bookname) = 0;
//     void return_book(string isbncode);
//     int calc_fine();
// };

// // Derived class: Student
// class Student : public User {
// public:
//     void display_menu() override;
//     void issue_book(string bookname) override;
// };

// // Derived class: Faculty
// class Faculty : public User {
// public:
//     void display_menu() override;
//     void issue_book(string bookname) override;
// };

// // Derived class: Librarian
// class Librarian : public User {
// public:
//     void display_menu() override;
//     void issue_book(string bookname) override;
// };

// class Library {
// private:
//     vector<Book> books;

//     // Helper function to split CSV lines
//     vector<string> split(const string &s, char delimiter) {
//         vector<string> tokens;
//         stringstream ss(s);
//         string token;
//         while (getline(ss, token, delimiter)) {
//             tokens.push_back(token);
//         }
//         return tokens;
//     }

//     // Load books from CSV file
//     void loadBooksFromCSV(const string &filename) {
//         ifstream file(filename);
//         if (!file.is_open()) {
//             cerr << "Error: Could not open " << filename << "\n";
//             return;
//         }

//         string line;
//         while (getline(file, line)) {
//             vector<string> tokens = split(line, ',');
//             if (tokens.size() == 4) {
//                 int id = stoi(tokens[0]);
//                 string title = tokens[1];
//                 string author = tokens[2];
//                 bool isIssued = (tokens[3] == "1");
//                 books.emplace_back(id, title, author, isIssued);
//             }
//         }

//         file.close();
//     }

// public:
//     Library(const string &filename) {
//         loadBooksFromCSV(filename);
//         cout << "Library initialized with " << books.size() << " books.\n";
//     }

//     void displayBooks() {
//         if (books.empty()) {
//             cout << "No books available in the library.\n";
//             return;
//         }

//         cout << "Available Books in the Library:\n";
//         for (const auto &book : books) {
//             cout << "ID: " << book.id << ", Title: " << book.title
//                  << ", Author: " << book.author
//                  << (book.isIssued ? " (Issued)" : " (Available)") << "\n";
//         }
//     }
// };

// void User::see_all_books() {
//     readfile("all_books_data.csv");
//     cout << "Title | Author | Publisher | ISBN | Issued\n";
//     for (auto &book : content) {
//         for (auto &field : book) cout << field << " | ";
//         cout << "\n";
//     }
// }

// void User::see_issued_books() {
//     readfile("issued_books_data.csv");
//     bool hasBooks = false;
//     for (auto &entry : content) {
//         if (entry[0] == id) {
//             hasBooks = true;
//             cout << "Issued Books: ";
//             for (size_t i = 1; i < entry.size(); i++) cout << entry[i] << " ";
//             cout << "\n";
//         }
//     }
//     if (!hasBooks) cout << "No books issued.\n";
// }

// void User::return_book(string isbncode) {
//     readfile("issued_books_data.csv");
    
//     bool found = false;
//     for (auto &entry : content) {
//         if (entry[0] == id && entry[2] == isbncode) {
//             content.erase(remove(content.begin(), content.end(), entry), content.end());
//             found = true;
//             break;
//         }
//     }

//     if (found) {
//         writefile(content, "issued_books_data.csv");
//         cout << "Book returned successfully.\n";
//     } else {
//         cout << "You have not issued this book.\n";
//     }
// }


// // ✅ Implement User Class Functions
// void User::login() {
//     cout << "Enter your ID: ";
//     cin >> id;
//     cout << "Enter your Password: ";
//     cin >> password;
    
//     readfile("all_users_data.csv");

//     for (auto &user : content) {
//         if (user.size() < 4) continue;

//         if (user[1] == id && user[2] == password) {  
//             name = user[0];
//             role = stoi(user[3]); // Store role
//             cout << "Login successful! Welcome " << name << ".\n";
//             return;
//         }
//     }
//     cout << "Invalid credentials. Exiting...\n";
//     exit(1);
// }

// int User::calc_fine() {
//     readfile("issued_books_data.csv");
//     int fine = 0;
//     time_t current_time = time(0);
//     for (auto &entry : content) {
//         if (entry[0] == id) {
//             time_t issue_time = stoi(entry[2]);
//             int days_borrowed = (current_time - issue_time) / 86400;
//             int allowed_days = (role == 1) ? 15 : 30;
//             if (days_borrowed > allowed_days) {
//                 fine += (days_borrowed - allowed_days) * 10;
//             }
//         }
//     }
//     return fine;
// }

// // ✅ Implement Student Class Functions
// void Student::display_menu() {
//     while (true) {
//         cout << "\nStudent Menu:\n1. See All Books\n2. See Issued Books\n3. Issue Book\n4. Return Book\n5. Logout\nEnter choice: ";
//         int choice;
//         cin >> choice;

//         if (choice == 1) see_all_books();
//         else if (choice == 2) see_issued_books();
//         else if (choice == 3) {
//             string bookname;
//             cout << "Enter book name: ";
//             cin >> ws;  
//             getline(cin, bookname);
//             issue_book(bookname);
//         } 
//         else if (choice == 4) {
//             string isbn;
//             cout << "Enter ISBN of book to return: ";
//             cin >> isbn;
//             return_book(isbn);
//         } 
//         else if (choice == 5) {
//             cout << "Logging out...\n";
//             break;
//         } 
//         else {
//             cout << "Invalid choice. Please try again.\n";
//         }
//     }
// }

// void Student::issue_book(string bookname) {
//     if (calc_fine() > 0) {
//         cout << "You have unpaid fines. Please clear them before borrowing.\n";
//         return;
//     }
//     readfile("all_books_data.csv");
//     for (auto &book : content) {
//         if (book[0] == bookname && book[4] == "0") {
//             book[4] = "1";
//             writefile(content, "all_books_data.csv");
//             writefileappend({id, bookname, book[3], to_string(time(0))}, "issued_books_data.csv");
//             cout << "Book issued successfully.\n";
//             return;
//         }
//     }
//     cout << "Book not available.\n";
// }



// void Faculty::display_menu() {
//     while (true) {
//         cout << "\nFaculty Menu:\n1. See All Books\n2. See Issued Books\n3. Issue Book\n4. Return Book\n5. Logout\nEnter choice: ";
//         int choice;
//         cin >> choice;

//         if (choice == 1) see_all_books();
//         else if (choice == 2) see_issued_books();
//         else if (choice == 3) {
//             string bookname;
//             cout << "Enter book name: ";
//             cin >> ws;
//             getline(cin, bookname);
//             issue_book(bookname);
//         }
//         else if (choice == 4) {
//             string isbn;
//             cout << "Enter ISBN of book to return: ";
//             cin >> isbn;
//             return_book(isbn);
//         }
//         else if (choice == 5) {
//             cout << "Logging out...\n";
//             break;
//         }
//         else {
//             cout << "Invalid choice. Please try again.\n";
//         }
//     }
// }

// void Faculty::issue_book(string bookname) {
//     // Check if faculty has overdue books beyond 60 days
//     readfile("issued_books_data.csv");
//     time_t current_time = time(0);
//     int book_count = 0;

//     for (auto &entry : content) {
//         if (entry[0] == id) {
//             time_t issue_time = stoi(entry[3]);
//             int days_borrowed = (current_time - issue_time) / 86400;
//             if (days_borrowed > 60) {
//                 cout << "You have a book overdue by more than 60 days. You cannot borrow a new book.\n";
//                 return;
//             }
//             book_count++;
//         }
//     }

//     // Check if faculty has already borrowed 5 books
//     if (book_count >= 5) {
//         cout << "You have already borrowed the maximum allowed books (5). Return a book to borrow another.\n";
//         return;
//     }

//     // Check if the requested book is available
//     readfile("all_books_data.csv");
//     bool book_found = false;

//     for (auto &book : content) {
//         // Case-insensitive comparison
//         if (strcasecmp(book[0].c_str(), bookname.c_str()) == 0) {
//             book_found = true;

//             if (book[4] == "0") { // Book is available
//                 book[4] = "1"; // Mark as issued
//                 writefile(content, "all_books_data.csv");
                
//                 // Add entry to issued_books_data.csv
//                 writefileappend({id, book[0], book[3], to_string(current_time)}, "issued_books_data.csv");
//                 cout << "Book issued successfully.\n";
//                 return;
//             } else {
//                 cout << "Book is already issued.\n";
//                 return;
//             }
//         }
//     }

//     if (!book_found) {
//         cout << "Book not found.\n";
//     }
// }

// class Book {
//     public:
//         int id;
//         string title;
//         string author;
//         bool isIssued;
    
//         Book(int id, string title, string author) {
//             this->id = id;
//             this->title = title;
//             this->author = author;
//             this->isIssued = false;
//         }
//     };
    
//     class Library {
//         private:
//             vector<Book> books;
        
//             // Helper function to split CSV lines
//             vector<string> split(const string &s, char delimiter) {
//                 vector<string> tokens;
//                 stringstream ss(s);
//                 string token;
//                 while (getline(ss, token, delimiter)) {
//                     tokens.push_back(token);
//                 }
//                 return tokens;
//             }
        
//             // Load books from CSV file
//             void loadBooksFromCSV(const string &filename) {
//                 ifstream file(filename);
//                 if (!file.is_open()) {
//                     cerr << "Error: Could not open " << filename << "\n";
//                     return;
//                 }
        
//                 string line;
//                 while (getline(file, line)) {
//                     vector<string> tokens = split(line, ',');
//                     if (tokens.size() == 4) {
//                         int id = stoi(tokens[0]);
//                         string title = tokens[1];
//                         string author = tokens[2];
//                         bool isIssued = (tokens[3] == "1");
//                         books.emplace_back(id, title, author, isIssued);
//                     }
//                 }
        
//                 file.close();
//             }
        
//         public:
//             Library(const string &filename) {
//                 loadBooksFromCSV(filename);
//                 cout << "Library initialized with " << books.size() << " books.\n";
//             }
        
//             void displayBooks() {
//                 if (books.empty()) {
//                     cout << "No books available in the library.\n";
//                     return;
//                 }
        
//                 cout << "Available Books in the Library:\n";
//                 for (const auto &book : books) {
//                     cout << "ID: " << book.id << ", Title: " << book.title
//                          << ", Author: " << book.author
//                          << (book.isIssued ? " (Issued)" : " (Available)") << "\n";
//                 }
//             }
// };


// // ✅ Implement Librarian Class Functions
// void Librarian::display_menu() {
//     cout << "Librarian Menu: Add/Remove Users & Books\n";
// }
// void Librarian::issue_book(string bookname) {
//     cout << "Librarians cannot issue books.\n";
// }

// // ✅ File Handling Functions
// void readfile(string fname) {
//     content.clear();
//     vector<string> row;
//     string line, word;
//     fstream file(fname, ios::in);
//     if (file.is_open()) {
//         while (getline(file, line)) {
//             row.clear();
//             stringstream str(line);
//             while (getline(str, word, ',')) row.push_back(word);
//             content.push_back(row);
//         }
//         file.close();
//     } else cout << "Could not open the file: " << fname << "\n";
// }

// void writefile(vector<vector<string>> par, string fname) {  
//     fstream fout(fname, ios::out);
//     for (auto &x : par) {
//         for (size_t i = 0; i < x.size(); i++) {
//             fout << x[i];
//             if (i < x.size() - 1) fout << ",";
//         }
//         fout << "\n";
//     }
//     fout.close();
// }

// void writefileappend(vector<string> par, string fname) {  
//     fstream fout(fname, ios::out | ios::app);
//     for (size_t i = 0; i < par.size(); i++) {
//         fout << par[i];
//         if (i < par.size() - 1) fout << ",";
//     }
//     fout << "\n";
//     fout.close();
// }

// // ✅ Main Function
// int main() {
//     Library library("all_books_data.csv");
//     string userType;
//     cout << "Enter user type (Student/Faculty/Librarian): ";
//     cin >> userType;

//     User *user = nullptr;
//     if (userType == "Student") user = new Student();
//     else if (userType == "Faculty") user = new Faculty();
//     else if (userType == "Librarian") user = new Librarian();
//     else {
//         cout << "Invalid user type. Exiting...\n";
//         return 1;
//     }

//     user->login();
//     user->display_menu();  // ✅ Ensures that the user remains in the menu until logout

//     delete user;
//     return 0;
// }



