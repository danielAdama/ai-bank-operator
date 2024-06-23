import redis

def test_connection():
    try:
        r = redis.Redis(host='localhost', port=6379)
        r.ping()
        print("Connection successful")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_connection()
