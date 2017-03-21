<?php
require("test_torrent_functions.php");

$mysqli = mysqli_connect("localhost", "apdb", "pwd4apdb", "apdb");
$eztvUrl = "https://eztv.ag";

function HTTPPost($url, $referer, $postFields, &$cookies, &$inputFields, &$headers) {
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_USERAGENT, "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.1) Gecko/20061204 Firefox/2.0.0.1");
	curl_setopt($ch, CURLOPT_URL, $url);
	if ($referer != null) {
		curl_setopt($ch, CURLOPT_REFERER, $referer);
	}
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($ch, CURLINFO_HEADER_OUT, true);
	curl_setopt($ch, CURLOPT_COOKIEJAR, './cookie.txt'); 
	curl_setopt($ch, CURLOPT_COOKIEFILE, './cookie.txt');
	curl_setopt($ch, CURLOPT_HTTPHEADER, Array("Content-Type:application/x-www-form-urlencoded"));
	curl_setopt($ch, CURLOPT_FOLLOWLOCATION, TRUE);
	#return curl_getinfo($ch, CURLINFO_EFFECTIVE_URL);
	if ($postFields != null) {
		curl_setopt($ch, CURLOPT_POST, count($postFields));
		$post = POSTArrayToStr($postFields);
		#echo "Sending ".count($postFields)." headers in post: ".$post."\n";
		curl_setopt($ch,CURLOPT_POSTFIELDS, $post);
	}

	$output = curl_exec($ch);
	
	$headers = curl_getinfo($ch);
	preg_match_all('/^Set-Cookie:\s*([^;]*)/mi', $output, $matches);
	$cookies = array();
	foreach($matches[1] as $item) {
		parse_str($item, $cookie);
		$cookies = array_merge($cookies, $cookie);
	}

	$pattern = "/<[^i]*input[^>]+>/i";
	$matches = array();
	$inputFields = array();
	if (preg_match_all($pattern, $output, $matches)) {
		//echo print_r($matches, true);
		foreach($matches[0] as $match) {
			$pattern = '/name="([^"]+)"/i';
			$matches2 = array();
			if (preg_match($pattern, $match, $matches2)) {
				$name = trim($matches2[1]);
				$pattern = '/value="([^"]+)"/i';
				$matches2 = array();
				if (preg_match($pattern, $match, $matches2)) {
					$value = trim($matches2[1]);
					$inputFields[urlencode($name)] = $value;
				}
			}

		}
	}else{
		echo "No input found !\n";
	}
	return $output;
}

function POSTArrayToStr($postFields) {
	$post = "";
	foreach($postFields as $name => $value) {
		if ($post != "") {
			$post .= "&";
		}
		$post .= $name."=".$value;
	}
	return $post;	
}

function POSTStrToArray($post) {
	$postFieldsTmp = explode("&", $post);
	$postFields = array();
	foreach($postFieldsTmp as $field) {
		$field = explode("=", $field);
		$postFields[trim($field[0])] = trim($field[1]);
	}
	return $postFields;	
}

function POSTfromInput($inputFields) {
	$postFields = array();
	foreach($inputFields as $name => $value) {
		$postFields[urlencode($name)] = urlencode($value);
	}
	return $postFields;
}

$url = "https://eztv.ag/login/";
$referer = null;
$cookies = array();
$headers = array();
$postFields = null;
$inputFields = array();
$output = HTTPPost($url, $referer, $postFields, $cookies, $inputFields, $headers);
//$post = "MasterPage%24cphWidget%24Email=paoletti.antonello%40gmail.com
//&MasterPage%24cphWidget%24Password=resistore
//&MasterPage%24cphWidget%24RememberMeCheckbox=yes
//&rmShown=1
//&MasterPage%24cphWidget%24LoginButton=Accedi";
$postFields = POSTfromInput($inputFields);
$postFields["loginname"] = "zioanx";
$postFields["password"] = "resistore";
$postFields["submit"] = "Login";
unset($postFields["search"]);
#echo print_r($postFields, true)."\n";

$cookies = array();
$headers = array();
$inputFields = array();
$referer = $url;
$output = HTTPPost($url, $referer, $postFields, $cookies, $inputFields, $headers);
#echo print_r($headers, true)."\n";
#file_put_contents("./output.htm", $output);

$cookies = array();
$headers = array();
$inputFields = array();
$referer = $url;
$url = "https://eztv.ag/myshows/list/";
$html = HTTPPost($url, $referer, $postFields, $cookies, $inputFields, $headers);
#echo print_r($headers, true)."\n";

$pattern = '/<a href="(\/shows\/\d+\/[^\/]+\/)" class="thread">([^<]+)<\/a>/';
$matches = array();
if (preg_match_all($pattern, $html, $matches)) {
	#echo print_r($matches, true)."\n";
	echo "* \033[31mResetting favourites...\033[0m\n";
	resetSerie();
	echo "* \033[34mGetting eztv favourites...\033[0m\n";
	foreach ($matches[1] as $i => $showUrl) {
		$url = $eztvUrl.$showUrl;
		#echo $url."\n";
		echo " - \033[34m".$matches[2][$i]."\033[0m: ";
		$cookies = array();
		$headers = array();
		$inputFields = array();
		$referer = $url;
		$html2 = HTTPPost($url, $referer, $postFields, $cookies, $inputFields, $headers);
		#echo print_r($headers, true)."\n";
		$pattern2 = '/<a href="(magnet[^"]+)" class="magnet" title="([^"]+)" rel="nofollow"><\/a>/';
		$matches2 = array();
		if (preg_match_all($pattern2, $html2, $matches2)) {
			#echo print_r($matches2, true)."\n";
			$total = $new = 0;
			foreach ($matches2[1] as $j => $magnetUrl) {
				$magnetUrl = urldecode($magnetUrl);
				$pattern3 = "/urn:btih:([^&]+)&/";
				$matches3 = array();
				if (preg_match($pattern3, $magnetUrl, $matches3)) {
					$total++;
					#echo print_r($matches3, true)."\n";
					#echo $matches2[2][$i]." ".$magnetUrl."\n";
					$raw = array();
					$raw["title"] = trim(str_replace(" Magnet Link", "", $matches2[2][$j]));
					$raw["magnetURI"] = trim($magnetUrl);
					$raw["infoHash"] = trim(strtoupper($matches3[1]));
					$raw["contentLength"] = 0;
					$raw["link"] = "";
					#echo print_r($raw, true)."\n";		
					$info = parseTorrentInfo($raw);
					#echo print_r($info, true)."\n";
					$new += saveTorrentInfo($info);
					if (trim($info["serie"]) != "") {
                				saveSerie($info["serie"], true, trim($matches[2][$i]));
        				}
				}
			}
			echo $total." torrents (".$new." new)\n";
		}	
	}
}

//echo print_r($inputFields, true);
//var_dump($cookies);
?>
