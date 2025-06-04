class ChatRoom:
    def __init__(self):
        self.group_messages = []
        self.direct_messages = {}

    def send_group(self, sender, text):
        self.group_messages.append((sender.username, text))

    def send_direct(self, sender, receiver, text):
        key = (sender.username, receiver.username)
        self.direct_messages.setdefault(key, []).append(text)

class User:
    def __init__(self, username):
        self.username = username

class Admin(User):
    def send_group(self, chatroom, text):
        chatroom.send_group(self, text)

    def send_direct(self, chatroom, employee, text):
        chatroom.send_direct(self, employee, text)

class Employee(User):
    def read_group(self, chatroom):
        for sender, msg in chatroom.group_messages:
            print(f"{sender}: {msg}")

    def request_change(self, chatroom, admin, text):
        chatroom.send_direct(self, admin, f"REQUEST: {text}")

def main():
    chatroom = ChatRoom()
    boss = Admin("boss")
    employees = {
        "alice": Employee("alice"),
        "bob": Employee("bob"),
    }
    admins = {"boss": boss}

    current_user = None
    while True:
        if not current_user:
            user = input("Login as (boss/alice/bob or q to quit): ")
            if user == 'q':
                break
            if user in admins:
                current_user = admins[user]
            elif user in employees:
                current_user = employees[user]
            else:
                print("Unknown user")
        else:
            if isinstance(current_user, Admin):
                cmd = input("(A)dmin options: g-send group, d-send direct, r-read group, l-logout: ")
                if cmd == 'g':
                    msg = input("Group message: ")
                    current_user.send_group(chatroom, msg)
                elif cmd == 'd':
                    emp_name = input("Send to employee: ")
                    if emp_name in employees:
                        msg = input("Message: ")
                        current_user.send_direct(chatroom, employees[emp_name], msg)
                    else:
                        print("No such employee")
                elif cmd == 'r':
                    Employee.read_group(current_user, chatroom)
                elif cmd == 'l':
                    current_user = None
            else:
                cmd = input("(E)mployee options: r-read group, c-request change, l-logout: ")
                if cmd == 'r':
                    current_user.read_group(chatroom)
                elif cmd == 'c':
                    msg = input("Change request: ")
                    current_user.request_change(chatroom, boss, msg)
                elif cmd == 'l':
                    current_user = None

if __name__ == '__main__':
    main()
