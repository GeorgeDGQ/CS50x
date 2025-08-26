# Jorge Daniel Gómez Quintana "Sentimental-readability"

def main():
    text = input("Text: ")

    letters = 0
    spaces = 0
    sentences = 0

    for char in text:
        if char.isalpha():
            letters += 1
        elif char == ' ':
            spaces += 1
        elif char in ['.', '!', '?']:
            sentences += 1

    if len(text) == 0:
        words = 0
    else:
        words = spaces + 1

    if words > 0:
        L = (letters / words) * 100
        S = (sentences / words) * 100
    else:
        L = 0.0
        S = 0.0

    index = 0.0588 * L - 0.296 * S - 15.8
    grade = round(index)

    if grade < 1:
        print("Before Grade 1")
    elif grade >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {int(grade)}")

if __name__ == "__main__":
    main()
