<?php
// Instant deploy hook for www.gurucadd.com. GitHub calls this after each push (Settings > Webhooks).
// NOT served from the website itself: upload this file once to public_html/site-hook/deploy.php,
// next to a deploy_config.php (NOT in git):
//   <?php return ['secret'=>'long-random-text','repo'=>'/home/guru/repositories/gurucadd-site','live'=>'/home/guru/public_html/preview'];
// Change 'live' to '/home/guru/public_html' when the site goes live. Files are only added or overwritten, never deleted.
header('Content-Type: text/plain');
$cfgf=__DIR__.'/deploy_config.php';
if(!is_file($cfgf)){http_response_code(500);exit("deploy_config.php missing\n");}
$cfg=require $cfgf;
if(empty($cfg['git'])&&is_file('/usr/local/cpanel/3rdparty/bin/git'))$cfg['git']='/usr/local/cpanel/3rdparty/bin/git';
$body=file_get_contents('php://input');
$sig=$_SERVER['HTTP_X_HUB_SIGNATURE_256']??'';
if(!$sig||!hash_equals('sha256='.hash_hmac('sha256',$body,$cfg['secret']),$sig)){http_response_code(403);exit("bad signature\n");}
if(($_SERVER['HTTP_X_GITHUB_EVENT']??'')==='ping')exit("pong\n");
if(!function_exists('shell_exec')||in_array('shell_exec',array_map('trim',explode(',',ini_get('disable_functions'))))){http_response_code(500);exit("shell_exec disabled on this host\n");}
$repo=escapeshellarg($cfg['repo']);$git=escapeshellarg($cfg['git']??'git');
$home=preg_match('#^(/home\d*/[^/]+)/#',$cfg['repo'],$m)?$m[1]:(getenv('HOME')?:'');
$out=shell_exec(($home?'export HOME='.escapeshellarg($home).'; ':'')."cd $repo && $git fetch origin 2>&1 && $git reset --hard origin/main 2>&1");
$src=rtrim($cfg['repo'],'/').'/site';$dst=rtrim($cfg['live'],'/');
$skip=['taskflow','preview','site-hook','cgi-bin','.htaccess','.git'];
$ok=true;$n=0;
function cp_tree($a,$b,$skip,&$ok,&$out,&$n,$top=true){
  if(!is_dir($b)&&!@mkdir($b,0755,true)){$ok=false;$out.="mkdir failed: $b\n";return;}
  foreach(scandir($a) as $f){
    if($f==='.'||$f==='..'||($top&&in_array($f,$skip,true)))continue;
    if(is_dir("$a/$f"))cp_tree("$a/$f","$b/$f",$skip,$ok,$out,$n,false);
    elseif(!@copy("$a/$f","$b/$f")){$ok=false;$out.="copy failed: $f\n";}else $n++;
  }
}
if(!is_dir($src)){http_response_code(500);exit("site/ folder missing in repo\n");}
cp_tree($src,$dst,$skip,$ok,$out,$n);
if(function_exists('opcache_reset'))@opcache_reset();
echo ($ok?"deployed $n files\n":"PARTIAL\n").$out;
