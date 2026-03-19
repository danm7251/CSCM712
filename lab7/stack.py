open_brackets = ["(", "[", "{"]
closed_brackets = [")", "]", "}"]

def isWellParenthesized(s):
    stack = []

    for char in s:
        if char in open_brackets:
            # Keep track of opening brackets to match closing ones against.
            stack.append(char)
            print("\nEncountered opening bracket: " + char + "\nStack = " + str(stack))
        elif char in closed_brackets:
            # If we find a closing bracket, check it has a matching opening bracket
            paired = open_brackets[closed_brackets.index(char)]
            print("\nEncountered closing bracket: " + char + "\nAssociated bracket: " + paired)

            if len(stack) == 0:
                print("\nStack was empty so no matching opening bracket was found!\nStack = " + str(stack))
                return False

            if paired != stack.pop():
                print("\nPopped stack, associated bracket: " + paired + " not found!")
                return False
            
            print("Stack = " + str(stack))
            
    # If any opening brackets that never matched slip through they will be left in the stack
    if len(stack) != 0:
        print("\nLeftover brackets!\nStack = " + str(stack))

    return True
            

if __name__ == "__main__":
    s = "{ x * (y + z^(2i) }"
    result = isWellParenthesized(s)
    print()
    print(result)