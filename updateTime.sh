# Recharge les unités user
systemctl --user daemon-reload

# Active et démarre le timer
systemctl --user enable edt.timer
systemctl --user start edt.timer

# Vérifier le status du timer
systemctl --user list-timers
