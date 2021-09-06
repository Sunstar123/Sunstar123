leaf_container = {}


class Leaf:
	def __init__(self, key, parent, name):
		self.key = key
		self.parent = parent
		self.name = name
		self.kids = []
		self.kids_names = []

	def __str__(self):
		return str(self.name)


def create_leaf(key, parent_name, name):
	if parent_name:
		parent = ""
		for leaf in leaf_container.values():
			if leaf.name == parent_name:
				parent = leaf
		if not parent:
			return False
	else:
		parent = parent_name
	leaf_container[key] = Leaf(key, parent, name)
	try:
		parent.kids.append(leaf_container[key])
		parent.kids_names.append(name)
	except AttributeError:
		pass

	return True


def print_tree(start):
	if start == "failure":
		return False
	if start.kids:
		print(f"Parent {start} contains: {str(start.kids_names)[1:-1]}")
	else:
		print(f"Child {start} contains nothing")  # optional whether one print statement is desired per leaf/branch
	for kid in start.kids:
		print_tree(kid)
	return True


def print_ancestry(start):
	if start == "failure":
		return False
	if start.parent:
		print(f"Parent of {start.name} is {start.parent.name}")
		print_ancestry(start.parent)
	else:
		print(f"{start.name} has no parent")
	return True


def name_to_leaf(name):
	for leaf in leaf_container.values():
		if leaf.name == name:
			return leaf
	return "failure"


def commands():
	print("""
List of Commands:
help: show these commands
quit: end the program
np: create a new parent
nc: create a new child
pt: print tree from any branch
pa: print ancestry of any leaf
""")


def main():
	commands()
	print("Welcome To Tree\nGive all points different names to avoid problems\n")
	run = True
	while run:
		# print("\n")
		com = input("Enter a command:\n")
		if com == "help":
			commands()
		elif com == "quit":
			run = False
		elif com == "np":
			name = input("Enter a name: ")
			print(f"Parent created with name: {name}")
			create_leaf(len(leaf_container), "", name)
		elif com == "nc":
			if len(leaf_container) > 0:
				name = input("Enter a name: ")
				parent = input("Enter the name of the parent: ")
				if create_leaf(len(leaf_container), parent, name):
					print(f"Child of parent: {parent} created with name: {name}")
				else:
					print("No node exists with name:", parent)
			else:
				print("Cannot create a new child when there is no parents")
		elif com == "pa":
			starting_point = input("Enter the starting point name")
			if not print_ancestry(name_to_leaf(starting_point)):
				print("That starting point does not exist")
		elif com == "pt":
			starting_point = input("Enter the starting point name")
			if not print_tree(name_to_leaf(starting_point)):
				print("That starting point does not exist")
		else:
			print("Command not recognized")
			print("Type 'help' for a list of commands")


main()
