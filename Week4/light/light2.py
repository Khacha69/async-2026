import asyncio
import time
import httpx

BASE_URL = "http://172.16.2.117:8088"
STUDENT_ID = "6710301054"

LIGHT_DELAYS = {
    "light_1": 0.5,
    "light_2": 1.2,
    "light_3": 2.0,
    "light_4": 0.8,
}


async def turn_on_light(client: httpx.AsyncClient, light_id: str):
    url = f"{BASE_URL}/api/{STUDENT_ID}/lights/{light_id}"
    payload = {"status": "ON"}

    print(f"-> กำลังเปิด {light_id} (delay {LIGHT_DELAYS[light_id]}s) ...")
    start = time.time()

    response = await client.post(url, json=payload)

    elapsed = time.time() - start

    if response.status_code == 200:
        print(f"{light_id} ติดแล้ว (ใช้เวลา {elapsed:.2f} วินาที) -> {response.json()}")
    else:
        print(f"{light_id} ผิดพลาด [{response.status_code}] -> {response.text}")


async def main():
    total_start = time.time()

    async with httpx.AsyncClient(timeout=30) as client:
        # ยิงทุกดวงพร้อมกัน (concurrent) แทนการ await ทีละตัว
        tasks = [turn_on_light(client, light_id) for light_id in LIGHT_DELAYS]
        await asyncio.gather(*tasks)

    total_elapsed = time.time() - total_start
    print(f"เวลารวมทั้งหมด: {total_elapsed:.2f} วินาที")


if __name__ == "__main__":
    asyncio.run(main())