<?php

// Requires ImageMagick ext

function _build_mount_atlas($mount_id) {
    $mount_id = (int) $mount_id;

    $q = "SELECT * FROM mount_sprites WHERE mount_id = {$mount_id}";
    $sprites = $this->db->queryAll($q);

    $w = 0;
    $h = 0;
    foreach ($sprites as $s) {
        if ($s['w'] > $w) $w = $s['w'];
        if ($s['h'] > $h) $h = $s['h'];
    }

    $count = count($sprites);

    $atlas = NewMagickWand();
    MagickSetFormat($atlas, "png32");
    $pwand = NewPixelWand();
    PixelSetColor($pwand, "none");
    MagickNewImage($atlas, $w, $h*$count, $pwand);

    for ($i = 0; $i < $count; $i++) {
        $to_composite = NewMagickWand();
        MagickReadImage($to_composite, '/usr/local/home/vhosts/admin.brokenbulbstudios.com/httpdocs'.$sprites[$i]['path']);
        MagickSetFormat($to_composite, "png32");

        $draw = NewDrawingWand();
        MagickCompositeImage($atlas, $to_composite, MW_OverCompositeOp, 0, $h*$i);
    }

    MagickDrawImage($atlas, $draw);
    MagickWriteImage($atlas, "/usr/local/home/vhosts/lostmoons.brokenbulbstudios.com/httpdocs/swf/images/mounts/{$mount_id}.png");

    `optipng /usr/local/home/vhosts/lostmoons.brokenbulbstudios.com/httpdocs/swf/images/mounts/{$mount_id}.png`;
}
