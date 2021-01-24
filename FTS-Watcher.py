import socket
import time
import logging
import sys
import getopt


def is_open(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        return True
    except:
        return False


def check(srv_name, ip, port):
    if is_open(ip, port):
        up = True
        return up
    else:
        up = False
        logging.warning(srv_name + " is down")
        return up


if __name__ == '__main__':
    help_txt = "This Python script is to be used to monitor the ports opened by FTS \n" \
               "The results are logged in FTS-Watcher.log wherever you run the script \n\n" \
               "Arguments:\n" \
               "-u --ui : the ip for the ui\n" \
               "-d --dp : the ip for data packages\n" \
               "-a --api : the ip for the api\n" \
               "-c --cot : the ip for CoT\n\n"
    ip = "127.0.0.1"
    ui_ip = ip
    dp_ip = ip
    api_ip = ip
    cot_ip = ip
    cmd_args = sys.argv
    arg_list = cmd_args[1:]
    stort_opts = "hu:d:a:c:"
    long_opts = ["help", "ui", "dp", "api", "cot"]
    args, values = getopt.getopt(arg_list, stort_opts, long_opts)
    for current_arg, current_val in args:
        if current_arg in ("-h", "--help"):
            print(help_txt)
            exit(1)
        if current_arg in ("-u", "--ui"):
            ui_ip = current_val
        if current_arg in ("-d", "--dp"):
            dp_ip = current_val
        if current_arg in ("-a", "--api"):
            api_ip = current_val
        if current_arg in ("-c", "--cot"):
            cot_ip = current_val
    logging.basicConfig(filename='FTS-Watcher.log', filemode='w', format='%(asctime)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S')
    logging.warning('Starting FTS-Watcher')
    logging.warning('Base IP is set to : ' + ip)
    logging.warning('UI IP set to : ' + ui_ip)
    logging.warning('Data Package IP set to : ' + dp_ip)
    logging.warning('CoT IP set to : ' + cot_ip)
    logging.warning('Giving FTS 20 secs to start....')
    time.sleep(20)
    while True:
        check1 = check("HTTP Data Package", dp_ip, "8080")
        check2 = check("TCP CoT", cot_ip, "8087")
        check3 = check("SSL CoT", cot_ip, "8089")
        check4 = check("SSL Data Package", dp_ip, "8443")
        check5 = check("UI", ui_ip, "5000")
        check6 = check("API", api_ip, "19023")
        checks = [check1, check2, check3, check4, check5, check6]
        fail_count = 0
        for c in checks:
            if c is False:
                fail_count += 1
        if fail_count == 0:
            logging.warning('All Running')
        time.sleep(5)
