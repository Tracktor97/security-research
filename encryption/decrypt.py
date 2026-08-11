import time
start_time = time.perf_counter()
# NOTE:
# Rotation ciphers are cryptographically insecure and are implemented
# here strictly for educational and analytical purposes.


# Initializing a nested list containing the frequencies of english
# characters.
ALPHA_FREQ = [['E', 529117365], ['T', 390965105], ['A', 374061888],
              ['O', 326627740], ['I', 320410057], ['N', 313720540],
              ['S', 294300210], ['R', 277000841], ['H', 216768975],
              ['L', 183996130], ['D', 169330528], ['C', 138416451],
              ['U', 117295780], ['M', 110504544], ['F', 95422055],
              ['G', 91258980], ['P', 90376747], ['W', 79843664],
              ['Y', 75294515], ['B', 70195826], ['V', 46337161],
              ['K', 35373464], ['J', 9613410], ['X', 8369915],
              ['Z', 4975847], ['Q', 4550166]]
# Initializing empty lists to store the letters and the freq values
letters = []
values = []
# Initializing a counter to denote the first list position to iterate
# through all values in the ALPHA_FREQ nested list.
count = 0
# Iterating through ALPHA_FREQ[] and appending the values to the empty
# lists for letters[] and values[]
for items in ALPHA_FREQ:
    # Avoiding index errors
    if count < 26:
        letters.append(ALPHA_FREQ[count][0])
        values.append(ALPHA_FREQ[count][1])
    count += 1


def main():
    '''
    The main() function is being used to call on the modules availble
    within this program. The first module is the Rotation cipher module
    which will be able to crack rotation ciphers. All subsequent modules
    will be called from the main function to be initiated.
    '''
    # Initializing choice variable and cont[inue] variable as a sentinel
    cont = ''
    choice = ''
    # While loop being used to accept user input for a module choice
    while cont != 'n':
        # Storing user input to the choice variable to call a function()
        choice = input('Which module would you like to access? '
                       '\n1. Rotation Cipher'
                       '\nPlaceholder                            \033[2A')
        print()
        print('\033[-5A')
        if choice == '1':  # If choice is 1 call rotation_cipher()
            rotation_cipher()
        else:  # If an invalid choice is provided
            cont = input('That is not a valid choice. Continue? '
                         'y or n ')


def rotation_cipher():
    '''The rotation_cipher() function is used to call on the functions
    required to determine and crack a rotation cipher. These calls
    include the enter_text(), frequency(), brute_force(), comparison(),
    and shift_ordinance(). ValueErrors are checked for at multiple
    stages in the execution of the rotation_cipher().
    '''
    # Call to the enter_text() to store in text local variable
    text = enter_text()
    sen = 'yes'  # Initializing a sentinel
    # While loop to get user input and call functions if input is valid
    while sen == "yes":
        # Try suite checking for valueErrors and Unbound errors
        try:

            verbose = input('Would you like to run in verbose mode? y or n ')
            # Storing the value of the frequency() in var
            var = frequency(text, verbose.lower())
            # Determining if the user would like to use brute force
            if var == 'Brute Force':
                brute_force(text, verbose)  # Calling the brute_force()
                break  # Breaking out of the module
            else:  # If frequency() runs normally name variables
                avg, sums, value = var[0], var[1], var[2]
            # Call the comparison() function and store in variables
            rotations, ordi = comparison(avg, sums, value, verbose)
            # Call the shift_ordinance() function
            shift_ordinance(text, rotations, value, ordi, verbose)
        # If a ValueError is raised print message to enter correct value
        except ValueError:
            print('\nPlease enter a value A-Z:\n')
        # If Unbound raised print message to enter correct value
        except UnboundLocalError:
            print('That is not a valid value, Try again\n')
        # If the functions execute without error ask for another value
        else:
            # Store the input in the sen variable to decide loop status
            sen = input('\nWould you like to enter another value? yes or no: ')


def enter_text():
    '''
    The enter_text() function is used to capture text from the user. For
    use in any module.
    '''
    text = input('Enter the text to test: ')
    # Normalize the text to uppercase for case insensitivity
    text = text.upper()
    return text  # Return the normalized text


