<?php
require("test_torrent_functions.php");

$mysqli = mysqli_connect("localhost", "apdb", "pwd4apdb", "apdb");

/***************************************************************************/
echo "* \033[35meztv rss updates:\033[0m ";
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
	return parseTorrentInfo($info);
}
$torrentFound = $torrentAdded = 0;
foreach ($rss->channel->item as $item) {
	$torrentFound++;
	#echo $item->title ."\n";
	$info = parseItem($item);
	//echo print_r($info, true)."\n";
	$torrentAdded += saveTorrentInfo($info);
	if (trim($info["serie"]) != "") {
		saveSerie($info["serie"]);
	}
}
echo $torrentFound." (".$torrentAdded." new)\n";
?>
