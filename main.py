#Imports
import pycurl
import os
import platform
import ntpath
import subprocess
import requests

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
    for path in path_list:
        print("-------------")
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
    result = []
    page_count = 1
    repo_count = 0
    while(True):
        repo_list = requests.get('https://github.com/'+user+'?page='+str(page_count)+'&tab=repositories')
        count = -1
        for s in repo_list.text.split("codeRepository\">"):
            count += 1
            if count == 0:
                continue
            name = s.split("</a>")[0].replace(" ","").replace("\n","")
            url = "https://github.com/"+user+"/" + name
            if len(result) == 0:
                result.append([name, url])
                continue
            if name not in result[0]:
                result.append([name, url]) # repo["size"], repo["updated_at"]])
            else:
                return result
        page_count += 1

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
                print(repo["name"])
                repo_count += 1
                result.append([repo["name"], repo["url"], repo["size"], repo["updated_at"]])
        except:
            print("Failed to recive data from github!")
            return result
        #print(r.text)
        page_count += 1

# if ok
def user_request(question):
    inp = input(question + " [y/n]: ")
    while(lower(inp) not in ['y','n']):
        inp = input(question + " [y/n]: ")
    return inp == "y"

# Download all repos
def download_all_repos(url_list, exception_list = []):
    for url in url_list:
        if url not in exception_list:
            download_repo(url_list)

# Download a repo
def download_repo(url, path):
    process = subprocess.Popen("git clone " + url_list, shell=True , cwd = path)
    output = process.communicate()[0]


# Save repos to different location
def move_repos_to_backup_dir(github_path, backup_path):
    pass

# Show all repos
def show_status():
    pass

# Show recommendations to remove
def show_recommendations():
    pass

# Starts here
def main():
    # Update repos
    dirs_list = scan_dir("..") # get all repos as path
    #pull_all_repos(dirs_list) # pull all repos

    # show dates
    for folder in dirs_list:
        pass
    '''
        print(ntpath.basename(folder))
        print(creation_date(folder))
        print(get_folder_size(folder) + " bytes")
    '''

    current_repos_list = get_current_repos("..") # get all repos as names
    #current_repos_list += get_current_repos("path_to_backup")

    #show folders
    '''
    for repo in current_repos_list:
        print(repo) # show list with current repos
    '''

    repos_on_github_list = get_all_repos_on_github_html_requests("grebtsew")

    repos_that_need_to_be_downloaded = []

    for repo in repos_on_github_list:
        #compare current with github

        if repo[0] not in current_repos_list:
            repos_that_need_to_be_downloaded.append(repo)
            print(repo)


    #show

if __name__ == "__main__":
    # execute only if run as a script
    main()
