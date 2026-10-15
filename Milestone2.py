import csv

with open("IoT - 23 Import.csv", newline='') as file:
    reader = csv.DictReader(file)

    for row in reader:
        protocol= row["protocol"]
        service= row["service"]
        orig= int(row["orig_bytes"])
        resp= int(row["resp_bytes"])

        sum= orig + resp

        if service== sum > 500:
            result= "Flagged"
            reason= "bytes exceed over 500"
        elif sum > 500:
            result= "flagged"
            reason= "high traffic"
        else:
            result= "not flagged"
            reason= "low traffic"

        print("Protocol:", protocol)
        print("Service:", service)
        print("Sum Bytes:", sum)
        print("Result:", result)
        print("Reason:", reason)
        print()