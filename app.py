import csv


class Customer:
    def __init__(self, first_name, last_name, age, state):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.state = state
        self.identifier = (first_name, last_name, age, state)

    def __eq__(self, other):
        if isinstance(other, Customer):
            return self.identifier == other.identifier
        return False

    def __hash__(self):
        return hash(self.first_name + self.last_name + str(self.age) + self.state)

    def __str__(self):
        return "Customer: %s %s, %s, %s" % (
            self.first_name,
            self.last_name,
            self.age,
            self.state,
        )


def read_csv_file(filename):
    customers = []
    with open(filename, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            customer = Customer(*row)
            if customer not in customers:
                customers.append(customer)
    return customers


def find_shared_customers(*stores):
    if stores is not None:
        shared_customers = set(read_csv_file(stores[0]))
        for store in stores[1:]:
            shared_customers.intersection_update(read_csv_file(store))
    return shared_customers


def set_shared_customers_to_string(shared_customers):
    return "\n".join([str(customer) for customer in shared_customers])


### For printing and testing purposes ###
if __name__ == "__main__":
    shared_customers = find_shared_customers("Store1.csv", "Store2.csv")
    shared_customers_str = set_shared_customers_to_string(shared_customers)
    print(shared_customers_str)
