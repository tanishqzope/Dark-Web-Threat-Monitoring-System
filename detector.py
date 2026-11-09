import psutil

known_pids = set()


def initialize_processes():
    """
    Remember every process running when monitoring starts.
    """
    global known_pids

    known_pids = {
        p.pid
        for p in psutil.process_iter()
    }


def detect_new_process():
    """
    Detects processes that started
    after monitoring began.
    """

    global known_pids

    for process in psutil.process_iter(
        ["pid", "name"]
    ):

        try:

            pid = process.info["pid"]

            if pid not in known_pids:

                known_pids.add(pid)

                return (
                    pid,
                    process.info["name"].lower()
                )

        except:
            pass

    return None, None