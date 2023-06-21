from utils.helpers import use_dotenv, check_dir, check_file
from data.files import process_files

use_dotenv()


def check_process_files():
    bad_count = 0
    output = "FAILED:\n"

    def handle_bad(bad_count, output, item):
        bad_count += 1
        # print(f"BAD: {item}")
        output += item + "\n"

    def handle_good(item):
        # print(f"GOOD: {item}")
        pass

    for item in process_files:
        if item["type"] == "dir":
            handle_good(item["name"]) if check_dir(
                item["path"], create=item["create"]
            ) else handle_bad(bad_count, output, item["name"])
        elif item["type"] == "file":
            handle_good(item["name"]) if check_file(
                item["path"], create=item["create"]
            ) else handle_bad(bad_count, output, item["name"])

    print("BAD COUNT: " + str(bad_count))
    if bad_count != 0:
        raise Exception(output)
