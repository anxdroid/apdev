<?php

function parseTorrentInfo($raw) {
	//echo "Parsing torrent info from ".print_r($raw, true)."...\n";
	$pattern = "/S(\d{2})E(\d{2})/";
	$matches = array();
	$info = array();
	$info["infoHash"] = $raw["infoHash"];
	$info["magnetURI"] = $raw["magnetURI"];
	$info["contentLength"] = $raw["contentLength"];
	$info["link"] = $raw["link"];
	$info["title"] = $raw["title"];
	$info["stagione"] = "";
	$info["risoluzione"] = array();
	$title = $raw["title"];
	if (preg_match($pattern, $title, $matches)) {
		//echo $matches[1]." ".$matches[2]."\n";
		$info["stagione"] = 1 * $matches[1];
		$info["episodio"] = 1 * $matches[2];
		$title = str_replace($matches[0], "|", $title);
		//echo $title."\n";
	}
	if (!isset($info["stagione"])) {
		$pattern = "/(\d{4} \d{2} \d{2})/";
		if (preg_match($pattern, $title, $matches)) {
			//echo $matches[1]."\n";
			$info["episodio"] = $matches[1];
			$title = str_replace($matches[1], "|", $title);
		}	
	}
	if (!isset($info["stagione"])) {
		$pattern = "/Series (\d{1,2}) (\d{1,2} ?of ?\d{1,2})/";
		if (preg_match($pattern, $title, $matches)) {
			echo $matches[0]."\n";
			$info["stagione"] = 1 * $matches[1];
			$info["episodio"] = $matches[2];
			$title = str_replace($matches[0], "|", $title);
		}
	}
	$pattern = "/([72018]{3,4}p)/";
	if (preg_match($pattern, $title, $matches)) {
		//echo $matches[1]."\n";
		$info["risoluzione"][] = $matches[1];
		$title = str_replace($matches[0], "|", $title);
	}
	if(strstr($title, "HDTV") !== false) {
		$title = str_replace("HDTV", "|", $title);
		$info["risoluzione"][] = "HDTV";
	}
	$pattern = "/(x[2645]{3})/";
    if (preg_match($pattern, $title, $matches)) {
		//echo $matches[1]."\n";
		$info["codec"]["video"] = $matches[1];
		$title = str_replace($matches[1], "|", $title);
    }
	$pattern = "/(mp4)/";
    if (preg_match($pattern, $title, $matches)) {
		//echo $matches[1]."\n";
		$info["codec"]["video"] = $matches[1];
		$title = str_replace($matches[1], "|", $title);
    }
    $pattern = "/(AAC)/";
    if (preg_match($pattern, $title, $matches)) {
		//echo $matches[1]."\n";
		$info["codec"]["audio"] = $matches[1];
		$title = str_replace($matches[1], "|", $title);
    }	
	$pattern = "/( ?\| ?)/";
	if (preg_match_all($pattern, $title, $matches)) {
        foreach($matches[1] as $match) {
			$title = str_replace($match, "|", $title);
		}
	}
	$pattern = "/\|{2,}/";
	if (preg_match($pattern, $title, $matches)) {
		$title = str_replace($matches[0], "|", $title);
	}
	$tokens = explode("|", $title);
	$info["serie"] = $tokens[0];
	//echo "Parsed torrent info :".print_r($info, true)."\n";
	//echo $title."\n";
	return $info;	
}
?>