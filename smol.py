from main import *


if __name__ == "__main__":
    u1 = User(1,client,allUsers)
    u2 = User(2,client,allUsers)

    # setup government
    gov = Democracy(u1)


    current_user = u1
    while current_user:
        print(current_user)
        actions = gov.unprivilegedActions
        if current_user in gov.leaders:
            actions += gov.privilegedActions
        for indx, action in enumerate(actions):
            print(f'{indx}: {action}')

        # switch turn
        if current_user == u1: 
            current_user = u2 
        else: 
            current_user = u1
        input('Next Turn')