def frequency(text, verbose):
    '''
    The frequency() function is used to determine the frequency of
    the letters within the given string. Which will be used later to
    come up with possible replaced characters.
    '''
    # Initializing a counter
    count = 0
    # Initializing an empty list that will store the top 3 letters
    top_3 = []
    # Iterating through the items in the letters list
    for i in letters:
        # Storing the count of a letter in a variable named counts
        counts = text.count(i)
        # Using an if statement to determine if this value is greater
        # then the last value stored. Starts at 0
        if counts > count:
            count = counts
            # Appending the letter to the top_3[]
            top_3.append(i)
    # Reversing the values in top_3[] to put the highest value at
    # the top
    top_3.reverse()
    # While loop to pop the last entry in the list so long as the list
    # is larger than 3.
    while len(top_3) > 3:
        top_3.pop()
    while len(top_3) < 3:
        top_3.append('None')
    # Printing messages and more information if in verbose mode
    if verbose == 'y':
        # Displaying top_3[] by their frequency of appearance
        print(f'{top_3[0]} appears the most in this string of chracters.'
              f' {abs(ord("E")-ord(top_3[0]))} spots away from "E" '
              'in english.')
        if top_3[1] == 'None':
            print('N/A')
        else:
            print(f'{top_3[1]} appears the second most after that. In english.'
                  f' {abs(ord("T")-ord(top_3[1]))} spots away from "T" '
                  'in english.')
        if top_3[2] == 'None':
            print('N/A')
        else:
            print(f'{top_3[2]} appears the third most often! "A" in english.'
                  f' {abs(ord("A")-ord(top_3[2]))} spots away from "A" '
                  'in english.')
    # Asking the user what value you would like to test.
    value = input("What value would you like to test? (Enter 0 for brute "
                  "force) ")
    # Checking if the value the user entered is 0 to activate the brute
    # force function by returning 'Brute Force' from this function.
    if value == '0':
        return 'Brute Force'
    value = value.upper()
    sums = sum(values)
    ind = letters.index(value)
    normalize = int(values[ind])
    avg_total = (normalize/sums) * 100
    times = text.count(value)
    if verbose == 'y':
        print(f'{value} appears {times} times in the text.')

    avg = (times/len(text)) * 100
    # print(len(text))
    if verbose == 'y':
        print(f'This is {avg:.2f}% of the entire text.')
        print(f'{value} appears in {avg_total:.2f}% of the English language.')
    return avg, sums, value


def comparison(avg, sums, value, verbose):
    '''Placeholder'''
    freq = []
    diff = []
    ordi = []
    rotations = []
    i = 0
    for items in values:
        appen = (items/sums) * 100
        freq.append(appen)
        # print(f'{freq[i]:.2f}')
        i += 1
    for items in freq:
        diff.append(abs(items-avg))
        i += 1
    # print(diff)
    # min(diff)
    for i in range(3):
        diff_index = diff.index(min(diff))
        # print(diff_index)
        # print(letters[diff_index])
        ordi.append(ord(letters[diff_index]))
        diff[diff_index] = 50
    # print(ordi)
    for i in ordi:
        k = abs(ord(value) - i)
        if verbose == 'y':
            print(f'{value} is {k} letters away from {chr(i)}')
        rotations.append(k)
        total = 1
    for i in freq:
        total += (i / 100)
    if verbose == 'y':
        print(f'{total:.2f}')
    return rotations, ordi


def shift_ordinance(text, r_value, value, ordi, verbose):
    a = 0
    for j in r_value:
        new_text = []
        for i in text:
            if ord(i) < 64 or ord(i) > 90:
                rotated = ord(i)
            elif ord(i) + j > 90:
                rotated = ((abs(ord(i) + j)) - 90) + 64
            else:
                rotated = ord(i) + j
            new_text.append(chr(rotated))
        x = ''.join(str(e) for e in new_text)
        if verbose == 'y':
            print(f'\nUsing {chr(ordi[a])} in place of {value}' +
                  f'({j} spaces away) we arrive at this result.')
            print(f'This is a ROT{j}')
        legibility = english_comparison(x, verbose)
        if legibility > 50 or legibility != 0 and verbose == 'y':
            print(f'\n {x}')
            return f'This is a ROT{abs(j - 26)}'
        if verbose == 'y':
            print('The result is not legible')
            print(x)
        a += 1

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    if verbose == 'y':
        print(f"The execution time is: {execution_time}")


def english_comparison(result, verbose):
    total_score = 0
    split_result = []
    common_30_words = ['THE', 'BE', 'TO', 'OF', 'AND', 'WAS', 'IN', 'THAT',
                       'HAVE', 'ALL', 'IT', 'FOR', 'NOT', 'ON', 'WITH', 'HE',
                       'AS', 'YOU', 'DO', 'AT', 'THIS', 'BUT', 'HIS', 'BY',
                       'FROM', 'THEY', 'WE', 'SAY', 'HER', 'SHE']
    split_result = result.split()
    for i in common_30_words:
        counts = split_result.count(i)
        if counts > 0:
            total_score += 5
    if total_score > 10:
        total_score += abs((len(result)/30) - 100)
    if total_score > 100:
        total_score = 100
    if verbose == 'y':
        print(f'There is a {int(total_score)}% chance this is english.')
    return total_score


def brute_force(text, verbose):
    brute_list = []
    for i in range(26):
        value = ord('A') + i
        value = chr(value).upper()
        sums = sum(values)
        ind = letters.index(value)
        normalize = int(values[ind])
        avg_total = (normalize/sums) * 100
        times = text.count(value)
        avg = (times/len(text)) * 100
        if verbose == 'y':
            print(f'This is {avg:.2f}% of the entire text.')
            print(f'{value} appears in {avg_total:.2f}% of the English \
                  language.')
        rotations, ordi = comparison(avg, sums, value, verbose)
        rot = shift_ordinance(text, rotations, value, ordi, verbose)
        if rot is not None:
            brute_list.append(value)
            brute_list.append(rot)
    print(brute_list)


if __name__ == '__main__':
    main()
