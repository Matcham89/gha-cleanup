import subprocess

# input repo information
print('Provide Owner/User ID:')
OWNER = input()
print ("Provide Repo ID:")
REPO = input()


# function to delete manually disabled workflow
def delete_runs(WORKFLOW_ID):
    for workflow_id in WORKFLOW_ID:
        print(f"Deleting runs: {workflow_id}")
        subprocess.run(f"gh api -X GET /repos/{OWNER}/{REPO}/actions/workflows/{workflow_id}/runs | jq '.workflow_runs[] | .id' | xargs -I{{}} gh api -X DELETE /repos/{OWNER}/{REPO}/actions/runs/{{}}", shell=True)

# delete runs
while True:
    # set workflow id variable - only disabled_manually workflows
    WORKFLOW_ID = subprocess.check_output(f"gh api -X GET /repos/{OWNER}/{REPO}/actions/workflows | jq '.workflows[] | select(.state == \"disabled_manually\") | .id'", shell=True).decode().split()
    
    # if workflow_id has a value, run delete_runs function
    if WORKFLOW_ID:
        delete_runs(WORKFLOW_ID)
    else:
        # if workflow_id has no value, echo exit command
        print("There are no disabled manually workflows")
        break
