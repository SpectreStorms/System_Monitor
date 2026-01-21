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
    logging.info(initial_stats)
    while True:
        stats = collect_stats()
        logging.info(stats)
        send_email(stats)
        time.sleep(config.WAIT)

def initial_stats() -> str:
    """Collects the information used to initialize the log
    
    Returns:
        str: Formatted string with system statistics
    """
    # CPU
    system_information = "\n"    # Stores information logged in system_monitor.log
    system_information += "CPU\n----------\n"
    system_information += f'CPU Cores: {psutil.cpu_count(logical=False)}\n'
    system_information += f'CPU Logical Processors: {psutil.cpu_count()}\n'

    # Memory
    system_information += "\nMemory\n----------\n"
    system_information += f"RAM: {convert_bit_to_gb(psutil.virtual_memory().total)} GB\n"

    # Storage
    system_information += "\nStorage\n----------\n"
    for disk in psutil.disk_partitions():
        system_information += f'"{disk.device}: {convert_bit_to_gb(psutil.disk_usage(disk.device).total)} GB\n'
    system_information += "\n"

    return system_information

def collect_stats() -> str:
    """Collects the system information to be sent in an email
    
    Returns:
        str: Formatted string with system statistics
    """
    # CPU
    system_information = "\n"    # Stores the contents of the email
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
