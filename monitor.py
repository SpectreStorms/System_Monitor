import psutil, smtplib, logging, time
from datetime import datetime
import config


logging.basicConfig(
    filename='system_monitor.log',
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def main():
    while True:
        stats = collect_stats()
        logging.info(stats)
        send_email(stats)
        time.sleep(config.WAIT)


def collect_stats() -> str:
    """Collects the system information to be sent in an email
    
    Returns:
        str: Formatted string with system statistics
    """
    # CPU
    system_information = ""    # Stores the contents of the email
    system_information += "\nCPU\n----------\n"
    system_information += f'CPU Usage: {psutil.cpu_percent(interval=0.1)}%\n'
    for index, logical_processor in enumerate(psutil.cpu_percent(percpu=True, interval=0.1)):
        system_information += f'Logical Processor {index+1}: {logical_processor}%\n'    # Logical processors are often threads
    
    # Memory
    system_information += "\nMemory\n----------\n"
    system_information += f'Memory Usage: {psutil.virtual_memory().percent}%\n'

    # Storage
    system_information += "\nStorage\n----------\n"
    for disk in psutil.disk_partitions():
        usage = psutil.disk_usage(disk.device)
        system_information += f'"{disk.device}: {convert_bit_to_gb(usage.used)} GB / {convert_bit_to_gb(usage.total)} GB\n'
        system_information += f'"{disk.device}": {100 - usage.percent}% free\n'
    
    return system_information

def send_email(email_contents: str):
    """Sends the email to the designated recipients
    
    Args:
        email_contents (str): Statistics sent to the monitoring emails
    """
    print(email_contents)
    message = f"""Subject: {config.SUBJECT}\r\n\r\n{email_contents}\r\n""".encode('utf-8')
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(config.SENDER, config.KEY)
    server.sendmail(config.SENDER, config.RECIPIENTS, message)
    server.quit()

def convert_bit_to_gb(bits: int) -> float:
    """Converts bits to gigabytes

    Arg:
        bits (int): Number of raw bits

    Returns:
        float: Number of gigabytes rounded to the second significant digit
    """

    return round((bits / 1073741824), 2)

if __name__ == "__main__":
    main()
