import sys, time, os

# TODO add traceback to error messages

# Params:
module_version="v1.1" # module version
ce_input_folder="./input/" # set the input folder
ce_output_folder="./output/" # set the output folder
ce_tmp_folder="./tmp/"
ce_log_file="./logs/logfile_{}.log".format(time.strftime("%Y%m%d%H%M%S")) # set the log file name

# functions to be used:

def ce_display_progress(count, total, status=''):   # uses the sys library
    try:
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))
        percents = round(100.0 * count / float(total), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)
        sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
        sys.stdout.flush()
    except Exception as e:
        ce_logging ("ce_display_progress","Issue occured: "+str(e),"ERROR")


def ce_logging (ext_processName, ext_messageToLog, ext_messageLevel):
    try:
        import logging
        log = logging.getLogger()
        log.setLevel(logging.DEBUG) # set default level of logging; should be on debug (lowest level) to be activated

        if not len(log.handlers): # prevent new handlers which causes duplicates
            onScreenLog = logging.StreamHandler() # set handler to print logging messages to screen
            onScreenLog.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            onScreenLog.setLevel(logging.DEBUG) # set default level to print onto sceen
            log.addHandler(onScreenLog)

            toFileLog = logging.FileHandler(ce_log_file) # set handler to print logging messages to file
            toFileLog.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            toFileLog.setLevel(logging.INFO) # set default level to print into the file
            log.addHandler(toFileLog)

        level=logging.getLevelName(ext_messageLevel.upper())
        log.log(level,ext_processName + " :: " + ext_messageToLog)
    except Exception as e:
        ce_logging ("ce_logging","Issue occured: "+str(e),"ERROR")

# Default run:
if __name__ == "__main__":
    print ("Core Engine version number {}. Needs to be imported as a module.".format(module_version))