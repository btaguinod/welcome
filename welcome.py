from datetime import date, timedelta, datetime
import pytz
from git.repo import Repo

# TEXT_GRID = """\

# █ █ █ ███ █    ██   ██  █   █ ███ █
# █ █ █ █   █   █  █ █  █ ██ ██ █   █
# █ █ █ ██  █   █    █  █ █ █ █ ██  █
# █ █ █ █   █   █  █ █  █ █   █ █
#  █ █  ███ ███  ██   ██  █   █ ███ █
#                                    """.splitlines()
# TEXT_GRID2 = """\

# ██ ██ ██ ████ ██    ████   ████  ██   ██ ████ ██
# ██ ██ ██ ██   ██   ██  ██ ██  ██ ███ ███ ██   ██
# ██ ██ ██ ███  ██   ██     ██  ██ ██ █ ██ ███  ██
# ██ ██ ██ ██   ██   ██  ██ ██  ██ ██   ██ ██
#  ██████  ████ ████  ████   ████  ██   ██ ████ ██
#                                    """.splitlines()
TEXT_GRID = """\
                                                  
██  ██  ██ ████ ██    ████   ████  ██   ██ ████ ██
██  ██  ██ ██   ██   ██  ██ ██  ██ ███ ███ ██   ██
██  ██  ██ ███  ██   ██     ██  ██ ██ █ ██ ███  ██
██  ██  ██ ██   ██   ██  ██ ██  ██ ██   ██ ██
 ████████  ████ ████  ████   ████  ██   ██ ████ ██
                                                  """.splitlines()


# TEXT_GRID2 = """\

# ████    ████    ████  ████████  ████        ████████      ████████    ████      ████  ████████  ████
# ████    ████    ████  ████      ████      ████    ████  ████    ████  ██████  ██████  ████      ████
# ████    ████    ████  ██████    ████      ████          ████    ████  ████  ██  ████  ██████    ████
# ████    ████    ████  ████      ████      ████    ████  ████    ████  ████      ████  ████
#   ████████████████    ████████  ████████    ████████      ████████    ████      ████  ████████  ████
#                                    """.splitlines()
# TEXT_GRID = """\
                                   
# ████    ████    ████  ████████  ████        ████████      ████████    ████      ████  ████████  ████
# ████    ████    ████  ████      ████      ████    ████  ████    ████  ██████  ██████  ████      ████
# ████    ████    ████  ██████    ████      ████          ████    ████  ████  ██  ████  ██████    ████
# ████    ████    ████  ████      ████      ████    ████  ████    ████  ████      ████  ████         
#   ██████    ██████    ████████  ████████    ████████      ████████    ████      ████  ████████  ████
#                                    """.splitlines()

COMMIT_COUNT = 10
GRAPH_WIDTH = 52

def get_start_date() -> date:
    today = date.today()
    days_from_sunday = (today.weekday() + 1) % 7
    return today - timedelta(days=days_from_sunday, weeks=GRAPH_WIDTH)
    
def is_up_to_date() -> bool:
    return date.today().weekday() != 6

def reset_commits():
    repo = Repo('.')
    first_commit = repo.iter_commits(reverse=True).__next__()
    repo.index.reset(first_commit,False,None,True,soft=True)
    repo.git.add('.')
    repo.git.commit('-m','code','--amend')

def make_commits():
    start_date = get_start_date()
    repo = Repo('.')
    for i in range(GRAPH_WIDTH * 7):
        current_date = start_date + timedelta(days=i)
        if should_make_commits(start_date, current_date):
            for j in range(COMMIT_COUNT):
                current_date_str = current_date.strftime("%b. %d, %Y")
                current_datetime = datetime(
                    year=current_date.year,
                    month=current_date.month,
                    day=current_date.day,
                    tzinfo=pytz.utc
                )
                repo.index.commit("AUTOMATED COMMIT: {} - {}".format(current_date_str, j + 1), author_date=current_datetime, commit_date=current_datetime)


def date_to_grid_location(start_date: date, current_date: date) -> tuple[int, int]:
    day_difference = (current_date - start_date).days
    return day_difference // 7, day_difference % 7


def should_make_commits(start_date: date, current_date: date) -> bool:
    x, y = date_to_grid_location(start_date, current_date)
    return y < len(TEXT_GRID) and x < len(TEXT_GRID[y]) and TEXT_GRID[y][x] == "█"


if __name__ == "__main__":
    print('Checking start date')
    # if is_up_to_date():
    #     print('commits are up to date. Skipping updates')
    #     exit()

    print('resetting commits')
    reset_commits()

    print('making new commits')
    make_commits()