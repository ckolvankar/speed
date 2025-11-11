import speedtest
import csv
import subprocess
import re
import platform
from datetime import datetime

def measure_ping_latency(host, count=4):
    
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, str(count), host]

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            # Parse ping output for latency
            if platform.system().lower() == 'windows':
                match = re.search(r'Average = (\d+)ms', stdout)
            else: # Linux/macOS
                match = re.search(r'min/avg/max/mdev = [\d.]+/([\d.]+)/[\d.]+/', stdout)

            if match:
                return float(match.group(1))
            else:
                print(f"Could not parse ping output for {host}")
                return None
        else:
            print(f"Ping command failed for {host}: {stderr.strip()}")
            return None
    except FileNotFoundError:
        print("Ping command not found. Please ensure it's installed and in your PATH.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def test_internet_speed():
    try:
        st = speedtest.Speedtest()

        print("Finding best server...")
        st.get_best_server()  # Finds the best server based on ping

        print("Performing download speed test...")
        download_speed_bps = st.download()  # Returns speed in bits per second
        download_speed_mbps = download_speed_bps / 1_000_000  # Convert to Mbps

        print("Performing upload speed test...")
        upload_speed_bps = st.upload()  # Returns speed in bits per second
        upload_speed_mbps = upload_speed_bps / 1_000_000  # Convert to Mbps

        ping = st.results.ping

        print("\n--- Internet Speed Test Results ---")
        print(f"Ping: {ping:.2f} ms")
        print(f"Download Speed: {download_speed_mbps:.2f} Mbps")
        print(f"Upload Speed: {upload_speed_mbps:.2f} Mbps")
        now = datetime.now()
        formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
        print(formatted_date)

        target_host = "8.8.8.8"
        latency1 = measure_ping_latency(target_host)

        
        with open('document1.csv','a') as fd:
            order_csv_append = csv.writer(fd)
            order_csv_append.writerow([formatted_date,latency1, download_speed_mbps,upload_speed_mbps])
    except speedtest.SpeedtestException as e:
        print(f"An error occurred during the speed test: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    while(True):
	    test_internet_speed()
        
