# gurucadd-site

Source for www.gurucadd.com. Everything served lives in `site/`.

## Deploy
Push to `main`. Then either the GitHub webhook deploys it, or in cPanel > Git Version Control > Manage > Deploy HEAD Commit (uses `.cpanel.yml`, copies `site/` into `public_html`). A cPanel cron can also pull the repo (see docs/DEPLOY.md).


## White hero backup
The light/white hero (v0.60) is saved in `backup/` (`index-white-hero.html`, `hero-site-white.webp`) and as git tag `hero-white-v0.60`. To bring it back, add `hero-white` to the hero div (`<div class="hero on-navy hero-white">`) or preview with `/?hero=white`-style edit.
