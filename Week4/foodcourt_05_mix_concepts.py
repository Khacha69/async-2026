# foodcourt_05_mix_concepts.py
import asyncio
import time
from time import ctime
from food_utils import send_order_to_kitchen

async def main():
    MY_STUDENT_ID = "6710301054"
    print(f"{ctime()} | --- [Task 5] ")
    start_time = time.perf_counter()

    # 
    noodle_task = asyncio.create_task(
        send_order_to_kitchen(MY_STUDENT_ID, "noodle", "Wonton Noodles")
    )

    # 
    chicken_task = asyncio.create_task(
        asyncio.wait_for(
            send_order_to_kitchen(MY_STUDENT_ID, "hainanese_chicken", "Chicken Rice Special"),
            timeout=1.0
        )
    )

    try:
        results = await asyncio.gather(noodle_task, chicken_task)
        print(f"{ctime()} | Success: All food served on time! Received {len(results)} dishes.")
    except asyncio.TimeoutError:
        print(f"{ctime()} | TimeoutError: One of the orders exceeded its deadline.")

    elapsed = time.perf_counter() - start_time
    print(f"{ctime()} | Total elapsed time: {elapsed:.2f} seconds.")


if __name__ == "__main__":
    asyncio.run(main())