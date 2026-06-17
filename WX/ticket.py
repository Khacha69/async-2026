import sys

def calculate_ticket_price(age):
    if age < 12:
        return 120
    elif age <= 60:
        return 200
    else:
        return 150

def main():
    test_age = int(input("age = "))
    result = calculate_ticket_price(test_age)
    print("price", result)

if __name__ == "__main__":
    main()