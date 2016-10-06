<?php
function get_gd_image($source_image_path)
{	
		list( $source_image_width, $source_image_height, $source_image_type ) = getimagesize( $source_image_path );
		switch ( $source_image_type )
		{
		  case IMAGETYPE_GIF:
			$source_gd_image = imagecreatefromgif( $source_image_path );
			break;

		  case IMAGETYPE_JPEG:
			$source_gd_image = imagecreatefromjpeg( $source_image_path );
			break;

		  case IMAGETYPE_PNG:
			$source_gd_image = imagecreatefrompng( $source_image_path );
			imagesavealpha($source_gd_image, true);
			break;
		}
		return $source_gd_image;
}

function generate_miscrit_backgrounds( $source_image_path, $settings )
{
	list( $source_image_width, $source_image_height, $source_image_type ) = getimagesize( $source_image_path );

	$source_gd_image = get_gd_image($source_image_path);

	if ( $source_gd_image === false )
	{
	  return false;
	}

	$source_aspect_ratio = $source_image_width / $source_image_height;

	$resize_needed = false;

	$thumbnail_image_width = $source_image_width;
	$thumbnail_image_height = $source_image_height;

	if ( $source_image_width > $settings['thumbnail_image_max_width'] ) {
		$thumbnail_image_width = $settings['thumbnail_image_max_width'];
		$thumbnail_image_height = (int)floor($thumbnail_image_width / $source_aspect_ratio);

		$resize_needed = true;
	}

	if ( $thumbnail_image_height  > $settings['thumbnail_image_max_height'] ) {
		$thumbnail_image_height = $settings['thumbnail_image_max_height'];
		$thumbnail_image_width = (int)floor($thumbnail_image_height * $source_aspect_ratio);

		$resize_needed = true;
	}

	if ( !$resize_needed ) {
		return $source_gd_image;
	}

	$thumbnail_gd_image = imagecreatetruecolor( $thumbnail_image_width, $thumbnail_image_height );
	imagesavealpha($thumbnail_gd_image, true);
	imagealphablending( $thumbnail_gd_image, false );

	imagecopyresampled( $thumbnail_gd_image, $source_gd_image, 0, 0, 0, 0, $thumbnail_image_width, $thumbnail_image_height, $source_image_width, $source_image_height );

	return $thumbnail_gd_image;
}

function make_image() {
    $source_image = '/ulhv/volcanoisland.brokenbulbstudios.com/httpdocs'.$image['path'];
    $dest_image = '/ulhv/volcanoisland.brokenbulbstudios.com/httpdocs/game/assets/miscrits/'.$settings['dest_dir'].'/'.$image['name'].'_'.$game.'.png';

    $background_image = $settings[$game];

    if (file_exists($dest_image))
        @unlink($dest_image);

    $img_source  = generate_miscrit_backgrounds($source_image, $settings);

    $img_bg = get_gd_image($background_image);

    $dest_x = floor((imagesx($img_bg) / 2) - (imagesx($img_source) / 2));
    $dest_y = $settings['dest_y'] - (imagesy($img_source) / 2);

    imagecopy($img_bg, $img_source, $dest_x, $dest_y, 0, 0, imagesx($img_source), imagesy($img_source));

    imagesavealpha($img_bg, true);
    imagealphablending( $img_bg, false );
    $res = imagepng ( $img_bg, $dest_image );

    $url = 'http://sunfallshores.brokenbulbstudios.com'.substr($dest_image, 50);
    echo "<a href='$url'>$url</a><br />";
}

