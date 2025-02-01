###############################
# Maxim Muradov
#Id: 346975386
# ex7
###############################

import csv

# Global BST root
ownerRoot = None

########################
# 0) Read from CSV -> HOENN_DATA
########################

def read_hoenn_csv(filename):
    data_list = []
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')
        first_row = True
        for row in reader:
            if first_row:
                first_row = False
                continue
            if not row or not row[0].strip():
                break
            d = {
                "ID": int(row[0]),
                "Name": str(row[1]),
                "Type": str(row[2]),
                "HP": int(row[3]),
                "Attack": int(row[4]),
                "Can Evolve": str(row[5]).upper()
            }
            data_list.append(d)
    return data_list

HOENN_DATA = read_hoenn_csv("hoenn_pokedex.csv")

########################
# 1) Helper Functions
########################

def read_int_safe(prompt):
    """
    Prompt the user for an integer, re-prompting on invalid input.
    """
    while True:
        x = input(prompt)
        if x.lstrip('-').isdigit() and (x[0] == '-' or x.isdigit()):
            return int(x)
        print("Invalid input.")

def get_poke_dict_by_id(poke_id):
    """
    Return a copy of the Pokemon dict from HOENN_DATA by ID, or None if not found.
    """
    for pokemon in HOENN_DATA:
        if pokemon['ID'] == poke_id:
            return pokemon
    return None

def get_poke_dict_by_name(name):
    """
    Return a copy of the Pokemon dict from HOENN_DATA by name, or None if not found.
    """
    for pokemon in HOENN_DATA:
        if pokemon['Name'].lower() == name.lower():
            return pokemon
    return None

def display_pokemon_list(poke_list):
    """
    Display a list of Pokemon dicts, or a message if empty.
    """
    if not poke_list:
        print("There are no pokemons in this Pokedex.\n")
        return
    for pokemon in poke_list:
        print(f"ID: {pokemon['ID']}, Name: {pokemon['Name']}, Type: {pokemon['Type']}, HP: {pokemon['HP']}, Attack: {pokemon['Attack']}, Can Evolve: {'TRUE' if pokemon['Can Evolve'] == 'TRUE' else 'FALSE'}")

########################
# 2) BST (By Owner Name)
########################

def create_owner_node(owner_name, first_pokemon=None):
    """
    Create and return a BST node dict with keys: 'owner', 'pokedex', 'left', 'right'.
    """
    return {
        "owner": owner_name,
        "pokedex": [HOENN_DATA[first_pokemon]],
        "left": None,
        "right": None
    }

def insert_owner_bst(root, new_node):
    """
    Insert a new BST node by owner_name (alphabetically). Return updated root.
    """
    if not root:
        return new_node
    if new_node["owner"].lower() == root["owner"].lower():
        return root
    elif new_node["owner"].lower() < root["owner"].lower():
        root["left"] = insert_owner_bst(root["left"], new_node)
    else:
        root["right"] = insert_owner_bst(root["right"], new_node)
    return root

def find_owner_bst(root, owner_name):
    """
    Locate a BST node by owner_name. Return that node or None if missing.
    """
    if not root:
        return None
    if root['owner'].lower() == owner_name.lower():
        return root
    elif root['owner'].lower() > owner_name.lower():
        return find_owner_bst(root['left'], owner_name)
    else:
        return find_owner_bst(root['right'], owner_name)

def min_node(node):
    """
    Return the leftmost node in a BST subtree.
    """
    while node["left"] is not None:
        node = node["left"]
    return node

def delete_owner_bst(root, owner_name):
    """
    Remove a node from the BST by owner_name. Return updated root.
    """
    if not root:
        return None
    if root['owner'].lower() > owner_name.lower():
        root['left'] = delete_owner_bst(root['left'], owner_name)
    elif root['owner'].lower() < owner_name.lower():
        root['right'] = delete_owner_bst(root['right'], owner_name)
    else:
        if root["left"] is None:
            return root['right']
        elif root["right"] is None:
            return root['left']
        else:
            temp = min_node(root["right"])
            root['owner'], root['pokedex'] = temp["owner"], temp["pokedex"]
            root['right'] = delete_owner_bst(root['right'], temp["owner"])
    return root

########################
# 3) BST Traversals
########################

