import sys
specialist_state = {
    "free": 0,
    "busy": 0,
    "docu": 0
}

patient_state = {
    "wait":   0,
    "inside": 0,
    "done":   0
}


class Node:
    def __init__(self, wait, free, busy, inside, docu, done, firing_sequence):
        # initial marking M0 use this constructor
        if wait == 0 and free == 0 and busy == 0 and inside == 0 and docu == 0 and done == 0:
            self.START = None
            self.CHANGE = None
            self.END = None
            self.wait = patient_state["wait"]
            self.free = specialist_state["free"]
            self.busy = specialist_state["busy"]
            self.inside = patient_state["inside"]
            self.docu = specialist_state["docu"]
            self.done = patient_state["done"]
            self.firing_sequence = ""
            self.insert(patient_state["wait"], specialist_state["free"], specialist_state["busy"],
                        patient_state["inside"], specialist_state["docu"], patient_state["done"], "")
        # other marking will use this constructor
        else:
            self.START = None
            self.CHANGE = None
            self.END = None
            self.wait = wait
            self.free = free
            self.busy = busy
            self.inside = inside
            self.docu = docu
            self.done = done
            self.firing_sequence = firing_sequence


    def decide_start(self, wait, free):
        if wait > 0 and free > 0:
            return True
        else:
            return False


    def decide_change(self, busy, inside):
        if busy > 0 and inside > 0:
            return True
        else:
            return False


    def decide_end(self, docu):
        if docu > 0:
            return True
        else:
            return False


    def insert(self, wait, free, busy, inside, docu, done, firing_sequence):
        if self.decide_start(wait, free) or self.decide_change(busy, inside) or self.decide_end(docu):
            START_firing_sequence = firing_sequence
            CHANGE_firing_sequence = firing_sequence
            END_firing_sequence = firing_sequence
            if self.decide_start(wait, free):
                START_firing_sequence += "start"
                print("Firing_sequence is:", START_firing_sequence)
                START_firing_sequence += ", "
                temp_wait = wait - 1
                temp_free = free - 1
                temp_busy = busy + 1
                temp_inside = inside + 1
                print('M = [{}.wait, {}.free, {}.busy, {}.inside, {}.docu, {}.done]\n'.format(temp_wait, temp_free,
                                                                                              temp_busy, temp_inside,
                                                                                              docu, done))
                self.START = Node(wait - 1, free - 1, busy + 1, inside + 1, docu, done, START_firing_sequence)
                self.START.insert(wait - 1, free - 1, busy + 1, inside + 1, docu, done, START_firing_sequence)

            if self.decide_change(busy, inside):
                CHANGE_firing_sequence += "change"
                print("Firing_sequence is:", CHANGE_firing_sequence)
                CHANGE_firing_sequence += ", "
                temp_busy = busy - 1
                temp_inside = inside - 1
                temp_docu = docu + 1
                temp_done = done + 1
                print('M = [{}.wait, {}.free, {}.busy, {}.inside, {}.docu, {}.done]\n'.format(wait, free,
                                                                                              temp_busy, temp_inside,
                                                                                              temp_docu, temp_done))
                self.CHANGE = Node(wait, free, busy - 1, inside - 1, docu + 1, done + 1, CHANGE_firing_sequence)
                self.CHANGE.insert(wait, free, busy - 1, inside - 1, docu + 1, done + 1, CHANGE_firing_sequence)

            if self.decide_end(docu):
                END_firing_sequence += "end"
                print("Firing_sequence is:", END_firing_sequence)
                END_firing_sequence += ", "
                temp_free = free + 1
                temp_docu = docu - 1
                print('M = [{}.wait, {}.free, {}.busy, {}.inside, {}.docu, {}.done]\n'.format(wait, temp_free,
                                                                                              busy, inside,
                                                                                              temp_docu, done))
                self.END = Node(wait, free + 1, busy, inside, docu - 1, done, END_firing_sequence)
                self.END.insert(wait, free + 1, busy, inside, docu - 1, done, END_firing_sequence)
        else:
            return


def start(mode):
    if mode == 1:
        if specialist_state["free"] > 0:
            specialist_state["free"] -= 1
            specialist_state["busy"] += 1
            print('M = [{}.free, {}.busy, {}.docu]'.format(specialist_state["free"], specialist_state["busy"], specialist_state["docu"]))
    elif mode == 2:
        if patient_state["wait"] > 0:
            patient_state["wait"] -= 1
            patient_state["inside"] += 1
            print('M = [{}.wait, {}.inside, {}.done]'.format(patient_state["wait"], patient_state["inside"], patient_state["done"]))
    elif mode == 3:
        if specialist_state["free"] > 0 and patient_state["wait"] > 0:
            specialist_state["free"] -= 1
            patient_state["wait"] -= 1
            specialist_state["busy"] += 1
            patient_state["inside"] += 1
            print('M = [{}.wait, {}.free, {}.busy, {}.inside,{}.docu, {}.done]'.format(patient_state["wait"],
                                                                                       specialist_state["free"],
                                                                                       specialist_state["busy"],
                                                                                       patient_state["inside"],
                                                                                       specialist_state["docu"],
                                                                                       patient_state["done"]))
    elif mode == 4:
        pass


