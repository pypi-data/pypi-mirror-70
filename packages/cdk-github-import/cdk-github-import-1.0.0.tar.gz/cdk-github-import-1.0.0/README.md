# `cdk-github-import`

Import local file assets into a new GitHub repository

# Usage

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_github_import import Deployment

# create a new github repository pahud/new-repo and import all files from ./lib to it
Deployment(stack, "NewImport",
    path="./lib",
    owner="pahud",
    repository_name="new-repo",
    access_token=cdk.SecretValue.secrets_manager("my-github-token",
        json_field="token"
    )
)
```

## Private repository

Set `visibility` to `PRIVATE` to create a private GitHub repository.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
visibility: RepositoryVisibility.PRIVATE,
```
