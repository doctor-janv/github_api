import subprocess
import json

#================================================
# Gets the combined status of a repository
# General repo path github.com/username/repo
# branch: name of the branch
def CurlGetStatus(username : str, repo : str, branch : str):
    cmd = \
    'curl -L ' + \
    '-H "Accept: application/vnd.github+json" ' + \
    '-H "X-GitHub-Api-Version: 2022-11-28" ' + \
    'https://api.github.com/repos/' + \
    username + \
    '/' + \
    repo + \
    '/commits/' + \
    branch + \
    '/status'

    print(cmd)

    process = subprocess.Popen(cmd,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=True, 
                               shell=True)
    process.wait()
    out, err = process.communicate()
    json_start = out.find("{")
    header = out[0:json_start]
    json_message = json.loads(out[json_start:])

    return_data = {}
    if "state" in json_message:
        print("Status retrieved: ", json_message["state"])
        return_data["state"] = json_message["state"]

    if "sha" in json_message:
        return_data["sha"] = json_message["sha"]

    ofile = open("ZCurlGetStatus.txt", "w")
    ofile.write(json.dumps(json_message, indent=2))
    ofile.close()

    return return_data

#================================================
# Sets the status of a specific commit of a repository
# General repo path github.com/username/repo
# PAT        : Personal Access Token
# sha        : The commit sha
# status     : "error", "failure", "pending" or "success"
# context    : The associated name of the status
# description: An optional description
def CurlSetStatus(PAT : str, username : str, repo : str, 
                  sha : str, status : str,
                  context : str, description : str = "No description"):
    cmd = \
    'curl -L   -X POST   ' + \
    '-H "Accept: application/vnd.github+json" ' + \
    '-H "Authorization: Bearer ' + PAT + '" ' + \
    '-H "X-GitHub-Api-Version: 2022-11-28" ' + \
    'https://api.github.com/repos/' + \
    username + \
    '/' + \
    repo + \
    '/statuses/' + \
    sha + ' ' + \
    '-d \'{"state":\"' + status + '\",' + \
    '"description":"' + description + '",' + \
    '"context":"' + context + '"}\''

    print(cmd)

    process = subprocess.Popen(cmd,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=True,
                               shell=True)
    process.wait()
    out, err = process.communicate()