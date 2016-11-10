from mplayer import Player, CmdPrefix

# Set default prefix for all Player instances
Player.cmd_prefix = CmdPrefix.PAUSING_KEEP

# Since autospawn is True by default, no need to call player.spawn() manually
player = Player()

# Play a file
player.loadfile("temp.mp3")

# Pause playback
player.pause()

# Get title from metadata
metadata = player.metadata or {}
print(metadata.get('Title', ''))

# Print the filename
print(player.filename)

# Seek +5 seconds
player.time_pos += 5

# Set to fullscreen
player.fullscreen = True

# Terminate MPlayer
player.quit()