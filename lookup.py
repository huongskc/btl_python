import argparse
import requests
import pandas as pd
import sys
import json

BASE_URL = "http://127.0.0.1:5000"

def main():
    parser = argparse.ArgumentParser(description="Tra cứu thông tin cầu thủ hoặc câu lạc bộ")
    parser.add_argument("--name", type=str, help="Tên cầu thủ")
    parser.add_argument("--club", type=str, help="Tên câu lạc bộ")
    args = parser.parse_args()

    if not args.name and not args.club:
        print("Vui lòng nhập --name hoặc --club")
        sys.exit(1)

    #Xử lý theo tiêu chí
    if args.name:
        url = f"{BASE_URL}/player"
        params = {"name": args.name}
        filename = f"{args.name.replace(' ', '_')}.csv"
    else:
        url = f"{BASE_URL}/club"
        params = {"club": args.club}
        filename = f"{args.club.replace(' ', '_')}.csv"

    #Gửi request đến Flask API
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Lỗi {response.status_code}: {response.text}")
        sys.exit(1)

    data = response.json()

    #Nếu không có dữ liệu
    if not data or isinstance(data, dict) and "message" in data:
        print("Không tìm thấy dữ liệu phù hợp.")
        sys.exit(0)

    #In JSON ra màn hình
    print(json.dumps(data, indent=4, ensure_ascii=False))

    #Xuất ra file CSV
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    print(f"\nDữ liệu đã được lưu vào: {filename}")

if __name__ == "__main__":
    main()
