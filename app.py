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
    shared_customers = []
    for customer in read_csv_file(stores[0]):
        if customer in read_csv_file(stores[1]):
            shared_customers.append(customer)

    shared_customers_str = "\n".join([str(customer) for customer in shared_customers])
    print(shared_customers_str)

    return shared_customers


if __name__ == "__main__":
    shared_customers = find_shared_customers("Store1.csv", "Store2.csv")
