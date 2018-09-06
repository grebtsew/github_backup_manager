#Imports
import pycurl
import platform
import os
import ntpath
import subprocess

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

# Get size of repon on github
def get_repo_github_size():
    # Using pycurl
    buffer = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'http://pycurl.io/')
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    body = buffer.getvalue()
    # Body is a string in some encoding.
    # In Python 2, we can print it without knowing what the encoding is.
    print(body)
    pass

# if ok
def user_request():
    pass


# Download a repo
def download_repo(url):
    pass
# Download all repos
def download_all_repos(url_list, exception_list = []):
    for url in url_list:
        if url not in exception_list:
            download_repo(url_list)

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

    #show folders
    '''
    for repo in current_repos_list:
        print(repo) # show list with current repos
    '''

if __name__ == "__main__":
    # execute only if run as a script
    main()
