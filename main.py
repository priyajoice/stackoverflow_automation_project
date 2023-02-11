from subprocess import Popen, PIPE
import sys
import requests
import webbrowser


# Read a python file and if check for error
def extract_error(cmd):
    proc = Popen([sys.executable, cmd], stdout=PIPE, stderr=PIPE, text=True)
    out, err = proc.communicate()

    if err:
        error = err.splitlines()[-1]
        print(error)
        send_req(error)
    else:
        print("No errors found!")


# make HTTP request using StackOverflow API and return the JSON file
def send_req(error):
    def make_req(err):
        resp = requests.get("https://api.stackexchange.com/" +
                            "/2.2/search?order=desc&tagged=python&sort=activity&intitle={}&site=stackoverflow".format(
                                err))
        return resp.json()

    filter_err = error.split(":")
    get_urls(make_req(filter_err[0]))
    get_urls(make_req(filter_err[1]))
    get_urls(make_req(error))


# stores the URLs of those solutions which are
# marked as "answered" by StackOverflow. And then finally
# open up the tabs containing answers from StackOverflow on the browser.
def get_urls(rjson):
    url_list = []
    count = 0

    for i in rjson['items']:
        if i['is_answered']:
            url_list.append(i["link"])
        count += 1

        if count == 3 or count == len(rjson['items']):
            break

    for i in url_list:
        webbrowser.open(i)


if __name__ == "__main__":
    extract_error("test.py")
