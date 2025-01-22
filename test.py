

people = []

def sign_up():
    while True:
        global people
        if len(people) >=4:
            print("no more signup!")
            print(f"list of people {people}")
            break
        else:
            people.append(input("input name: "))
            print(len(people))

sign_up()