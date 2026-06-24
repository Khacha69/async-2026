from time import ctime, time
import asyncio

async def update_cup_number(customer_name):
    print(f"{ctime()} | LCD: Processing for customer {customer_name}...")
    await asyncio.sleep(1)
    print(f"{ctime()} | LCD: Done for customer {customer_name}.")

async def make_coffee(customer_name):
    print(f"{ctime()} | Making coffee for {customer_name}...")
    await asyncio.sleep(1)
    print(f"{ctime()} | Coffee ready for {customer_name}!")

    await update_cup_number(customer_name)

async def main():
    queue = ['A', 'B', 'C']

    print(f"{ctime()} | === Asyncio Coffee Machine ===")
    start_time = time()

    tasks = []

    for customer in queue:
        task = asyncio.create_task(make_coffee(customer))
        tasks.append(task)

    await asyncio.gather(*tasks)

    duration = time() - start_time
    print(f"{ctime()} | Total time: {duration:0.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())