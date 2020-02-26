from unittest import mock
import requests
import json
import unittest


class TestFunctions(unittest.TestCase):

    def test_getHub_repo(self):
        self.assertEqual(len(getHub_repo("richkempinski")), 5)
        with self.assertRaises(ValueError):
            getHub_repo("test__")

    @mock.patch('requests.get')
    def testGetNumberOfCommits(self, mockedReq):
        mockedReq.return_value = MockResponse('[{”sha”:1}, {”sha”:2}…{”sha”:8}]')
        commits = number_commits(self.user, self.repo)
        self.assertEqual(len(commits), 8)


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
    get_url = f'https://api.github.com/repos/{user_name}/{repo}/commits'
    resp = requests.get(get_url)
    commits = resp.text
    repos = json.loads(commits)
    result = []
    for item in repos:
        result.append(item['sha'])
    return result


def main():
    user_name = input("Please enter the GitHub user ID: ")

    for repo in getHub_repo(user_name):
        num = number_commits(user_name, repo)
        print(f"Repo: {repo} Number of commits: {num}")


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
    main()
