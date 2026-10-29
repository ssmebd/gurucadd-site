# gurucadd-site

Source for www.gurucadd.com. Everything served lives in `site/`.

## Deploy
Push to `main`. Then either the GitHub webhook deploys it, or in cPanel > Git Version Control > Manage > Deploy HEAD Commit (uses `.cpanel.yml`, copies `site/` into `public_html`). A cPanel cron can also pull the repo (see docs/DEPLOY.md).

