import sys
import math

def word_freq(filename:str, case_sensitive:bool=False) -> dict:
    """Count the frequencies of words in a file.

    Args:
        filename (str): Name of the file to read

    Returns:
        word_dict (dict): Returns a dictionary with words as
        keys and frequencies as values
    """
    word_dict = {}
    with open(filename) as f:
        text = f.read()
        words = text.split()

        for word in words:
            if case_sensitive:
                word = word.strip("""!"#$%&'()*,-./:;?@[]_""")
            else:
                word = word.strip("""!"#$%&'()*,-./:;?@[]_""").lower()

            if word in word_dict:
                word_dict[word] += 1
            else:
                word_dict[word] = 1

    return word_dict



def summary(filename:str) -> tuple:
    """Read a file with one number per line. 
    Any non-numeric lines are ignored.
    Count various summary statistics of the numbers.

    Args:
        filename (str): Name of the file to read

    Returns:
        summa (int): The sum of all numbers
        avg (float): The average of the numbers
        standard_dev (float): The standard deviation of the numbers
    """
    with open(filename) as f:
        number_list = []
        for line in f.readlines():
            try:
                number = float(line.strip())
                number_list.append(number)
            except ValueError:
                continue
        
        if len(number_list) == 0:
            raise Exception("The file contains no numbers.")
        else:
            summa = sum(number_list)
            avg = summa / len(number_list)
            standard_dev = math.sqrt(sum([(x - avg) ** 2 for x in number_list]) / (len(number_list) - 1))
    return (summa, avg, standard_dev)


def file_statistics(filename:str) -> tuple:
    """Read a file with text. Count the number of lines,
    words and characters (including spaces) in the file.

    Args:
        filename (str): Name of the file to read

    Returns:
        no_of_lines (int): The number of lines
        no_of_words (int): The number of words
        no_of_chars (int): The number of characters
    """
    with  open(filename) as f:
        text = f.readlines()
        no_of_lines = len(text)
        no_of_words = 0
        no_of_chars = 0
        for line in text:
            no_of_chars += len(line)
            words = line.split()
            no_of_words += len(words)

    return (no_of_lines, no_of_words, no_of_chars)



def main():
    print(file_statistics('holmes.txt'))


if __name__ == '__main__':
    main()