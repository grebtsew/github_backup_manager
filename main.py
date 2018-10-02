#Imports
import os
import platform
import ntpath
import subprocess
from bs4 import BeautifulSoup
import requests
from datetime import datetime

'''
Modify these variables!
'''

destination_path = "C:\\Users\\Daniel\\Documents\\GitHub"
user_name = "grebtsew"

'''
This program helps with backing up all github repos on local drive.
I use this to keep up-to-date copies on my external drive.
'''

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

# Get all repon currently installed
def scan_dir(path):
    return [(os.path.abspath(path) + "\\" + f) for f in os.listdir(path)]

def get_current_repos(path):
    return os.listdir(path)

# Pull all repos
def pull_all_repos(path_list):
    print("Will now pull all repos in github folder:")
    count = 1
    for path in path_list:
        print("------" + str(count) + "/"+ str(len(path_list)) + " ------")
        count += 1
        print(ntpath.basename(path))
        try:
            process = subprocess.Popen("git pull", shell=True , cwd = path)
            output = process.communicate()[0]
        except:
            print("Failed to git pull " + path)
        print("-------------")

# Get date of file change
def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime

# Get size of folder
def get_folder_size(path):
    total = 0

    for entry in os.scandir(path):
        if entry.is_file():
            total += entry.stat().st_size
        elif entry.is_dir():
            total += get_folder_size(entry.path)
    return total

def get_all_repos_on_github_html_requests(user):
    # using html code and string manupulation
    # fixed page number with next button

    result = []
    repo_count = 0
    page_count = 0
    next_link = 'https://github.com/'+user+'?page='+str(page_count)+'&tab=repositories'

    while(True):
        repo_list = requests.get(next_link)
        r = repo_list.text.split("codeRepository\"");

        for s in range( 1, len(r)):
            name = r[s].split("</a>")[0].replace(" ","").replace("\n","").replace(">","")
            url = "https://github.com/"+user+"/" + name
            if len(result) == 0:
                result.append([name, url])
                continue
            if [name, url] not in result:
                result.append([name, url]) # repo["size"], repo["updated_at"]])
            else:
                return result

        # get next link
        soup = BeautifulSoup(repo_list.text, "lxml") # lxml is just the parser for reading the html
        links = soup.find_all('a')
        for link in links:
            if(link.getText() == 'Next'):
                next_link = link.get('href')

def get_all_repos_on_github_api_requests(user):
    # using github api
    # This need more requests to be useful!
    result = []
    page_count = 1
    repo_count = 0
    while(True):
        repo_list = requests.get('https://api.github.com/users/'+user+'/repos?page='+str(page_count))
        if len(repo_list.json()) == 0:
            return result
        try:
            for repo in repo_list.json():
                #print(repo["name"])
                repo_count += 1
                result.append([repo["name"], repo["url"], repo["updated_at"],repo["size"]])
        except:
            print("Failed to recive data from github!")
            return result
        #print(r.text)
        page_count += 1

# if ok
def user_request(question):
    inp = input(question + " [y|n]: ")
    while(inp.lower() not in ['y','n', '']):
        inp = input(question + " [y|n]: ")
    return inp == "y"

# Download all repos
def download_all_repos(repo_list, path):
    count = 1
    print("Will now clone all repos that does not exist on destination folder, this might take a while :")
    for repo in repo_list:
        count += 1
        print("------" + str(count) + "/"+ str(len(repo_list)) + " ------")
        download_repo(url[1], path)

# Download a repo
def download_repo(url, path):
        try:
            print(url)
            process = subprocess.Popen("git clone " + url, shell=True , cwd = path)
            output = process.communicate()[0]
        except:
            print("Failed to clone repo from url : " + url)
        print()

def create_information_array_local(dirs_list):
    result = []

    for folder in dirs_list:
        path = folder
        name = ntpath.basename(folder)
        date = creation_date(folder)
        size = get_folder_size(folder)
        result.append([name, path, date, size])

    return result

def create_information_array_github_api(repos_github):
    temp = get_all_repos_on_github_api_requests(user_name)
    res = []
    for e in temp:
        for a in repos_github:
            if(e[0] in a):
                res.append(e);
    return res

