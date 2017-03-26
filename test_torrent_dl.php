<?php
require __DIR__ . '/vendor/autoload.php';
use Transmission\Transmission;
use Transmission\Client;
use JsonRPC\Client as KodiClient;
require("test_torrent_functions.php");
/***************************************************************************/

$mysqli = mysqli_connect("localhost", "apdb", "pwd4apdb", "apdb");

/***************************************************************************/

$transmissionClient = new Client();
$transmissionClient->authenticate('osmc', 'osmc');
$transmission = new Transmission();
$transmission->setClient($transmissionClient);
$torrentPath = "/home/osmc/INCOMPLETI";

/***************************************************************************/

$kodiPath = "/media/LaCie/Anto/SERIE";
$kodiUrl = "http://anto:resistore@192.168.1.3:81/jsonrpc";

/***************************************************************************/

$preferiti = array("risoluzione" => "720");

/***************************************************************************/

function doDownload() {
	global $mysqli, $transmission, $preferiti;
	$sql = "SELECT t.*, s.eztvTitle, s.preferita, s.stagione stagioneMin, s.episodio episodioMin 
	FROM apdb.torrent_rss t JOIN apdb.torrent_serie s ON t.serie = s.serie AND s.preferita = 1 
	WHERE t.scaricato = 0 AND t.errore = 0 AND
	(
		CAST(t.stagione AS UNSIGNED) > CAST(s.stagione AS UNSIGNED) 
	OR 
		(CAST(t.stagione AS UNSIGNED) = CAST(s.stagione AS UNSIGNED) AND CAST(t.episodio AS UNSIGNED) >= CAST(s.episodio AS UNSIGNED)))
	ORDER BY serie ASC, CAST(t.stagione AS UNSIGNED) DESC, CAST(t.episodio AS UNSIGNED) DESC";
	//echo $sql."\n";
	$res = mysqli_query($mysqli, $sql) or die(mysqli_error($mysqli)."\n");

	$torrents = array();
	$lastEpisode = $lastShow = "";
	$skipShow = "";
	$stagioniMin = array();
	while ($row = mysqli_fetch_assoc($res)) {
		if ($row["stagione"] == "") {
			$row["stagione"] = "Unica";	
		}
		$currEpisode = "S".$row["stagione"]."E".$row["episodio"];
		if ($lastShow != $row["serie"]) {
			//echo $row["serie"]." ".$currEpisode."\n";
		}
		
		if (isset($stagioniMin[$row["serie"]])) {
			$row["stagioneMin"] = $stagioniMin[$row["serie"]]["stagioneMin"];
			$row["episodioMin"] = $stagioniMin[$row["serie"]]["episodioMin"]; 
		}
		
		//echo $currEpisode."\n";
		if ($row["serie"] != $skipShow) {
			if (1*$row["stagioneMin"] == 0 && $lastEpisode != "" && $lastShow == $row["serie"] && $currEpisode != $lastEpisode) {
				#echo "No boundaries defined for '".$row["serie"]."' taking only latest episode: ".$lastEpisode." !\n";
				#$skipShow = $row["serie"];
			}else{
				//echo $currEpisode." ".$lastEpisode." ".$row["serie"]." ".$lastShow." MIN ".$row["stagioneMin"]."\n";
				$torrents[$row["serie"]][$row["stagione"]][$row["episodio"]][$row["risoluzione"]] = $row;
				if (1*$row["stagioneMin"] == 0) {
					echo " - \033[31m".$row["serie"]." downloading from: ".$currEpisode."\033[0m\n";
					saveSerie($row["serie"], true, $row["eztvTitle"], $row["stagione"], $row["episodio"]);
					$stagioniMin[$row["serie"]]["stagioneMin"] = $row["stagione"];
					$stagioniMin[$row["serie"]]["episodioMin"] = $row["episodio"];
					$skipShow = $row["serie"];	
				}
			}
		}
		if ($lastShow != $row["serie"] && $lastShow != "") {
			$lastEpisode = "";
		}else{
			$lastEpisode = $currEpisode;
		}
		$lastShow = $row["serie"];
	}
	$scaricare = array();
	foreach($torrents as $serie => $serieInfo)
		foreach($serieInfo as $stagione => $stagioneInfo) 
			foreach($stagioneInfo as $episodio => $episodioInfo) {
				if (count($episodioInfo) == 1) {
					$keys = array_keys($episodioInfo);
					$scaricare[] = $episodioInfo[$keys[0]];
				}else{
					foreach($episodioInfo as $risoluzione => $row) {
						if (strstr($risoluzione, $preferiti["risoluzione"]) !== false) {
							$scaricare[] = $row;
						}
					}
				}
			}
	#echo "found ".count($scaricare)." episodes...\n";
	#echo print_r($scaricare, true)."\n";
	foreach($scaricare as $row) {	
		//echo print_r($row, true)."\n";
		$transmission->add($row["magnetURI"]);
		
		try {
			$torrent = $transmission->get($row["infoHash"]);
			echo " - \033[34m".$row["title"]."\033[0m status:".$torrent->getStatus()." perc:".$torrent->getPercentDone()."%\n";
			if ($torrent != null) {
				if ($torrent->getPercentDone() == 0 || $torrent->getStatus() != 4) {
					$transmission->start($torrent);
					#echo "   \033[32mSuccesfully added to download queue\033[0m\n";
				}

				$sql = "UPDATE apdb.torrent_rss SET 
				contentLength = ".(1*$torrent->getSize()).",
				percentDone = ".(1*$torrent->getPercentDone()).", 
				status = ".(1*$torrent->getStatus()).", 
				startDate = ".(1*$torrent->getStartDate())." 
				WHERE infoHash = '".mysqli_real_escape_string($mysqli, $row["infoHash"])."'";
				//echo $sql."\n";
				$res = mysqli_query($mysqli, $sql) or die(mysqli_error($mysqli)."\n");
				
			}
		} catch (RuntimeException $e) {
			echo " - \033[31mError on ".$row["title"]."\033[0m\n";
			$sql = "UPDATE apdb.torrent_rss SET errore = 1
			WHERE infoHash = '".mysqli_real_escape_string($mysqli, $row["infoHash"])."'";
			$res = mysqli_query($mysqli, $sql) or die(mysqli_error($mysqli)."\n");
			saveSerie($row["serie"], true, $row["eztvTitle"], 0, 0);
		}

	}
}

