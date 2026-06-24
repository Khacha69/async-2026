from time import sleep, ctime, time
import multiprocessing

def update_cup_number(customer_name):
    print(f"{ctime()} | LCD: Processing for customer {customer_name}...")
    sleep(1)
    print(f"{ctime()} | LCD: Done for customer {customer_name}.")

def make_coffee(customer_name):
    print(f"{ctime()} | Making coffee for {customer_name}...")
    sleep(1)
    print(f"{ctime()} | Coffee ready for {customer_name}!")

    update_cup_number(customer_name)

def main():
    queue = ['A', 'B', 'C']
    processes = []

    print(f"{ctime()} | === Multi-processing Coffee Machine ===")
    start_time = time()

    # สร้าง Process ให้ลูกค้าแต่ละคน
    for customer in queue:
        p = multiprocessing.Process(
            target=make_coffee,
            args=(customer,)
        )
        processes.append(p)

    # สั่งให้ทุก Process เริ่มทำงาน
    for p in processes:
        p.start()

    # รอให้ทุก Process ทำงานเสร็จ
    for p in processes:
        p.join()

    duration = time() - start_time
    print(f"{ctime()} | Total time: {duration:0.2f} seconds")

if __name__ == "__main__":
    main()