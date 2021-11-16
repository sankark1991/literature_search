"""Main file for modifying the database"""
import pickle
import argparse


# We want the following functionality: given a year and a list of 1-3 authors, list all papers (handle + title) which
# involve all those authors and are from within 2 years of that year.


# Add new paper
def add_new_entry(D):
    year = int(input('Type the reference year. '))
    month = int(input('Type the reference month. '))
    arxiv = input('Type the arXiv identifier. ')
    authors = input("Type the list of author last names, separated by commas (no spaces). ").split(',')
    tags = input("Add tags, separated by ' ; '.").split(' ; ')
    name = input("Type the reference handle, or type x if you would like one automatically generated. ")
    if name == 'x':
        name = f"{authors[0]}-{year}-{month}"

    print("Type the handles for the important papers which this paper cites. Type 'done' when finished.")
    parents = []
    while True:
        X = input()
        if X == 'done':
            break
        else:
            parents.append(X)


    print("Type the handles for the important papers which cite this paper. Type 'done' when finished.")
    children = []
    while True:
        X = input()
        if X == 'done':
            break
        elif X == '\n':
            pass
        else:
            children.append(X)

    D[name] = {'year': year,
               'month': month,
               'arxiv': arxiv,
               'authors': authors,
               'tags': tags,
               'parents': parents,
               'children': children}

    for c in children:
        if c in D.keys():
            D[c]['parents'].append(name)
    for p in parents:
        if p in D.keys():
            D[p]['children'].append(name)
    f = open('database.pckl', 'wb')
    pickle.dump(D, f)
    f.close()

# Delete a paper
def delete_entry(D):
    name = input('Type the reference handle. ')
    D.pop(name)
    for k in D.keys():
        d = D[k]
        d['parents'].remove(name)
        d['children'].remove(name)

# Rename a paper TODO
def rename(D, name):
    pass

# Modify an entry TODO
def modify_entry(d):

    pass

def create_database(filename):
    f = open(f"{filename}.pckl", 'wb')
    pickle.dump(dict(), f)
    f.close()

def main(args):
    filename = args.filename
    if args.new_database:
        create_database(filename)
    f = open(f"{filename}.pckl", 'rb')
    D = pickle.load(f)
    f.close()

    print('Current list of papers:')
    for name in D.keys():
        print(f"\nName: {name}")
        entry = D[name]
        for k in entry.keys():
            print(f"{k}: {entry[k]}")

    while True:
        print_str = "\nWhat would you like to do?"
        print_str += "\nmk = add a paper"
        print_str += "\nx = exit"
        print_str += "\nrm = remove a paper"
        print_str += "\nls = list the paper handles"
        print_str += "\nopen XXX = get information about paper XXX"
        print_str += "\nmod XXX = modify information about paper XXX"
        X = input(print_str + "\n")
        if X == 'x':
            break
        elif X == 'mk':
            add_new_entry(D)
        elif X == 'rm':
            delete_entry(D)
        elif X == 'ls':
            for k in D.keys():
                print(k)
            print("")
        elif X[:4] == 'open':
            print("")
            d = D[X[5:]]
            for k in d.keys():
                print(f"{k}: {d[k]}")
            print("")
        elif X[:3] == 'mod':
            d = D[X[4:]]
            modify_entry(d)
        else:
            print('Command not understood.')

    f = open(f"{filename}.pckl", 'wb')
    pickle.dump(D, f)
    f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--filename',
        type=str, default='database'
    )
    parser.add_argument(
        '--new_database',
        type=bool, default=False
    )
    args = parser.parse_args()
    main(args)