def bfs_traversal(root):
    owner_list = []
    gather_all_owners(root, owner_list)
    for i in owner_list:
        print(f"Owner: {i['owner']}")
        display_pokemon_list(i["pokedex"])

def pre_order(root):
    if root is None:
        return
    print(f"Owner: {root['owner']}")
    display_pokemon_list(root['pokedex'])
    pre_order(root["left"])
    pre_order(root["right"])

def in_order(root):
    if root is None:
        return
    in_order(root["left"])
    print(f"Owner: {root['owner']}")
    display_pokemon_list(root["pokedex"])
    in_order(root["right"])

def post_order(root):
    if root is None:
        return
    post_order(root["left"])
    post_order(root["right"])
    print(f"Owner: {root['owner']}")
    display_pokemon_list(root["pokedex"])

########################
# 4) Pokedex Operations
########################

def add_pokemon_to_owner(owner_node):
    """
    Prompt user for a Pokemon ID, find the data, and add to this owner's pokedex if not duplicate.
    """
    id = read_int_safe("Enter Pokemon ID to add: ")
    if id < 0 or id > 135:
        print(f"ID {id} not found in Hoenn data.\n")
        return
    new_pokemon = get_poke_dict_by_id(id)
    if new_pokemon is None:
        print(f"ID {id} not found in Hoenn data.\n")
        return
    for i in owner_node['pokedex']:
        if i == new_pokemon:
            print("Pokemon already in the list. No changes made.\n")
            return
    owner_node["pokedex"].append(new_pokemon)
    print(f"Pokemon {new_pokemon['Name']} (ID {new_pokemon['ID']}) added to {owner_node['owner']}'s Pokedex.")

def release_pokemon_by_name(owner_node):
    """
    Prompt user for a Pokemon name, remove it from this owner's pokedex if found.
    """
    name = input("Enter Pokemon Name to release: ")
    for i in owner_node['pokedex']:
        if name.lower() in i['Name'].lower():
            owner_node['pokedex'].remove(i)
            print(f"Releasing {i['Name']} from {owner_node['owner']}.\n")
            return
    print(f"No Pokemon named '{name}' in {owner_node['owner']}'s Pokedex.\n")

def evolve_pokemon_by_name(owner_node):
    """
    Evolve a Pokemon by name:
    1) Check if it can evolve
    2) Remove old
    3) Insert new
    4) If new is a duplicate, remove it immediately
    """
    name = input("Enter Pokemon Name to evolve: ")
    for i in owner_node['pokedex']:
        if name.lower() in i['Name'].lower():
            if i['Can Evolve'] == 'FALSE':
                print(f"Pokemon {i['Name']} cannot evolve.\n")
                return
            elif i['Can Evolve'] == 'TRUE':
                id = get_poke_dict_by_id(i['ID'] + 1)
                print(f"Pokemon evolved from {i['Name']} (ID {i['ID']}) to {id['Name']} (ID {id['ID']}).")
                owner_node['pokedex'].remove(i)
                for i in owner_node['pokedex']:
                    if i == id:
                        count = owner_node['pokedex'].index(i)
                        owner_node['pokedex'].remove(i)
                        print(f"{i['Name']} was already present; releasing it immediately.\n")
                        owner_node['pokedex'].insert(count, id)
                        return
                owner_node['pokedex'].append(id)
                return
    print(f"No Pokemon named '{name}' in {owner_node['owner']}'s Pokedex.\n")

########################
# 5) Sorting Owners by # of Pokemon
########################

def gather_all_owners(root, arr):
    """
    Collect all BST nodes into a list (arr).
    """
    if root is None:
        return
    arr.append(root)
    gather_all_owners(root['left'], arr)
    gather_all_owners(root['right'], arr)

def sort_owners_by_num_pokemon():
    """
    Gather owners, sort them by (#pokedex size, then alpha), print results.
    """
    global ownerRoot
    if not ownerRoot:
        print("No owners at all.\n")
        return
    owner_list = []
    gather_all_owners(ownerRoot, owner_list)
    owner_list.sort(choice=lambda owner_node: (len(owner_node['pokedex']), owner_node['owner'].lower()))
    print("=== The Owners we have, sorted by number of Pokemons ===")
    for i in owner_list:
        print(f"Owner: {i['owner']} (has {len(i['pokedex'])} Pokemon)")

########################
# 6) Print All
########################

