from time import sleep, ctime, time
import threading

def update_cup_number(customer_name):
    thread_name = threading.current_thread().name

    print(f"{ctime()} | [{thread_name}] LCD: Processing cup number for customer {customer_name}...")
    sleep(1)
    print(f"{ctime()} | [{thread_name}] LCD: Done for customer {customer_name}.")

def make_coffee(customer_name):
    thread_name = threading.current_thread().name

    print(f"{ctime()} | [{thread_name}] Making coffee for customer {customer_name}...")
    sleep(1)
    print(f"{ctime()} | [{thread_name}] Coffee ready for customer {customer_name}!")

    update_cup_number(customer_name)

def main():
    queue = ['A', 'B', 'C']
    threads = []

    print(f"{ctime()} | === Threading Coffee Machine ===")
    start_time = time()

    # สร้าง Thread ให้ลูกค้าแต่ละคน
    for customer in queue:
        t = threading.Thread(
            target=make_coffee,
            args=(customer,),
            name=f"Thread-{customer}"
        )
        threads.append(t)
        t.start()

    # รอให้ทุก Thread ทำงานเสร็จ
    for t in threads:
        t.join()

    duration = time() - start_time
    print(f"{ctime()} | Total time: {duration:0.2f} seconds")

if __name__ == "__main__":
    main()