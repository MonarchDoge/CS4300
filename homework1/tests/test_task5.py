# Pure list didn't have needed functionality. Using a list of dicts instead.
# AI generated the list of books, my own favorites are a bit eccentric.
my_favorite_books = [
    {"title": "1984", "author": "George Orwell"},
    {"title": "Brave New World", "author": "Aldous Huxley"},
    {"title": "Fahrenheit 451", "author": "Ray Bradbury"},
    {"title": "The Hobbit", "author": "J.R.R. Tolkien"},
    {"title": "Dune", "author": "Frank Herbert"},
]

print("First three books:")
for book in my_favorite_books[:3]:
    print(f"{book['title']} by {book['author']}")

# Dictionary representing a student database
student_database = {
    "John": "1",
    "Joe": "2",
    "Greg": "3",
}

# Check first three titles
def test_favorite_books_first_three():
    first_three = [book["title"] for book in my_favorite_books[:3]]
    expected = ["1984", "Brave New World", "Fahrenheit 451"]
    assert first_three == expected

# Check that the keys exist
def test_student_database_contains_students():
    assert "John" in student_database
    assert "Joe" in student_database
    assert "Greg" in student_database

# All student IDs are unique
def test_student_ids_unique():
    ids = list(student_database.values())
    assert len(ids) == len(set(ids))