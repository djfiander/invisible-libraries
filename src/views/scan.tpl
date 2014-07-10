<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
    <body>
%if defined('error'):
        <p><strong>{{error}}</strong></p>
	<audio src="/files/Plastic_Pipe.ogg" type="audio/ogg" autoplay="">
	</audio>
%end
%if defined('title'):
	<p>{{title}}</p>
%end
	<form action="/scan" method="post">
	    <label for="isbn">ISBN</label>: <input name="isbn" type="text" autofocus="autofocus" />
	    <input value="Scan" type="submit" />
	</form>
    </body>
</html>
