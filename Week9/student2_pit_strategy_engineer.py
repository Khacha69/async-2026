import asyncio
import redis.asyncio as redis

# ⚙️ CONFIGURATION
REDIS_HOST = '172.16.46.79'
GROUP_ID = 'g01'
STUDENT_ID = '6710301054'

STREAM_KEY = f"f1:telemetry:{GROUP_ID}"
GROUP_NAME = "f1_pitwall"
CONSUMER_NAME = f"engineer_pit_strategy_{STUDENT_ID}"

async def init_group(r: redis.Redis):
    try:
        await r.xgroup_create(STREAM_KEY, GROUP_NAME, id="$", mkstream=True)
        print(f"✅ Consumer Group '{GROUP_NAME}' initialized.")
    except redis.ResponseError as e:
        if "BUSYGROUP" not in str(e): raise e

async def process_message(msg_id, data):
    """แยกฟังก์ชันประมวลผล 1 ข้อความ คืนค่า True/False ว่าประมวลผลสำเร็จไหม"""
    try:
        tire_wear = float(data['tire_wear'])   # อาจ error ได้ที่นี่
    except (KeyError, ValueError) as e:
        print(f"⚠️ Bad data in {msg_id}: {e} -> skip & ack")
        return  # ข้ามข้อความเสีย แต่ยัง ack ต่อ (ดูด้านล่าง)

    if tire_wear > 75.0:
        print(f"🛞 🚨 [PIT STRATEGY] BOX BOX BOX! Tires critical: {tire_wear}% (ID: {msg_id})")
    elif tire_wear > 50.0:
        print(f"🛞 ⚠️ [PIT STRATEGY] Prepare Soft Compound. Tires at {tire_wear}%")

async def pit_strategy_worker():
    r = redis.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)
    await init_group(r)
    print(f"🔧 Pit Strategy Engineer Ready... [Consumer: {CONSUMER_NAME}]")

    try:
        while True:
            try:
                entries = await r.xreadgroup(GROUP_NAME, CONSUMER_NAME, {STREAM_KEY: '>'}, count=10, block=1000)
            except redis.ConnectionError as e:
                print(f"🔌 Connection lost: {e} -> retry in 2s")
                await asyncio.sleep(2)   # กัน loop รัวถี่เกินตอน connection หลุด
                continue

            if entries:
                for stream, msgs in entries:
                    for msg_id, data in msgs:
                        await process_message(msg_id, data)
                        # ack เสมอ ไม่ว่า process_message จะเจอ error ภายในหรือไม่
                        await r.xack(STREAM_KEY, GROUP_NAME, msg_id)
            # ตัด asyncio.sleep(0.01) ออก เพราะ block=1000 หน่วงให้อยู่แล้วตอนไม่มีข้อมูล
    finally:
        await r.aclose()   # ปิด connection ให้เรียบร้อยตอน Ctrl+C หรือ error ร้ายแรง
        print("👋 Connection closed.")

if __name__ == "__main__":
    try:
        asyncio.run(pit_strategy_worker())
    except KeyboardInterrupt:
        print("🛑 Stopped by user.")