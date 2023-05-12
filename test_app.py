import csv
import unittest
import os
from app import (
    Customer,
    read_csv_file,
    find_shared_customers,
    set_shared_customers_to_string,
)


class TestCustomer(unittest.TestCase):
    def test_customer_creation(self):
        customer = Customer("Logan", "Martin", 26, "Ohio")
        self.assertEqual(customer.first_name, "Logan")
        self.assertEqual(customer.last_name, "Martin")
        self.assertEqual(customer.age, 26)
        self.assertEqual(customer.state, "Ohio")

    def test_customer_equal(self):
        customer1 = Customer("Ash", "Ketchup", 13, "Oregon")
        customer2 = Customer("Ash", "Ketchup", 13, "Oregon")
        customer3 = Customer("Mary", "Jane", 22, "")
        customer4 = Customer("Mary", "Jane", 22, "")
        customer5 = Customer("", "", "", "")
        customer6 = Customer("", "", "", "")

        self.assertEqual(customer1, customer2)
        self.assertEqual(customer3, customer4)
        self.assertEqual(customer5, customer6)

    def test_customer_not_equal(self):
        customer1 = Customer("James", "Davis", 19, "Alabama")
        customer2 = Customer("James", "Davis", "19", "Alabama")
        customer3 = Customer("Emily", "Kim", 20, "Wisconsin")
        customer4 = Customer("emily", "Kim", 20, "Wisconsin")
        customer5 = Customer("Mia", "Perez", 32, "Idaho")
        customer6 = Customer("Mia", "Perez", 32, "Utah")

        self.assertNotEqual(customer1, customer2)
        self.assertNotEqual(customer3, customer4)
        self.assertNotEqual(customer5, customer6)

    def test_customer_hash(self):
        customer1 = Customer("Leo", "Flores", 34, "Alaska")
        customer2 = Customer("Logan", "Martin", 26, "Ohio")
        customer3 = Customer("Leo", "Flores", 34, "Alaska")

        self.assertNotEqual(hash(customer1), hash(customer2))
        self.assertEqual(hash(customer1), hash(customer3))

    def test_customer_to_string(self):
        customer1 = Customer("Natalie", "Rivera", 24, "Kansas")
        customer1_string = "Customer: Natalie Rivera, 24, Kansas"
        self.assertEqual(str(customer1), customer1_string)
        customer2 = Customer("Oliver", "Young", 52, "Colorado")
        customer2_string = "Customer: Oliver, Young, 52, Iowa"
        self.assertNotEqual(str(customer2), customer2_string)


class TestCSVFileReading(unittest.TestCase):
    def setUp(self):
        with open("test_file.csv", "w") as file:
            file.write("first_name,last_name,age,state\n")
            file.write("Sam,Wise,30,Maryland\n")
            file.write("Rem,Lock,20,Montana\n")

    def tearDown(self):
        os.remove("test_file.csv")

    def test_read_csv_file(self):
        customers = read_csv_file("test_file.csv")
        self.assertIsInstance(customers, list)
        self.assertTrue(all(isinstance(customer, Customer) for customer in customers))

        self.assertEqual(len(customers), 2)
        self.assertEqual(customers[0].first_name, "Sam")
        self.assertEqual(customers[0].last_name, "Wise")
        self.assertEqual(customers[0].age, 30)
        self.assertEqual(customers[0].state, "Maryland")
        self.assertEqual(customers[1].first_name, "Rem")
        self.assertEqual(customers[1].last_name, "Lock")
        self.assertEqual(customers[1].age, 20)
        self.assertEqual(customers[1].state, "Montana")

        customer1 = read_csv_file("Store1.csv")
        self.assertIsInstance(customer1, list)
        self.assertTrue(all(isinstance(customer, Customer) for customer in customers))

        self.assertEqual(len(customer1), 103)
        self.assertEqual(customer1[0].first_name, "Sophia")
        self.assertEqual(customer1[0].last_name, "Smith")
        self.assertEqual(customer1[0].age, 28)
        self.assertEqual(customer1[0].state, "Hawaii")

        customer2 = read_csv_file("Store2.csv")
        self.assertIsInstance(customer2, list)
        self.assertTrue(all(isinstance(customer, Customer) for customer in customers))

        self.assertEqual(len(customer2), 97)
        self.assertEqual(customer2[0].first_name, "Alex")
        self.assertEqual(customer2[0].last_name, "Smith")
        self.assertEqual(customer2[0].age, 23)
        self.assertEqual(customer2[0].state, "Florida")

    def test_read_csv_file_non_existing_file(self):
        with self.assertRaises(IOError):
            read_csv_file("non_existing_file.csv")

    def test_read_csv_file_empty_file(self):
        with open("empty_file.csv", "w"):
            pass

        with self.assertRaises(StopIteration):
            read_csv_file("empty_file.csv")

        os.remove("empty_file.csv")

    def test_remove_duplicate_customers(self):
        with open("fake_list.csv", "w") as file:
            file.write("first_name,last_name,age,state\n")
            file.write("Mary,Jane,30,New York\n")
            file.write("Mary,Jane,30,New York\n")
            file.write("Carlos,Wake,22,Florida\n")
            file.write("Leo,Flores,48,Utah\n")
            file.write("Carlos,Wake,22,Florida\n")

        duplicates_customers = read_csv_file("fake_list.csv")

        expected_customers = [
            Customer("Mary", "Jane", 30, "New York"),
            Customer("Carlos", "Wake", 22, "Florida"),
            Customer("Leo", "Flores", 48, "Utah"),
        ]

        self.assertEqual(set(duplicates_customers), set(expected_customers))

        os.remove("fake_list.csv")


class TestFindSharedCustomers(unittest.TestCase):
    def test_find_shared_customers(self):
        shared_customers = find_shared_customers("Store1.csv", "Store2.csv")
        self.assertIsInstance(shared_customers, set)
        self.assertEqual(len(shared_customers), 12)

        expected_customers = {
            "Customer: Charlotte Wilson, 58, Idaho",
            "Customer: James Davis, 19, Alabama",
            "Customer: Avery Thompson, 39, Delaware",
            "Customer: Leo Flores, 34, Alaska",
            "Customer: Oliver Young, 52, Colorado",
            "Customer: Dominic Johnson, 71, Ohio",
            "Customer: Madison Martin, 25, Massachusetts",
            "Customer: Logan Martin, 26, Ohio",
            "Customer: Evelyn Harris, 79, Nebraska",
            "Customer: Natalie Rivera, 24, Kansas",
            "Customer: Emily Kim, 72, North Dakota",
            "Customer: Mia Perez, 22, Oregon",
        }

        self.assertSetEqual(
            set(str(customer) for customer in shared_customers), expected_customers
        )


class TestSetSharedCustomersToString(unittest.TestCase):
    def test_set_shared_customers_to_string(self):
        customers = []
