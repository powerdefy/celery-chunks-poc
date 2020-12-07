import csv

from faker import Faker

fake = Faker()

csv_file_path = "test.csv"
with open(csv_file_path, "w") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=["first_name", "last_name"])
    writer.writeheader()
    for _ in range(10000):
        first_name, last_name, *_ = fake.name().split(" ")
        writer.writerow({"first_name": first_name, "last_name": last_name})