def change(mode):
    if mode == 1:
        if specialist_state["busy"] > 0:
            specialist_state["busy"] -= 1
            specialist_state["docu"] += 1
            print('M = [{}.free, {}.busy, {}.docu]'.format(specialist_state["free"], specialist_state["busy"], specialist_state["docu"]))
    if mode == 2:
        if patient_state["inside"] > 0:
            patient_state["done"] += 1
            patient_state["inside"] -= 1
            print('M = [{}.wait, {}.inside, {}.done]'.format(patient_state["wait"], patient_state["inside"], patient_state["done"]))
            return
        else:
            print("")
    elif mode == 3:
        if specialist_state["busy"] > 0 and patient_state["inside"] > 0:
            specialist_state["busy"] -= 1
            patient_state["inside"] -= 1
            specialist_state["docu"] += 1
            patient_state["done"] += 1
            print('M = [{}.wait, {}.free, {}.busy, {}.inside,{}.docu, {}.done]'.format(patient_state["wait"],
                                                                                       specialist_state["free"],
                                                                                       specialist_state["busy"],
                                                                                       patient_state["inside"],
                                                                                       specialist_state["docu"],
                                                                                       patient_state["done"]))
    elif mode == 4:
        pass


def end(mode):
    if mode == 1:
        if specialist_state["docu"] > 0:
            specialist_state["docu"] -= 1
            specialist_state["free"] += 1
            print('M = [{}.free, {}.busy, {}.docu]'.format(specialist_state["free"], specialist_state["busy"], specialist_state["docu"]))
    elif mode == 2:
        pass
    elif mode == 3:
        if specialist_state["docu"] > 0:
            specialist_state["docu"] -= 1
            specialist_state["free"] += 1
            print('M = [{}.wait, {}.free, {}.busy, {}.inside, {}.docu, {}.done]'.format(patient_state["wait"],
                                                                                       specialist_state["free"],
                                                                                       specialist_state["busy"],
                                                                                       patient_state["inside"],
                                                                                       specialist_state["docu"],
                                                                                       patient_state["done"]))
    elif mode == 4:
        pass


def Mode_processing(mode):
    if mode == 0:
        sys.exit()
    #SPECIALIST
    elif mode == 1:
        # Enter number of tokens of states
        input_mode = input("Enter the number of tokens of place 'free': ")
        specialist_state["free"] = int(input_mode)
        input_mode = input("Enter the number of tokens of place 'busy': ")
        specialist_state["busy"] = int(input_mode)
        input_mode = input("Enter the number of tokens of place 'docu': ")
        specialist_state["docu"] = int(input_mode)
        print('M0 = [{}.free, {}.busy, {}.docu]'.format(specialist_state["free"], specialist_state["busy"], specialist_state["docu"]))
        mode_operation(mode)
    # PATIENT
    elif mode == 2:
        #Enter number of tokens of states
        input_mode = input("Enter the number of tokens of place 'wait': ")
        patient_state["wait"] = int(input_mode)
        input_mode = input("Enter the number of tokens of place 'inside': ")
        patient_state["inside"] = int(input_mode)
        input_mode = input("Enter the number of tokens of place 'done': ")
        patient_state["done"] = int(input_mode)
        print('M0 = [{}.wait, {}.inside, {}.done]'.format(patient_state["wait"], patient_state["inside"], patient_state["done"]))
        mode_operation(mode)
    #SUPERMODEL_NET
    elif mode == 3 or mode == 4:
        # Enter number of tokens of states of specialist
        input_mode = input("Enter the number of tokens of place 'free': ")
        specialist_state["free"] = int(input_mode)
        input_mode = input("Enter the number of tokens of place 'busy': ")
        specialist_state["busy"] = int(input_mode)
        input_mode = input("Enter the number of tokens of place 'docu': ")
        specialist_state["docu"] = int(input_mode)

        # Enter number of tokens of states of patient
        input_mode = input("Enter the number of tokens of place 'wait': ")
        patient_state["wait"] = int(input_mode)
        input_mode = input("Enter the number of tokens of place 'inside': ")
        patient_state["inside"] = int(input_mode)
        input_mode = input("Enter the number of tokens of place 'done': ")
        patient_state["done"] = int(input_mode)

        print('M0 = [{}.wait, {}.free, {}.busy, {}.inside, {}.docu, {}.done]\n'.format(patient_state["wait"], specialist_state["free"],
                                                                            specialist_state["busy"], patient_state["inside"],
                                                                            specialist_state["docu"], patient_state["done"]))
        mode_operation(mode)
    else:
        main()


def mode_operation(mode):
    # OPERATION
    while True:
        if mode == 2:
            transition = input("Choose the transition to fire\n 1. Start\n 2. Change\n 3. Exit Operation\n Your input: ")
            if int(transition) == 1:
                start(mode)
            elif int(transition) == 2:
                change(mode)
            elif int(transition) == 3:
                return
            else:
                print("Please enter VALID mode number!!!!")
        elif mode == 4:
            root = Node(0, 0, 0, 0, 0, 0, "")
            return
        else:
            transition = input("Choose the transition to fire\n 1. Start\n 2. Change\n 3. End\n 4. Exit Operation\n Your input: ")
            if int(transition) == 1:
                start(mode)
            elif int(transition) == 2:
                change(mode)
            elif int(transition) == 3:
                end(mode)
            elif int(transition) == 4:
                return
            else:
                print("Please enter VALID mode number!!!!")


def Reset_Mode():
    for element in specialist_state:
        specialist_state[element] = 0
    for element in patient_state:
        patient_state[element] = 0


def main():
    while True:
        print(
            " Mode_0 = exit program\n Mode_1 = Specialist_NET\n Mode_2 = Patient_Net\n Mode_3 = SuperModel_Net\n Mode_4 = Reachable_calculator")
        input_mode = input("Enter the Mode: ")
        mode = int(input_mode)
        Mode_processing(mode=mode)
        Reset_Mode()

main()