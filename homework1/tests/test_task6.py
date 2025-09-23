import pytest
# Counts the amount of words in a file
def word_counter(file_name):
    count = 0
    with open(file_name, 'r') as file:
        data = file.read()
        word_list = data.split()
    return len(word_list)

# Creates a temmporary file that is used to test the word counter
def test_answer(tmp_path):
    temp_file = tmp_path / "my_temp_file.txt"
    temp_file.write_text("I think I'm understanding this")
    assert word_counter(str(temp_file)) == 5