function checkCompletion() {
	global $mysqli;
	$sql = "SELECT serie, stagione, episodio, infoHash FROM apdb.torrent_rss WHERE percentDone = 100";
	$res = mysqli_query($mysqli, $sql) or die(mysqli_error($mysqli)."\n");
	while ($row = mysqli_fetch_assoc($res)) {
		$sql = "UPDATE apdb.torrent_rss SET scaricato = 1 
		WHERE
		(serie = '".mysqli_real_escape_string($mysqli, $row["serie"])."'
			AND stagione = '".mysqli_real_escape_string($mysqli, $row["stagione"])."'
			AND episodio = '".mysqli_real_escape_string($mysqli, $row["episodio"])."'
			AND infoHash = '".mysqli_real_escape_string($mysqli, $row["infoHash"])."')";
		#echo $sql."\n";
		mysqli_query($mysqli, $sql) or die(mysqli_error($mysqli)."\n");
		$sql = "UPDATE apdb.torrent_rss SET scaricato = -1 
		WHERE
		(serie = '".mysqli_real_escape_string($mysqli, $row["serie"])."'
			AND stagione = '".mysqli_real_escape_string($mysqli, $row["stagione"])."'
			AND episodio = '".mysqli_real_escape_string($mysqli, $row["episodio"])."'
			AND infoHash <> '".mysqli_real_escape_string($mysqli, $row["infoHash"])."')";
		#echo $sql."\n";
		mysqli_query($mysqli, $sql) or die(mysqli_error($mysqli)."\n");
	}
}

