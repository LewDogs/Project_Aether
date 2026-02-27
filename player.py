
class Player:
    _instance = None  # This stores the single instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # Create the instance only if it doesn't exist
            cls._instance = super(Player, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    

    def init_player(self, looped):
        name = ""
        self.visited = {1}
        self.current_location = 1
        # Not Looped is the initial prompt, if looped is true, it will continue prompting with that sentence.
        if (not looped):
            name = input("Welcome to the New World, Hero! Please, tell me your name: ")
        elif (looped):
            name = input("You didn't say 'yes', so I take that as a no! What is your name, Hero? ")

        # Check the name
        confirm = input("You said your name is " + name + " correct? ")
        if (confirm == "yes" or confirm == "y"):
            print("Brilliant! Welcome " + name + " to the New World. Let us begin our adventure!")
            print("--------")
            self.name = name
            return
        else:
            self.init_player(True)



