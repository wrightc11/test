import os
import multiprocessing

check = False
true = 0

def process1(shared_dict):
    # User has to enter 10 different user ID's and names to setup student 'accounts'
    for i in range(10):
        user_id = input("Enter user ID: ")
        name = input("Enter user name: ")
        shared_dict[user_id] = name

def write_text(shared_dict):
    # Write the contents of the memory to textfile to be printed later
    with open('user_ids.txt', 'w') as f:
        for user_id, name in shared_dict.items():
            f.write(f"{user_id},{name}\n")

def process2(shared_dict):
    while check:
        # Check if the user ID is in memory, if yes user enters a candidate voting
        user_id = input("Enter an ID to check: ")
        if user_id in shared_dict:
            name = shared_dict[user_id]
            vote = input("Please select a candidate to vote for (dan, rob, john): ")
            shared_dict[user_id] = (name, vote)
            check = True
        else:
            print("ID Invalid, Try Again")
            check = True

if __name__ == '__main__':
    # Create shared memory
    manager = multiprocessing.Manager()
    shared_dict = manager.dict()

    # Process create
    id_process = multiprocessing.Process(target=process1, args=(shared_dict,))
    check_process = multiprocessing.Process(target=process2, args=(shared_dict,))

    # Process Start
    id_process.start()
    check_process.start()

    # Process finished
    id_process.join()
    check_process.join()

    # Read the file and print out the votes
    with open('user_ids.txt', 'r') as f:
        for line in f:
            fields = line.strip().split(',')
            user_id, name, vote = fields

            print(f"User with ID {user_id} voted for: '{vote}'")
