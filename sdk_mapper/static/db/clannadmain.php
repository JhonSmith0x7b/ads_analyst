
<?php session_start();?>
<html>
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta property="og:image" content="http://cdn-deeplink.haloapps.com/upload/20170122/148507742396702.jpg"/>
<title>ClannadBar--官方小说--开发中的同好会</title>
<link href="../static/css/bootstrap.min.css" rel="stylesheet">
<link href="../static/css/mycss.css" rel="stylesheet">
<link href="../static/css/bootstrap-select.css" rel="stylesheet">
<!-- 
 <link href="../static/css/bootstrap-responsive.min.css" rel="stylesheet">
<link href="../static/css/bootstrap-theme.min.css" rel="stylesheet">
 -->
<script src="../static/js/jquery-2.1.4.min.js"></script>
<script src="../static/js/bootstrap.min.js"></script>
<script src="../static/js/bootstrap-select.js"></script>
<script type="text/javascript">
$(function(){
	$('#novelCollapseGe1mu').collapse();
})
</script>
</head>
<body>

<!-- video test -->
<!--
<section class="section-introduction fullscreen" id="introduction" style="height: 597px;"> 
<div class="hero-novideo-bg"> 
</div> 
<div class="hero-media"> 
<video autoplay="" id="lifestyle-lapse" loop="" mute=""> 
<source src="http://jcgy.qiniudn.com/koudai-test-karma-lifestyle-film.mp4" 
type="video/mp4"> 
</video> 
</div> 
<div class="hero-media-mask"> 
</div> 
<div class="introduction vertical-align text-center fade in" style="margin-top: -78.5px;"> 
<p> 
内容.
</p> 
-->
<!-- video test over-->
<!-- head area -->
<div id="top"></div>
<!-- 
<input type="button" value="test" style="margin-top:100px" onClick="changePage(3);">
 -->
<?php
include 'head.htm';
?>
<div style="margin-top:180px"></div>
<div class="title well "></div>
<script type="text/javascript">
	$('#navNovel').addClass('active');
</script>
<!-- head area   END-->
<?php
$action = $_REQUEST ['action'];
$chapter = $_REQUEST ['chapter'];
if ($action == 'readnovel') {
	$novelContent = '';
	include 'novelcontent.php';
}
?>
<!-- novel list -->
<div class="container">
<div class="row">
<div class="col-xs-12">
<div class="panel-group" id="novelTheme"><!-- 被光守护的坡道上 -->
<div class="panel panel-default">
<div class="panel-heading">
<h4 class="panel-title"><a data-toggle="collapse"
	data-parent="novelTheme" href="#novelCollapseShikari"
	aria-expanded="false" class="collapsed"> 被光守护的坡道上 </a></h4>
</div>
<div id="novelCollapseShikari" class="panel-collapse collapse novelCollapse"
	aria-expanded="false" style="height: 0px;">
<div class="row">
<div class="col-xs-4"><a href="?action=readnovel&chapter=shikarinachu">拿出勇气吧</a></div>
<div class="col-xs-4"><a href="?action=readnovel&chapter=shikarilianyi">连衣裙</a></div>
<div class="col-xs-4"><a href="?action=readnovel&chapter=shikarinanxing">男性朋友们</a></div>
</div>
<div class="row">
<div class="col-xs-4"><a href="?action=readnovel&chapter=shikarinage">那个时候的我</a></div>
<div class="col-xs-4"><a href="?action=readnovel&chapter=shikarigongzi">公子的日记</a></div>
<div class="col-xs-4"><a href="?action=readnovel&chapter=shikarixintiao">心跳加速的瞬间</a></div>
</div>
<div class="row">
<div class="col-xs-4"><a href="?action=readnovel&chapter=shikaritebie">特别的夜晚</a></div>
<div class="col-xs-4"><a href="?action=readnovel&chapter=shikariwode">我的哥哥</a></div>
<div class="col-xs-4"><a href="?action=readnovel&chapter=shikarigeshi">各式各样的味道</a></div>
</div>
<div class="row">
<div class="col-xs-4"><a href="?action=readnovel&chapter=shikarizhouyu">咒语的秘密</a></div>
<div class="col-xs-4"><a href="?action=readnovel&chapter=shikarierren">二人的回忆</a></div>
<div class="col-xs-4"><a href="?action=readnovel&chapter=shikarilaoshi">老师的回忆</a></div>
</div>
<div class="row">
<div class="col-xs-4"><a href="?action=readnovel&chapter=shikaritade"
	onclick="">她的境界线</a></div>
