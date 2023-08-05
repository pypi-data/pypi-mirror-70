# meeshkan-hosted-secrets
Utility python package to access [Secret Manager](https://cloud.google.com/secret-manager/docs) secrets on [meeshkan.io](https://meeshkan.io).

```python
from meeshkan_hosted_secrets import access_secret_string

secret_string = access_secret_string("MY_SECRET_NAME")
secret_bytes = access_secret_bytes("ANOTHER_SECRET_NAME")
```
