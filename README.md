# releases.wagtail.org

Infrastructure to support nightly releases and upgrade checks.

## Upgrade checker

Wagtail’s [latest.txt](https://github.com/wagtail/wagtail/blob/main/scripts/latest.txt) file contains metadata bout Wagtail releases, and is published the [latest.sh script](https://github.com/wagtail/wagtail/blob/main/scripts/latest.sh).

## Nightly releases

Wagtail’s CircleCI continuous integration [triggers publication of nightly releases](https://github.com/wagtail/wagtail/blob/main/.circleci/trigger-nightly-build.sh). Those releases are shared on the [nightly releases index](https://releases.wagtail.org/nightly/index.html).

## Infrastructure

`releases.wagtail.org` (and the legacy `releases.wagtail.io`) is hosted in an S3 bucket (named `releases.wagtail.io`). ACLs are used to mark files as public.

For additional security and performance, CloudFront is used to globally cache requests. CloudFront handles TLS termination, HTTPS redirects, compression and caching.

## Deploying changes

To deploy changes in this repository, run the `deploy.py` script using `uv`:

```
uv run deploy.py
```

You must have access to the relevant S3 bucket (`releases.wagtail.io`).

`deploy.py` will upload the files, and then clear the cache. The cache is cleared in the background, so may take a couple minutes for the changes to propagate.
