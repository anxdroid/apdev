<?php
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
	#curl_setopt($ch, CURLOPT_FOLLOWLOCATION, TRUE);
	#return curl_getinfo($ch, CURLINFO_EFFECTIVE_URL);
	if ($postFields != null) {
		curl_setopt($ch, CURLOPT_POST, count($postFields));
		$post = POSTArrayToStr($postFields);
		//$post = "__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=8PC6PYc%2B6otPd2lk%2BElVZsNJsLt%2B9YX3cW4ru592oCVHT4fAw8YUtehOsrx9qVYbVlrilFrfiHzSy0a8c%2FRfFmiVBUikc0h7NfMMtIu%2FR1Aey6PEoOi3nSDrwGwqxyjE0SC9p4Rny5ZmcEvSK%2BVdrSMIVUSrSNPe5t6kcdcGoJlSkBsBtsXiwB7C44IWfDBC%2FD3Mf25rPpjTL1qqs7djrNCGmIvUiwE5JGWAamdI%2BLtMjbGWpW%2FfPKBUO3kLXCyvF3f1xMvpEupU8BMliwOTqe3FpKM1sncjqIqFer8IoSTTlrZrGUdwHFQIoUT%2BZjDFC1y6sjfWf7krodOQEg1Zhgcj9AyIvd8FIdvE%2FujLHDG1Qp936SATx6S6rx0cPP%2FEVLy%2BWi1N%2Fjy7BaCJ5pHybJRm%2BIKV8MX5%2FbH%2Fwbvz0WgaAW1S1s4B%2BjLaAkaUGLlQOWNgBJw%2FpUtkRdLjWtWRkAeao1AFEd70yXRVZ4Rb4WsB3vTiMxaViyvEXz828enK9JqhnbJMPeXTPEj1DT9gAEDNohoMSfJlY8trqVK2kGPqaETca8uuMiIHdcDA8rLKS1HsjI2aGFNUW%2BQArNkaPn5Ja7AvSIoblCT9%2BQ7lAnySzNUb%2Bx%2BTX%2FzeUvAAwzXZXPojrkBgKVWtvwS1IXObLRjlIADNC3KzUE%2BSZiuqdXpCE0V2Da8TXDCh562W6tHMXktmrdWOnLE2xa2CoR67oiyhuqRtW6r3voaHDsONJUk4ToxjYV6DIy7tBMkS9pVY7pLJA8KopTYOa%2FrWcVm%2BOam8prWonUSItCwz1DJCvsipTLoZXv9KXQh5HAQXyHgI2tAF6AfYqi8CtpJYGPhEk%2BPUGsC34sDr56eLdT8u%2F6unXkl7LGOapPSItVfIJOru89VK%2Bz%2B%2Bf70sr09CDtDdQkCm3cwAYGex4X6mdjWoQlQuCgSdaVkZYPZ72MlpvgZKjY3JB%2FYV4E0EmoyJs1rHfnsmcyQmRGbtSD5K%2F37cpvTYC%2F%2BD60hNwArJQgBY1nEtrCldqtdtzlUENuk4Wk9Nvn5%2BAmLyzL84C%2B2sm8CCXhgw6Mv1v%2Bf8XByIP3z5BxC1DjWJctLE66Hyq4heqcKE%2BolnnrCH7pW1gVkf3XFxlhw%2BEHvCdtxD%2Fr8cy%2F2SClHFYLaMpLuwJaeTdfF9m8PZh5ZQnD%2BqzDg%2BXPaocaWCfD5iwAeQaPJO09qpebx6c2hdawRQDIb9xKsAdMY8dqKQEZsV5oR%2B%2F8VQHIgacapDoy9QUtC0CxG7UAns%2Bm6Ek%2BKz%2BwQEU%2FiOTTTDTbomldI45BvP%2FFbT25N5MflVu6YZz3P2nf71zHjQ2zh8%2B7LPwFE%2BBnKYa31zSd0wupyYipvGlgc4y7SRSLsGpr%2BsZiA4%2FFVJU1XzgmLkXEAcDdt7%2BH1Nu8cS31o2rdpu4b4DEwwTGqd19MRYOL4BV8GrY2tbvz8tUjawl95UfO3kwovmgyeHFFkZBAu1rSReeQy8suyozASIolcqvPd6aV%2BAucvudi9FFZELJwgHd39aSdv31sUudPDolSRhcmiY5HexRdBdNrNPEbiCRbhJcBvYx492U5N8%2B28%2BWuOro8ZhSLsWUYr%2FGJF6hHXwmKt%2F6dFRPPcHScHF5CKq5L5K1C4ooNHmUAEXwiHN7sAkCdqsf3ACcho1m8PgDSVLxWekGaiu%2Bgbws5jmeW32o4GxN1yiD7bA2mZEuxCeyRFddlji3AO6nlx6bQ6M0FjhYQz5YdxaPiNtlXekXAxQCwxaA47HFkS5w0M4wDk%2Bpn%2BxrsAqWX5daAt9tcVGYSE70CcZzSacshNOzW6zbKKwKmh065fi2kbQT%2B4%2BplVZjmnMIIPL7Suelsu95kafMiT5kx82vHS0PyMo4M64g9EJoCoGQ1qwWPWFXzdqlWlOz8jK011XCnwOyazK7J%2BJJr2ETDNbHnpDBCByc9CWd%2BbT5ZxOicuWObDdNDSUpD09baQeHpY0q6JWVJ25oY7sRIFr3Fh6OnnUR8hblyeqwk5Av372UFm0fAJCbm0DkjJYq2y4EAlCcTRgZbUMAh95003eDncd%2BO8JgTJaoD8T63QkQjjwa%2FPNO0BwQF4ZwuQUC3X0mhtTtDa%2FwW8TZ%2B816EZMrZnpuYvi8bphnq8FF4W5LfaL0yIeEGBOOF1LWkAFJLbZeoxuygH5%2FRB5neLvZQG5zlIYhNYa0Hl884IVjh%2B5qYc5NZjp%2FLSRj7HCmNxzA%2BDa4a5UT4jkKp%2F%2B5Sft9UST5EbUwz%2B%2FxDB9ew%3D%3D&__VIEWSTATEGENERATOR=3FE2630A&__VIEWSTATEENCRYPTED=&__EVENTVALIDATION=KZl4EPEi86PP9FQSGm5RtMX8TuD2oDXg5UkNVXLTSINu%2F9UwsuwTmj4RHh8ol9dyBhGD90pX%2Fy1%2BFtROiON3afr4dJDBySbfnowvzHKZqMikyY95Xlejold8pmOaVVA%2FAns4C6GJ4pvpc2yt%2FE6rx8%2BQVtiCma8RW3TpJZ9kStBNynjtiUVNWieBujGhmT4CLf1CxLDUBVbzRSrOgEAt2Mmkl5X4uXtMmQzVibex%2Fps54N5ZkC17I6Ol7jTY6bG9&MasterPage%24cphWidget%24Email=paoletti.antonello%40gmail.com&MasterPage%24cphWidget%24Password=resistore&MasterPage%24cphWidget%24RememberMeCheckbox=yes&rmShown=1&MasterPage%24cphWidget%24LoginButton=Accedi";
		echo "Sending ".count($postFields)." headers in post: ".$post."\n";
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

$url = "http://nwg.novaproject.it/Portal/loginPage.aspx?ReturnUrl=%2fPortal%2fDefault.aspx";
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
$postFields["MasterPage%24cphWidget%24Email"] = "paoletti.antonello%40gmail.com";
$postFields["MasterPage%24cphWidget%24Password"] = "resistore";
$postFields["rmShown"] = "1";
$postFields["MasterPage%24cphWidget%24LoginButton"] = "Accedi";
$postFields["__EVENTTARGET"] = "";
$postFields["__EVENTARGUMENT"] = "";
$postFields["__VIEWSTATEENCRYPTED"] = "";

//echo print_r($inputFields, true)."\n";

$cookies = array();
$headers = array();
$inputFields = array();
$output = HTTPPost($url, $referer, $postFields, $cookies, $inputFields, $headers);
echo print_r($headers, true)."\n";
file_put_contents("./output.htm", $output);

//echo print_r($inputFields, true);
//var_dump($cookies);
?>