def print_all_owners():
    """
    Let user pick BFS, Pre, In, or Post. Print each owner's data/pokedex accordingly.
    """
    global ownerRoot
    if not ownerRoot:
        print("No owners in the BST.\n")
        return
    print('1) BFS\n'
          '2) Pre-Order\n'
          '3) In-Order\n'
          '4) Post-Order\n')
    choice = read_int_safe("Your choice: \n")
    if choice == 1:
        bfs_traversal(ownerRoot)
    elif choice == 2:
        pre_order(ownerRoot)
    elif choice == 3:
        in_order(ownerRoot)
    elif choice == 4:
        post_order(ownerRoot)
    else:
        print("Invalid choice.")

########################
# 7) The Display Filter Sub-Menu
########################

def display_filter_sub_menu(owner_node):
    while True:
        print('\n-- Display Filter Menu --')
        print('1. Only a certain Type\n'
              '2. Only Evolvable\n'
              '3. Only Attack above __\n'
              '4. Only HP above __\n'
              '5. Only names starting with letter(s)\n'
              '6. All of them!\n'
              '7. Back')
        choice = read_int_safe("Your choice: ")
        if choice == 1:
            print_pokemon_type(owner_node)
        elif choice == 2:
            print_evolvable(owner_node)
        elif choice == 3:
            print_attack_above(owner_node)
        elif choice == 4:
            print_hp_above(owner_node)
        elif choice == 5:
            print_names(owner_node)
        elif choice == 6:
            display_pokemon_list(owner_node['pokedex'])
        elif choice == 7:
            print("Back to Pokedex Menu.")
            break
        else:
            print("Invalid choice.")

def print_pokemon_type(node):
    """
    By type
    """
    pokemon_type = input("Which Type? (e.g. GRASS, WATER): ")
    pokedex = node["pokedex"]
    type_exist = sum(1 for pokemon in node['pokedex'] if pokemon["Type"].lower() == pokemon_type.lower())
    if type_exist == 0:
        print("There are no Pokemons in this Pokedex that match the criteria.\n")
        return
    for i in node["pokedex"]:
        if i["Type"].lower() == pokemon_type.lower():
            print(f"ID: {i['ID']}, Name: {i['Name']}, Type: {i['Type']}, HP: {i['HP']}, Attack: {i['Attack']}, Can Evolve: {'TRUE' if i['Can Evolve'] == 'TRUE' else 'FALSE'}")
    print('\n')

def print_evolvable(node):
    """
    BY evolving ability
    """
    pokedex = node['pokedex']
    can_evolve = sum(1 for pokemon in pokedex if pokemon['Can Evolve'] == 'TRUE')
    if can_evolve == 0:
        print("There are no Pokemons in this Pokedex that match the criteria.\n")
        return
    for i in node['pokedex']:
        if i['Can Evolve'] == 'TRUE':
            print(f"ID: {i['ID']}, Name: {i['Name']}, Type: {i['Type']}, HP: {i['HP']}, Attack: {i['Attack']}, Can Evolve: {'TRUE' if i['Can Evolve'] == 'TRUE' else 'FALSE'}")
    print('\n')

def print_attack_above(node):
    """
    By attack
    """
    attack = read_int_safe("Enter Attack threshold: ")
    pokedex = node['pokedex']
    attack_s = sum(1 for pokemon in pokedex if pokemon['Attack'] >= attack)
    if attack_s == 0:
        print("There are no Pokemons in this Pokedex that match the criteria.\n")
        return
    for i in node['pokedex']:
        if i['Attack'] >= attack:
            print(f"ID: {i['ID']}, Name: {i['Name']}, Type: {i['Type']}, HP: {i['HP']}, Attack: {i['Attack']}, Can Evolve: {'TRUE' if i['Can Evolve'] == 'TRUE' else 'FALSE'}")
    print('\n')

def print_hp_above(node):
    """
    By hp
    """
    hp = read_int_safe("Enter HP threshold: ")
    pokedex = node['pokedex']
    hp_s = sum(1 for pokemon in pokedex if pokemon['HP'] >= hp)
    if hp_s == 0:
        print("There are no Pokemons in this Pokedex that match the criteria.\n")
        return
    for i in node['pokedex']:
        if i['HP'] >= hp:
            print(f"ID: {i['ID']}, Name: {i['Name']}, Type: {i['Type']}, HP: {i['HP']}, Attack: {i['Attack']}, Can Evolve: {'TRUE' if i['Can Evolve'] == 'TRUE' else 'FALSE'}")
    print('\n')