def show_information_array(array):
    print()
    print("----- SHOW REPOs -----")
    count = 1
    size = 0
    for elem in array:
        size += elem[3]
        print("----- "+ str(count) + "/"+str(len(array)) +" -----")
        print("NAME: " + elem[0])
        print("PATH: " + elem[1])
        print("DATE: " + str(datetime.fromtimestamp(elem[2]).strftime('%Y-%m-%d %H:%M:%S')))
        print("SIZE: " + str(elem[3]) + " bytes  == " + str(elem[3]/1000000000) + " gb")
        print()
        count += 1
    print("Total size : " + str(size/1000000000) + " gb")

    return size

def show_information_array_github(array):
    print()
    print("----- SHOW REPOs -----")
    count = 1
    size = 0
    for elem in array:
        size += elem[3]
        print("----- "+ str(count) + "/"+str(len(array)) +" -----")
        print("NAME: " + elem[0])
        print("PATH: " + elem[1])
        print("DATE: " + elem[2])
        print("SIZE: " + str(elem[3]) + " kb == " +str(elem[3]/1000000) + " gb" )
        print()
        count += 1
    print("Total size : " + str(size/1000000) + " gb")

    return size

def get_download_size(pretty_array):
    size = 0
    for elem in pretty_array:
        size += elem[3]

    return size

# Starts here
def main():
    print("GITHUB backup manager")
    print("This program will backup your repos for you.")
    print()
    print("Make sure to modify your destination path and user name in this file.")
    print("Current destination path = " + destination_path)
    print("Current user name = " + user_name)
    print()
    print("Scan destination directory...")
    # Update repos
    dirs_list = scan_dir(destination_path) # get all repos as path
    print("Found "+str(len(dirs_list)) + " projects on destination_path.")

    print()

    print("Update repos here if you want.")
    if(user_request("Do you want to pull all existing repos?")):
        pull_all_repos(dirs_list) # pull all repos, update them

    current_repos_list = get_current_repos(destination_path)

    print("")
    print("Get all repo names from github.com for user " + user_name + " ...")

    repos_on_github_list = get_all_repos_on_github_html_requests(user_name)

    repos_that_need_to_be_downloaded = []

    print("Succesfully scanned projects!")
    for repo in repos_on_github_list:

        #compare current with github
        if repo[0] not in current_repos_list:
            repos_that_need_to_be_downloaded.append(repo)

    # Status and request
    print()
    print("----- STATUS -----")
    print("Number of repos on github: " + str(len(repos_on_github_list)))
    print("Number of repos in backupfolder: " + str(len(dirs_list)))
    print("Number of repos to download: " + str(len(repos_that_need_to_be_downloaded)))

    download_size = 0
    local_pretty_array = []
    github_pretty_array = []

    # Controller
    if(user_request("Do you want to see information about each existing repo?")):
        local_pretty_array = create_information_array_local(dirs_list)
        show_information_array(local_pretty_array)

    if user_request("Do you want to see information about each repo about to be downloaded?"):
        github_pretty_array = create_information_array_github_api(repos_that_need_to_be_downloaded)
        if(len(github_pretty_array) > 0):
            show_information_array_github(github_pretty_array)
        else:
            print("Daily github api requests exceeded!")

    if(len(github_pretty_array) > 0):
        download_size = get_download_size(github_pretty_array)
    else:

        github_pretty_array = create_information_array_github_api(repos_that_need_to_be_downloaded)
        download_size = get_download_size(github_pretty_array)

    if(download_size == 0):
        if user_request("Daily github api requests exceeded, this means we cant calculate approximated download size, so download at own risk of filling your computer. Do you want to proceed?"):
            download_all_repos(repos_that_need_to_be_downloaded, destination_path)
    else:
        if user_request("Download all repos of the approximated total size " + str(download_size/1000000) + " gb? (size can be inaccurate!)"):
            download_all_repos(repos_that_need_to_be_downloaded, destination_path)
        else:
            if user_request("Step through each repo?"):
                count = 1
                for repo in repos_that_need_to_be_downloaded:

                    if user_request("Download repo named "+ repo[0] +" ? " + str(count) + "/" + str(len(repos_that_need_to_be_downloaded))):
                        download_repo(repo[1],destination_path)
                    count += 1

    print("All done exiting program. Have a great day!")

if __name__ == "__main__":
    # execute only if run as a script
    main()
