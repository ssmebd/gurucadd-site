# Deploy

1. cPanel > Git Version Control > Create: clone `https://github.com/ssmebd/gurucadd-site` to `repositories/gurucadd-site`.
2. Preview first (cron every 5 min):
   `cd $HOME/repositories/gurucadd-site && git pull -q origin main && mkdir -p $HOME/public_html/preview && cp -r site/. $HOME/public_html/preview/`
3. Go live later (replace the cp above):
   `rsync -a --exclude=taskflow --exclude=preview --exclude=.htaccess --exclude=cgi-bin site/ $HOME/public_html/`
   Never use `--delete`. Back up public_html before the first live run. `public_html/taskflow/` must not be touched.

## Instant deploy (webhook, replaces the 5-minute cron)
1. Upload `deploy.php` to `public_html/site-hook/deploy.php` and create `public_html/site-hook/deploy_config.php` (see the header of deploy.php).
2. GitHub > repo Settings > Webhooks > Add: Payload URL `https://www.gurucadd.com/site-hook/deploy.php`, Content type `application/json`, same secret, event "Just the push event".
3. Start with `'live'` = `/home/guru/public_html/preview`; switch to `/home/guru/public_html` to go live.
