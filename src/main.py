import subprocess
import threading


def run_script(script_name):
    subprocess.run(["python", "-m", script_name])


if __name__ == "__main__":
    thread1 = threading.Thread(
        target=run_script, args=(("src.database.main"),)
    )
    thread2 = threading.Thread(target=run_script, args=(("src.bot_main"),))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
