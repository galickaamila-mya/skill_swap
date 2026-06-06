import os
import sys
import time
import redis


def main():
    host = os.environ.get("REDIS_HOST", "127.0.0.1")
    port = int(os.environ.get("REDIS_PORT", "6379"))
    attempts = int(os.environ.get("REDIS_WAIT_ATTEMPTS", "30"))
    for attempt in range(1, attempts + 1):
        try:
            client = redis.Redis(
                host=host, port=port, socket_connect_timeout=3, socket_timeout=3
            )
            client.ping()
            print(f"Redis готов: {host}:{port}")
            return
        except redis.RedisError as exc:
            print(
                f"[{attempt}/{attempts}] Redis недоступен ({host}:{port}): {exc}"
            )
            time.sleep(1)
    print("Не удалось подключиться к Redis.", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
