<?php
    function sendReq($url, $headers) {
        echo $url."\n";
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_VERBOSE, 1);
        curl_setopt($ch, CURLOPT_HEADER, 1);
        curl_setopt($ch, CURLOPT_URL, $url);
        //curl_setopt($ch, CURLOPT_POST, 1);
        //curl_setopt($ch, CURLOPT_POSTFIELDS, $vars);  //Post Fields
        //curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
        $response = curl_exec ($ch);
        echo $response."\n---------------------\n";
        $header_size = curl_getinfo($ch, CURLINFO_HEADER_SIZE);
        $header = substr($response, 0, $header_size);
        echo $header."\n---------------------\n";
        $body = substr($response, $header_size);
        curl_close ($ch);
    }

    $host = "http://192.168.1.154";
    $realm = "registered_user@power-one.com";
    $user = "admin";
    $pass = "Thejedi82";
    $nonce = "060c1917968d6fbbda561ea5707e2e28";
    $nc = "00000002";
    $cnonce = "ddf4bfcaf87acba9";
    $method = 'GET';
    $uri = "/v1/feeds/ser4:120399-3G96-3016/datastreams/m101_1_W?_=1574784046328";
    $uri = "/v1/status?_=1574845879374";
    $params = "&end=2019-11-19T23:00:00Z&interval=5min&maxDataPointsPerPage=288&start=2019-11-18T23:00:00Z&timeFormat=utc";
    $userToken = 'db6e106cf2b982d8dce1cf2ba2e0d449';
    $qop = "auth";

    $HA1 = $userToken;
    $HA2 = md5($method.":".$uri);
    $response = md5($HA1.":".$nonce.":".$nc.":".$cnonce.":".$qop.":".$HA2);

    echo "HA2: ".$HA2."\n";
    echo "Response: ".$response."\n";

    $authorization = 'X-Digest username="' . $user . '", ' .
    'realm="' . $realm . '", ' . 
    'nonce="' . $nonce . '", ' .
    'uri="' . $uri . '", ' .
    'response="' . $response . '", ' .
    'qop=' . $qop . ', ' . 
    'nc=' . $nc . ', ' .
    'cnonce="' . $cnonce . '"';

    echo $authorization."\n";
    //sendReq($host.$uri, array("Authorization", $authorization));
    //echo $header;

/*
$uri = "../au/logger/v1/wifi/status?_=1574783509760";
03f378fea024edfc07ae34caf217517c
a2610f52640f1030f125de0a00bbad27
*/
    
/*
user {id: "admin", authToken: "db6e106cf2b982d8dce1cf2ba2e0d449"}
auth-svc.js:123 HA1 db6e106cf2b982d8dce1cf2ba2e0d449
auth-svc.js:124 method GET
auth-svc.js:125 uri ../au/logger/v1/wifi/status?_=1574783509760
auth-svc.js:126 HA2 03f378fea024edfc07ae34caf217517c
auth-svc.js:127 RESPONSE a2610f52640f1030f125de0a00bbad27

var REALM = $filter('AuthFilter').getRealm(challenge);
                    var HA1 = user.authToken;
                    var HA2 = md5(method . ':' . uri);
                    var NONCE = $filter('AuthFilter').getNonce(challenge);
                    var NC = $filter('AuthFilter').getNc();
                    var CNONCE = $filter('AuthFilter').getCnonce();
                    var QOP = $filter('AuthFilter').getQop(challenge);
                    var RESPONSE = md5(HA1 . ':' .
                                       NONCE . ':' .
                                       NC . ':' .
                                       CNONCE . ':' .
                                       QOP . ':' .
                                       HA2);

                    var auth = 
                        'X-Digest username="' . user.id . '", ' .
                        'realm="' . REALM . '", ' . 
                        'nonce="' . NONCE . '", ' .
                        'uri="' . uri . '", ' .
                        'response="' . RESPONSE . '", ' .
                        'qop=' . QOP . ', ' . 
                        'nc=' . NC . ', ' .
                        'cnonce="' . CNONCE . '"';
*/
    
?>
