import gitlab
import base64

def gitlab_add_file(GITLAB_TOKEN, GITLAB_PROJECT_ID, filename, folder, content, note):
    gl=gitlab.Gitlab('https://gitlab.com',private_token=GITLAB_TOKEN)
    gl.auth()
    p=gl.projects.get(GITLAB_PROJECT_ID)
    data={
        'branch_name':'master', 
        'branch':'master', 
        'commit_message':note,
        'actions':[{
            'action':'create',
            'file_path':folder+"/"+filename,
            'content':base64.b64encode(content).decode(),
            'encoding': 'base64'
        }]
    }
    try:
        c=p.commits.create(data)
    except gitlab.exceptions.GitlabCreateError:
        return "already exists"
    return c