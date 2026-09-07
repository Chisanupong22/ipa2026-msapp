import time
import json
from producer import produce
from database import get_router_info


def scheduler():
    INTERVAL = 10.0
    next_run = time.monotonic()
    count = 0

    while True:
        now = time.time()
        now_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
        ms = int((now % 1) * 1000)
        now_str_with_ms = f"{now_str}.{ms:03d}"
        print(f"[{now_str_with_ms}] run #{count}")

        try:
            for data in get_router_info():
                if "_id" in data:
                    data["_id"] = str(data["_id"])

                body_str = json.dumps(data)
                produce("localhost", body_str)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(3)

        count += 1
        next_run += INTERVAL
        time.sleep(max(0.0, next_run - time.monotonic()))


if __name__ == "__main__":
    scheduler()