<div class="col-xs-4"><a href="?action=readnovel&chapter=shikarisinian">四年前的因缘</a></div>
<div class="col-xs-4"><a
	href="?action=readnovel&chapter=shikarishengping">胜平的过去</a></div>
</div>
<div class="row">
<div class="col-xs-4"><a href="?action=readnovel&chapter=shikariguhe">古河面包师再结成</a></div>
<div class="col-xs-4"><a href="?action=readnovel&chapter=shikaridajia">大家在澡堂</a></div>
</div>
</div>
</div>
<!-- 被光守护的坡道上 END -->
<div class="panel panel-default">
<div class="panel-heading"
	style="">
<h4 class="panel-title"><a data-toggle="collapse"
	data-parent="novelTheme" href="#novelCollapseGe1mu" aria-expanded="false"
	class="collapsed"> 游戏文本 </a></h4>
</div>
<div id="novelCollapseGe1mu" class="panel-collapse collapse novelCollapse"
	aria-expanded="false" style="height: 0px;">
<div class="row">
<div class="col-xs-4"><a href="?action=readnovel&chapter=ge1munagisa">古河渚</a></div>
<div class="col-xs-4"><a href="?action=readnovel&chapter=ge1muafterstory1">AfterStory1周目</a></div>
<div class="col-xs-4"><a href="?action=readnovel&chapter=ge1muafterstory2">AfterStory</a></div>
</div>
<div class="row">
<div class="col-xs-4"><a href="?action=readnovel&chapter=ge1mukotomi">一之濑琴美</a></div>
<div class="col-xs-4"><a href="?action=readnovel&chapter=ge1mutomoyo">坂上智代</a></div>
<div class="col-xs-4"><a href="?action=readnovel&chapter=ge1mufuuko">伊吹风子</a></div>
</div>
<div class="row">
<div class="col-xs-4"><a href="?action=readnovel&chapter=ge1muryo">藤林椋</a></div>
<div class="col-xs-4"><a href="?action=readnovel&chapter=ge1mukyo">藤林杏</a></div>
<div class="col-xs-4"><a href="?action=readnovel&chapter=ge1muyukine">宫泽有纪宁</a></div>
</div>
<div class="row">
<div class="col-xs-4"><a href="?action=readnovel&chapter=ge1mumisae">相乐美佐枝</a></div>
<div class="col-xs-4"><a href="?action=readnovel&chapter=ge1musunohara">春园兄妹</a></div>
<div class="col-xs-4"><a href="?action=readnovel&chapter=ge1mukappei">柊胜平</a></div>
</div>
</div>
</div>
<div class="panel panel-default">
<div class="panel-heading">
<h4 class="panel-title"><a data-toggle="collapse"
	data-parent="novelTheme" href="#novelCollapseTwo" aria-expanded="false"
	class="collapsed"> Another Stroy</a></h4>
</div>
<div id="novelCollapseTwo" class="panel-collapse collapse novelCollapse"
	aria-expanded="false" style="height: 0px;">
<div class="row">
<div class="col-xs-4"><a href="?action=readnovel&chapter=monogataritomoyoafter">智代After</a></div>
<div class="col-xs-4"><a href="?action=readnovel&chapter=monogatarifuuko1">风子小宇宙</a></div>
<div class="col-xs-4"><a href="?action=readnovel&chapter=monogatarifuuko2">希望的宇宙</a></div>
</div>
<div class="row">
<div class="col-xs-4"><a href="?action=readnovel&chapter=monogatarikotomi">尾巴王国的小琴美</a></div>
<div class="col-xs-4"><a href="?action=readnovel&chapter=narcissus">Narcissus</a></div>
<div class="col-xs-4"><a href="?action=readnovel&chapter=repal">仙剑奇侠传四</a></div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
<br>
<br>
<br>
<?php 
include'foot.htm';
if(!isset($_SESSION['is_old'])){
	$ip = $_SERVER['REMOTE_ADDR'];
	$date = date('y.m.d H:i', time());
	$url='http://clannadbar.com/py123000?'.'ip='.$ip.'&date='.$date;
	$whut = file_get_contents($url);
	echo $whut;
}else{
	$_SESSION['is_old'] = true;
	echo 'old';
}
?>
<!-- novel list end -->

</div>
</section>

</body>
</html>
