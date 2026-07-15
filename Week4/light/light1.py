import asyncio
import time
import httpx

BASE_URL = "http://172.16.2.117:8088"
STUDENT_ID = "6710301054"

LIGHT_IDS = ["light_1", "light_2", "light_3", "light_4"]


async def turn_on_light(client: httpx.AsyncClient, light_id: str):
    url = f"{BASE_URL}/api/{STUDENT_ID}/lights/{light_id}"
    payload = {"status": "ON"}

    print(f"-> เปิด {light_id} ...")
    start = time.time()

    await client.post(url, json=payload)

    elapsed = time.time() - start
    print(f"   {light_id} ติดแล้ว (ใช้เวลา {elapsed:.2f} วินาที)")


async def main():
    total_start = time.time()

    async with httpx.AsyncClient(timeout=30) as client:
        for light_id in LIGHT_IDS:
            await turn_on_light(client, light_id)

    total_elapsed = time.time() - total_start
    print(f"\nเปิดครบทุกดวงแล้ว (เวลารวม {total_elapsed:.2f} วินาที)")


if __name__ == "__main__":
    asyncio.run(main())