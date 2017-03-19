<?php

function resetSerie() {
	global $mysqli;
	$sql = "UPDATE apdb.torrent_serie SET preferita = 0";
	$res = mysqli_query($mysqli, $sql) or die(mysqli_error ( $mysqli )."\n".$sql."\n");	
}

function saveSerie($serie, $preferita = false, $eztvTitle = "") {
                global $mysqli;
                $sql = "INSERT INTO apdb.torrent_serie (serie, preferita, eztvTitle)
                SELECT * FROM (
                SELECT '".mysqli_real_escape_string($mysqli, trim($serie))."' as serie,
		".($preferita ? 1 : 0)." as preferita,
		'".mysqli_real_escape_string($mysqli, $eztvTitle)."' as eztvTitle
		) AS tmp
                WHERE NOT EXISTS (
        	SELECT serie FROM apdb.torrent_serie 
        	WHERE serie = '".mysqli_real_escape_string($mysqli, trim($serie))."') LIMIT 1";
                //echo $sql."\n";
                $res = mysqli_query($mysqli, $sql) or die(mysqli_error ( $mysqli )."\n".$sql."\n");

		$sql = "UPDATE apdb.torrent_serie 
		SET preferita = ".($preferita ? 1 : 0).",
		eztvTitle = '".mysqli_real_escape_string($mysqli, $eztvTitle)."'
		WHERE serie = '".mysqli_real_escape_string($mysqli, trim($serie))."'";
		$res = mysqli_query($mysqli, $sql) or die(mysqli_error ( $mysqli )."\n".$sql."\n");
}

function saveTorrentInfo($info) {
        global $mysqli;
        unset($info["codec"]);
        $info["risoluzione"] = print_r($info["risoluzione"], true);
        if ($info["stagione"] == "") {
                $info["stagione"] = "Unica";
        }
        $sql = "INSERT INTO apdb.torrent_rss (data";
        foreach($info as $k => $v) {
                $sql .= ", ".$k;
        }
        $sql .= ") SELECT * FROM (SELECT NOW() as data";
    foreach($info as $k => $v) {
                $sql .= ", '".mysqli_real_escape_string($mysqli, trim($v))."' as ".$k;
    }
        $sql .= ") as tmp WHERE NOT EXISTS (SELECT * FROM apdb.torrent_rss WHERE infoHash = '".mysqli_real_escape_string($mysqli, trim($info["infoHash"]))."')";
        //echo $sql."\n";
        $res = mysqli_query($mysqli, $sql) or die(mysqli_error ( $mysqli )."\n".$sql."\n");
        #echo "Affected: ".mysqli_affected_rows($mysqli)."\n";
        $affected = mysqli_affected_rows($mysqli);
        if ($affected > 0) {
                echo "New torrent to download ".$info["title"]." ".$info["infoHash"]."\n";
        }
        return $affected;
}

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
	/*
	if(strstr($title, "HDTV") !== false) {
		$title = str_replace("HDTV", "|", $title);
		$info["risoluzione"][] = "HDTV";
	}
	*/
	if (count($info["risoluzione"]) == 0) {
		$info["risoluzione"][] = "480p";		
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
