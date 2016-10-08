<?php echo 'hello world'; ?>
<?php phpinfo(); ?>
<?php
$redis = new Redis();
$conn = $redis->connect($_ENV['REDIS_HOST'], 6379);
if (!$conn) {
    echo "Couldn't connect to redis";
}
