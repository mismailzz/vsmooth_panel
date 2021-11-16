<?php
shell_exec("/frontail/frontail/bin/frontail /var/log/system.log");
header('Location: http://localhost:8000/index.html');
?>