function handleDone() {
	global $torrentPath, $kodiPath, $mysqli, $transmission;
	$sql = "SELECT * FROM apdb.torrent_rss WHERE spostato = 0 AND scaricato = 1";
	#echo $sql."\n";
	$res = mysqli_query($mysqli, $sql) or die(mysqli_error($mysqli)."\n");
	while ($row = mysqli_fetch_assoc($res)) {
		$torrent = $transmission->get($row["infoHash"]);
		#echo print_r($row, true)."\n";
		$row["path"] = $kodiPath."/".$row["serie"];
		#echo $row["path"]."\n";
		if (!file_exists($row["path"])) {
			echo "Creating ".$row["path"]."...\n";
			mkdir($row["path"], 0777);
		}
		$row["path"] .= "/S".str_pad($row["stagione"], 2, "0", STR_PAD_LEFT);
		if (!file_exists($row["path"])) {
		        echo " - Creating ".$row["path"]."...\n";
		        mkdir($row["path"], 0777);
		}
		#echo $row["path"]."\n";
		#echo print_r($torrent->getFiles(), true)."\n";
		foreach($torrent->getFiles() as $file) {
			$filename = $torrentPath."/".$file->getName();
			if (file_exists($filename)) {
				$ext = substr($file->getName(), -3);
				$torSize = number_format($file->getSize() / 1024 / 1024, 2);
				$actSize = number_format(filesize($filename) / 1024 / 1024, 2);
				$perc = number_format(100 * $file->getSize() / $row["contentLength"], 2);
				#echo $filename." ".$torSize." MB (actual: ".$actSize." MB) ".$perc."% of total size\n";
				
				if ($file->getSize() == filesize($filename) && $perc > 60) {
					$row["path"] .= "/".str_replace(" ", ".", $row["serie"]).".S".str_pad($row["stagione"], 2, "0", STR_PAD_LEFT)."E".str_pad($row["episodio"], 2, "0", STR_PAD_LEFT);
					if (strstr($row["risoluzione"], "720p") !== false) {
						$row["path"] .= ".720p";
					}elseif (strstr($row["risoluzione"], "1080p") !== false) {
						$row["path"] .= ".1080p";
					}
					$row["path"] .= ".".$ext;
					echo " - Stopping torrent...\n";
					$transmission->stop($torrent);
					rename($filename, $row["path"]);
					echo " - File moved to ".$row["path"]."\n";
					$sql = "UPDATE apdb.torrent_rss SET spostato = 1 WHERE infoHash = '".mysqli_real_escape_string($mysqli, $row["infoHash"])."'";
					#echo $sql."\n";
					mysqli_query($mysqli, $sql) or die(mysqli_error($mysqli)."\n");
				}
			}
		}	
	}
}

function cleanLibrary() {
        global $kodiPath;
        $kodiclient = new KodiClient('http://anto:resistore@localhost:81/jsonrpc');
        #echo print_r($kodiclient, true)."\n";
        $result = $kodiclient->execute('VideoLibrary.Clean', []);                                                                          echo print_r($result, true)."\n";                                    }

function updateLibrary() {
	global $kodiPath;
	$kodiclient = new KodiClient('http://anto:resistore@localhost:81/jsonrpc');
	#echo print_r($kodiclient, true)."\n";
	$result = $kodiclient->execute('VideoLibrary.Scan', ["directory" => $kodiPath]);
	echo print_r($result, true)."\n";
}
echo "* \033[35mDownloading...\033[0m\n";
doDownload();
checkCompletion();
echo "* \033[35mHandling completed...\033[0m\n";
handleDone();
echo "* \033[35mUpdating Kodi library...\033[0m";
updateLibrary();
echo "* \033[35mCleaning Kodi library...\033[0m";
cleanLibrary();
?>
