# Deploy

1. cPanel > Git Version Control > Create: clone `https://github.com/ssmebd/gurucadd-site` to `repositories/gurucadd-site`.
2. Preview first (cron every 5 min):
   `cd $HOME/repositories/gurucadd-site && git pull -q origin main && mkdir -p $HOME/public_html/preview && cp -r site/. $HOME/public_html/preview/`
3. Go live later (replace the cp above):
   `rsync -a --exclude=taskflow --exclude=preview --exclude=.htaccess --exclude=cgi-bin site/ $HOME/public_html/`
   Never use `--delete`. Back up public_html before the first live run. `public_html/taskflow/` must not be touched.
