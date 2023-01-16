cmd_/home/debian/ece434HW/hw05/ebbchar/modules.order := {   echo /home/debian/ece434HW/hw05/ebbchar/ebbchar.ko; :; } | awk '!x[$$0]++' - > /home/debian/ece434HW/hw05/ebbchar/modules.order
