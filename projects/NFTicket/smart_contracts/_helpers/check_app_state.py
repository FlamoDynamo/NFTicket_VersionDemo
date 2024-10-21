# smart_contracts\_helpers\check_app_state.py:
import os
from algosdk.v2client import algod
from dotenv import load_dotenv
from algosdk import encoding

# Tải biến môi trường từ file .env
load_dotenv()

ALGOD_ADDRESS = os.getenv('NODELY_ENDPOINT_URL')
ALGOD_TOKEN = os.getenv('NODELY_API_KEY')
APP_ID = 724715171  # Application ID của bạn

# Khởi tạo client
client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

def check_app_state(app_id):
    try:
        app_info = client.application_info(app_id)
        global_state = app_info['params']['global-state']

        # Chuyển đổi global state từ base64
        decoded_state = {}
        for item in global_state:
            # Giải mã khóa từ base64
            key_bytes = encoding.base64.b64decode(item['key'])
            try:
                key_str = key_bytes.decode('utf-8')
            except UnicodeDecodeError:
                # Nếu không decode được, chuyển đổi từng byte thành ký tự
                key_str = ''.join([chr(b) for b in key_bytes])

            # Lấy giá trị
            if item['value']['type'] == 1:
                # Bytes
                value = item['value']['bytes']
                # Nếu cần, chuyển đổi bytes thành số nguyên
                try:
                    value_int = int.from_bytes(value, byteorder='big')
                    value = value_int
                except:
                    pass  # Giữ nguyên bytes nếu không thể chuyển đổi
            elif item['value']['type'] == 2:
                # Uint
                value = item['value']['uint']
            else:
                value = None

            decoded_state[key_str] = value

        print("Global State của Smart Contract:")
        for k, v in decoded_state.items():
            print(f"{k}: {v}")

        # Lấy timestamp hiện tại từ block cuối cùng
        status = client.status()
        last_round = status.get('last-round')
        if last_round is None:
            raise Exception("Không thể lấy thông tin block cuối cùng.")

        block_info = client.block_info(last_round)
        # Debug: In ra block_info để kiểm tra cấu trúc
        print("Block Info:", block_info)

        # Truy xuất timestamp từ 'ts' trong 'block'
        if 'block' in block_info and 'ts' in block_info['block']:
            current_time = block_info['block']['ts']
        else:
            raise Exception("Không thể lấy timestamp từ block cuối cùng.")

        # Kiểm tra và in ra các sự kiện đã kết thúc
        event_count = decoded_state.get("event_count", 0)

        for i in range(1, event_count + 1):
            end_time = decoded_state.get(f"event_end_{i}", 0)
            is_stopped = decoded_state.get(f"event_stopped_{i}", 0)
            if current_time >= end_time and is_stopped == 0:
                print(f"Sự kiện {i} đã kết thúc nhưng chưa được dừng.")
            elif current_time < end_time:
                print(f"Sự kiện {i} vẫn đang diễn ra.")
            else:
                print(f"Sự kiện {i} đã được dừng.")

    except Exception as e:
        print(f"Error fetching application info: {e}")

if __name__ == "__main__":
    check_app_state(APP_ID)