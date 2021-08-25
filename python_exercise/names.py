from name_function import get_formatted_name

print("Enter q at any time to quit!")

while True:
    first = input("\n Please give me a first name: ")
    if first == 'q':
        break
    last=input("please give me a last name: ")
    if last == 'q':
        break

    formatted_name = get_formatted_name(first, last)
    print(f"\t Neatly formatted naem:{formatted_name}.")
    