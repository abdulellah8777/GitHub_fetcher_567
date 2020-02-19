import requests
import json
import unittest


class TestFunctions(unittest.TestCase):
    def test_getHub_repo(self):
        self.assertEqual(len(getHub_repo("richkempinski")), 5)
        with self.assertRaises(ValueError):
            getHub_repo("test__")

    def test_getHub_repo(self):
        self.assertEqual(number_commits("richkempinski", "helloworld"), 6)


def getHub_repo(user_name):
    """ to get the names of the repositories in GetHub """
    output = []
    get_url = requests.get(f'https://api.github.com/users/{user_name}/repos')
    repo_list = get_url.json()

    try:
        for line in repo_list:
            repo = line.get('name')
            output.append(repo)
    except (TypeError, KeyError, IndexError, AttributeError):
        raise ValueError('unable to get the repositories from this user ID')

    return output


def number_commits(user_name, repo):
    """ to get the number of commits in a repository """
    get_url = requests.get('https://api.github.com/repos/{}/{}/commits'.format(user_name, repo))
    commits = get_url.json()

    if commits == 0:
        print('the repo has no commits')

    return len(commits)


def main():
    user_name = input("Please enter the GitHub user ID: ")

    for repo in getHub_repo(user_name):
        num = number_commits(user_name, repo)
        print(f"Repo: {repo} Number of commits: {num}")


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
    main()
