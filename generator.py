import numpy as np
import sys
import json, csv

COMMAND_ERROR = 0
COMMAND_CORRECT = 1

mode = 0
number = 0
def command_handler():
    argc = len(sys.argv)

    # Check if there is -h or --help flag.
    for i in sys.argv[1:argc]:
        if i == "-h" or i == "--help":
            return help_command("")

    # There exists unpaired flag or value, or there is no flag.
    if argc % 2 == 0 or argc == 1:
        return help_command("Wrong format! Please check out your command.\n")

    # Process the command and setup corresponding variables.
    has_flag_used = np.zeros(2) # {-m, -n}
    for i in np.arange(1, argc, 2):
        flag = sys.argv[i]
        value = sys.argv[i + 1]
        if flag == "-m" or flag == "--mode":
            if not has_flag_used[0]:
                has_flag_used[0] = 1
                mode = int(value)
            else:
                return help_command("Multiple mode options! Please check out your command.\n")
        elif flag == "-n" or flag == "--number":
            if not has_flag_used[1]:
                has_flag_used[1] = 1
                number = int(value)
            else:
                return help_command("Multiple number options! Please check out your command.\n")
        else:
            return help_command("Invalid option(s)! Please check out your command.\n")
    if not has_flag_used[0]:
        return help_command("No mode value! Please check out your command.\n")
    if not has_flag_used[1] and mode == 1:
        return help_command("No number value! Please check out your command.\n")
    if has_flag_used[1] and mode == 0:
        return help_command("Number option is not valid in mode 0! Please check out your command.\n")
    
    return COMMAND_CORRECT

def help_command(err_msg):
    print(err_msg, end="")
    print("Usages:")
    print("  exec | python {} -m <mode> -n <number>".format(sys.argv[0]))
    print("  help | python {} -h".format(sys.argv[0]))
    print("Options:")
    print("  -h, --help   | Show usages and list available options.")
    print("  -m, --mode   | Specify the generating mode.")
    print("               |   0 - generate possible permutations of attributes' dictionary.")
    print("               |   1 - generate training data.")
    print("  -n, --number | Specify the number of generated training data.")
    print("               | This option is only valid when the mode flag sets to 1.")
    return COMMAND_ERROR

def generate_possible_dict():
    # Read files.
    attributes = json.load(open("attributes.json"))
    rule_reader = csv.reader(open("rules.csv", newline=''))

    # Build options encoding dictionary.
    option_dict = []
    for attr in attributes["attributes"]:
        new_dict = {}
        encoder = 0
        for option in attributes["options"][attr]:
            new_dict[option] = encoder
            encoder += 1
        option_dict.append(new_dict)

    # Build encoded possible permutations.
    encoded_attr = []
    for attr in attributes["attributes"]:
        encoded_attr.append(np.arange(len(attributes["options"][attr])))
    permutation = encoded_attr[0]
    permutation = [(x, y) for x in permutation for y in encoded_attr[1]]
    for attr in encoded_attr[2:]:
        temp = []
        for x in permutation:
            for y in attr:
                new_x = list(x)
                new_x.append(y)
                temp.append(new_x)
        permutation = temp
    
    # Build rules list.
    attr_list = []
    rule_list = []
    for index, line in enumerate(rule_reader):
        if index == 0:
            attr_list = line
        else:
            rule_list.append(line)

    # Generate results for all possible permutations.
    result = []
    for count in range(len(permutation)):
        result = get_result(permutation[count], attr_list, rule_list, option_dict)
        permutation[count].append(result)

    # Save dictionary of possible permutations.
    writer = csv.writer(open("dictionary.csv", 'w', newline=''))
    attr_list.append("result")
    writer.writerow(attr_list)
    for target in permutation:
        temp = []
        for index, data in enumerate(target[:-1]):
            temp.append(list(option_dict[index].keys())[list(option_dict[index].values()).index(data)])
        temp.append(target[-1])
        writer.writerow(temp)

def get_result(target, attr_list, rule_list, option_dict):
    result = 0
    for rule in rule_list:
        result = -1
        for index in range(len(attr_list)):
            if rule[index] == "*":
                continue
            if target[index] != option_dict[index][rule[index]]:
                result = 0
                break
        if result == -1:
            result = 1
            break
    return result

def generate_training_data():
    return

if command_handler():
    if mode == 0:
        generate_possible_dict()
    else:
        generate_training_data()
