<?php

$mysqli = mysqli_connect("localhost", "apdb", "pwd4apdb", "apdb");

/***************************************************************************/

$rss = simplexml_load_file('https://eztv.ag/ezrss.xml', 'SimpleXMLElement', LIBXML_NOCDATA);
if ($rss === false) {
	die("Exiting...\n");
}
$ns = $rss->getNamespaces(true);

function parseItem($item) {
	global $ns;
	$pattern = "/S(\d{2})E(\d{2})/";
	$matches = array();
	$info = array();
	$info["infoHash"] = (string) $item->children($ns['torrent'])->infoHash;
	$info["magnetURI"] = (string) $item->children($ns['torrent'])->magnetURI;
	$info["contentLength"] = (string) $item->children($ns['torrent'])->contentLength;
	$info["link"] = (string) $item->link;
	$info["title"] = (string) $item->title;
	$info["stagione"] = "";
	$info["risoluzione"] = array();
	$title = $item->title;
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
	//echo $title."\n";
	return $info;	
}

function saveInfo($info) {
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
	if (mysqli_affected_rows($mysqli) > 0) {
		echo "New torrent to download ".$info["title"]." ".$info["infoHash"]."\n";
	}
}

function saveSerie($serie) {
		global $mysqli;
		$sql = "INSERT INTO apdb.torrent_serie (serie)
		SELECT * FROM (
		SELECT '".mysqli_real_escape_string($mysqli, trim($serie))."') AS tmp
		WHERE NOT EXISTS (
    	SELECT serie FROM apdb.torrent_serie 
    	WHERE serie = '".mysqli_real_escape_string($mysqli, trim($serie))."') LIMIT 1";
		//echo $sql."\n";
		$res = mysqli_query($mysqli, $sql);	
}

foreach ($rss->channel->item as $item) {
	#echo $item->title ."\n";
	$info = parseItem($item);
	//echo print_r($info, true)."\n";
	saveInfo($info);
	if (trim($info["serie"]) != "") {
		saveSerie($info["serie"]);
	}
}
?>
