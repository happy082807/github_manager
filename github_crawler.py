from github import Github
import pandas as pd
import time

def main():
    account = input('Account: ')
    password = input('Password: ')
    g = Github(account, password)
    status = g.get_api_status().status

    if status == 'good':
        todo = input('(1)Export file (2)Delete member (3)End    ')
        while todo is not '3':
            if todo is '1':
                repos = org_repos(g)
                ex_file(repos)
            elif todo is '2':
                dodel = input('Delete member (account/n):')
                while dodel is not 'N' and dodel is not 'n':
                    delete_member(g,repos,dodel)
                    dodel = input('Delete another member (account/n):')
            todo = input('(1)Export file (2)Delete member (3)End    ')
    else:
        print(status)

def org_repos(g):

    repos = []

    for repo in g.get_user().get_repos():
        for user in repo.get_contributors():
            ispublic = 'public'
            if(repo.private):
                ispublic = 'private'
            repos.append([repo.full_name, ispublic, user.login])

    repos = pd.DataFrame(repos, columns=['Repo', 'Auth', 'User'])

    return repos

def ex_file(r):
    r = r.sort_values(by=['Repo', 'User'], ascending=True)
    fn = time.strftime('%Y%m%d')
    r.to_csv(fn + '.csv', index = False)
    print('File name:' + fn + '.csv')

def delete_member(g,r,m):

    print('Account:'+ m)
    m_r = r.Repo[r.User == m].tolist()
    print(m_r)
    del_r = input('Delete all?(Y/N)')
    if del_r is 'Y' or del_r is 'y':
        for repo in m_r:
            if g.get_user().get_repo(repo).has_in_collaborators(m):
                g.get_user().get_repo(repo).remove_from_collaborators(m)
        print('Finish')


if __name__ == "__main__":
    main()
