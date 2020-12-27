
import asyncio


class Player():

  def __init__(self):
    pass

  def queue(self,content_path):
    pass

  def close(self):
    pass

  def reset(self):
    pass
  
async def run_subprocess(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()
    
    
    print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')
    
    return proc, stdout, stderr

class MidiPlayer(Player):
  open_audio_cmd = "fluidsynth -i -a pulseaudio /usr/share/sounds/sf2/FluidR3_GM.sf2 {}"
  def __init__(self):
    super(MidiPlayer, self).__init__()
    self._lock = asyncio.Semaphore(1)
    self._loop = asyncio.get_event_loop()

  def queue(self,content_path):
    print("queue-ing task")

    asyncio.run(run_subprocess(self.open_audio_cmd.format(content_path)))
    #task = self._loop.create_task(self._queue(content_path))


  def reset(self):
    pass
  def close(self):
    pass
  
  @asyncio.coroutine
  def _queue(self,content_path):
    print('entered queue')
    with(self._lock):
      print('aquired lock!')
      # create music process and await for it to finish
      _ = asyncio.run_until_complete(run_subprocess(self.open_audio_cmd.format(content_path)))



