def phoneFizz(input):
    output = ""
    for x in range(1, input+1):
        if x % 5 == 0 and x % 3 == 0:
            output += ("fizzbuzz ")
        elif x % 5 == 0:
            output += ("fizz ")
        elif x % 3 == 0:
            output += ("buzz ")
        else:
            output += str(x)+" "
    return output
