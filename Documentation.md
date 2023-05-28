# Documentation

<!--
I know that Python 3 is the standard now, I just kept the default build that was on my system. Did not want to install any dependency or upgrade if it was not necessary.
-->

## Tools

Language: Python 2.7 </br>
Testing Framework: Unittest </br>
Formatter: Black

## Summary

Create a Customer class with constructor which hold a first name, last name, age and state to match the csv files. Also have a equality operator, hash and string method.

The read_csv_file function read the the csv files and return a list of customers objects without any duplicates.

The find_share_customers function can take X numbers of csv files as input. It reads all the csv files using the read_csv_file function and return an Customer objects with customers that all the csv files share.

The set_shared_customers_to_string function takes the shared_customers set as the input and convert it into a format where it is more readable.

## Code Breakdown

<strong>Customer Class</strong>

<!--
    class Customer:

    A class representing a customer.

    Attributes:
        first_name (str): The customer's first name.
        last_name (str): The customer's last name.
        age (int): The customer's age.
        state (str): The customer's state.
        identifier (tuple): A tuple representing the customer's identifier.

-->

    def __init__(self, first_name, last_name, age, state):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.state = state
        self.identifier = (first_name, last_name, age, state)

<!--
    Initializes a new instance of the Customer class.

        The function initializes the instance's first name, last name, age, and state attributes using the arguments passed in

        Args:
            first_name (str): The customer's first name.
            last_name (str): The customer's last name.
            age (int): The customer's age.
            state (str): The customer's state.
-->

    def __eq__(self, other):
        if isinstance(other, Customer):
            return self.identifier == other.identifier
        return False

<!--
    Determines whether two customers are equal.

        Args:
            other (Customer): The other customer to compare with.

        Returns:
            bool: True if the customers are equal, False otherwise.

        Examples:
            Customer('Alex' "Reed', 27, 'Nebraska) == Customer('Alex' "Reed', 27, 'Nebraska) return True

            Customer('Sally', 'May', 30, 'California') == Customer('Sally', 'May', 25, 'California') return False because they are not strictly equal. While they may have 3/4 attributes the same, all attribute need to be the same for the function to return True.

            Customer('Nessie' "Jackson', 22, 'Kentucky')  == Customer('Will' "Cameron', 22, 'Washington') return False
-->

    def __hash__(self):
        return hash(self.identifier)

<!--
    Computes a hash value for the customer.

        Returns:
            int: A hash value for the customer.
-->

    def __str__(self):
        return "Customer: %s %s, %s, %s" % (
            self.first_name,
            self.last_name,
            self.age,
            self.state,
        )

<!--
    Gets a string representation of the customer.

        Returns:
            str: A string representation of the customer.

            Examples: Customer: Avery Thompson, 39, Delaware
                      Customer: Oliver Young, 52, Colorado
-->

<strong>Read CSV Files</strong>

    def read_csv_file(filename):
      customers = []
        with open(filename, "r") as file:
          reader = csv.reader(file)
        try:
            next(reader)
        except StopIteration:
            raise StopIteration("CSV file is empty")
        for row in reader:
            first_name, last_name, age, state = row
            if age:
                customer = Customer(first_name, last_name, int(age), state)
            if customer not in customers:
                customers.append(customer)
        return customers

<!--
    Reads a CSV file containing customer data.

    Args:
        filename (str): The name of the CSV file to read.
        errorHandler to check for an empty csv file.

    Returns:
        list: A list of Customer objects.

-->

<strong>Find Shared Customers</strong>

      def find_shared_customers(*stores):
        if stores is not None:
          shared_customers = set(read_csv_file(stores[0]))
        for store in stores[1:]:
            shared_customers.intersection_update(read_csv_file(store))
        return shared_customers

<!--
    Finds the customers that are shared across multiple stores.

    Args:
        *stores (str): The names of the CSV files containing the store data.

        Call the read csv function on each store and find the customers that visited every store.

    Returns:
        set: A set of Customer objects that are shared across all stores.
-->

<strong>Set Shared Customers To String</strong>

      def set_shared_customers_to_string(shared_customers):
        return "\n".join([str(customer) for customer in shared_customers])

<!--
    Converts a set of shared customers to a string.

    Args:
        shared_customers (set): A set of Customer objects.

    Returns:
        str: A string representation of the shared customers.

    Example:

        shared_customers = set(
          Customer('Alex', 'Reed', 26, 'Ohio'),
          Customer('Max', 'Carwell', 32, 'Oklahoma'),
          Customer('Sam', 'Press', 20, 'Montana'),
          Customer('Monica', 'Samson', 21, 'Maine')
        )

        expected_result = "
          Customer: Alex Reed, 26, Ohio
          Customer: Max Carwell, 32, Oklahoma
          Customer: Sam Press, 20, Montana
          Customer: Monica Samson, 21, Maine
        "
-->
