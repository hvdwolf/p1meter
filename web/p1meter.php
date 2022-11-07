<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Overzicht p1 meter data</title>
<style>
    body {
        width: 85em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
    th, td { padding: 5px; }

</style>
<link rel="stylesheet" type="text/css" href="js/jquery-ui.css">
  <script src="https://code.jquery.com/jquery-3.6.0.js"></script>
  <script src="https://code.jquery.com/ui/1.13.2/jquery-ui.js"></script>
<script>
  $( function() {
    $( "#datepicker" ).datepicker({dateFormat:"yy-mm-dd"});
  } );
</script>

<link rel="shortcut icon" href="web_images/favicon.ico" >
</head>

<body>
<h2>Overzicht p1 meter data</h2>
<form>
<strong>Verbruik vandaag</strong>&nbsp;<input type="submit" name="btn_submit" value="Stroom vandaag"/>&nbsp;<input type="submit" name="btn_submit" value="Gas vandaag" />&nbsp;&nbsp;&nbsp;
<strong>Verbruik op datum</strong>&nbsp;<input type="submit" name="btn_submit" value="Stroom op datum" />&nbsp;<input type="submit" name="btn_submit" value="Gas op datum" />&nbsp;<input type="text" name="txtDate"  id="datepicker" >
<p><strong>Overzichten</strong>&nbsp;<input type="submit" name="btn_submit" value="Per dag" /> <input type="submit" name="btn_submit" value="Per week" />&nbsp;<input type="submit" name="btn_submit" value="Per maand" />
<!-- radio button group periodes -->
&nbsp;&nbsp;&nbsp;<strong>Periodes (dagen/weken/maanden)</strong>
<input type="radio" name="periodes" id="vier" value="4" /><label for="vier">4</label>
<input type="radio" name="periodes" id="zeven" value="7" checked="checked" /><label for="zeven">7</label>
<input type="radio" name="periodes" id="twaalf" value="12" /><label for="twaalf">12</label>
<input type="radio" name="periodes" id="veertien" value="14" /><label for="veertien">14</label>
<input type="radio" name="periodes" id="dertig" value="30" /><label for="dertig">30</label>
<input type="radio" name="periodes" id="9999" value="9999" /><label for="9999">Onbeperkt</label>
<p><strong>Type grafiek</strong>
<!-- VPG => V = Verbruikt P =  Produced  G = Gas -->
<input type="radio" name="grafiektype" id="VPG" value="VPG" checked="checked" /><label for="VPG">Verbruikt/Geproduceerd/Gas</label>
<input type="radio" name="grafiektype" id="VP" value="VP" /><label for="VP">Verbruikt/Geproduceerd</label>
<input type="radio" name="grafiektype" id="V" value="V" /><label for="V">Verbruikt</label>
<input type="radio" name="grafiektype" id="P" value="P" /><label for="P">Geproduceerd</label>
<input type="radio" name="grafiektype" id="G" value="G" /><label for="G">Gas verbruik</label>
</form>
<?php
print "<div style=\"color:blue\"><strong>Gevraagd:</strong> Optie \"".$_REQUEST['btn_submit']."\"; periodes ".$_REQUEST['periodes']."; grafiektype ".$_REQUEST['grafiektype']."; datum ".$_REQUEST['txtDate']."</div>";

//print "<br>Command is: /BigData/software/p1meter/wp1meter.py \"".$_REQUEST['btn_submit']."\" ".$_REQUEST['periodes']." ".$_REQUEST['grafiektype']."<br>";
$command = escapeshellcmd("/BigData/software/p1meter/wp1meter.py \"".$_REQUEST['btn_submit']."\" ".$_REQUEST['periodes']." ".$_REQUEST['grafiektype']." ".$_REQUEST['txtDate']);
$output = shell_exec($command);
//print "<br>Output from python script<br>";
//print $output;
//print("<br>After output");

?>
<p><img src="<?php echo '/tmp/'.$output; ?>" />
</body>
</html>