def print_names(node):
    """
    By name
    """
    name = input("Starting letter(s): ")
    pokedex = node['pokedex']
    letters = sum(1 for pokemon in pokedex if pokemon['Name'].lower().startswith(name.lower()))
    if letters == 0:
        print("There are no Pokemons in this Pokedex that match the criteria.\n")
        return
    for i in node['pokedex']:
        if i['Name'].lower().startswith(name.lower()):
            print(f"ID: {i['ID']}, Name: {i['Name']}, Type: {i['Type']}, HP: {i['HP']}, Attack: {i['Attack']}, Can Evolve: {'TRUE' if i['Can Evolve'] == 'TRUE' else 'FALSE'}")
    print('\n')

########################
# 8) Sub-menu & Main menu
########################

def new_pokedex():
    """
    Creating and insrting newpokedex
    """
    global ownerRoot
    name = input("Owner name: ")
    root = find_owner_bst(ownerRoot, name)
    if root is not None:
        print(f"Owner '{name}' already exists. No new Pokedex created.\n")
        return
    print('Choose your starter Pokemon:\n'
          '1) Treecko\n'
          '2) Torchic\n'
          '3) Mudkip')
    while True:
        starter = read_int_safe("Your choice: ")
        if starter < 0 or starter > 3:
            print("Invalid input.")
        else:
            break
    starter_map = {1: 0, 2: 3, 3: 6}
    starter_index = starter_map[starter]
    if ownerRoot is None:
        ownerRoot = create_owner_node(name, starter_index)
    else:
        new_node = create_owner_node(name, starter_index)
        ownerRoot = insert_owner_bst(ownerRoot, new_node)
    print('New Pokedex created for ' + name + ' with starter ' + HOENN_DATA[starter_index]['Name'] + ".\n")

def delete_owner():
    """
    delete owner
    """
    name = input("Enter owner to delete: ")
    global ownerRoot
    if not ownerRoot:
        print("No owners to delete.\n")
        return
    root = find_owner_bst(ownerRoot, name)
    if root is None:
        print(f"Owner '{name}' not found.")
        return
    print(f"Deleting {root['owner']}'s entire Pokedex...")
    ownerRoot = delete_owner_bst(ownerRoot, name)
    print("Pokedex deleted.")


def existing_pokedex():
    """
    Ask user for an owner name, locate the BST node, then show sub-menu:
    - Add Pokemon
    - Display (Filter)
    - Release
    - Evolve
    - Back
    """
    global ownerRoot
    if not ownerRoot:
        print("No owners at all.\n")
        return
    name = input("Owner name: ")
    root = find_owner_bst(ownerRoot, name)
    if root is None:
        print(f"Owner '{name}' not found.\n")
        return
    while True:
        print("\n-- " + root["owner"] + "'s Pokedex Menu --")
        print('1. Add Pokemon\n'
              '2. Display Pokedex\n'
              '3. Release Pokemon\n'
              '4. Evolve Pokemon\n'
              '5. Back to Main\n')
        choice = read_int_safe("Your choice: ")
        if choice == 1:
            add_pokemon_to_owner(root)
        elif choice == 2:
            display_filter_sub_menu(root)
        elif choice == 3:
            release_pokemon_by_name(root)
        elif choice == 4:
            evolve_pokemon_by_name(root)
        elif choice == 5:
            print("Back to Main Menu.")
            break
        else:
            print("Invalid choice.")

def main_menu():
    print('=== Main Menu ===')
    print('1. New Pokedex\n'
          '2. Existing Pokedex\n'
          '3. Delete a Pokedex\n'
          '4. Display owners by number of Pokemon\n'
          '5. Print All\n'
          '6. Exit')

def main():
    while True:
        main_menu()
        choice = read_int_safe("Your choice: ")
        if choice == 1:
            new_pokedex()
        elif choice == 2:
            existing_pokedex()
        elif choice == 3:
            delete_owner()
        elif choice == 4:
            sort_owners_by_num_pokemon()
        elif choice == 5:
            print_all_owners()
        elif choice == 6:
            break
        else:
            print("Invalid choice.")
    print("Goodbye!\n")

if __name__ == "__main__":
    main()
